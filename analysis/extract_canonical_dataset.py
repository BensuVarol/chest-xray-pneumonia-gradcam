"""Retrieve one complete image tree from the official duplicated Kaggle ZIP.

This optional helper uses public SDK/range requests and checks each selected
ZIP member's CRC. It does not claim to download or MD5-check the entire ZIP.
Downloaded images are subsequently SHA-256-checked by the notebook.
"""

import argparse
import io
import json
import math
import os
import shutil
import struct
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from kagglehub.clients import build_kaggle_client
from kagglesdk.datasets.types.dataset_api_service import ApiDownloadDatasetRequest

parser = argparse.ArgumentParser()
parser.add_argument("--cache-dir", required=True)
parser.add_argument("--output-dir", required=True)
args = parser.parse_args()
cache_dir = Path(args.cache_dir).resolve()
output_dir = Path(args.output_dir).resolve()
started = time.monotonic()
with build_kaggle_client() as client:
    request = ApiDownloadDatasetRequest()
    request.owner_slug = "paultimothymooney"
    request.dataset_slug = "chest-xray-pneumonia"
    request.dataset_version_number = 2
    response = client.datasets.dataset_api_client.download_dataset(request)
    response.raise_for_status()
    total = int(response.headers["Content-Length"])
    url = response.url
    response.close()

    def fetch(start, end):
        with requests.get(
            url, headers={"Range": f"bytes={start}-{end}"}, timeout=(10, 60)
        ) as response:
            assert response.status_code == 206
            assert response.headers["Content-Range"] == f"bytes {start}-{end}/{total}"
            content = response.content
        assert len(content) == end - start + 1
        return content

    tail_start = max(0, total - 65557)
    tail = fetch(tail_start, total - 1)
    eocd = tail.rfind(b"PK\x05\x06")
    assert eocd >= 0
    fields = struct.unpack("<4s4H2LH", tail[eocd : eocd + 22])
    central_offset = fields[6]
    central = fetch(central_offset, total - 1)
    scratch = cache_dir / "canonical_transfer"
    scratch.mkdir(exist_ok=True)
    sparse_path = scratch / "selected_tree_zip_view.zip"
    # A sparse logical view is used only to access selected ZIP members.
    with sparse_path.open("wb") as view:
        view.truncate(total)
        view.seek(central_offset)
        view.write(central)
    with zipfile.ZipFile(sparse_path) as z:
        selected = [
            info
            for info in z.infolist()
            if info.filename.startswith("chest_xray/chest_xray/")
            and Path(info.filename).suffix.lower()
            in {".jpg", ".jpeg", ".png", ".bmp", ".gif"}
        ]
        assert (
            len(selected) == 5856
        ), "Unexpected canonical tree; inspect provider inventory before continuing."
        canonical_start = min(info.header_offset for info in selected)
        # The local header's optional fields end before the next member header.
        ordered = sorted(z.infolist(), key=lambda info: info.header_offset)
        offsets = [info.header_offset for info in ordered]
        last = max(info.header_offset for info in selected)
        canonical_end = next(offset for offset in offsets if offset > last)
    partial = cache_dir / "datasets/paultimothymooney/chest-xray-pneumonia/2.archive"
    retained = partial.open("rb").seek(0, 2) if partial.exists() else 0
    segments = []
    if retained:
        segments.append((0, partial, retained))
    part_folders = sorted(partial.parent.glob("range_parts_*"))
    if retained and part_folders:
        step = math.ceil((total - retained) / 8)
        for part in sorted(part_folders[-1].glob("segment_*.part")):
            index = int(part.stem.split("_")[1])
            with part.open("rb") as f:
                size = f.seek(0, 2)
            if size:
                segments.append((retained + index * step, part, size))
    coverage = []
    with sparse_path.open("r+b") as destination:
        for start, path, size in segments:
            stop = min(start + size, canonical_end)
            begin = max(start, canonical_start)
            if begin >= stop:
                continue
            with path.open("rb") as source:
                source.seek(begin - start)
                destination.seek(begin)
                remaining = stop - begin
                while remaining:
                    chunk = source.read(min(8 * 1024 * 1024, remaining))
                    assert chunk
                    destination.write(chunk)
                    remaining -= len(chunk)
            coverage.append((begin, stop))
    gaps = []
    cursor = canonical_start
    for start, stop in sorted(coverage):
        if start > cursor:
            gaps.append((cursor, start))
        cursor = max(cursor, stop)
    if cursor < canonical_end:
        gaps.append((cursor, canonical_end))
    tasks = []
    for start, stop in gaps:
        for begin in range(start, stop, 32 * 1024 * 1024):
            tasks.append((begin, min(stop, begin + 32 * 1024 * 1024)))
    missing = sum(stop - start for start, stop in gaps)
    print(
        f"Canonical tree: {len(selected)} images; {missing} missing compressed bytes in {len(tasks)} blocks.",
        flush=True,
    )

    def transfer(item):
        start, stop = item
        data = fetch(start, stop - 1)
        with sparse_path.open("r+b") as destination:
            destination.seek(start)
            destination.write(data)
        return len(data)

    received = 0
    with ThreadPoolExecutor(max_workers=8) as workers:
        for future in as_completed([workers.submit(transfer, item) for item in tasks]):
            received += future.result()
            print(
                f"Canonical transfer: {received}/{missing} bytes; elapsed {time.monotonic()-started:.1f}s",
                flush=True,
            )
output_dir.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(sparse_path) as z:
    for info in selected:
        relative = Path(info.filename).relative_to("chest_xray/chest_xray")
        target = (output_dir / relative).resolve()
        assert target.is_relative_to(output_dir)
        target.parent.mkdir(parents=True, exist_ok=True)
        # Reading to EOF verifies this member's CRC through ZipExtFile.
        with z.open(info) as source, target.open("wb") as destination:
            shutil.copyfileobj(source, destination)
evidence = dict(
    provider="Official Kaggle SDK dataset version 2 archive",
    canonical_images=len(selected),
    selected_members_crc_check="PASS",
    full_archive_md5_checked=False,
    duplicate_tree_and_mac_metadata_excluded=True,
    output_directory=str(output_dir),
    missing_compressed_bytes_transferred=missing,
    elapsed_seconds=time.monotonic() - started,
    note="Notebook verifies the available original SHA-256 hashes after this selected-tree extraction. No KaggleHub full-bundle completion marker is created.",
)
project = Path(__file__).resolve().parents[1]
(project / "evidence/dataset_retrieval.json").write_text(
    json.dumps(evidence, indent=2), encoding="utf-8"
)
print(json.dumps(evidence, indent=2), flush=True)
