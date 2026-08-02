# Design-aware uncertainty and adjusted associations

Annual prevalence intervals use a stratified cluster bootstrap (300 replicates) with ENDES stratum and cluster fields. The adjusted association model is a weighted logistic regression with model-based 95% intervals. These estimates describe observed associations; they do not establish causality.

## Annual weighted prevalence with 95% intervals

|   survey_year |   sample_size |   weighted_anemia_prevalence |   ci_95_lower |   ci_95_upper |   bootstrap_replicates |
|--------------:|--------------:|-----------------------------:|--------------:|--------------:|-----------------------:|
|     2019.0000 |    10320.0000 |                       0.3983 |        0.3849 |        0.4094 |               300.0000 |
|     2020.0000 |     6051.0000 |                       0.3825 |        0.3654 |        0.4006 |               300.0000 |
|     2021.0000 |    10902.0000 |                       0.3844 |        0.3739 |        0.3956 |               300.0000 |
|     2022.0000 |    10557.0000 |                       0.4199 |        0.4094 |        0.4310 |               300.0000 |
|     2023.0000 |     9951.0000 |                       0.4278 |        0.4147 |        0.4406 |               300.0000 |
|     2024.0000 |     9758.0000 |                       0.4351 |        0.4232 |        0.4455 |               300.0000 |

## Interpretation boundary

The bootstrap is a transparent design-aware course implementation, not an official INEI replicate-weight estimator. The logistic model uses relative survey weights and model-based intervals; a full survey-design variance model remains a later methodological extension. It is an association model, not a prediction model and not evidence of a causal effect.

The primary trend continues to use legacy `HW57` in every year. A separate 2024 sensitivity comparison is produced by `sensitivity_2024.py`.
