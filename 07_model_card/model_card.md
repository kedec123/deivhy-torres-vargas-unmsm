# Model Card: Exploratory ENDES Child Anemia Classifier

## Model details

Two models are trained in `05_pipeline/src/train.py`: logistic regression and random forest. They predict the **legacy ENDES anemia category** in a de-identified analytical dataset for reproducibility practice. Logistic regression is the primary baseline; random forest is a non-linear comparison. Fixed seeds are 13, 21, 42, 87, and 100.

## Intended use

The intended use is a course demonstration of reproducible preprocessing, experiment tracking, and subgroup inspection. The model may support exploratory discussion of which observed survey variables are informative in this dataset.

## Out-of-scope use

Do not use this model for diagnosis, screening, treatment, triage, benefit eligibility, risk scoring of an individual, or ranking a household, department, or community. It is not validated for clinical care and should not be deployed in a health service.

## Inputs and output

Inputs are child age, child sex code, maternal education code, wealth quintile, urban-rural residence code, department code, and survey year. The output is a probability-like score and a thresholded exploratory label. Haemoglobin values and the anemia outcome are not included among features.

## Evaluation design

Each experiment uses a stratified 75/25 train-test split. Imputation, scaling, and one-hot encoding are learned inside the pipeline on training data. Training uses normalized ENDES weights; the reported classifier metrics are unweighted holdout metrics and should not be read as population prevalence measures. MLflow stores seed, model, data SHA-256, Git commit, and metrics for every run.

Across the five fixed splits, logistic regression had mean AUC-ROC 0.7063, PR-AUC 0.6353, accuracy 0.6550, F1 0.6241, and recall 0.6509. Random forest had mean AUC-ROC 0.7043 and F1 0.6198. These values describe one internal exploratory task only; they are not a measure of clinical benefit, calibration, transportability, or fairness.

## Known limitations and risks

ENDES is cross-sectional and records a limited set of variables. The model can reflect survey measurement, structural inequities, and the selected definition of anemia. Department and residence are useful for group description but can also encode historical disadvantage. The outcome is a survey-derived category, not a clinical examination. The 2024 measurement update makes cross-year interpretation especially sensitive.

The model card is paired with `datasheet.md`, `11_bias_audit/endes_subgroup_check.md`, and the ethics protocol. A similar overall score across groups would not prove fairness, and a difference would require contextual investigation rather than a mechanical fix.
