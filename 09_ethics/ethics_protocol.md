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
