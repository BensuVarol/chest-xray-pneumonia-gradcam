# Recorded V5 results

The [latest recorded run](latest_run.json) points to `20261022T185949_703755Z`. These files were generated during the preserved 22 October 2026 saved-model CPU verification. They are original full-precision CSV/JSON result files and saved figures from that matching research package, not transcriptions of rounded notebook tables. The current GitHub update rechecks artifact identity and prediction arithmetic; it does not claim another training or image-inference run.

## Evaluation scope

- Fitting / validation / historical benchmark: **3,781 / 956 / 624 images**.
- Locked decision rule: **PNEUMONIA if score >= 0.72**.
- Historical confusion matrix in NORMAL/PNEUMONIA order: **[[186, 48], [10, 380]]**.
- Historical accuracy **90.7051%**, precision **88.7850%**, recall **97.4359%**, F1 **92.9095%**, ROC-AUC **0.97456717**.
- Supplemental exact-byte-unique denominator: **618**, with six extra repeated files and no conflicting exact-byte labels.
- The historical benchmark informed earlier development. These results do not establish untouched independent test performance, verified patient/site independence, calibrated probabilities or clinical validity.

## Main files

| Artifact | Description |
|---|---|
| [historical_metrics.json](20261022T185949_703755Z/historical_metrics.json) | Primary 624-file result |
| [historical_predictions.csv](20261022T185949_703755Z/historical_predictions.csv) | All 624 recorded model scores and predictions |
| [historical_unique_metrics.json](20261022T185949_703755Z/historical_unique_metrics.json) | Supplemental 618-unique-byte result |
| [locked_run_policy.json](20261022T185949_703755Z/locked_run_policy.json) | Validation selection rule, selected threshold and validation metrics |
| [validation_predictions.csv](20261022T185949_703755Z/validation_predictions.csv) | All 956 recorded validation scores |
| [validation_threshold_grid.csv](20261022T185949_703755Z/validation_threshold_grid.csv) | Full 0.01–0.99 threshold search |
| [split_verification.json](20261022T185949_703755Z/split_verification.json) | Split membership, overlap checks and removals |
| [all_misclassifications.csv](20261022T185949_703755Z/all_misclassifications.csv) | All 48 FP and 10 FN cases with score distances |
| [normal_filename_group_errors.csv](20261022T185949_703755Z/normal_filename_group_errors.csv) | Descriptive IM/NORMAL2 error breakdown; not verified patient/site subgroups |
| [training_metric_history.csv](20261022T185949_703755Z/training_metric_history.csv) | Four-decimal console-log history from the original 14 training epochs |
| [verification.json](20261022T185949_703755Z/verification.json) | Recorded environment, score comparisons and execution limits |

## Saved figures

[Training curves](20261022T185949_703755Z/training_curves.png), [validation threshold selection](20261022T185949_703755Z/validation_threshold_selection.png), [historical confusion matrix/ROC/PR](20261022T185949_703755Z/historical_evaluation_curves.png), [TN/TP/FP/FN predictions](20261022T185949_703755Z/example_predictions.png), and Grad-CAM [TN](20261022T185949_703755Z/TN_gradcam.png), [TP](20261022T185949_703755Z/TP_gradcam.png), [FP](20261022T185949_703755Z/FP_gradcam.png), [FN](20261022T185949_703755Z/FN_gradcam.png).

Raw images are obtained separately from the dataset provider. See [third-party attribution](../THIRD_PARTY_NOTICES.md), [the main README](../README.md), and [current repository-update provenance](../evidence/repository_update.json).
