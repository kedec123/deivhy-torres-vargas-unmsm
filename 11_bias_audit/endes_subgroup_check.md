# ENDES Exploratory Subgroup Check

This is separate from the Adult Census fairness benchmark. It describes one saved logistic-regression holdout split from the ENDES pipeline (seed 42) by child sex and urban-rural residence. It is a diagnostic table, not a fairness certification and not a basis for acting on individual predictions.

| grouping       |   group |     n |   observed_anemia_rate |   mean_predicted_probability |   accuracy_at_0_5 |   true_positive_rate_at_0_5 |
|:---------------|--------:|------:|-----------------------:|-----------------------------:|------------------:|----------------------------:|
| child_sex_code |       1 |  7295 |                 0.4614 |                       0.5174 |            0.6506 |                      0.6999 |
| child_sex_code |       2 |  7090 |                 0.4181 |                       0.4619 |            0.6588 |                      0.5877 |
| residence_code |       1 | 10038 |                 0.4056 |                       0.4554 |            0.6634 |                      0.5807 |
| residence_code |       2 |  4347 |                 0.5197 |                       0.5700 |            0.6345 |                      0.7676 |

Observed rates, average scores, accuracy, and true-positive rate can differ across groups for many reasons, including prevalence, sampling, measurement, missing variables, and the selected threshold. Any difference should prompt data and context review; it does not identify a cause or a policy response by itself.
