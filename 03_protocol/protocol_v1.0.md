# Research Protocol (v1.0)

## Title

**Child anemia in Peru, 2019-2024: weighted trends and associated inequalities among children aged 6-35 months.**

## Background and problem

Anemia in early childhood remains a persistent concern in Peru. Earlier national work has found differences by child age, household resources, maternal characteristics, residence, and territory. At the same time, the 2024 change in anemia guidance complicates a simple reading of recent trends: a change in the classification rule can alter a prevalence estimate without representing the same amount of change in child health.

This study addresses a practical gap. It will create a documented, de-identified analytical file from the official ENDES modules for 2019-2024 and use a legacy-comparable outcome for the primary trend. The 2024 updated field will be described separately as a sensitivity issue. This makes the study narrower than a causal programme evaluation, but more transparent about what the data can support.

## Research question and objectives

**Question.** How did legacy-comparable anemia prevalence among Peruvian children aged 6-35 months change between 2019 and 2024, and which observed child, maternal, household, and territorial characteristics were associated with anemia in pooled ENDES data?

**Objectives.**

1. Estimate weighted annual prevalence in the eligible population using the legacy ENDES category.
2. Describe differences by child sex, maternal education, wealth quintile, urban-rural residence, and department.
3. Estimate adjusted associations in a pooled repeated cross-sectional model, including survey year.
4. Document the 2024 measurement transition without combining incompatible outcome definitions.

## Design, source, and population

The study uses a quantitative repeated cross-sectional design and anonymous public-use ENDES microdata. It joins the child haemoglobin module (`REC44`), birth-history module (`REC21`), and household/mother module (`REC0111`) for 2019-2024. The primary population includes children aged 6-35 completed months with a valid legacy ENDES anemia category (`HW57`). Records outside this range or without a valid primary outcome are excluded. The build process removes ENDES case and household identifiers from the released analytical CSV.

## Variables and measurement

The primary outcome is `anemia_legacy`, coded one for legacy ENDES categories 1-3 and zero for category 4. The explanatory set includes age in months, child sex, maternal education, wealth quintile, residence, department, and survey year. The normalized weight `V005/1,000,000`, cluster, and stratum are retained for design-aware analysis and documentation. The file also retains `HW57A` and `HW56A` for 2024 sensitivity work; they do not replace the primary historical outcome.

## Analysis plan

First, the study will report sample counts and weighted annual prevalence. Second, it will present subgroup summaries and inspect missingness and measurement comparability. Third, it will estimate adjusted associations appropriate for repeated cross-sectional survey data, reporting effect estimates with uncertainty and avoiding causal language. The reproducibility exercise uses logistic regression and random forest with fixed seeds, train-only preprocessing, and subgroup checks; these models are explicitly exploratory and are not clinical tools.

The current pipeline uses normalized weights for descriptive summaries but does not yet calculate design-based standard errors or confidence intervals. Any final inferential analysis will use an appropriate survey-design implementation before being presented as population inference.

## Ethics, data governance, and dissemination

The project uses anonymous secondary data and does not contact participants. Its main risks are inappropriate re-identification, territorial stigma, and overinterpretation. Only the de-identified analytical CSV is used downstream; original archives remain in controlled DVC storage. Results will be reported as population patterns with contextual caveats, not as judgements about communities or individual families. Detailed safeguards are in `09_ethics/` and `10_data_mgmt/`.

## Timeline

| Months | Activities |
|---|---|
| 1-2 | Finalise question, literature records, data contract, and comparability decision. |
| 3-4 | Build and validate data; complete descriptive and design-aware analyses. |
| 5-6 | Fit association models, conduct sensitivity and subgroup checks, and draft results. |
| 7-8 | Obtain genuine peer feedback, revise the protocol, and prepare the final course materials. |

## Limitations

The design is observational and repeated cross-sectional. It cannot establish causal effects of social characteristics or interventions. Variables are limited to what ENDES measures, and the measurement transition in 2024 requires continuing scrutiny. These limitations are part of the study's interpretation, not an afterthought.
