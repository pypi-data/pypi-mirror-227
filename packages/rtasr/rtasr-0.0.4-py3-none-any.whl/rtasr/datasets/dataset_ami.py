"""Download the AMI dataset and prepare it for benchmarking.

More information here: https://groups.inf.ed.ac.uk/ami/corpus/

This dataset is used for Speaker Diarization.

Usage:
    rtasr download -d ami --no-cache
"""

import asyncio
import json
import traceback
from pathlib import Path
from typing import Any, Dict, List

import aiofiles
import aiohttp
from rich import print
from rich.live import Live
from rich.progress import Progress, TaskID

from rtasr.concurrency import ConcurrencyHandler, ConcurrencyToken
from rtasr.constants import DATASETS
from rtasr.utils import create_live_panel, download_file, get_files, resolve_cache_dir

concurrency_handler = ConcurrencyHandler(limit=DATASETS["ami"]["concurrency_limit"])


async def prepare_ami_dataset(output_dir: str = None, use_cache: bool = True) -> None:
    """
    Download the AMI dataset and prepare it for benchmarking.

    Args:
        output_dir (str):
            Path to the directory where the dataset is stored.
            If not specified, the dataset will be stored in the
            default `~/.cache/rtasr/datasets` directory.
        use_cache (bool):
            Whether to use the cache or not. Defaults to True.
            If set to False, the dataset will be downloaded
            again even if it is already present in the cache.
    """
    if output_dir is None:
        cache_datasets_dir = resolve_cache_dir() / "datasets"
        cache_datasets_dir.mkdir(parents=True, exist_ok=True)
        output_dir = cache_datasets_dir / "ami"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    dataset_metadata: Dict[str, Any] = DATASETS["ami"]

    (
        current_progress,
        step_progress,
        splits_progress,
        progress_group,
    ) = create_live_panel()

    manifest_split_paths: List[Path] = []
    with Live(progress_group):
        async with aiohttp.ClientSession() as session:
            current_progress_task_id = current_progress.add_task(
                "Downloading dataset files: AMI"
            )
            splits_progress_task_id = splits_progress.add_task(
                "", total=len(dataset_metadata["splits"])
            )

            split_tasks = []
            for split in dataset_metadata["splits"]:
                split_dir = output_dir / split
                split_dir.mkdir(parents=True, exist_ok=True)

                split_tasks.append(
                    _download_ami_split(
                        split,
                        split_dir,
                        session,
                        step_progress,
                        use_cache,
                        dataset_metadata,
                    )
                )

            step_progress_task_ids: List[TaskID] = []
            for future in asyncio.as_completed(split_tasks):
                try:
                    task_id = await future
                    if not isinstance(task_id, int):
                        raise Exception(
                            "Download failed for split:"
                            f" {task_id}\n{traceback.format_exc()}"
                        )
                    else:
                        step_progress_task_ids.append(task_id)
                except Exception as e:
                    raise Exception(e) from e
                finally:
                    splits_progress.advance(splits_progress_task_id)

            splits_progress.update(splits_progress_task_id, visible=False)
            for task_id in step_progress_task_ids:
                step_progress.update(task_id, visible=False)

            current_progress.stop_task(current_progress_task_id)
            current_progress.update(
                current_progress_task_id,
                description="[bold green]Dataset AMI downloaded.",
            )

        current_progress_task_id = current_progress.add_task(
            "Preparing manifest files: AMI"
        )
        splits_progress_task_id = splits_progress.add_task(
            "", total=len(dataset_metadata["splits"])
        )

        split_tasks = []
        for split in dataset_metadata["splits"]:
            split_dir = output_dir / split
            split_tasks.append(
                _prepare_ami_manifest_split(split_dir, use_cache, dataset_metadata)
            )

        for future in asyncio.as_completed(split_tasks):
            try:
                manifest_paths = await future
                if not isinstance(manifest_paths, list):
                    raise Exception(
                        "Manifest preparation failed for one split:"
                        f" {manifest_paths}\n{traceback.format_exc()}"
                    )
                else:
                    manifest_split_paths.extend(manifest_paths)
            except Exception as e:
                raise Exception(e) from e
            finally:
                splits_progress.advance(splits_progress_task_id)

        splits_progress.update(splits_progress_task_id, visible=False)
        current_progress.stop_task(current_progress_task_id)
        current_progress.update(
            current_progress_task_id,
            description="[bold green]Manifest files prepared.",
        )

    print("[bold green]Manifest files created:[/bold green]")
    for manifest_path in manifest_split_paths:
        print(f"  - {manifest_path}")


async def _download_ami_split(
    split: str,
    split_dir: Path,
    session: aiohttp.ClientSession,
    step_progress: Progress,
    use_cache: bool,
    dataset_metadata: Dict[str, Any],
) -> TaskID:
    """Download a split of the AMI dataset."""
    filepath = await download_file(
        dataset_metadata["urls"]["list"].format(split),
        split_dir,
        session,
        use_cache=use_cache,
    )
    async with aiofiles.open(filepath, mode="r") as f:
        content = await f.read()

    file_ids = content.strip().split("\n")
    filtered_file_ids = [
        file_id
        for file_id in file_ids
        if file_id not in dataset_metadata["exclude_ids"]
    ]
    audio_types = dataset_metadata["audio_types"]

    file_download_results: List[Dict[str, str]] = []
    for file_id in filtered_file_ids:
        for audio_type in audio_types:
            file_download_results.append(
                _download_file(
                    url=f"https://groups.inf.ed.ac.uk/ami/AMICorpusMirror//amicorpus/{file_id}/audio/{file_id}.{audio_type}.wav",
                    output_dir=split_dir / "audio" / audio_type,
                    session=session,
                    use_cache=use_cache,
                )
            )
        file_download_results.append(
            _download_file(
                url=dataset_metadata["urls"]["rttm"].format(split, file_id),
                output_dir=split_dir / "rttm",
                session=session,
                use_cache=use_cache,
            )
        )
        file_download_results.append(
            _download_file(
                url=dataset_metadata["urls"]["uem"].format(split, file_id),
                output_dir=split_dir / "uem",
                session=session,
                use_cache=use_cache,
            )
        )

    step_task_id = step_progress.add_task(
        "", action=split, total=len(file_download_results)
    )
    for future in asyncio.as_completed(file_download_results):
        try:
            r = await future
            if not isinstance(r, Path):
                raise Exception(f"Download failed: {r}\n{traceback.format_exc()}")
        except Exception as e:
            raise Exception(e) from e
        finally:
            step_progress.advance(step_task_id)

    return step_task_id


async def _download_file(
    url: str,
    output_dir: Path,
    session: aiohttp.ClientSession,
    use_cache: bool,
) -> Path:
    """Wrapper around the utils download_file function to add concurrency."""
    concurr_token: ConcurrencyToken = await concurrency_handler.get()

    file_path = await download_file(url, output_dir, session, use_cache)

    concurrency_handler.put(concurr_token)

    return file_path


async def _prepare_ami_manifest_split(
    split_dir: Path,
    use_cache: bool,
    dataset_metadata: Dict[str, Any],
) -> List[Path]:
    """Prepare a manifest file."""
    rttm_files = []
    async for path in get_files(split_dir / "rttm"):
        rttm_files.append(path)

    uem_files = []
    async for path in get_files(split_dir / "uem"):
        uem_files.append(path)

    manifest_paths: List[Path] = []
    audio_types = dataset_metadata["audio_types"]
    for audio_type in audio_types:
        audio_type_path = split_dir / "audio" / audio_type
        audio_files = []
        async for path in get_files(audio_type_path):
            audio_files.append(path)

        audio_type_manifest_path = split_dir / f"manifest_{audio_type}.json"
        if use_cache is False or not audio_type_manifest_path.exists():
            manifest_path = await _create_manifest(
                audio_files, audio_type_manifest_path, rttm_files, uem_files
            )
        else:
            manifest_path = audio_type_manifest_path

        manifest_paths.append(manifest_path)

    return manifest_paths


async def _create_manifest(
    audio_files: List[Path],
    manifest_filepath: Path,
    rttm_files: List[Path],
    uem_files: List[Path],
) -> Path:
    """Create a manifest file."""
    if not len(audio_files) == len(rttm_files) == len(uem_files):
        raise Exception(
            f"Number of audio files ({len(audio_files)}), rttm files"
            f" ({len(rttm_files)}) and uem files ({len(uem_files)}) do not match."
            " Please check the dataset folder, there might be some extra or missing"
            " files."
        )

    if manifest_filepath.exists():
        manifest_filepath.unlink(missing_ok=True)

    manifest_file_content = []
    for audio, rttm, uem in zip(
        sorted(audio_files), sorted(rttm_files), sorted(uem_files)
    ):
        assert (
            audio.stem.split("_")[0]
            == rttm.stem.split(".")[0]
            == uem.stem.split(".")[0]
        )

        async with aiofiles.open(rttm, mode="r") as f:
            content = await f.read()

        labels = [
            line.strip().split()[7] for line in content.splitlines() if line.strip()
        ]
        meta = [
            {
                "audio_filepath": str(audio),
                "offset": 0,
                "duration": None,
                "label": "infer",
                "text": "-",
                "num_speakers": len(set(labels)),
                "rttm_filepath": str(rttm),
                "uem_filepath": str(uem),
                "ctm_filepath": None,
            }
        ]
        manifest_file_content.extend(meta)

    async with aiofiles.open(manifest_filepath, mode="w") as f:
        await f.write(json.dumps(manifest_file_content, indent=4))

    return manifest_filepath
