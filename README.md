<p align="center">
  <img src="assets/hero.png" alt="Project Publisher reviews, positions, publishes and keeps a project's public materials current" width="100%">
</p>

<p align="center">
  <strong>Your project changed. Its README, Release and launch posts did not. Project Publisher finds the mismatch, fixes the public materials you approve and leaves remote actions to you.</strong>
</p>

<p align="center">
  <a href="#find-the-biggest-public-gap-first">Find the biggest public gap</a> ·
  <a href="examples/self-audit-bundle-safety.md">See the release leak it caught</a> ·
  <a href="README.zh-CN.md">简体中文</a>
</p>

A project can work locally and still lose people when it becomes public: the name describes only the first demo, the README starts with maintainer detail, the install path is hard to find, the Release explains changes instead of value, or later updates leave the public story behind.

Project Publisher handles that public side of the project. It reviews what exists, sharpens the name and position, prepares the smallest useful release surface, turns real evidence into distribution material, and resynchronizes the public story after the product changes. Its first pass is read-only, and it adapts the work to the actual project type instead of forcing everything through one template.

Install Project Publisher and its bundled Humanizer from the public repository:

```bash
git clone https://github.com/weike-zhang/project-publisher.git
python3 project-publisher/scripts/install.py
```

Then ask: `Use $project-publisher to review this project before I publish or update it. Start read-only and tell me the biggest reason a new visitor may not try it.` Nothing changes in the first pass; you get a concrete gap report first. The v0.3.0 public clone, integrated installer and Skills CLI discovery are [verified from clean temporary paths](evals/results/public-install-v0.3.0.md); [the earlier Codex first audit covers the published v0.2.0 Skills-only path under the former name](evals/results/codex-first-audit-v0.2.0.md).

## Keep files from outside the project out of the release ZIP

While auditing its own repository, the Skill found that a symlink inside the project could read a file outside the project directory. The old bundler copied those bytes into the ZIP.

```text
project/
├── README.md
└── outside.txt -> /etc/hosts

Release stopped: outside.txt is a symbolic link
ZIP not created; target file not read
```

The bundler now stops before reading the target. Release ZIP contents are part of the same audit as the README, and regression tests preserve the fix.

[Read the reproduction, root cause and limits](examples/self-audit-bundle-safety.md) · [Inspect the historical v0.1.2 fix Release](https://github.com/weike-zhang/launch-github-project/releases/tag/v0.1.2)

This is release-safety evidence, not a claim that automation can prove ownership, product quality or adoption.

## Find the biggest public gap first

The same public install path works from a clean directory:

```bash
git clone https://github.com/weike-zhang/project-publisher.git
python3 project-publisher/scripts/install.py
```

The integrated installer adds Project Publisher, bundled Humanizer and the dependency-guard Hook, then verifies the required command-line tools. Review and trust the Hook with `/hooks`; the installer cannot grant trust for you. Project Publisher uses Humanizer after factual claims and evidence are settled, then reruns its own comprehension and desire-to-try checks. If any dependency failed, was declined or is unavailable in the active host, it reports the affected proof and fallback when that stage is reached. [See all install paths and boundaries](docs/INSTALL.md).

From the project you want to publish:

```text
Use $project-publisher to review this project before I publish or update it.
Start read-only. Tell me the biggest reason a new visitor may not understand or
try it, show me the evidence, and recommend the smallest useful fix.
Do not perform remote actions without my explicit approval.
```

A useful first response is structured like this:

```text
Primary type       Agent Skill
Observed           SKILL.md, install path, scripts, release history
Public gap         no direct input/output proof on the first screen
Release blocker    version metadata and latest Release disagree
Human decisions    asset rights, visibility, exact remote target
Action taken       none; read-only audit
```

The findings vary by repository. The Skill inspects first, labels assumptions, explains why each artifact is needed and waits for approval before remote work. See [installation and update options](docs/INSTALL.md).

## What it handles

| Need | Result |
| --- | --- |
| The project name describes one demo, platform or release moment | A short identity that fits the durable role, with the missing precision carried by the description and evidence |
| A README that lists features but does not explain the value | A README that says who the project is for, shows direct proof and gives readers a first step |
| The project changed but its README still teaches old behavior or commands | A full reread after implementation, followed by an in-place update when any public contract moved |
| Every section has an image, including raster text that renders badly | One hero by default; code blocks for paths and short output, and charts only when real data needs plotting |
| Uncertainty about what can safely become public | A redacted secret scan, publishing blockers and the asset-rights questions that still need a decision |
| Tests being used as marketing proof | A report that separates release checks and observed behavior from adoption or popularity |
| A stale or hand-written Release page | A page generated from structured evidence, including optional version-pinned visual proof |
| A source archive that may contain local debris | A deterministic ZIP that excludes local state, rejects symlinks and is actually listed and extracted |
| Local, PR, tag and Release versions drifting apart | A version check that distinguishes an uploaded artifact from a public Release |
| A launch post that merely announces a repository | Distribution material built around a useful result, caught failure or reproducible proof |

Depending on the project, the Skill may prepare documentation, evidence, release assets or a distribution brief. It will not add a website, community, benchmark or roadmap unless the project actually supports one.

## Automatic checks and human decisions

| Automated | Still requires judgment |
| --- | --- |
| Local links, unresolved placeholders and machine-specific paths | Whether the first screen makes sense to the intended reader |
| Redacted secret-pattern scan | Whether an apparent secret or personal detail is genuinely safe |
| Nested repositories, editor files, internal drafts and identity-setup copy | Whether assets, data and screenshots may legally be published |
| Release-page freshness and semantic version alignment | Whether the evidence supports the public promise |
| Deterministic bundle contents, symlinks and extraction | Whether the repository deserves to be public and where it should be published |

A clean scan is a gate result, not proof of safety, usefulness or demand.

## How the publication lifecycle works

1. Audit files, Git state, risks and gaps without editing.
2. Classify the primary project type and check whether its name and promise match the durable role.
3. Build the reader path and the smallest evidence surface for the core promise.
4. Validate links, secrets, public content, visuals, versions and the actual ZIP.
5. Prepare the Release and evidence-led distribution material, then perform only the remote actions that were approved.
6. Verify the public result from a visitor view and resynchronize it when the project changes.

## Evidence and compatibility

| Surface | Current status | Evidence |
| --- | --- | --- |
| Public v0.2.0: global install → invoke → first audit | Verified on Codex CLI 0.147.0-alpha.6.5 | [Install, clean fixture and observed output](evals/results/codex-first-audit-v0.2.0.md#post-publication-check) |
| Historical local 0.2.0 candidate: project install → invoke → first audit | Verified on the same host before publication | [Candidate fixture, command and sanitized output](evals/results/codex-first-audit-v0.2.0.md#release-candidate-check) |
| Public v0.3.0: clone → integrated install → Skills CLI discovery | Verified after the repository rename | [Clean temporary-path verification](evals/results/public-install-v0.3.0.md) |
| Release scripts | Verified on Python 3.12 for the published v0.2.0 path | [Regression tests](tests/test_release_tools.py) and [historical GitHub Actions path](https://github.com/weike-zhang/launch-github-project/actions/workflows/validate.yml) |
| Project-type routes and evaluation files | Integrity checked | [Fixture validator](evals/validate_fixtures.py); not a model-quality score |
| Distribution behavior | One exploratory pair | [Exact prompt, baseline, Skill response and limitations](evals/results/model-comparison.md) |
| Other Agent Skills hosts | Unverified | Compatibility reports with host and version are welcome |

## Permissions and limits

- Installing the Skill does not authorize repository creation, Push, visibility changes, Releases or external posts. Every remote action needs an exact target and explicit approval.
- Secret detection is pattern-based and never replaces human review.
- The bundler rejects symlinks and non-regular files, but it is not a sandbox against malicious concurrent file replacement.
- Automated checks cannot prove asset ownership, privacy safety, product quality, user adoption or unsigned rendering.
- Working notes belong in `.project-publisher/`; the directory is ignored and excluded from release bundles.

Read [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md), the [visual asset notice](assets/ASSET-NOTICE.md) and [third-party notices](THIRD-PARTY-NOTICES.md) for the full boundaries.

## Contributing

The most useful contribution is a reproducible release failure, a project type the current routing mishandles, a broken first-success path or a public claim whose evidence cannot be checked. See [CONTRIBUTING.md](CONTRIBUTING.md).

MIT licensed. Built by [Weike Zhang](https://github.com/weike-zhang).
