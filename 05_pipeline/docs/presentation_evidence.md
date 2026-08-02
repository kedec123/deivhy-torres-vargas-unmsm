# Presentation evidence: Child Anemia in Peru

## One-minute project summary

- **Topic:** weighted trends and observed inequalities in child anemia among Peruvian children aged 6-35 months, using ENDES 2019-2024.
- **Main problem:** a quantitative repeated cross-sectional secondary analysis of population patterns, not a clinical prediction system.
- **Data:** de-identified tabular survey data. The analytical file contains numeric and categorical variables for 57,539 eligible children.
- **Primary outcome:** `anemia_legacy`, a binary legacy-comparable category derived from ENDES `HW57` (1 = anemia; 0 = no anemia).
- **Secondary ML exercise:** binary classification used only to practise reproducible preprocessing, comparison, and experiment tracking.

## Data preparation and quality controls

The construction script temporarily joins ENDES `REC44`, `REC21`, and `REC0111`, applies the 6-35-month eligibility rule, creates a project-only non-identifying row label, and removes ENDES person, household, and case identifiers from the analytical CSV. Quality checks confirm 57,539 records, no duplicate analysis IDs, age range 6-35 months, positive weights, and no missing primary outcome. See `data/create_dataset.py`, `data_dictionary.csv`, and `quality_checks.md`.

For the classifier, numeric features use median imputation and standardization. Categorical features use most-frequent imputation and one-hot encoding. These transformations are fitted only on the training partition through a scikit-learn pipeline.

## Algorithm selection and observed results

Logistic Regression is the interpretable baseline. Random Forest and Extra Trees are nonlinear ensemble comparisons. The models are not selected by preference: each is evaluated on the same five prespecified stratified 80/20 splits (seeds 13, 21, 42, 87, and 100), and all metrics are recorded in MLflow.

| Model | Mean AUC-ROC | AUC-ROC SD | Mean F1 | Mean recall |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.7077 | 0.0038 | 0.6249 | 0.6506 |
| Random Forest | 0.7051 | 0.0035 | 0.6193 | 0.6396 |
| Extra Trees | 0.7050 | 0.0027 | 0.6223 | 0.6480 |

The values are internal exploratory results, not clinical performance, population prevalence, external validation, or evidence of fairness.

## Main analytical evidence

The primary descriptive analysis uses ENDES weights. Annual uncertainty intervals use a stratified-cluster bootstrap with the recorded stratum and cluster fields. A weighted logistic association model provides adjusted, non-causal associations. The 2024 legacy and updated outcome definitions are reported separately; they are not mixed into one trend.

## Presentation boundaries

- No causal claim: observed associations do not show what causes anemia or whether a programme worked.
- No clinical use: no diagnosis, screening, triage, treatment, eligibility, or ranking of people or territories.
- No claim that the separate Adult Census fairness exercise is an ENDES fairness result.
- The annual bootstrap intervals are design-aware course evidence, not official INEI replicate-weight estimates.
