# Reproducibility Audit

## Audit boundary

This assessment examines the reporting and access conditions of Kukkar et al. (2026), described in `paper_source.md`. It does **not** claim to have reproduced the reported 98.5% accuracy. A reader should not infer an error from a missing item; it means only that the item was not available in the article or linked materials checked on the audit date.

| Criterion | Assessment | Evidence observed | Practical consequence |
|---|---|---|---|
| Data access | Partial | The article identifies the TDHS 2022 file and DHS access route, but says access was obtained with permission. | A qualified researcher may seek access, but a clean rerun is not immediate. |
| Code availability | Not public | The data/code statement says code is available on request and a public repository is planned. | Exact preprocessing and training cannot be independently inspected from a public repository. |
| Random seeds | Not reported | The methods describe stratification and model families, but no seed was located in the report. | Exact reruns may vary. |
| Partitions and leakage controls | Partial | A stratified train-test split and preprocessing steps are described, but the exact partition, fit order for every transformation, and full pipeline are unavailable. | The risk of unobservable leakage cannot be ruled out. |
| Repetitions and stability | Not reported | Repeated k-fold validation is described as future work. | The uncertainty from resampling is not quantified. |
| Evaluation and uncertainty | Partial | Multiple point metrics and explanatory plots are presented; confidence intervals and an independently reproducible test set are not provided. | Point performance should be interpreted cautiously. |
| Compute and environment | Not reported | No complete hardware, package-lock, or executable environment specification was found. | Runtime and exact numerical reproduction are difficult to assess. |

## Overall reading

The paper is useful as a methodological comparison point because it makes the modelling goal and several preprocessing choices visible. Its public reproducibility is limited by the absence of released code, seeds, a fully specified environment, and repeated-split uncertainty. Those are reporting gaps, not proof that the findings are wrong.

## What this repository does differently

The ENDES project records source checksums, a DVC state, fixed seeds, train-only preprocessing, an executable environment, MLflow parameters and metrics, and a separate subgroup audit. These practices make the workflow easier to inspect. They do not make the exploratory model clinically valid or eliminate the need for independent replication.
