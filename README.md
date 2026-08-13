<div align="center">
  <img src="assets/hero.png" alt="Launch GitHub Project — prepare any project for a safe, evidence-based launch" width="100%">

# Launch GitHub Project

**Turn a local project into the smallest credible GitHub repository it needs.**

[简体中文](README.zh-CN.md) · [Install](docs/INSTALL.md) · [First GitHub launch guide](docs/FIRST-GITHUB-LAUNCH.zh-CN.md)

</div>

Most launch advice assumes a software product. This Skill starts with what exists, classifies the project, and creates only the public surface that its type and evidence justify.

It can prepare software, CLI tools, Agent Skills, datasets, courses, documentation, research, design resources, content projects, portfolios, and general projects. It audits before editing, redacts suspected secrets, keeps compatibility claims honest, packages a deterministic ZIP, and asks grouped questions only at real decision points.

![Release flow](assets/launch-flow.svg)

## What it produces

- repository metadata, name and positioning options;
- a README matched to the project type;
- installation, examples, data cards, methodology, case studies, or visual previews when needed;
- privacy, security, license and attribution guidance;
- checks for secrets, links, placeholders, asset-rights status and public-risk patterns;
- release notes, launch copy and a distribution plan selected from the user's outcome, audience, evidence, channels and effort;
- a handoff with exact local commands and explicit gates for any remote action.

## Quick start

Install the Skill:

```bash
npx skills add weike-zhang/launch-github-project --skill launch-github-project -g
```

Then invoke it from the project you want to prepare:

```text
Use $launch-github-project to prepare this project for GitHub. Start read-only,
classify the project, ask only grouped questions when a decision changes the
artifacts, and do not publish remotely without my explicit approval.
```

That is the end-user path. Maintainers and people running individual gates can use the commands in [Install](docs/INSTALL.md).

## A real failure this release now catches

During this repository's own release audit, a file symlink pointing outside the project was copied into the generated ZIP. Version 0.1.2 rejects file and directory symlinks before reading them, treats them as public-surface blockers, and covers the behavior with regression tests.

Read the complete [self-audit case](examples/self-audit-bundle-safety.md), including the reproduction, root cause, fix and verification commands.

## Design principles

1. Evidence before positioning: observed facts, inference, risk and missing decisions stay separate.
2. Type before template: a dataset needs a data card; a Skill needs trigger and behavior evidence; a portfolio needs outcomes and responsibility.
3. Goal before distribution: choose the smallest useful channel set for the user's desired result instead of applying a calendar formula.
4. Public surface before remote: review the exact staged tree, symlinks, archive contents, asset rights, claims, Git identity and unsigned visitor experience before publication.
5. Local before remote: public-risk checks and bundles are prepared locally; push, visibility, releases and external posts remain explicit handoff steps.

## Evaluation

The repository contains trigger prompts and scenario fixtures. Run:

```bash
python evals/validate_fixtures.py
```

This reports fixture and release-file checks as passed or failed; it is not a model-quality score. The published pilot comparison includes its method, complete sanitized outputs and limitations. No adoption or popularity metrics are invented.

## License

MIT. See [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before publishing a project that contains third-party material.

Built by [Weike Zhang](https://github.com/weike-zhang).
