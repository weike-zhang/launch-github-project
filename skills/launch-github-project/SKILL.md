---
name: launch-github-project
description: Audit, position, document, validate, package, and prepare the GitHub launch of any project type, including software, CLI tools, Agent Skills, datasets, courses, documentation, research, design resources, content projects, and portfolios. Use when a user wants to publish or open-source a project, make a repository release-ready, improve or resynchronize its README after project changes, generate a GitHub Release page or Release asset, evaluate launch readiness, or plan evidence-based distribution. Ask only when a decision becomes necessary, adapt outputs to the project type, and require explicit authorization before remote or public actions.
---

# Launch GitHub Project

Turn the project that actually exists into the smallest complete public repository it needs. Do not force every project through a software or Agent Skill template.

## Start with a read-only audit

1. Inspect the project root, important files, Git status and current documentation.
2. Run `python3 scripts/audit_repository.py <project-root> --json` when the script is available from this Skill.
3. Run `python3 scripts/check_secrets.py <project-root> --json` before preparing public artifacts.
4. Run `python3 scripts/review_public_surface.py <project-root> --json` to expose caches, nested repositories, editor files, pending-rights copy, internal drafts and misleading fixture scores.
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

Before drafting a README, identify the reader's recognizable situation, the outcome they want and the proof the project can honestly show. Order the page around the reader's decision path. Translate internal mechanisms, protocol names and maintainer terminology into observable user consequences before presenting implementation detail. Do not treat synonym replacement or a more casual tone as a substitute for clear positioning.

For Chinese README, Release, repository description or distribution copy, read [references/chinese-public-copy.md](references/chinese-public-copy.md). Treat English and Chinese as sibling narratives that share facts, evidence and boundaries, not as a master document and its line-by-line translation. Give the Chinese page its own hook, familiar failure scene, concrete cost, proof and action; require a native-speaker read-aloud check and localized text inside public visuals.

After the factual draft is complete, use `$humanizer` when it is installed to review README prose, repository descriptions, Release copy and every user-visible string embedded in images. Use file mode for a single document or embedded mode inside a larger launch task. Preserve commands, links, version numbers, observed results and evidence boundaries. Reject fabricated specificity, and do not flatten a real author voice merely because one sentence matches a generic detector. Treat this as a voice pass only: natural copy can still be generic, product-blind or unpersuasive. If Humanizer is unavailable, apply the AI-pattern check in [references/readme-patterns.md](references/readme-patterns.md) manually.

Create or improve only the artifacts justified by the project:

- README and repository metadata;
- license and attribution guidance;
- usage, installation, data card, methodology, visual preview or case-study evidence;
- examples, tests, Evals or reproducibility steps;
- security, privacy and contribution guidance;
- Release notes and package manifest;
- visual assets and distribution copy.

Do not add badges, governance documents, CI, websites, videos, telemetry or community files merely to look mature.

Default to one project-owned hero or product preview and no other images. Before adding another visual, apply the necessity and format gate in `references/readme-patterns.md`. Use text, a table or a code block when it communicates the evidence just as well. Use a reproducible chart only for real quantitative data or a relationship that becomes materially clearer when plotted; keep its source data and generation script. Use screenshots for observable UI state. Avoid raster diagrams full of prose, especially localized Chinese copy, and never present decorative generated art as product evidence. If a hero or necessary proof visual exists, decide explicitly whether it belongs in the initial viewport; do not leave it below several paragraphs by accident.

After drafting and the voice pass, perform both cold-reader gates in `references/readme-patterns.md`: comprehension and desire to try. Require the opening to name a recognizable pain or goal, a project-specific first result, and a low-commitment next step. If replacing the project name with an unrelated tool leaves the headline equally plausible, rewrite it. If a target reader cannot identify why the project matters, what changes in use and what to try without understanding the implementation first, or if the initial viewport is visually dominated by undifferentiated prose while the useful proof sits below the fold, revise the reading path before validating links or packaging.

## Resynchronize the current README after project changes

After changing project behavior, commands, interfaces, versions, compatibility, permissions, limits, visuals or evidence, reopen every public README and read each one from start to finish. Compare the current project with every affected claim, example, command, image and link. Decide explicitly whether the README needs an update; do not assume documentation remains correct because the change was small.

When an update is needed, edit the authoritative README in place. Replace or remove stale content instead of appending a second explanation that contradicts the first. Preserve unrelated user-authored content and voice. If the README is generated, update its source and regenerate it. Keep localized README siblings factually aligned while allowing native wording and reading order. Do not create `README.new.md`, a suggestion file or a parallel draft unless the user asks for one.

When no update is needed, record which change was reviewed and why it does not affect public use. In either case, reread the complete final README after the decision and rerun relevant command, link, claim and rendered-opening checks. A diff of the edited paragraph is not a full README review.

## Design the first-success and adoption path

Read [references/adoption-and-trust.md](references/adoption-and-trust.md) when improving a public launch, README, evidence plan or distribution surface.

- State the user outcome before the internal method.
- Keep the end-user quick start to the fewest actions that produce a visible result; move maintainer gates out of that path.
- Make proof test the core promise directly. A release Skill needs real release artifacts and caught failures, not only fixture integrity or launch copy.
- Separate discovery, first success, repeat use, contribution and popularity. Stars do not prove activation or value.
- Match repeat use to project frequency; do not invent an empty community, website or recurring workflow to imitate a mature project.
- Prefer artifact-led distribution: show a useful result, caught failure, reproducible comparison or user outcome before announcing that a repository exists.

## Validate claims and artifacts

- Use the project's native checks when available.
- Use `python3 scripts/check_links.py <project-root>` for local Markdown links.
- Search for unresolved placeholders and private material.
- Verify commands from a clean path when practical.
- Reject or resolve symlinks explicitly before scanning or packaging; never follow a repository link into unreviewed local files.
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
python3 scripts/build_release_bundle.py <project-root> --output <destination.zip>
```

The bundle must exclude Git data, local state, credentials, caches, build debris and its own output. Inspect the archive list and extract it into a temporary directory before calling it ready.

## Generate a GitHub Release page

Read [references/release-page.md](references/release-page.md). Generate the page from structured release evidence with:

```bash
python3 scripts/generate_release_page.py <project-root> \
  --spec <release-spec.json> --output <release-page.md>
```

Lead with the user-visible reason to update, then provide changes, install or update instructions, exact verification, compatibility and limitations. When a visual makes the change easier to judge, include a version-pinned image and a caption stating what it proves. Check that local `HEAD`, the remote default branch, any open release PR and the latest Release tag describe the same publication state. Never call an open PR published, and never publish a tag whose version metadata disagrees with the tag.

Before CI or publication, run `python3 scripts/generate_release_page.py <project-root> --check-all` to validate every versioned JSON spec that has a generated Markdown page. Do not hardcode the current version into a permanent validation workflow.

Generating local Markdown is reversible. Creating the GitHub Release, tag or asset remains a remote action that requires explicit authorization. After publication, verify the Release page and asset as an unsigned visitor.

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
- [references/chinese-public-copy.md](references/chinese-public-copy.md): native Chinese persuasion, translationese traps and bilingual workflow.
- [references/privacy-and-license.md](references/privacy-and-license.md): privacy, ownership and license decisions.
- [references/release-checklist.md](references/release-checklist.md): local verification and remote approval gates.
- [references/public-surface-review.md](references/public-surface-review.md): final public-content, evidence, rights, history and remote-page audit.
- [references/distribution-playbook.md](references/distribution-playbook.md): goal-driven distribution planning.
- `scripts/audit_repository.py`: read-only readiness and type-signal audit.
- `scripts/check_secrets.py`: redacted secret-pattern scan.
- `scripts/check_links.py`: local Markdown link verification.
- `scripts/review_public_surface.py`: deterministic public-surface blocker and warning scan.
- [references/adoption-and-trust.md](references/adoption-and-trust.md): first-success, proof, retention and contribution checks derived from real adoption failures.
- `scripts/build_release_bundle.py`: deterministic ZIP builder with safety exclusions and symlink rejection.
- [references/release-page.md](references/release-page.md): required Release-page content, version alignment and remote-state gates.
- `scripts/generate_release_page.py`: deterministic GitHub Release-page generator and stale-page check.
