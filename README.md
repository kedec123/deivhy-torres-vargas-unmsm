# UNMSM Research Methods - Deivhy Torres

Doctoral course repository for *Research Methods and Scientific Integrity in AI and Advanced Technologies* at UNMSM.

**Author:** Deivhy Torres  
**Current research topic:** Child anemia in Peru, with emphasis on children aged 6 to 35 months and national inequalities during 2019-2024.

## What this repository covers

This repository currently documents the first five sessions of the course. It is organized as a partial but coherent project: the paradigm is defined first, the method is justified second, the first protocol outline follows from those choices, the literature review frames the gap, and the technical artifact shows how a reproducible analysis pipeline can be built.

At this stage, the repository should be read as a **sessions 1-5 submission**, not as the final full-course repository. Later units such as ethics, data management, bias auditing, peer review, and the final protocol versions are still pending.

## Current structure

- `01_paradigm/` - paradigm justification for the child anemia topic
- `02_method/` - research question refinement and method-fit matrix
- `03_protocol/` - protocol outline v0.1
- `04_literature/` - mini systematic review, PRISMA diagram, and gap analysis
- `05_pipeline/` - reproducible baseline pipeline using Git, DVC, MLflow, and Docker

## How to read the project

If you want the research logic, start with `01_paradigm/` and move in order to `04_literature/`. Each folder represents one step in the course sequence.

If you want the technical artifact, go directly to `05_pipeline/README.md`. The reproducibility stack is intentionally self-contained there, even though the final course brief also shows a wider repository layout for later sessions.

## Technical status

The pipeline is centered on a small synthetic ENDES-like dataset created only for reproducibility practice. It does **not** claim to be the final analytical dataset for the research project. The current artifact demonstrates versioning, experiment tracking, and environment documentation, while the substantive doctoral work remains focused on the protocol and literature components.

The main teaching environment for the technical artifact is now **Google Colab**, which matches the way the work was developed in class. Local execution remains documented as an alternative path, but Colab is the easiest route to show how the notebook and results were actually produced.

Docker instructions are included because they are required by the course brief. However, Docker was **not** validated locally in the present environment because Docker is not installed on this machine. That limitation is documented rather than hidden.

## What is still pending for the final course brief

- later-session folders and deliverables beyond Session 5
- a final DVC remote setup tested from a fresh external clone
- later protocol versions (`v1.0` and `v2.0`)
- ethics, data management, bias, integrity, and reflective writing materials

## Integrity note

The methodological documents in `01` to `04` are working academic drafts. They should be treated as materials to be personally reviewed, refined, and defended by the author before final course submission.
