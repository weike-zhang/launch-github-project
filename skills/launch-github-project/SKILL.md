---
name: launch-github-project
description: Audit, position, document, validate, package, and prepare the GitHub launch of any project type, including software, CLI tools, Agent Skills, datasets, courses, documentation, research, design resources, content projects, and portfolios. Use when a user wants to publish or open-source a project, make a repository release-ready, improve launch materials, prepare README or Release assets, evaluate launch readiness, or plan evidence-based distribution. Ask only when a decision becomes necessary, adapt outputs to the project type, and require explicit authorization before remote or public actions.
---

# Launch GitHub Project

Turn the project that actually exists into the smallest complete public repository it needs. Do not force every project through a software or Agent Skill template.

## Start with a read-only audit

1. Inspect the project root, important files, Git status and current documentation.
2. Run `python scripts/audit_repository.py <project-root> --json` when the script is available from this Skill.
3. Run `python scripts/check_secrets.py <project-root> --json` before preparing public artifacts.
4. Run `python scripts/review_public_surface.py <project-root> --json` to expose caches, nested repositories, editor files, pending-rights copy, internal drafts and misleading fixture scores.
5. Separate observed evidence, inference, risk and missing decisions.
6. Complete safe work first; do not begin with a questionnaire.

Never echo a full suspected secret. Preserve unrelated user changes. Do not initialize Git, create a remote, push, release, change visibility, or post externally unless the user explicitly asks for that action.

## Classify before packaging

Read [references/project-type-routing.md](references/project-type-routing.md). Select one primary type and only the auxiliary types that materially affect the release:

- software or CLI;
- Agent Skill;
- dataset;
- course or documentation;
- research;
- design resource;
- content project;
- portfolio;
- general project.

Base the classification on files and actual use, not the desired marketing label. If evidence is insufficient, use the general standard and mark the classification tentative.

## Ask at decision points

Ask only when the missing choice changes the current artifact or action. Combine related questions at the same point, normally two to four.

Examples:

- Before naming and positioning: target user, intended outcome and author or project brand.
- Before repository creation: repository name, visibility and license.
- When risk is found: remove, replace, keep local, or obtain permission.
- Before distribution planning: goal, audience, available proof, existing channels and effort constraints.
- Before a remote action: exact repository, visibility, branch, Release and external destinations.

Explain why the decision is needed, recommend a safe default, and continue with a reversible draft when the choice can wait. Vague approval is not authorization for public, destructive or privacy-sensitive actions.

## Build only the necessary release surface

Read [references/repository-standard.md](references/repository-standard.md) for common requirements and [references/readme-patterns.md](references/readme-patterns.md) for type-specific README sections.

Create or improve only the artifacts justified by the project:

- README and repository metadata;
- license and attribution guidance;
- usage, installation, data card, methodology, visual preview or case-study evidence;
- examples, tests, Evals or reproducibility steps;
- security, privacy and contribution guidance;
- Release notes and package manifest;
- visual assets and distribution copy.

Do not add badges, governance documents, CI, websites, videos, telemetry or community files merely to look mature.

## Validate claims and artifacts

- Use the project's native checks when available.
- Use `python scripts/check_links.py <project-root>` for local Markdown links.
- Search for unresolved placeholders and private material.
- Verify commands from a clean path when practical.
- Mark compatibility as verified, partial or unverified.
- Keep raw evaluation inputs and limitations with reported scores.
- Never invent users, metrics, benchmarks, endorsements or download counts.

Read [references/privacy-and-license.md](references/privacy-and-license.md) before recommending public release when ownership, personal data, third-party content or licensing is uncertain.

## Review the exact public surface

Read [references/public-surface-review.md](references/public-surface-review.md) after drafting release materials and again immediately before a public push.

- Resolve every automated blocker and review warnings individually.
- Require a final state for each material asset: confirmed for public use, replace, or keep local.
- Keep rejected generation prompts, replacement instructions, author-profile drafts and distribution plans out of the public repository unless they intentionally help users or contributors.
- Call schema, file-count and fixture checks release integrity, not model or product quality; do not convert them into performance percentages.
- Publish behavior scores only with methods and complete sanitized raw outputs.
- Review commit messages, authors, contributors and nested repository history before staging.
- After publication, verify the remote page as an unsigned visitor; a successful push is not completion.

## Prepare a release bundle

Read [references/release-checklist.md](references/release-checklist.md). Use:

```bash
python scripts/build_release_bundle.py <project-root> --output <destination.zip>
```

The bundle must exclude Git data, local state, credentials, caches, build debris and its own output. Inspect the archive list and extract it into a temporary directory before calling it ready.

## Plan distribution from the user's goal

Read [references/distribution-playbook.md](references/distribution-playbook.md) only when the user asks for launch or promotion planning.

Choose the smallest useful combination based on:

- desired outcome;
- target audience;
- real, publishable evidence;
- channels the user actually has;
- time, format and maintenance constraints;
- privacy and disclosure boundaries.

Do not produce a fixed day-by-day calendar or every possible content module. Match the proof format to the project: behavior comparison for a Skill, reproducibility for research, data cards for datasets, visual previews for design resources, and responsibility plus outcomes for portfolios.

## Handoff remote publishing explicitly

When local preparation is complete, report:

- what is ready;
- what remains partial or unverified;
- exact public-risk decisions still required;
- the commands or GitHub UI steps for the chosen publication path.

Use a dedicated GitHub publish workflow such as `yeet` for branch, commit, push and PR when appropriate. Do not silently absorb those operations into this Skill.

## Resources

- [references/project-type-routing.md](references/project-type-routing.md): project classification and type-specific proof.
- [references/repository-standard.md](references/repository-standard.md): common release-ready requirements.
- [references/readme-patterns.md](references/readme-patterns.md): README selection by project type.
- [references/privacy-and-license.md](references/privacy-and-license.md): privacy, ownership and license decisions.
- [references/release-checklist.md](references/release-checklist.md): local verification and remote approval gates.
- [references/public-surface-review.md](references/public-surface-review.md): final public-content, evidence, rights, history and remote-page audit.
- [references/distribution-playbook.md](references/distribution-playbook.md): goal-driven distribution planning.
- `scripts/audit_repository.py`: read-only readiness and type-signal audit.
- `scripts/check_secrets.py`: redacted secret-pattern scan.
- `scripts/check_links.py`: local Markdown link verification.
- `scripts/review_public_surface.py`: deterministic public-surface blocker and warning scan.
- `scripts/build_release_bundle.py`: deterministic ZIP builder with safety exclusions.
