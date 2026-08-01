# Retraction Analysis: Roxadustat Pooled Analysis

## Record examined

Provenzano et al., **"Pooled Analysis of Roxadustat for Anemia in Patients With Kidney Failure Incident to Dialysis,"** *Kidney International Reports*, 6(3), 613-623, DOI [10.1016/j.ekir.2020.12.018](https://doi.org/10.1016/j.ekir.2020.12.018). The publisher's article page labels the paper as retracted and links the formal [retraction notice](https://doi.org/10.1016/j.ekir.2022.01.1069).

## What is directly supported by the notice

The publisher states that there were significant concerns about the analysis, including deviations from the proposed analytic plan identified after publication. It also states that the authors did not address the concerns to the editors' satisfaction and that there was no consensus among authors about the nature or extent of corrections. Those are the reasons given for the retraction.

## What can reasonably be inferred

The retraction means the original pooled analysis should not be relied upon as a stable source for clinical or policy claims. It illustrates why analysis plans, versioned code, documented changes, and a clear correction process matter in health research.

## What remains unknown from the notice

The notice does not establish that every underlying trial result was invalid, identify individual responsibility, or allow this project to diagnose intent. It would be improper to make those claims without a separate authoritative investigation record.

## Lesson for this repository

This project keeps the data-build logic, parameters, DVC state, experiment records, and protocol versions visible. If an analysis decision changes, the change should be documented in Git and the resulting outputs regenerated. Transparent records do not prevent mistakes, but they make them easier to inspect and correct.

## Evidence boundary

| Statement | Status in this analysis | Basis |
|---|---|---|
| The pooled analysis is retracted. | Directly supported. | Publisher article page and linked formal retraction notice. |
| The notice identifies concerns about analysis-plan deviations and unresolved author-editor issues. | Directly supported. | Notice as summarised in the record above. |
| The original paper should not be used as a stable source for clinical or policy conclusions. | Reasonable research-use inference. | Retraction status and stated concerns. |
| Every underlying trial result is invalid or a particular person acted improperly. | Not established. | The notice does not provide sufficient evidence for those claims. |

This distinction matters. A retraction is serious, but responsible integrity analysis does not turn a notice into an unsupported story about intent, blame, or every component of a wider evidence base.

## Repository response rule

If a cited study, data source, or reported result used in this repository is corrected, withdrawn, or found to be erroneous, the author will create a dated issue or commit that identifies the affected artefact, revises the interpretation, regenerates any dependent output, and preserves the prior version in Git history. The aim is traceable correction rather than silent replacement.

## How the record was assessed

The analysis began with the publisher's retraction record, not with a social-media summary or an assumption based on the study topic. The article and notice were read for statements the publisher explicitly made, then separated from the broader conclusions that a responsible reader may draw about use of the article. The verification route and date are preserved below.

This method is intentionally narrow. It does not attempt to investigate the authors, reconstruct the disputed analysis, or reanalyse the underlying trials. Those activities would require evidence and authority that this repository does not have. The value of the exercise is learning to stop at the boundary of the available record while still acting appropriately on a retraction.

## Practical questions for future citations

Before relying on a health-research paper, the author should check whether the article has a correction, expression of concern, or retraction; inspect whether the claim being cited is still supported by the current record; and revise any dependent text if its evidentiary status changes. This is especially important when a study informs a protocol decision, a metric choice, or a clinical-policy statement.

## Source record

| Record | Verification source | Checked | Use in this repository |
|---|---|---|---|
| ENDES microdata access and modules | [INEI microdata catalogue](https://www.inei.gob.pe/media/difusion/apps/files/basic-html/page3.html) and the direct module URLs in `05_pipeline/docs/source_manifest.csv` | 2026-07-31 | Data construction. |
| ENDES 2024 measurement context | [ENDES 2024 portal](https://proyectos.inei.gob.pe/endes/2024/departamentales/map/principal.html) | 2026-07-31 | Comparability boundary. |
| Literature records | Persistent PubMed and SciELO links in `04_literature/systematic_review.md` | 2026-07-31 | Review and protocol context. |
| Reproducibility audit paper | [PubMed Central full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13305737/) | 2026-07-31 | Session 6 audit. |
| Retraction record | [Publisher retraction page](https://www.sciencedirect.com/science/article/pii/S2468024920318519) | 2026-07-31 | Session 12 analysis. |
| Peruvian data-protection framework | [Law No. 29733](https://www.gob.pe/institucion/anpd/normas-legales/358664-29733) | 2026-07-31 | Data-management and ethics context. |
