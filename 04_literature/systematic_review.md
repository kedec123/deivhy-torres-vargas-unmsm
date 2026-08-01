# Focused Systematic Literature Review

## Review question

What does Peru-focused published research show about anemia among young children, its social and territorial distribution, implementation challenges, and the measurement choices that matter for interpreting recent ENDES trends?

## Scope and search record

This is a focused, auditable course review rather than a claim of exhaustive global coverage. The search was rerun on **31 July 2026** in PubMed and SciELO using English and Spanish terms. The full strings, dates, result counts retained for screening, and source URLs are recorded in `search_log.csv`. Every candidate in the retained set is represented in `screening_log.csv`.

The final review includes ten peer-reviewed studies. It prioritises Peru-specific work in children under five, with particular value given to children aged 6-35 months, ENDES analyses, programme evidence, and studies that clarify the current measurement debate. Earlier studies are included as historical and methodological context; they are not used as substitutes for the 2019-2024 analysis.

## Eligibility criteria

| Included | Excluded |
|---|---|
| Peru-specific child population or a clearly identifiable Peruvian subgroup. | Adult-only, pregnancy-only, or non-Peru studies. |
| Anemia is a main outcome, exposure, measurement issue, or implementation focus. | Anemia is mentioned only incidentally. |
| Peer-reviewed article in English or Spanish with a persistent link. | Editorials, protocols, or items without usable study information. |
| Prevalence, determinants, measurement, prevention, or implementation evidence. | Samples unable to inform the project question after full-text review. |

## PRISMA flow

The flow is calculated directly from `screening_log.csv`, not estimated after the fact.

| Stage | Records |
|---|---:|
| Identified in PubMed | 10 |
| Identified in SciELO | 2 |
| Duplicates removed | 0 |
| Title/abstract records screened | 12 |
| Full texts assessed | 12 |
| Full texts excluded | 2 |
| **Studies included** | **10** |

The matching visual flow is [`prisma_diagram.svg`](prisma_diagram.svg) and [`prisma_diagram.png`](prisma_diagram.png). The two full-text exclusions are documented individually: one study focused on infants aged 2-5 months, and one pooled children under five without a directly usable young-child stratum.

## What the evidence says

The studies converge on three useful points. First, anemia among young children in Peru is patterned rather than randomly distributed. National and local studies repeatedly report differences by age, poverty-related conditions, maternal characteristics, residence, altitude, and territory. Second, interventions such as micronutrient powders and child-care services cannot be judged by coverage alone. Uptake, caregiver experience, infection, water conditions, and local delivery shape whether an intervention is likely to help.

Third, the definition of anemia matters. Studies on altitude and the 2024 WHO update show that a change in cut-off or adjustment method can change a prevalence estimate substantially. This is not a minor technical detail: it affects how trend claims and policy targets should be interpreted.

The review does not support a simple statement that one factor "causes" anemia or that one policy has failed nationwide. Most included evidence is observational, setting-specific, or based on secondary data. Its strongest use in this project is to motivate a careful contemporary descriptive analysis and to set interpretation boundaries.

## Connection to the present study

The contribution of this project is deliberately modest and specific. It creates a documented 2019-2024 ENDES file for children aged 6-35 months, retains a legacy-comparable outcome across years, reports weighted descriptive patterns, and treats the 2024 update as a sensitivity issue. The project will not claim to estimate the causal effect of supplementation or of any social characteristic. The detailed study-by-study evidence is in `included_studies.md`; full citation records are in `references.bib`.

## Audit trail and limitations

The review can be audited because the search, screening, study table, bibliography, and PRISMA diagram are separate files rather than a retrospective narrative. `search_log.csv` records the exact source, date, query, and retained count. `screening_log.csv` records a decision for each retained record, including the two full-text exclusions. The PRISMA counts are calculated from that log.

This is still a course-scale review. It did not search every global database, perform a duplicate independent screening exercise, or conduct a formal risk-of-bias assessment for each design. Its purpose is to show a transparent route from a bounded search to a defensible protocol question. A thesis-level systematic review would need a registered protocol, broader retrieval, independent screening, and a pre-specified appraisal method.

## Implication for the protocol

The literature supports a question about current distribution, trends, and observed associations. It does not justify a claim that ENDES alone can evaluate supplementation effectiveness, identify individual clinical risk, or settle whether a national measurement change represents a biological change. Those boundaries are carried into `03_protocol/protocol_v1.0.md`, the model card, and the ethics documents.
