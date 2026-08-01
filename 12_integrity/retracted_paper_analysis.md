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
