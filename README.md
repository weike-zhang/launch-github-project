<p align="center">
  <img src="assets/hero.png" alt="Launch GitHub Project finds what stops new users from trying a project, then prepares its README, visuals, install path, Release page and source bundle" width="100%">
</p>

<p align="center">
  <strong>The project is finished, but the README, visuals, Release, and source bundle are not. Give the repository to this Skill, review the gaps it finds, then decide what it may change.</strong>
</p>

<p align="center">
  <a href="#run-a-read-only-launch-check">Run a read-only launch check</a> ·
  <a href="examples/self-audit-bundle-safety.md">See a real failure it caught</a> ·
  <a href="README.zh-CN.md">简体中文</a>
</p>

A project can work locally and still lose a new user on GitHub: the README starts with maintainer detail, the install path is hard to find, the Release explains changes instead of value, or the source bundle contains local debris.

Launch GitHub Project is an Agent Skill for finishing the public release. Its first pass is read-only: it identifies the biggest obstacle to first use, release blockers and decisions only you can make. After approval, it prepares the README, visuals, install guidance, Release page and source bundle for the actual project type instead of forcing everything through one template.

```bash
npx skills add weike-zhang/launch-github-project --agent codex --skill launch-github-project -g -y
```

Then ask: `Use $launch-github-project to audit this project for GitHub. Start read-only.` Nothing changes in the first pass; you get a concrete gap report first. [See the verified Codex first audit](evals/results/codex-first-audit-v0.2.0.md).

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

[Read the reproduction, root cause and limits](examples/self-audit-bundle-safety.md) · [Inspect the v0.1.2 fix Release](https://github.com/weike-zhang/launch-github-project/releases/tag/v0.1.2)

This is release-safety evidence, not a claim that automation can prove ownership, product quality or adoption.

## Run a read-only launch check

```bash
npx skills add weike-zhang/launch-github-project --agent codex --skill launch-github-project -g -y
```

From the project you want to publish:

```text
Use $launch-github-project to audit this project for GitHub.
Start read-only. Identify the project type, the smallest public surface it needs,
the evidence behind each claim, and every decision required before publishing.
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

## What it prepares

| Need | Result |
| --- | --- |
| A README that lists features but does not explain the value | A README that says who the project is for, shows direct proof and gives readers a first step |
| The project changed but its README still teaches old behavior or commands | A full reread after implementation, followed by an in-place update when any public contract moved |
| Every section has an image, including raster text that renders badly | One hero by default; code blocks for paths and short output, and charts only when real data needs plotting |
| Uncertainty about what can safely become public | A redacted secret scan, publishing blockers and the asset-rights questions that still need a decision |
| Tests being used as marketing proof | A report that separates release checks and observed behavior from adoption or popularity |
| A stale or hand-written Release page | A page generated from structured evidence, including optional version-pinned visual proof |
| A source archive that may contain local debris | A deterministic ZIP that excludes local state, rejects symlinks and is actually listed and extracted |
| Local, PR, tag and Release versions drifting apart | A version check that distinguishes an uploaded artifact from a public Release |

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

## How the release path works

1. Audit files, Git state, risks and gaps without editing.
2. Classify the primary project type before choosing artifacts.
3. Build the reader path and the smallest evidence surface for the core promise.
4. Validate links, secrets, public content, visuals, versions and the actual ZIP.
5. Generate a Release page for review, then perform only the remote actions that were approved.
6. Verify the public repository and Release from a visitor view.

## Evidence and compatibility

| Surface | Current status | Evidence |
| --- | --- | --- |
| Public v0.2.0: global install → invoke → first audit | Verified on Codex CLI 0.147.0-alpha.6.5 | [Install, clean fixture and observed output](evals/results/codex-first-audit-v0.2.0.md#post-publication-check) |
| Local 0.2.0 candidate: project install → invoke → first audit | Verified on the same host before publication | [Candidate fixture, command and sanitized output](evals/results/codex-first-audit-v0.2.0.md#release-candidate-check) |
| Release scripts | Verified on Python 3.12 | [Regression tests](tests/test_release_tools.py) and [GitHub Actions](https://github.com/weike-zhang/launch-github-project/actions/workflows/validate.yml) |
| Project-type routes and evaluation files | Integrity checked | [Fixture validator](evals/validate_fixtures.py); not a model-quality score |
| Distribution behavior | One exploratory pair | [Exact prompt, baseline, Skill response and limitations](evals/results/model-comparison.md) |
| Other Agent Skills hosts | Unverified | Compatibility reports with host and version are welcome |

## Permissions and limits

- Installing the Skill does not authorize repository creation, Push, visibility changes, Releases or external posts. Every remote action needs an exact target and explicit approval.
- Secret detection is pattern-based and never replaces human review.
- The bundler rejects symlinks and non-regular files, but it is not a sandbox against malicious concurrent file replacement.
- Automated checks cannot prove asset ownership, privacy safety, product quality, user adoption or unsigned rendering.
- Working notes belong in `.launch-github-project/`; the directory is ignored and excluded from release bundles.

Read [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md), the [visual asset notice](assets/ASSET-NOTICE.md) and [third-party notices](THIRD-PARTY-NOTICES.md) for the full boundaries.

## Contributing

The most useful contribution is a reproducible release failure, a project type the current routing mishandles, a broken first-success path or a public claim whose evidence cannot be checked. See [CONTRIBUTING.md](CONTRIBUTING.md).

MIT licensed. Built by [Weike Zhang](https://github.com/weike-zhang).
