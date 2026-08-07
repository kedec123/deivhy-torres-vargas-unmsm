# Design-based uncertainty and adjusted associations

Annual prevalence uses ENDES final weights, strata and primary sampling units. Taylor linearization is the primary design-based variance estimator. A stratified-cluster bootstrap with 300 replicates is retained as an independent sensitivity check. Both methods estimate the same legacy-comparable weighted prevalence; their intervals are compared in `analysis_ci_method_comparison.csv`.

## Annual weighted prevalence: Taylor linearization

|   survey_year |   sample_size |   weighted_anemia_prevalence |   taylor_standard_error |   taylor_ci_95_lower |   taylor_ci_95_upper |   design_degrees_of_freedom |   design_strata |   design_psus | ci_method            |
|--------------:|--------------:|-----------------------------:|------------------------:|---------------------:|---------------------:|----------------------------:|----------------:|--------------:|:---------------------|
|          2019 |         10320 |                       0.3983 |                  0.0062 |               0.3861 |               0.4105 |                        2865 |             245 |          3113 | Taylor linearization |
|          2020 |          6051 |                       0.3825 |                  0.0091 |               0.3646 |               0.4004 |                        1811 |             229 |          2056 | Taylor linearization |
|          2021 |         10902 |                       0.3844 |                  0.0059 |               0.3728 |               0.3960 |                        2896 |             221 |          3134 | Taylor linearization |
|          2022 |         10557 |                       0.4199 |                  0.0062 |               0.4078 |               0.4321 |                        2897 |             219 |          3137 | Taylor linearization |
|          2023 |          9951 |                       0.4278 |                  0.0066 |               0.4149 |               0.4408 |                        2861 |             220 |          3099 | Taylor linearization |
|          2024 |          9758 |                       0.4351 |                  0.0064 |               0.4225 |               0.4476 |                        2833 |             222 |          3073 | Taylor linearization |

## Bootstrap comparison

|   survey_year |   taylor_ci_95_lower |   taylor_ci_95_upper |   bootstrap_ci_95_lower |   bootstrap_ci_95_upper |
|--------------:|---------------------:|---------------------:|------------------------:|------------------------:|
|     2019.0000 |               0.3861 |               0.4105 |                  0.3849 |                  0.4094 |
|     2020.0000 |               0.3646 |               0.4004 |                  0.3654 |                  0.4006 |
|     2021.0000 |               0.3728 |               0.3960 |                  0.3739 |                  0.3956 |
|     2022.0000 |               0.4078 |               0.4321 |                  0.4094 |                  0.4310 |
|     2023.0000 |               0.4149 |               0.4408 |                  0.4147 |                  0.4406 |
|     2024.0000 |               0.4225 |               0.4476 |                  0.4232 |                  0.4455 |

## Modelled year effects

|   reference_year |   survey_year |   odds_ratio |   ci_95_lower |   ci_95_upper |   p_value |
|-----------------:|--------------:|-------------:|--------------:|--------------:|----------:|
|        2019.0000 |     2020.0000 |       1.0398 |        0.9750 |        1.1090 |    0.2341 |
|        2019.0000 |     2021.0000 |       0.9056 |        0.8538 |        0.9605 |    0.0010 |
|        2019.0000 |     2022.0000 |       1.0562 |        0.9957 |        1.1203 |    0.0693 |
|        2019.0000 |     2023.0000 |       1.1239 |        1.0581 |        1.1937 |    0.0001 |
|        2019.0000 |     2024.0000 |       1.1617 |        1.0923 |        1.2355 |    0.0000 |

## Interpretation boundary

Taylor intervals provide design-based uncertainty for the annual prevalence estimates under a stratified first-stage PSU variance approximation. The adjusted logistic model uses relative survey weights but its confidence intervals and p-values are model-based; they describe adjusted associations only, not a full design-based regression variance and never causal effects. The primary trend uses legacy `HW57` in every year. The separate 2024 `HW57A` sensitivity analysis is not mixed into the trend.
