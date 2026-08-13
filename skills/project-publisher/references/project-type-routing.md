# Project type routing

Choose one primary type based on how a user receives value. Add an auxiliary type only when it changes required material or verification.

| Type | Strong evidence | Required public proof | Common overreach |
| --- | --- | --- | --- |
| Software or CLI | source, package manifest, executable entrypoint | install, run, requirements, tests, demo, security boundary | adding deployment claims without a live check |
| Agent Skill | `SKILL.md`, bundled references or scripts | trigger examples, install path, compatibility, behavior Eval, permissions | calling prompt text an autonomous product |
| Dataset | structured data files, schemas, collection scripts | data card, fields, sample, source, license, bias and limitations | publishing data without rights or provenance |
| Course or documentation | lessons, chapters, guides, navigation | target learner, prerequisites, outcomes, index, maintenance | promising mastery without assessment evidence |
| Research | question, method, experiment, analysis | method, environment, data, reproduction, limitations | presenting exploratory results as established fact |
| Design resource | editable assets, templates, components | preview, formats, tool versions, usage, license | showing only a cover image without usable sources |
| Content project | articles, curated resources, media | scope, index, source rules, update policy, copyright | copying full third-party works |
| Portfolio | cases, artifacts, role descriptions | context, personal responsibility, decisions, evidence, boundaries | claiming team work or confidential results as personal |
| General project | coherent files and a defined use | goal, audience, how to use, example, limits, contribution | forcing an irrelevant technical template |

## Multi-type projects

Examples:

- A Skill with a small dashboard: primary Agent Skill, auxiliary software.
- A research repo that publishes its dataset: primary research, auxiliary dataset.
- A design system with documentation site: primary design resource, auxiliary documentation.

Do not generate every auxiliary checklist. Include only sections that affect a user's ability to understand, use, verify or legally reuse the project.

## Ask when classification changes work

Ask when files support two materially different interpretations, such as a course repository that may be intended as a personal learning log rather than a reusable course. Explain what README, license or validation would change.
