# Fairness Audit: Adult Census Benchmark

This audit uses Fairlearn's Adult Census dataset, not ENDES. It is included to meet the course requirement for a reproducible fairness exercise on a standard benchmark. The sensitive feature is recorded sex. The model deliberately excludes sex from training, then evaluates group differences by sex.

## Procedure

A logistic-regression baseline was evaluated on five stratified train-test splits. A Fairlearn `ThresholdOptimizer` with an equalized-odds constraint was then fitted on each training split. The audit reports accuracy, demographic-parity difference, and equalized-odds difference. Lower differences are closer to parity for the selected metric, but no single metric proves fairness.

## Results across fixed splits

| approach                 |   accuracy_mean |   demographic_parity_difference_mean |   equalized_odds_difference_mean |   equalized_odds_difference_min |   equalized_odds_difference_max |
|:-------------------------|----------------:|-------------------------------------:|---------------------------------:|--------------------------------:|--------------------------------:|
| baseline                 |          0.8082 |                               0.3012 |                           0.2000 |                          0.1948 |                          0.2058 |
| equalized_odds_threshold |          0.8328 |                               0.0821 |                           0.0257 |                          0.0022 |                          0.0739 |

The range of equalized-odds difference across seeds is reported to avoid relying on one convenient split. Mitigation can reduce one disparity measure while changing accuracy or other error patterns; the trade-off is part of the result, not a defect to hide.

## Files

- `bias_audit_splits.csv`: all split-level metrics.
- `bias_audit_by_group.csv`: group metrics for every split and approach.
- `before_after_chart.png`: average baseline-versus-mitigated comparison.
- `endes_subgroup_check.md`: a separate descriptive check for the project model, with no claim that Adult Census results transfer to Peru.
