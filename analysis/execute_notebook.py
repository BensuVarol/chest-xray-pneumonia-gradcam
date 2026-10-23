"""Execute the saved-model workflow in a new kernel using this Python environment.

Run from the project root: python analysis/execute_notebook.py
No global Jupyter kernel registration and no training are performed.
"""

import asyncio
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import nbformat
from nbclient import NotebookClient

project = Path(__file__).resolve().parents[1]
notebook_path = project / "Chest_XRay_Pneumonia_V5_Final_Research.ipynb"
evidence = project / "evidence"
evidence.mkdir(exist_ok=True)
notebook = nbformat.read(notebook_path, as_version=4)
nbformat.validate(notebook)
for cell in notebook.cells:
    if cell.cell_type == "code":
        cell.outputs = []
        cell.execution_count = None
original = project / "archive/Chest_XRay_Pneumonia_V5_Development_Record.ipynb"
original_hash = hashlib.sha256(original.read_bytes()).hexdigest()
source_hash = hashlib.sha256(
    "".join(c.source for c in notebook.cells).encode()
).hexdigest()
os.environ.update(
    PYTHONUTF8="1",
    CUDA_VISIBLE_DEVICES="-1",
    TF_ENABLE_ONEDNN_OPTS="0",
    TF_NUM_INTRAOP_THREADS="4",
    TF_NUM_INTEROP_THREADS="2",
    MPLBACKEND="module://matplotlib_inline.backend_inline",
)
# An optional cache path keeps the public image download outside the deliverable.
if "--cache-dir" in sys.argv:
    os.environ["KAGGLEHUB_CACHE"] = str(
        Path(sys.argv[sys.argv.index("--cache-dir") + 1]).resolve()
    )
if "--dataset-root" in sys.argv:
    os.environ["PNEUMONIA_DATA_ROOT"] = str(
        Path(sys.argv[sys.argv.index("--dataset-root") + 1]).resolve()
    )
started_at = datetime.now(timezone.utc).isoformat()
started = time.monotonic()
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
status = "FAILED"
failure = None


def announce(cell, cell_index, **kwargs):
    if cell.cell_type == "code":
        print(
            f"Executing cell {cell_index+1}/{len(notebook.cells)}: {cell.source.splitlines()[0][:85]}",
            flush=True,
        )


try:
    with tempfile.TemporaryDirectory(prefix="pneumonia-v5-kernel-") as tmp:
        spec = Path(tmp) / "kernels/pneumonia-v5-review"
        spec.mkdir(parents=True)
        (spec / "kernel.json").write_text(
            json.dumps(
                dict(
                    argv=[
                        sys.executable,
                        "-m",
                        "ipykernel_launcher",
                        "-f",
                        "{connection_file}",
                    ],
                    display_name="Pneumonia V5 isolated review",
                    language="python",
                )
            ),
            encoding="utf-8",
        )
        previous = os.environ.get("JUPYTER_PATH")
        os.environ["JUPYTER_PATH"] = str(Path(tmp)) + (
            os.pathsep + previous if previous else ""
        )
        client = NotebookClient(
            notebook,
            timeout=1800,
            kernel_name="pneumonia-v5-review",
            allow_errors=False,
            record_timing=True,
            on_cell_start=announce,
            resources={"metadata": {"path": str(project)}},
        )
        client.execute(cwd=str(project))
        status = "PASSED_DEFAULT_SAVED_MODEL_WORKFLOW"
except Exception as exc:
    failure = f"{type(exc).__name__}: {exc}"
    print(failure, flush=True)
finally:
    code_cells = [c for c in notebook.cells if c.cell_type == "code"]
    result = dict(
        status=status,
        execution_engine="nbclient; new ipykernel subprocess in the pinned dedicated verification environment",
        started_at_utc=started_at,
        finished_at_utc=datetime.now(timezone.utc).isoformat(),
        elapsed_seconds=time.monotonic() - started,
        python=platform.python_version(),
        platform=platform.platform(),
        python_interpreter=Path(sys.executable).name,
        cpu_only=True,
        training_rerun=False,
        environment_recreated_for_this_run=False,
        fresh_kernel_for_this_run=True,
        notebook_source_sha256=source_hash,
        executed_code_cells=sum(c.execution_count is not None for c in code_cells),
        total_code_cells=len(code_cells),
        error_outputs=sum(
            o.output_type == "error" for c in code_cells for o in c.outputs
        ),
        original_source_sha256=original_hash,
        original_source_unchanged=hashlib.sha256(original.read_bytes()).hexdigest()
        == original_hash,
        failure=failure,
    )
    notebook.metadata["research_provenance"].update(
        execution_status=status,
        fresh_kernel=True,
        training_reproduced=False,
        execution_environment="See evidence/fresh_execution.json and verification_environment_freeze.txt",
    )
    destination = (
        notebook_path
        if status.startswith("PASSED")
        else evidence / "fresh_execution_failed.ipynb"
    )
    nbformat.write(notebook, destination)
    (evidence / "fresh_execution.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    freeze = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    (evidence / "verification_environment_freeze.txt").write_text(
        freeze, encoding="utf-8"
    )
    print(json.dumps(result, indent=2), flush=True)
if failure:
    raise SystemExit(1)
