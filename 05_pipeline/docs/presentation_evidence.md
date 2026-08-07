# Presentation evidence: Child Anemia in Peru

## Topic, problem and data

- **Topic:** weighted trends and observed inequalities in child anemia among Peruvian children aged 6-35 months, using ENDES 2019-2024.
- **Main problem:** a quantitative repeated cross-sectional secondary analysis of population patterns, not a clinical prediction system.
- **Data:** 57,539 de-identified tabular survey records with numeric and categorical variables. ENDES weight, stratum and primary sampling unit fields support the annual prevalence estimates.
- **Primary outcome:** `anemia_legacy`, the binary legacy-comparable category derived from `HW57`.
- **Secondary exercise:** binary classification used only to practise reproducible preprocessing, model comparison and local experiment tracking.

## Main analytical evidence

Annual prevalence uses Taylor linearization with ENDES final weights, strata and PSUs; a stratified-cluster bootstrap with 300 replicates is retained as an independent comparison. The resulting Taylor 95% intervals are 38.6%-41.1% (2019), 36.5%-40.0% (2020), 37.3%-39.6% (2021), 40.8%-43.2% (2022), 41.5%-44.1% (2023), and 42.3%-44.8% (2024). See `analysis_by_year_with_ci.csv` and `analysis_ci_method_comparison.csv`.

The adjusted pooled logistic association model uses 2019 as the reference year. Relative to 2019, the modelled odds are significantly higher in 2023 (OR 1.1239, 95% CI 1.0581-1.1937, p<0.001) and 2024 (OR 1.1617, 95% CI 1.0923-1.2355, p<0.001). These intervals and p-values are model-based associations, not causal effects or a full survey-design regression variance estimator. See `modelled_year_effects_vs_2019.csv`.

The 2024 legacy `HW57` estimate (43.5%) and updated `HW57A` estimate (34.9%) are shown separately. Their difference is a measurement-definition sensitivity comparison, not evidence of an abrupt change in child health.

ENDES 2020 collection was adapted during the COVID-19 emergency, including telephone interviews and a gradual return to in-person work with biosecurity measures. The smaller 2020 analytical sample and its lower point estimate are therefore not over-interpreted as a definitive epidemiological change.

## Exploratory classifier — intentionally subordinate

Logistic Regression, Random Forest and Extra Trees are evaluated across the same five prespecified stratified 80/20 splits (seeds 13, 21, 42, 87 and 100). The best mean internal AUC-ROC is 0.7077 for Logistic Regression (SD 0.0038). This is neither clinical performance, external validation, population prevalence nor evidence of fairness. `experiment_results.csv` and `experiment_summary.csv` are the portable evidence; MLflow is recreated locally and excluded from Git because it stores machine paths.

## Reproducibility statement

A clean clone can run `data/download_endes.py` to obtain 18 public official ENDES archives, verify them against the committed SHA-256 source manifest, and rebuild the analytical CSV before running the analysis scripts. No Google Drive access, token or service-account key is required. DVC remains a checksum-based data-version record, not the required data-access path.

## Presentation boundaries

- No causal claim: observed associations do not identify what causes anemia or whether a programme worked.
- No clinical use: no diagnosis, screening, triage, treatment, eligibility or ranking of people or territories.
- No transfer of the separate Adult Census fairness exercise to ENDES.
- The annual Taylor intervals are design-based for prevalence; the adjusted model's inferential quantities are explicitly model-based.
