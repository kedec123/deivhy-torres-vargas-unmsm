# Method Fit Matrix

## Refined question

How did legacy-comparable anemia prevalence among Peruvian children aged 6-35 months change between 2019 and 2024, and which observed child, maternal, household, and territorial characteristics were associated with anemia in the pooled ENDES data?

## Candidate methods

| Method | What it would do |
|---|---|
| Repeated cross-sectional secondary analysis | Analyze ENDES 2019-2024 microdata to describe weighted trends and model adjusted associations. |
| Primary cross-sectional field survey | Collect new data in selected high-burden departments, gaining local detail but losing national coverage. |
| Quasi-experimental programme evaluation | Estimate the effect of an intervention such as supplementation or CRED under explicit identification assumptions. |

## E.D.F.C.V. decision matrix

Scores range from 1 (weak fit) to 5 (strong fit). They make the reasoning visible; they do not replace it.

| Criterion | Repeated cross-sectional analysis | Primary survey | Quasi-experimental evaluation |
|---|---:|---:|---:|
| **E - Epistemological fit**: supports measured population patterns | 5 | 4 | 5 |
| **D - Data availability**: access to adequate data now | 5 | 2 | 2 |
| **F - Feasibility**: manageable within the course and a doctoral protocol stage | 5 | 2 | 2 |
| **C - Contribution type**: directly answers the present national question | 5 | 3 | 3 |
| **V - Venue fit**: appropriate for public-health and nutrition audiences | 5 | 4 | 4 |
| **Total** | **25** | **15** | **16** |

The highest score is not a claim that the other two methods are weak research. It records fit to this particular question, data position, and course timeline. If the question changed from national patterns to caregiver experience or a defined intervention effect, the ranking would change as well.

## Decision

Repeated cross-sectional secondary analysis is the strongest option because the question is national, recent, and associative. ENDES offers repeated coverage, standardized child haemoglobin information, and social and territorial variables. It can support a careful account of distribution and persistence without pretending to answer a causal question it was not designed to answer.

A primary survey is attractive for local depth, but it would shift the study away from the current national question and require fieldwork, laboratory, ethics, and budget resources that are not justified at this stage. A quasi-experimental design could later evaluate a specific policy, but only if intervention exposure, timing, comparison groups, and assumptions are defined in advance. Applying that label now would overstate what the available data can identify.

## Boundary of the choice

The selected method can identify weighted patterns and adjusted associations. It cannot establish that maternal education, wealth, residence, or a programme caused an individual child's anemia status. The protocol and final reporting will keep that distinction explicit.

## Implementation implications

The selected method requires four safeguards. First, the primary trend must use one outcome definition across the series and show the 2024 transition separately. Second, descriptive estimates should use the documented ENDES weight and preserve the cluster and stratum fields for a later design-based analysis. Third, preprocessing for the exploratory classifier must be learned only in the training portion of the data. Fourth, tables and narratives must avoid language that turns territorial or socioeconomic associations into deficits of families or communities.

The technical classifier does not change the method choice. It is a bounded Session 5 artefact used to practise versioning, leakage control, experiment tracking, and subgroup inspection. The substantive method remains repeated cross-sectional secondary analysis.
