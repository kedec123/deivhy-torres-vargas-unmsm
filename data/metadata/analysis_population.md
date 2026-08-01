# Analysis population

The primary analytical population is children aged 6 to 35 completed months who have a valid legacy ENDES anemia category (`HW57`) in ENDES 2019-2024. This age range matches the project question and the age group used in recent official reporting.

The build keeps one record per eligible child after joining the child haemoglobin module (`REC44`), the birth-history module (`REC21`), and the household/mother characteristics module (`REC0111`). The join keys are used only during construction and are excluded from the released analytical CSV.

Records outside the age range, without a valid legacy anemia category, or without a successful module join are excluded. Missing covariates are retained in the data contract and handled explicitly by each downstream analysis; no outcome value is imputed. The primary outcome is a legacy-comparable binary indicator derived from `HW57`. The updated 2024 definition is retained as a sensitivity field and is not mixed into the historical trend.

The dataset supports population description and exploratory prediction. It is not a clinical decision tool, and associations in the data must not be interpreted as causal effects.
