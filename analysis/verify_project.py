"""Check the delivered notebook, assets and regenerated result files without fitting."""

import ast
import base64
import csv
import hashlib
import io
import json
import math
import re
from collections import Counter
from pathlib import Path

import nbformat
from PIL import Image
from verify_archived_predictions import metrics

project = Path(__file__).resolve().parents[1]
nb = nbformat.read(
    project / "Chest_XRay_Pneumonia_V5_Final_Research.ipynb", as_version=4
)
nbformat.validate(nb)
code = [c for c in nb.cells if c.cell_type == "code"]
assert len(nb.cells) == 32 and len(code) == 16
assert [c.execution_count for c in code] == list(range(1, 17))
assert (
    nb.metadata.research_provenance.execution_status
    == "PASSED_DEFAULT_SAVED_MODEL_WORKFLOW"
)
png_count = 0
for cell in nb.cells:
    assert "v3_" not in cell.source
    if cell.cell_type == "code":
        ast.parse(cell.source)
        assert not any(o.output_type == "error" for o in cell.outputs)
        for output in cell.outputs:
            if "image/png" in output.get("data", {}):
                raw = base64.b64decode(output.data["image/png"])
                Image.open(io.BytesIO(raw)).verify()
                png_count += 1
assert png_count == 8
latest = json.loads((project / "results/latest_run.json").read_text())
run_dir = project / latest["run_directory"]
verification = json.loads((run_dir / "verification.json").read_text())
assert (
    verification["original_source_unchanged"]
    and not verification["original_training_reproduced"]
)
for name, digest in json.loads(
    (project / "assets/integrity_manifest.json").read_text()
).items():
    assert (
        hashlib.sha256((project / "assets" / name).read_bytes()).hexdigest() == digest
    )
source = project / "archive/Chest_XRay_Pneumonia_V5_Development_Record.ipynb"
assert (
    hashlib.sha256(source.read_bytes()).hexdigest()
    == verification["source_archive_sha256"]
)


def readcsv(name):
    with (run_dir / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


for name, key in [
    ("historical_predictions.csv", "historical_metrics"),
    ("historical_unique_predictions.csv", "unique_byte_metrics"),
]:
    frame = readcsv(name)
    calculated = metrics(frame, verification["threshold"])
    for metric, value in calculated.items():
        assert math.isclose(value, verification[key][metric], abs_tol=1e-12), (
            name,
            metric,
            value,
        )
errors = readcsv("all_misclassifications.csv")
assert (
    len(errors)
    == verification["historical_metrics"]["fp"]
    + verification["historical_metrics"]["fn"]
)
assert Counter(r["error_type"] for r in errors) == {
    "FP": verification["historical_metrics"]["fp"],
    "FN": verification["historical_metrics"]["fn"],
}
for row in errors:
    assert math.isclose(
        float(row["signed_distance"]),
        float(row["p_pneumonia"]) - verification["threshold"],
        abs_tol=1e-7,
    )
    assert math.isclose(
        float(row["absolute_distance"]),
        abs(float(row["signed_distance"])),
        abs_tol=1e-7,
    )
history = readcsv("training_metric_history.csv")
assert Counter(r["phase"] for r in history) == {"head": 4, "fine_tune": 10}
# Independently check every recovered plotted metric against the original stdout.
original_stdout = (project / "assets/original_v5_training_stdout.txt").read_text(
    encoding="utf-8"
)
log_rows = []
for line in original_stdout.splitlines():
    if " - accuracy:" in line:
        pairs = dict(re.findall(r"([a-z_]+): ([0-9.e+-]+)", line))
        if all(
            key in pairs
            for key in [
                "accuracy",
                "auc",
                "loss",
                "val_accuracy",
                "val_auc",
                "val_loss",
            ]
        ):
            log_rows.append(pairs)
assert len(log_rows) == len(history)
for recovered, logged in zip(history, log_rows):
    for key in [
        "accuracy",
        "auc",
        "loss",
        "val_accuracy",
        "val_auc",
        "val_loss",
        "learning_rate",
    ]:
        assert math.isclose(float(recovered[key]), float(logged[key]), abs_tol=1e-12)
grid = readcsv("validation_threshold_grid.csv")
feasible = [
    r for r in grid if float(r["precision"]) >= 0.95 and float(r["recall"]) >= 0.95
]
chosen = max(
    feasible,
    key=lambda r: (float(r["specificity"]), float(r["threshold"]), float(r["f1"])),
)
assert float(chosen["threshold"]) == verification["threshold"]
for name in ["README.md", "requirements.txt", "technical_audit_report.md"]:
    assert (project / name).is_file() and (project / name).stat().st_size > 100
assert "Fresh image-based execution did not complete" not in (
    project / "README.md"
).read_text(encoding="utf-8")
result = dict(
    status="PASS",
    notebook_cells=len(nb.cells),
    executed_code_cells=len(code),
    embedded_pngs=png_count,
    actual_image_inventory_rows=len(readcsv("image_inventory.csv")),
    full_error_rows=len(errors),
    model_sha256=verification["model_sha256"],
    source_sha256=verification["source_archive_sha256"],
    original_source_unchanged=True,
    fresh_inference_reproduces_historical_metrics=True,
    saved_console_history_values_crosschecked=True,
    original_training_reproduced=False,
    independent_external_test=False,
)
(project / "evidence/final_quality_checks.json").write_text(
    json.dumps(result, indent=2), encoding="utf-8"
)
print(json.dumps(result, indent=2))
