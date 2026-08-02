# Model Card: Exploratory ENDES Child Anemia Classifier

## Model details

Three models are trained in `05_pipeline/src/train.py`: Logistic Regression, Random Forest, and Extra Trees. They predict the **legacy ENDES anemia category** in a de-identified analytical dataset for reproducibility practice. Logistic Regression is the interpretable baseline; Random Forest and Extra Trees are nonlinear ensemble comparisons. The models are evaluated on five prespecified splits using seeds 13, 21, 42, 87, and 100.

## Intended use

The intended use is a course demonstration of reproducible preprocessing, experiment tracking, and subgroup inspection. The model may support exploratory discussion of which observed survey variables are informative in this dataset.

## Out-of-scope use

Do not use this model for diagnosis, screening, treatment, triage, benefit eligibility, risk scoring of an individual, or ranking a household, department, or community. It is not validated for clinical care and should not be deployed in a health service.

## Inputs and output

Inputs are child age, child sex code, maternal education code, wealth quintile, urban-rural residence code, department code, and survey year. The output is a probability-like score and a thresholded exploratory label. Haemoglobin values and the anemia outcome are not included among features.

## Evaluation design

Each experiment uses a stratified 80/20 train-test split. Imputation, scaling, and one-hot encoding are learned inside the pipeline on training data. Training uses normalized ENDES weights; the reported classifier metrics are unweighted holdout metrics and should not be read as population prevalence measures. MLflow stores split seed, model, data SHA-256, Git commit, and metrics for every run.

Across the five prespecified splits, Logistic Regression had mean AUC-ROC 0.7077, PR-AUC 0.6377, accuracy 0.6563, F1 0.6249, and recall 0.6506. Random Forest had mean AUC-ROC 0.7051 and Extra Trees 0.7050. The AUC-ROC standard deviation was below 0.004 for each model. These values describe one internal exploratory task only; they are not a measure of clinical benefit, calibration, transportability, or fairness.

## Known limitations and risks

ENDES is cross-sectional and records a limited set of variables. The model can reflect survey measurement, structural inequities, and the selected definition of anemia. Department and residence are useful for group description but can also encode historical disadvantage. The outcome is a survey-derived category, not a clinical examination. The 2024 measurement update makes cross-year interpretation especially sensitive.

The model card is paired with `datasheet.md` and the ethics protocol. A similar overall score across groups would not prove fairness, and a difference would require contextual investigation rather than a mechanical fix.

## Version, ownership, and training record

| Item | Recorded value |
|---|---|
| Version | Course artefact, ENDES 2019-2024 build recorded on 31 July 2026 |
| Owner | Deivhy Torres Vargas |
| Framework | scikit-learn 1.5.2 |
| Training population | 57,539 eligible de-identified ENDES child records before the stratified split |
| Outcome | Legacy binary anemia category derived from `HW57` |
| Data version evidence | DVC pointer, source checksums, and dataset SHA-256 logged in MLflow |
| Reproducibility evidence | Five prespecified stratified splits, pinned dependencies, Git commit, and MLflow records |

## Reported internal performance

| Model | Mean AUC-ROC (SD) | Mean PR-AUC | Mean accuracy | Mean F1 | Mean recall |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.7077 (0.0038) | 0.6377 | 0.6563 | 0.6249 | 0.6506 |
| Random Forest | 0.7051 (0.0035) | 0.6401 | 0.6540 | 0.6193 | 0.6396 |
| Extra Trees | 0.7050 (0.0027) | 0.6402 | 0.6538 | 0.6223 | 0.6480 |

These are mean values across five prespecified internal splits, not confidence intervals and not an external validation. They should never be compared with a clinical benchmark or interpreted as evidence that the model improves child health outcomes.

## Evaluation factors

The retained subgroup check reports observed outcome rate, average score, accuracy, and true-positive rate by child sex and residence for one fixed logistic-regression split. It is a diagnostic prompt rather than a fairness certification. Department, residence, and household-related variables may encode structural conditions that are meaningful for population description but harmful if used to target or exclude an individual.

The separate Adult Census exercise in `11_bias_audit/` is included to practise fairness measurement and mitigation on a standard benchmark. Its results do not transfer automatically to ENDES, Peru, or anemia policy.

## Deployment and monitoring decision

This artefact is not approved for deployment. No API, score report, or automated decision should be built from it. A future model would require a separately approved purpose, clinical and external validation, calibration assessment, stakeholder review, a data-governance agreement, and an explicit monitoring plan. Any future update must create a new versioned data and model record rather than overwriting these results.
