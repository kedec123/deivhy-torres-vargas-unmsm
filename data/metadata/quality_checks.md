# Dataset quality checks

The file was built from the official anonymous ENDES modules listed in `source_manifest.csv`. The analytical output contains no ENDES case, household, or person identifier.

## Build checks

- Rows in the final eligibility population: 57,539.
- Duplicate analysis identifiers: 0.
- Age range: 6 to 35 months.
- Missing primary outcome: 0.
- The figures below are unweighted checks only; publication-style prevalence estimates are produced separately with the sampling weights.

## By year

|   survey_year |   eligible_children |   unweighted_legacy_anemia_prevalence |   positive_weights |
|--------------:|--------------------:|--------------------------------------:|-------------------:|
|     2019.0000 |          10320.0000 |                                0.4246 |         10320.0000 |
|     2020.0000 |           6051.0000 |                                0.4118 |          6051.0000 |
|     2021.0000 |          10902.0000 |                                0.4227 |         10902.0000 |
|     2022.0000 |          10557.0000 |                                0.4548 |         10557.0000 |
|     2023.0000 |           9951.0000 |                                0.4557 |          9951.0000 |
|     2024.0000 |           9758.0000 |                                0.4612 |          9758.0000 |

## Comparability note

The primary series uses the legacy ENDES category `HW57` in every year, including 2024. ENDES 2024 also contains the updated fields `HW56A/HW57A`; those fields are retained only for a transparent 2024 sensitivity check. The legacy series should not be presented as the official 2024 estimate reported under the updated national directive.
