"""Independently check archived metrics using only Python's standard library.

This checks prediction arithmetic/provenance, not fresh model inference.
ROC-AUC is computed from all positive/negative score pairs with ties weighted 0.5.
"""

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

project = Path(__file__).resolve().parents[1]
assets = project / "assets"


def rows(name):
    with (assets / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def metrics(frame, threshold):
    counts = Counter(
        (int(row["y_true"]), int(float(row["p_pneumonia"]) >= threshold))
        for row in frame
    )
    tn, fp, fn, tp = [counts[key] for key in [(0, 0), (0, 1), (1, 0), (1, 1)]]
    positives = [float(r["p_pneumonia"]) for r in frame if int(r["y_true"]) == 1]
    negatives = [float(r["p_pneumonia"]) for r in frame if int(r["y_true"]) == 0]
    auc = sum((p > n) + 0.5 * (p == n) for p in positives for n in negatives) / (
        len(positives) * len(negatives)
    )
    return dict(
        n=len(frame),
        threshold=threshold,
        tn=tn,
        fp=fp,
        fn=fn,
        tp=tp,
        accuracy=(tn + tp) / len(frame),
        precision=tp / (tp + fp) if tp + fp else 0.0,
        recall=tp / (tp + fn),
        specificity=tn / (tn + fp),
        f1=2 * tp / (2 * tp + fp + fn),
        roc_auc=auc,
    )


def main():
    policy = json.loads((assets / "original_locked_policy.json").read_text())
    manifest = json.loads((assets / "original_split_manifest.json").read_text())
    validation = rows("original_validation_predictions.csv")
    historical = rows("original_historical_predictions.csv")
    for frame, split in [(validation, "validation"), (historical, "historical_test")]:
        assert [r["file"] for r in frame] == manifest["files"][split]
        assert all(
            int(r["y_true"]) == int(Path(r["file"]).parent.name == "PNEUMONIA")
            for r in frame
        )
        assert all(
            math.isfinite(float(r["p_pneumonia"])) and 0 <= float(r["p_pneumonia"]) <= 1
            for r in frame
        )
    feasible = []
    for threshold in policy["protocol"]["threshold_grid"]:
        m = metrics(validation, threshold)
        if (
            m["precision"] >= policy["protocol"]["precision_floor"]
            and m["recall"] >= policy["protocol"]["recall_floor"]
        ):
            feasible.append(m)
    chosen = max(feasible, key=lambda m: (m["specificity"], m["threshold"], m["f1"]))
    assert chosen["threshold"] == policy["decision_threshold"]
    computed = metrics(historical, chosen["threshold"])
    reported = json.loads((assets / "original_historical_metrics.json").read_text())
    for key, value in computed.items():
        if key in reported:
            assert math.isclose(value, reported[key], abs_tol=1e-12)
    duplicates = defaultdict(list)
    for row in historical:
        duplicates[manifest["historical_test_hashes"][row["file"]]].append(row)
    assert all(len({r["y_true"] for r in group}) == 1 for group in duplicates.values())
    unique = [group[0] for group in duplicates.values()]
    model_hash = hashlib.sha256(
        (assets / "selected_model.keras").read_bytes()
    ).hexdigest()
    assert model_hash == policy["model_sha256"]
    result = dict(
        status="PASS",
        scope="Archived prediction arithmetic and artifact identity; not fresh image inference",
        model_sha256=model_hash,
        validation_selection=chosen,
        historical_metrics=computed,
        unique_byte_metrics=metrics(unique, chosen["threshold"]),
        extra_duplicate_files=len(historical) - len(unique),
        conflicting_hash_labels=0,
    )
    (project / "evidence/independent_prediction_checks.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
