# Research Protocol Draft (v1.0)

## Draft status

This is the first complete course draft, built from the preceding paradigm, method, literature, and data-contract records. It is not the submission-ready v2.0. Before using it as a final academic protocol, the author must personally verify the wording, references, methodological decisions, and any statement of planned analysis. The later v2.0 must show how genuine peer feedback changed the document.

## Title

**Child anemia in Peru, 2019-2024: weighted trends and associated inequalities among children aged 6-35 months.**

## Abstract

Child anemia remains a public-health concern in Peru, but recent comparisons require care because the measurement framework changed in 2024. This study proposes a quantitative repeated cross-sectional secondary analysis of anonymous public-use ENDES microdata from 2019 to 2024. It will estimate weighted legacy-comparable anemia prevalence among children aged 6-35 months, describe its distribution by selected child, maternal, household, and territorial characteristics, and estimate adjusted associations in pooled data. The primary outcome will use the legacy ENDES category (`HW57`) in every year. The newer 2024 fields will be retained for a separate sensitivity discussion rather than combined with the historical series. The protocol also includes a reproducible technical artefact: transparent data construction, DVC data versioning, MLflow experiment tracking, and a small exploratory classifier. That model is a teaching artefact, not a clinical tool. The study will report population patterns and uncertainty boundaries without claiming that observed characteristics or programmes cause a child's anemia status.

## 1. Background and problem

Anemia in early childhood has been repeatedly associated in Peru with age, household conditions, maternal characteristics, territory, and access to relevant services. The national burden is therefore not adequately described by one average alone. The course review in `04_literature/` also shows that prevention and service-delivery questions cannot be answered only by asking whether an intervention exists; implementation conditions and caregiver experience matter.

The immediate methodological problem is comparability. ENDES 2024 contains fields linked to the updated anemia guidance. A prevalence series that switches definitions without disclosure can confuse a classification change with a change in child health. The proposed analysis addresses this directly by retaining a legacy-comparable primary series and documenting the 2024 fields separately.

## 2. Rationale and contribution

The study does not promise a new causal determinant or a clinical prediction system. Its contribution is a documented and inspectable recent ENDES workflow for a clearly defined child population. The repository records source archives, checksums, variable definitions, population rules, reproducible scripts, and the distinction between descriptive analysis and exploratory modelling.

This focus has practical value because a reader can examine how the analytic population was constructed, how the outcome was defined, and where the interpretation stops. It also creates a baseline for a later doctoral stage that might add qualitative work, a programme evaluation, or a design better suited to causal identification.

## 3. Literature foundation

The focused systematic review includes ten peer-reviewed studies and keeps a search log, screening log, PRISMA flow, bibliography, and study table in `04_literature/`. National ENDES analyses provide evidence that anemia is socially and territorially patterned. Work on altitude and the 2024 measurement update makes the definition of the outcome central to trend interpretation. Qualitative and implementation studies show why coverage indicators alone cannot establish whether a prevention strategy is acceptable or effective in practice.

The review supports a careful descriptive and associative question. It does not support treating cross-sectional ENDES data as evidence of programme impact. The gap analysis therefore identifies a reproducibility and interpretation gap: recent, clearly documented trend evidence for the specified age group can be improved without overstating causal contribution.

## 4. Research question, objectives, and working expectation

**General question.** How did legacy-comparable anemia prevalence among Peruvian children aged 6-35 months change between 2019 and 2024, and which observed child, maternal, household, and territorial characteristics were associated with anemia in pooled ENDES data?

**General objective.** Describe weighted legacy-comparable anemia trends and observed inequalities among eligible children using ENDES 2019-2024.

**Specific objectives.**

1. Estimate weighted annual prevalence in the eligible population using the legacy ENDES category.
2. Describe differences by child sex, maternal education, wealth quintile, urban-rural residence, and department.
3. Estimate adjusted associations in a pooled repeated cross-sectional model that includes survey year.
4. Document the 2024 measurement transition without treating two outcome definitions as interchangeable.
5. Demonstrate a reproducible exploratory classification workflow without presenting it as clinical decision support.

**Working expectation.** The analysis expects anemia prevalence and modelled associations to differ across observed social and territorial characteristics. This is not a causal hypothesis about why those differences occur; it is an expectation that will be checked against the data and reported with uncertainty.

## 5. Paradigm and conceptual boundary

The project uses a quantitative empirical paradigm. Its claims concern measurable prevalence, subgroup distributions, time patterns, and statistical associations. The study is not mixed methods because it does not yet define a procedure for integrating qualitative evidence with the quantitative analysis. It is also not a quasi-experiment because no intervention exposure, comparison group, or causal identification strategy has been specified.

The conceptual frame distinguishes observed indicators from the processes they may represent. Maternal education, wealth, residence, and department are measured characteristics available in ENDES. They can indicate unequal social and service contexts, but they cannot by themselves reveal every pathway that produces anemia. This distinction prevents the analysis from assigning responsibility to an individual family or community.

## 6. Design, source, and population

The study uses a repeated cross-sectional secondary design with anonymous public-use ENDES microdata. For every year from 2019 through 2024, the workflow reads the child haemoglobin module (`REC44`), birth-history module (`REC21`), and household/mother module (`REC0111`). The original archives are read without modification and joined temporarily using ENDES keys; DVC versions the resulting de-identified analytical CSV.

The primary population is children aged 6-35 completed months with a valid legacy anemia category (`HW57`). The analytical CSV contains one project-generated `analysis_id` per eligible child. ENDES case, household, and person keys are used only during the build and are excluded from the released analytical file. The detailed inclusion, exclusion, and missing-data rules are in `05_pipeline/docs/analysis_population.md`.

## 7. Variables and measurement

The primary outcome is `anemia_legacy`, coded one for legacy category levels 1-3 and zero for level 4. The primary trend uses this definition in all six years. `HW56A` and `HW57A` are retained only for a 2024 sensitivity discussion; they do not replace the primary historical outcome.

The planned explanatory variables are child age in months, child sex code, maternal education code, wealth quintile, urban-rural residence, department, and survey year. The normalized individual sampling weight (`V005/1,000,000`), cluster, and stratum are retained to support design-aware reporting. The data dictionary in `05_pipeline/docs/data_dictionary.csv` provides the source field, coding, availability, and intended role for every released variable.

## 8. Analysis plan

The first stage will verify the data contract: expected years, age range, non-duplicated analysis IDs, non-missing primary outcome, and positive weights. The second stage will produce weighted annual and residence summaries. Annual prevalence will use Taylor-linearized design-based standard errors and confidence intervals with ENDES strata and primary sampling units; a stratified-cluster bootstrap will be retained as a comparison. The descriptive script does not duplicate those inferential calculations.

The third stage will estimate adjusted associations in pooled repeated cross-sectional data, including survey year. Effect estimates, uncertainty, missing-data decisions, and model diagnostics must be documented before any final conclusion is written. The analysis will describe association, not effect, and will report whether a result is sensitive to the 2024 measurement boundary.

The technical artefact runs Logistic Regression, Random Forest, and Extra Trees across five prespecified stratified 80/20 splits, with preprocessing fitted only on training data. Metrics and their variability are reported as internal exploratory results. The model will not be used for diagnosis, screening, treatment, triage, benefit eligibility, or ranking of children, households, departments, or communities.

## 9. Reproducibility and data governance

Git records code and document history. DVC records the analytical-data state, while local MLflow records experiment parameters, metrics, data hash, and Git commit when a reader runs the exploratory workflow. The repository provides a Colab notebook, pinned dependencies, a Dockerfile, and a documented local reproduction route. The source manifest records the official retrieval URL, date, archive name, checksum, module, and transformation for every input.

No credential is stored in Git. A clean clone can use `data/download_endes.py` to retrieve and verify the public official ENDES archives before rebuilding the analytical CSV. The DVC pointer remains a checksum record; any private cache is optional and local.

## 10. Ethics, risks, and dissemination

The project uses anonymous secondary data and does not recruit, contact, or intervene with participants. Its ethical risks are not zero: re-identification attempts, territorial stigma, careless causal language, and misuse of a model score could still cause harm. The data-management plan, model card, and ethics protocol set out safeguards, including minimum necessary variables, no external record linkage, no clinical use, local credential storage, and contextual reporting.

Results will be disseminated as a course artefact and, only after author review and applicable institutional checks, as a transparent methodological baseline. Any new data linkage, identifiable data, public release beyond the agreed access terms, or deployment proposal will pause the work until a fresh governance assessment is completed.

## 11. Feasibility and timeline

| Months | Planned activities | Evidence of completion |
|---|---|---|
| 1-2 | Confirm question, search record, data contract, and comparability decision. | Updated protocol, review logs, and source manifest. |
| 3-4 | Build and validate the CSV; complete descriptive and design-aware analyses. | Reproducible pipeline, quality checks, and analysis outputs. |
| 5-6 | Estimate associations, run sensitivity and subgroup checks, and draft results. | Versioned analysis code and documented modelling decisions. |
| 7-8 | Obtain genuine peer feedback, revise the protocol, and complete course materials. | Completed review forms, response table, reflective log, and v2.0. |

The schedule is feasible for a protocol stage because it uses existing public-use data and a bounded number of variables. It remains conditional on the author completing the required survey-analysis work and the remote-access verification rather than treating the present course pipeline as a finished thesis analysis.

## 12. Limitations

The design is observational and repeated cross-sectional. It cannot estimate the causal effect of maternal education, poverty, residence, or an intervention on individual anemia status. The available variables do not capture all nutritional, infectious, clinical, service, or environmental pathways. The 2024 measurement transition requires explicit sensitivity work, and the exploratory model has neither clinical validation nor external validation.

These are not reasons to abandon the study. They define the claim the study can responsibly make: a transparent account of recent patterns and observed associations in a specific ENDES child population.

## Repository-linked sources

- ENDES source and variable records: `05_pipeline/docs/source_manifest.csv` and `05_pipeline/docs/data_dictionary.csv`.
- Literature search and references: `04_literature/systematic_review.md`.
- Reproducibility, ethics, management, model, bias, and integrity records: `05_pipeline/` through `12_integrity/`.
