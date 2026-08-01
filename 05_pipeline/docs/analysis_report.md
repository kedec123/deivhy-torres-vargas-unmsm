# Weighted descriptive analysis

This report describes the de-identified analytical CSV built from the official ENDES modules. Estimates use the normalized ENDES individual weight (`V005/1,000,000`) as a descriptive weight. The current script does not compute design-based standard errors or confidence intervals; those are required before any formal population inference.

- Dataset SHA-256: `78e79e4bbff39d5cf317031b138c07a659a3de9cfdcb7f8cab227dbb8503cd6d`
- Eligible children: 57,539
- Outcome: legacy-comparable binary anemia category derived from `HW57`.
- Scope: children aged 6-35 months in ENDES 2019-2024.

## Trend by year

|   survey_year |   sample_size |   weighted_population |   weighted_anemia_prevalence |
|--------------:|--------------:|----------------------:|-----------------------------:|
|     2019.0000 |    10320.0000 |             4689.6039 |                       0.3983 |
|     2020.0000 |     6051.0000 |             3325.8423 |                       0.3825 |
|     2021.0000 |    10902.0000 |             4597.8122 |                       0.3844 |
|     2022.0000 |    10557.0000 |             4475.4625 |                       0.4199 |
|     2023.0000 |     9951.0000 |             4057.0028 |                       0.4278 |
|     2024.0000 |     9758.0000 |             3757.5018 |                       0.4351 |

## Interpretation boundary

The series is designed for internal comparability because it uses the legacy field in all years. It should not be substituted for the official 2024 figure produced with the updated measurement definition. The table is descriptive, not causal evidence.
