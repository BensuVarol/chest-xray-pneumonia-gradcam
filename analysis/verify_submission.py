"""Check final submission dependencies, source identity and portability.

This does not fit a model or replace the separate image-inference execution.
Cell indices in the dependency inventory are zero-based.
"""

import ast
import hashlib
import json
import re
from pathlib import Path

import nbformat

project = Path(__file__).resolve().parents[1]
notebook_path = project / "Chest_XRay_Pneumonia_V5_Final_Research.ipynb"
nb = nbformat.read(notebook_path, as_version=4)
nbformat.validate(nb)
manifest = json.loads((project / "assets/integrity_manifest.json").read_text())
dependencies = {}
for index, cell in enumerate(nb.cells):
    if cell.cell_type != "code":
        continue
    tree = ast.parse(cell.source)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.BinOp)
            and isinstance(node.op, ast.Div)
            and isinstance(node.left, ast.Name)
            and node.left.id == "ASSETS"
            and isinstance(node.right, ast.Constant)
            and isinstance(node.right.value, str)
        ):
            dependencies.setdefault("assets/" + node.right.value, set()).add(index)

required = {
    "assets/integrity_manifest.json",
    "requirements.txt",
    "archive/Chest_XRay_Pneumonia_V5_Development_Record.ipynb",
}
required.update("assets/" + name for name in manifest)
inventory = []
for name in sorted(required | set(dependencies)):
    path = project / name
    assert path.is_file(), "Missing submission dependency: " + name
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if name.startswith("assets/") and path.name in manifest:
        assert digest == manifest[path.name], name
    direct_cells = sorted(dependencies.get(name, set()))
    inventory.append(
        dict(
            file=name,
            exists=True,
            bytes=path.stat().st_size,
            sha256=digest,
            direct_consumer_cells=direct_cells,
            integrity_gate_cell=2 if name.startswith("assets/") else None,
        )
    )

source_path = project / "archive/Chest_XRay_Pneumonia_V5_Development_Record.ipynb"
source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
assert source_hash == nb.metadata.research_provenance.source_sha256
latest = json.loads((project / "results/latest_run.json").read_text())["run_directory"]
verification = json.loads((project / latest / "verification.json").read_text())
execution = json.loads((project / "evidence/fresh_execution.json").read_text())
assert (
    source_hash
    == verification["source_archive_sha256"]
    == execution["original_source_sha256"]
)
model_hash = hashlib.sha256(
    (project / "assets/selected_model.keras").read_bytes()
).hexdigest()
assert (
    model_hash
    == nb.metadata.research_provenance.model_sha256
    == verification["model_sha256"]
)
assert (
    execution["notebook_source_sha256"]
    == hashlib.sha256("".join(c.source for c in nb.cells).encode()).hexdigest()
)
assert execution["status"] == "PASSED_DEFAULT_SAVED_MODEL_WORKFLOW"
assert execution["error_outputs"] == 0 and execution["executed_code_cells"] == 16
assert not execution["training_rerun"]


def personal_path(value):
    if isinstance(value, str):
        normalized = value.lower().replace("\\", "/")
        while "//" in normalized:
            normalized = normalized.replace("//", "/")
        return bool(re.search(r"(?:[a-z]:/users/|/home/|/users/)", normalized))
    if isinstance(value, dict):
        return any(personal_path(v) for v in value.values())
    if isinstance(value, list):
        return any(personal_path(v) for v in value)
    return False


assert not personal_path(nb), "Personal absolute path in current notebook"
path_audit = []
for path in sorted((project / latest).iterdir()):
    if path.suffix == ".json":
        assert not personal_path(json.loads(path.read_text())), path.name
    elif path.suffix in {".csv", ".txt"}:
        assert not personal_path(path.read_text()), path.name
    path_audit.append(path.name)
for name in [
    "README.md",
    "requirements.txt",
    "technical_audit_report.md",
    "THIRD_PARTY_NOTICES.md",
    ".gitignore",
]:
    assert (project / name).is_file()
    assert not personal_path((project / name).read_text(encoding="utf-8"))
readme = (project / "README.md").read_text(encoding="utf-8")
for heading in [
    "Project Overview",
    "Dataset",
    "Methodology",
    "Model Architecture",
    "Training and Evaluation",
    "Results",
    "Grad-CAM",
    "Limitations",
    "Reproducibility Instructions",
]:
    assert "## " + heading in readme
for value in [
    "90.7051%",
    "97.4359%",
    "92.9095%",
    "0.97456717",
    "0.72",
    "186 / 48 / 10 / 380",
]:
    assert value in readme
assert (
    "akciğer dışı"
    in (project / "technical_audit_report.md").read_text(encoding="utf-8").lower()
)

result = dict(
    status="PASS",
    dependency_cell_indices="zero-based",
    required_files=inventory,
    missing_required_files=[],
    source_metadata_matches_archive=True,
    source_sha256=source_hash,
    model_sha256=model_hash,
    notebook_source_matches_latest_execution=True,
    personal_paths_in_current_notebook=False,
    latest_result_files_checked=path_audit,
    readme_required_sections_present=True,
    readme_results_consistent=True,
    original_archive_privacy_sanitized=False,
    original_training_reproduced=False,
    colab_execution_repeated=False,
    unavailable_nonblocking_historical_assets=[
        "Complete V1 model/predictions",
        "All V3 candidate models/predictions",
        "Original intermediate epoch checkpoints",
        "Original optimizer state",
        "Native original Keras History objects",
    ],
)
(project / "evidence/submission_asset_audit.json").write_text(
    json.dumps(result, indent=2), encoding="utf-8"
)
print(
    json.dumps(
        dict(
            status=result["status"],
            required_file_count=len(inventory),
            missing_required_files=[],
            source_metadata_matches_archive=True,
            personal_paths_in_current_notebook=False,
            notebook_source_matches_latest_execution=True,
        ),
        indent=2,
    )
)
