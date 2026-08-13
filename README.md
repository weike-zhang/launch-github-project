<p align="center">
  <img src="assets/hero.png" alt="Launch GitHub Project hero showing repository checks, claim review, release packaging and final verification" width="100%">
</p>

<p align="center">
  <strong>Check the repository, support public claims with evidence, and review the release before it goes live.</strong>
</p>

<p align="center">
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="docs/INSTALL.md">Install options</a> ·
  <a href="examples/self-audit-bundle-safety.md">Real failure and fix</a> ·
  <a href="https://github.com/weike-zhang/launch-github-project/releases/latest">Release</a>
</p>

<p align="center">
  <a href="https://github.com/weike-zhang/launch-github-project/actions/workflows/validate.yml"><img alt="Validate" src="https://github.com/weike-zhang/launch-github-project/actions/workflows/validate.yml/badge.svg"></a>
  <a href="https://github.com/weike-zhang/launch-github-project/releases/latest"><img alt="Latest release" src="https://img.shields.io/github/v/release/weike-zhang/launch-github-project"></a>
  <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-52D6A3"></a>
</p>

A project can work locally while its GitHub page still looks unfinished or leaves visitors unsure how to try it. Launch GitHub Project audits the repository, chooses materials for the project type, ties public claims to evidence and builds a deterministic release bundle. Remote actions still require your approval.

Use it when the work is finished locally but the repository is not ready for someone new to install, inspect or reuse. It supports software, Agent Skills, datasets, research, courses, design resources, portfolios and mixed projects without forcing them through one template.

```bash
npx skills add weike-zhang/launch-github-project --agent codex --skill launch-github-project -g -y
```

Then ask: `Use $launch-github-project to audit this project for GitHub. Start read-only.` [See the verified Codex first audit](evals/results/codex-first-audit-v0.2.0.md).

## A real failure it caught

<img src="assets/audit-proof.png" alt="A real self-audit showing a tracked symlink leaving the project, the release blocker, and the corrected release state" width="100%">

Running this Skill against its own repository found that a tracked file symlink could copy bytes from outside the reviewed project into a release ZIP. The bundler now rejects file and directory symlinks before reading them, regression tests preserve the fix, and the remaining concurrent-replacement boundary is documented.

[Read the reproduction, root cause and limits](examples/self-audit-bundle-safety.md) · [Inspect the v0.1.2 fix Release](https://github.com/weike-zhang/launch-github-project/releases/tag/v0.1.2)

This is release-safety evidence, not a claim that automation can prove ownership, product quality or adoption.

## Install and run your first audit

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

![Release workflow covering repository review, required materials, evidence, packaging, approval for remote actions and public verification](assets/launch-flow.svg)

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
