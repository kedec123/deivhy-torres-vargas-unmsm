# Fairness Audit: Adult Census Benchmark

This audit uses Fairlearn's Adult Census dataset, not ENDES. It is included to meet the course requirement for a reproducible fairness exercise on a standard benchmark. The sensitive feature is recorded sex. The model deliberately excludes sex from training, then evaluates group differences by sex. The favourable label for this exercise is income above 50K; this convention is specific to the benchmark and does not describe a health outcome.

## Labels before modelling

The first table checks whether the benchmark label already differs by the sensitive feature. Disparate impact is the smaller group selection rate divided by the larger one. A value closer to 1 indicates similar selection rates; it does not establish that the data-generating process is fair.

|   demographic_parity_difference |   disparate_impact |
|--------------------------------:|-------------------:|
|                          0.1945 |             0.3597 |

| sex    |   sample_size |   observed_favourable_rate |
|:-------|--------------:|---------------------------:|
| Female |         16192 |                     0.1093 |
| Male   |         32650 |                     0.3038 |

## Procedure

A logistic-regression baseline was evaluated on five stratified train-test splits. A Fairlearn `ThresholdOptimizer` with an equalized-odds constraint was then fitted on each training split. The audit reports accuracy, demographic-parity difference, disparate impact, and equalized-odds difference. Lower differences are closer to parity for the difference measures; disparate impact is read against 1. No single metric proves fairness.

## Results across fixed splits

| approach                 |   accuracy_mean |   demographic_parity_difference_mean |   disparate_impact_mean |   equalized_odds_difference_mean |   equalized_odds_difference_min |   equalized_odds_difference_max |
|:-------------------------|----------------:|-------------------------------------:|------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|
| baseline                 |          0.8082 |                               0.3012 |                  0.3389 |                           0.2000 |                          0.1948 |                          0.2058 |
| equalized_odds_threshold |          0.8328 |                               0.0821 |                  0.5847 |                           0.0257 |                          0.0022 |                          0.0739 |

## Group metrics across fixed splits

| approach                 | sex    |   selection_rate_mean |   true_positive_rate_mean |   false_positive_rate_mean |   accuracy_mean |
|:-------------------------|:-------|----------------------:|--------------------------:|---------------------------:|----------------:|
| baseline                 | Female |                0.1544 |                    0.7590 |                     0.0802 |          0.9022 |
| baseline                 | Male   |                0.4556 |                    0.8574 |                     0.2802 |          0.7616 |
| equalized_odds_threshold | Female |                0.1155 |                    0.5278 |                     0.0650 |          0.8904 |
| equalized_odds_threshold | Male   |                0.1976 |                    0.5029 |                     0.0643 |          0.8042 |

The range of equalized-odds difference across seeds is reported to avoid relying on one convenient split. Mitigation can reduce one disparity measure while changing accuracy or other error patterns; the trade-off is part of the result, not a defect to hide.

## Interpretation and limits

The benchmark begins with a visible difference in favourable-label rates by recorded sex. In the five internal splits, the equalized-odds post-processing step reduced the reported demographic-parity and equalized-odds differences and moved disparate impact closer to 1. This is an empirical result for this benchmark and these splits, not a declaration that the resulting system is fair in every relevant sense.

The mitigation changes decision thresholds after fitting the baseline model. It does not change the historical processes that produced the Adult Census labels, prove that sex is the only relevant protected attribute, or resolve potential differences by intersecting characteristics. Fairness criteria can conflict, and the preferred trade-off depends on the real decision context. The course exercise therefore documents the choice and its consequences instead of presenting mitigation as a universal fix.

## Files

- `bias_audit_splits.csv`: all split-level metrics.
- `before_after_chart.png`: average baseline-versus-mitigated comparison.
