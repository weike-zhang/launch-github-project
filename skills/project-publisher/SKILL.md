---
name: project-publisher
description: Review, name, document, check, package, publish, share, and update the public files for any project type, including software, CLI tools, Agent Skills, datasets, courses, documentation, research, design resources, content projects, and portfolios. Use when a user wants to publish or open-source a project, rename it, prepare a repository for release, improve or update its README after project changes, create a GitHub Release page or asset, check whether it is ready, plan how to share real proof, or keep later updates accurate. Ask only when a decision becomes necessary, adapt the work to the project type, and require clear approval before remote or public actions.
---

# Project Publisher

Help people understand and try the project that actually exists. Review it, explain who it is for, prepare only the files it needs, share real proof, and update the public files when the project changes. Do not force every project through a software or Agent Skill template.

## Resolve companion capabilities before work

Read [references/companion-orchestration.md](references/companion-orchestration.md) when the task includes public copy, visuals, rendered-page proof, security review or remote publication.

If `$HOME/.codex/project-publisher/install-state.json` exists, inspect it as installation evidence, then recheck the current host because that state may be stale. Before entering any stage whose required or conditional dependency is unavailable, failed, declined, disabled or untrusted, tell the user what is unavailable, what work or proof it affects, and which fallback can still complete. Never silently omit a companion pass or report its gate as passed.

- Inspect the Skills and tools that the current host actually exposes. A lock file, bundled folder or file on disk does not prove that the current session loaded it.
- Add each applicable companion to the working plan, announce its use and read its complete instructions before taking actions governed by it.
- The distributed package includes `$humanizer`. After facts, commands, links, versions and evidence boundaries are settled, use its file or embedded mode for public copy. If the host did not load it, run the manual AI-pattern pass in [references/readme-patterns.md](references/readme-patterns.md) and report that the companion pass was unavailable.
- Treat hooks as host lifecycle configuration, not callable subroutines. Inspect only active, trusted hooks; never claim a hook ran merely because a repository or plugin contains hook files. Keep required release gates in the bundled deterministic scripts.
- Never install a missing companion, enable a plugin, trust a hook or broaden permissions without the user's authorization.
- The repository installer may install bundled dependencies before a launch task. Its recorded result does not replace the runtime recheck above.

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

## Build or update a GitHub profile README

When the user wants to improve their GitHub profile page, read [references/profile-readme.md](references/profile-readme.md) before acting. A profile README renders at the top of the account page from a public `<username>/<username>` repository; it is an account-level artifact, not a project repository, so apply the portfolio rules rather than a software template.

Build it only from the user's real account: name, actual original repositories, real PR states, real contact. Never invent a job title, location, metrics, or claims. Keep a fork that backs an open PR; suggest deleting only stale or try-out forks, and only with per-repo authorization. Deleting a fork or changing repository visibility is a remote action that needs explicit user approval.

Pinned repositories are not settable through the GitHub API; hand the user the web steps from the reference instead of claiming an automated pin.

## Ask at decision points

Ask only when the missing choice changes the current artifact or action. Combine related questions at the same point, normally two to four.

Examples:

- Before naming and positioning: target user, intended outcome and author or project brand. Read [references/naming-and-positioning.md](references/naming-and-positioning.md) before proposing candidates or changing identifiers.
- Before repository creation: repository name, visibility and license.
- When risk is found: remove, replace, keep local, or obtain permission.
- Before distribution planning: goal, audience, available proof, existing channels and effort constraints.
- Before a remote action: exact repository, visibility, branch, Release and external destinations.

Explain why the decision is needed, recommend a safe default, and continue with a reversible draft when the choice can wait. Vague approval is not authorization for public, destructive or privacy-sensitive actions.

## Build only the necessary release surface

Read [references/repository-standard.md](references/repository-standard.md) for common requirements and [references/readme-patterns.md](references/readme-patterns.md) for type-specific README sections.

When naming or renaming the project, read [references/naming-and-positioning.md](references/naming-and-positioning.md). Name the durable role or outcome, not the first demo, platform or release stage. Keep identity, promise, capabilities and evidence separate; then validate speech, guessability, real scope, room to grow and search collision. Preserve historical release truth and treat remote renames as separately authorized actions.

Before drafting a README, identify the reader's recognizable situation, the outcome they want and the proof the project can honestly show. Order the page around the reader's decision path. Translate internal mechanisms, protocol names and maintainer terminology into observable user consequences before presenting implementation detail. Do not treat synonym replacement or a more casual tone as a substitute for clear positioning.

For Chinese README, Release, repository description or distribution copy, read [references/chinese-public-copy.md](references/chinese-public-copy.md). Treat English and Chinese as sibling narratives that share facts, evidence and boundaries, not as a master document and its line-by-line translation. Give the Chinese page its own hook, familiar failure scene, concrete cost, proof and action; require a native-speaker read-aloud check and localized text inside public visuals.

After the factual draft is complete, use the resolved `$humanizer` companion to review README prose, repository descriptions, Release copy and every user-visible string embedded in images. Use file mode for a single document or embedded mode inside a larger launch task. Preserve commands, links, version numbers, observed results and evidence boundaries. Reject fabricated specificity, and do not flatten a real author voice merely because one sentence matches a generic detector. Treat this as a voice pass only: natural copy can still be generic, product-blind or unpersuasive. If the current host did not load Humanizer, apply the AI-pattern check in [references/readme-patterns.md](references/readme-patterns.md) manually and keep that validation boundary explicit.

## Finish public copy with two manual cold reads

The first generated draft is not finished copy. Humanizer can remove common AI writing patterns, but it cannot decide whether a sentence helps this reader understand or try this project.

Use this order for every public language:

1. Finish the factual draft and lock commands, links, versions, proof and limits.
2. Run Humanizer on prose and visible image text, or report that it is unavailable and run the manual fallback.
3. Cold-read the complete result as a new target reader. Do not rely on repository history, author intent or a README in another language.
4. Give every line one main job: name a reader problem or goal, state a result, show proof, set a limit, or lead to a useful next step.
5. Revise lines that have no job, repeat another line, use author-only language, make a real user repeat Skill rules, or carry too many actions.
6. Cold-read the complete revised result a second time. Recheck comprehension, desire to try, speech, repeat-back and plain words.
7. Render the page and its images at normal and narrow widths, then run link, claim and package checks.

Do not call copy ready after generation, after Humanizer or after reviewing only the diff. Read [references/readme-patterns.md](references/readme-patterns.md) for the sentence tests and plain-word replacements.

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

During both cold reads, perform the comprehension and desire-to-try checks in `references/readme-patterns.md`. Require the opening to name a recognizable pain or goal, a project-specific first result, and a low-commitment next step. If replacing the project name with an unrelated tool leaves the headline equally plausible, rewrite it. If a target reader cannot identify why the project matters, what changes in use and what to try without understanding the implementation first, or if the first screen is mostly unbroken prose while useful proof sits below it, revise the reading path before validating links or packaging.

Give every public sentence, heading, navigation label, CTA and image string one clear job: help the reader recognize a pain or goal, state a user-visible result or advantage, add proof, set a boundary, or lead to a next step whose payoff is clear from context. Reject orphan imperatives such as “Try one feature,” “See an example,” “Ask once,” “试一个功能,” “看案例” or “问一次” when they describe only the reader's motion. Replacing `feature` with a concrete noun such as `login flow` does not fix the missing purpose. Rewrite from the question the reader would naturally ask or the result they will get, then read it aloud in that reader's language.

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
- [references/naming-and-positioning.md](references/naming-and-positioning.md): durable names, candidate tests, bilingual word order and rename migration gates.
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
- [references/companion-orchestration.md](references/companion-orchestration.md): companion Skill selection, Humanizer invocation, Hook boundaries and degraded-mode reporting.
- `scripts/build_release_bundle.py`: deterministic ZIP builder with safety exclusions and symlink rejection.
- [references/release-page.md](references/release-page.md): required Release-page content, version alignment and remote-state gates.
- `scripts/generate_release_page.py`: deterministic GitHub Release-page generator and stale-page check.
- [references/profile-readme.md](references/profile-readme.md): GitHub profile README build and refresh, fork handling and pinned-repository guidance.
