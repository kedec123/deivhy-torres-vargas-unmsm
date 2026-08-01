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

## Transparent score

For the purpose of this course audit, each criterion is scored from 0 to 2: 0 means no public evidence located, 1 means partial reporting or access, and 2 means a publicly executable record. The assessment is therefore **3/14 (21%)**, which is classified here as **limited public reproducibility**.

| Criterion | Score | Reason for the score |
|---|---:|---|
| Data access | 1/2 | The dataset route is named, but permission is still required. |
| Code availability | 0/2 | No public implementation was located. |
| Random seeds | 0/2 | No seed was reported in the checked record. |
| Partitions and leakage controls | 1/2 | A split is described, but the full executable pipeline is absent. |
| Repetitions and stability | 0/2 | Repeated validation is described as future work. |
| Evaluation and uncertainty | 1/2 | Several point metrics are reported without interval estimates. |
| Compute and environment | 0/2 | A complete executable environment is not reported. |

The score is a reading aid, not a judgement of author intent or scientific validity. A paper can be useful while being hard to reproduce, and a higher reporting score would not prove that its substantive claim is correct.

## Overall reading

The paper is useful as a methodological comparison point because it makes the modelling goal and several preprocessing choices visible. Its public reproducibility is limited by the absence of released code, seeds, a fully specified environment, and repeated-split uncertainty. Those are reporting gaps, not proof that the findings are wrong.

## What this repository does differently

The ENDES project records source checksums, a DVC state, fixed seeds, train-only preprocessing, an executable environment, MLflow parameters and metrics, and a separate subgroup audit. These practices make the workflow easier to inspect. They do not make the exploratory model clinically valid or eliminate the need for independent replication.

## Audit record

The source, audit date, and reason for selecting the paper are recorded in `paper_source.md`. This repository does not download or alter the audited paper. The audit is based on the accessible article and linked materials reviewed on that date; a later code release or correction could change the assessment and should be recorded in a new version rather than silently replacing this one.
