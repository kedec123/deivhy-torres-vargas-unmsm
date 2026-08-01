# Ethics Protocol

## Ethical frame

This project follows the Belmont principles of respect for persons, beneficence, and justice. It uses anonymous secondary ENDES data, so it does not recruit, contact, or intervene with participants. Low direct risk does not mean no ethical responsibility: analysis and communication can still produce harm through re-identification, stigma, or careless interpretation.

## Respect for persons and privacy

The pipeline uses only the minimum fields needed for the stated analysis. ENDES case and household keys are used during the temporary join and removed from the processed CSV. Raw archives and generated files are stored through DVC in an access-controlled remote. The project will not attempt linkage to identifiable external data, publish small-cell tables that could increase disclosure risk, or share credentials.

## Beneficence and non-maleficence

The expected benefit is a more transparent description of population patterns. Key risks are presenting associations as causes, treating a model score as a diagnosis, and stigmatising rural or high-burden territories. Reports will use contextual language, disclose measurement limits, and avoid ranking communities. The model card explicitly prohibits clinical or administrative use.

## Justice

Survey groups such as rural residents, poorer households, and departments are not deficits to be corrected by an algorithm. They represent social and service contexts that deserve careful interpretation. Subgroup analyses are included to reveal uneven performance or burdens, not to justify differential treatment.

## Governance and escalation

Before any dissemination beyond the course, the author will check whether institutional review is required for the planned use of public anonymous ENDES data. If new data linkage, identifiable information, or a deployment proposal is introduced, work stops until a new ethics review and data-governance assessment are completed.

## Scope and ethical decision

This is an ethics protocol for a course-stage secondary analysis. It is not an institutional ethics approval, a waiver, or a substitute for the rules that apply to a later thesis or publication. The data source is anonymous public-use ENDES material, and the project does not recruit participants, access clinical records, or return predictions to anyone. The low direct-contact risk narrows the protocol; it does not remove the duty to manage data and interpretation responsibly.

## Risk and safeguard matrix

| Risk | Why it matters | Safeguard | Escalation trigger |
|---|---|---|---|
| Re-identification | Joined survey fields can become more revealing when combined with external data. | Remove ENDES identifiers, do not link external person-level files, and keep DVC access restricted. | Any proposal to add a direct identifier or external linkage. |
| Territorial stigma | Averages by department or residence can be read as a judgement about people. | Use contextual language, avoid rankings of communities, and report limitations beside subgroup tables. | A request to publish granular or comparative labels. |
| Misuse of a score | An exploratory classifier could be mistaken for a clinical tool. | Model card prohibits diagnosis, triage, eligibility, and individual ranking. | Any request to deploy, screen, or automate a decision. |
| Measurement misinterpretation | The 2024 definition change can be mistaken for a health change. | Keep one legacy primary series and report the updated field as a separate sensitivity issue. | A request to combine definitions in one trend without justification. |
| Credential exposure | Data access can be expanded accidentally through a shared token. | Store credentials only in ignored local DVC configuration and rotate access if exposed. | A credential appears in Git, notebook output, or a shared drive. |

## Belmont principles in practice

**Respect for persons** means using no more data than the stated question requires and not treating anonymous data as permission for unlimited reuse. **Beneficence** means reducing foreseeable harm from inference, publication, and model misuse, not only avoiding direct physical harm. **Justice** means that observed inequality is not a reason to exclude or penalise a group; it is a reason to ask what contextual conditions the available survey cannot fully show.

## Accountability and review points

The repository owner is responsible for checking source conditions, approving collaborator access, and documenting a material change in Git. Any collaborator who finds a data-quality, privacy, or interpretive concern should record it before results are redistributed. Before a thesis extension, public release, or submission to a journal, the author should check relevant UNMSM, CONCYTEC, and source-data requirements with the appropriate institutional office rather than assuming that this course protocol settles them.

## Data and participant boundary

The analysis begins after ENDES collection. It does not alter the original survey, seek new consent, or make contact with a respondent. The project will not claim to speak for survey participants, infer a family's behaviour from a coded variable, or contact a community because of an observed estimate. The author is responsible for respecting the conditions attached to the public-use data and for seeking institutional guidance if the use extends beyond this bounded course purpose.

The analytical CSV is designed to be less identifying than the source modules, not to create a new open dataset. It removes join keys and excludes direct identifiers, but it still contains combinations of demographic, territorial, and survey variables. Sharing decisions must therefore consider disclosure risk, not merely the absence of names.

## Ethical analysis checkpoints

| Question before an action | Required response |
|---|---|
| Does the action add a direct identifier, coordinate, free text, or external individual-level linkage? | Stop and obtain a new governance assessment before proceeding. |
| Does a planned chart or table show a small or potentially identifiable subgroup? | Aggregate, suppress, or do not publish until a disclosure review is documented. |
| Does a result describe an association as a cause, a fault, or a ranking of people? | Rewrite the claim, state the design limit, and provide social context. |
| Does a collaborator need the raw archive or a credential? | Grant the minimum necessary access and record the reason and duration. |
| Does a proposed use involve diagnosis, triage, programme eligibility, or automated action? | Do not use this course model; require a separate clinical, legal, and ethical process. |

## Justice in communication

Justice applies to language as well as sampling. A higher observed prevalence in a department, rural area, or wealth category should be described as a population pattern within structural and service contexts. It should not be used to portray an area as inherently deficient or to decide that an individual deserves less attention. The repository will pair subgroup findings with the measurement and design limits that constrain interpretation.

The protocol also recognises an evidence gap: a national survey cannot replace local knowledge, caregiving experience, or community participation. If the work later proposes an intervention or a locally targeted system, affected stakeholders must shape that next stage rather than being represented only as rows in a dataset.
