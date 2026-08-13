# Launch GitHub Project

**Turn a local project into a GitHub release that strangers can understand, try, and verify.**

[简体中文](README.zh-CN.md) · [Install](docs/INSTALL.md) · [First launch guide](docs/FIRST-GITHUB-LAUNCH.zh-CN.md) · [Latest Release](https://github.com/weike-zhang/launch-github-project/releases/latest)

Use this Agent Skill when a project works locally but its public release surface is still uncertain: the README does not show the outcome, a generic checklist assumes every project is an app, evidence does not match the claims, or the default branch, tag and Release have drifted apart.

Launch GitHub Project starts read-only, identifies the project type, and prepares only the material a visitor needs to decide, try and verify. It can flag risky public files and package a deterministic ZIP, but it does not treat a clean scan as proof of safety, adoption or quality. Remote actions require an exact target and explicit authorization.

**Verify before installing:** [real self-audit and fix](examples/self-audit-bundle-safety.md) · [v0.1.2 Release and ZIP](https://github.com/weike-zhang/launch-github-project/releases/tag/v0.1.2) · [published pilot prompt and outputs](evals/results/model-comparison.md)

## Install and invoke

```bash
npx skills add weike-zhang/launch-github-project --skill launch-github-project -g
```

Then invoke it from the project you want to prepare:

```text
Use $launch-github-project to audit this project for GitHub.
Start read-only. Show me the smallest public surface this project type needs,
the evidence behind each claim, and every decision required before publishing.
Do not perform remote actions without my explicit approval.
```

See [Install](docs/INSTALL.md) for local-checkout, validation and update commands.

The first response should classify the project, separate facts from assumptions, list the smallest justified public artifacts, attach evidence to each public claim, and stop for decisions before any remote action. If it starts editing or proposes every artifact before that audit, stop and report the host and version; host-level behavior is not yet claimed as broadly verified.

## What changes for the project

| Starting state | Result from the Skill |
| --- | --- |
| One generic README template for every project | A reader path and evidence surface matched to software, an Agent Skill, dataset, research, course, design resource, portfolio or another real project type |
| Unsure which files are safe to expose | Redacted secret findings, public-surface blockers and explicit rights decisions before packaging |
| A passing script is being presented as product proof | Release integrity, behavior evidence, adoption evidence and popularity reported separately |
| Local version, open PR, default branch and Release disagree | A generated Release page and an explicit publication-state check instead of calling uploaded work published |
| Promotion starts with a calendar or a request for stars | A small distribution path based on the intended outcome, audience and evidence already available |

The Skill may prepare a README, install or reproduction steps, examples, data card, methodology, visual preview, privacy and license guidance, Release page, release ZIP or distribution brief. It does not generate all of them by default.

<img src="assets/hero.png" alt="Launch GitHub Project — prepare a GitHub release people can understand, try, and verify" width="760">

## Evidence from this repository

This project has been run against itself. The first self-audit found that a file symlink could copy bytes from outside the project into a release ZIP. Version 0.1.2 rejects file and directory symlinks before reading them and keeps the remaining race boundary explicit.

- [Reproduction, root cause, fix and limitations](examples/self-audit-bundle-safety.md)
- [v0.1.2 Release page and verified ZIP](https://github.com/weike-zhang/launch-github-project/releases/tag/v0.1.2)
- [Published pilot prompt, response pair and limitations](evals/results/model-comparison.md)

The pilot is one exploratory comparison, not a benchmark. It does not predict stars, adoption or launch reach.

## Evidence and compatibility

| Surface | Status | Evidence |
| --- | --- | --- |
| Skills CLI repository discovery | Verified | The installable `launch-github-project` Skill is discovered from the public repository |
| Release-tool regressions | Verified on Python 3.12 | [Tests](tests/test_release_tools.py) and [GitHub Actions](https://github.com/weike-zhang/launch-github-project/actions/workflows/validate.yml) |
| Fixture and route coverage | Release integrity only | `python3 evals/validate_fixtures.py`; not a model-quality score |
| Distribution behavior | Exploratory | One published [prompt and baseline/Skill response pair](evals/results/model-comparison.md) |
| Other Agent Skills hosts | Unverified | Compatibility reports are welcome |

## Permissions and limits

- Secret detection is pattern-based and requires human review; matched values are redacted.
- Automated checks cannot prove asset ownership, privacy safety, product quality or user adoption.
- The release bundler rejects symlinks and non-regular files, but it is not a general sandbox against malicious concurrent file replacement.
- Installing the Skill does not grant permission to create repositories, push, change visibility, publish Releases or post externally. Each remote action needs an explicit target and authorization.
- Working notes belong in `.launch-github-project/`, which is ignored and excluded from release bundles.

Read [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md) and the [visual asset notice](assets/ASSET-NOTICE.md) for the full boundaries.

## How it works

![Audit, classify, prove, package, then hand off remote actions explicitly](assets/launch-flow.svg)

1. Audit facts, risks, gaps and Git state without editing first.
2. Classify the primary project type before choosing public artifacts.
3. Build the reader path and direct evidence for the core promise.
4. Validate links, secrets, public surface, version metadata and the release package.
5. Hand off or perform only the specifically authorized remote actions, then verify the unsigned public result.

## Contributing and license

The most useful contribution is a reproducible release failure, a project type the current routing mishandles, or a public claim whose evidence cannot be checked. See [CONTRIBUTING.md](CONTRIBUTING.md).

MIT licensed. Built by [Weike Zhang](https://github.com/weike-zhang).
