<div align="center">
  <img src="assets/hero.png" alt="Launch GitHub Project — prepare any project for a safe, evidence-based launch" width="100%">

# Launch GitHub Project

**A goal-driven release workflow for projects of any type.**

[简体中文](README.zh-CN.md) · [Install](docs/INSTALL.md) · [First GitHub launch guide](docs/FIRST-GITHUB-LAUNCH.zh-CN.md)

</div>

Most launch advice assumes a software product. This Skill starts with what exists, classifies the project, and creates only the release surface that its type and evidence justify.

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

From the repository root, run the local gates against a target project:

```bash
python skills/launch-github-project/scripts/audit_repository.py ../target-project --json
python skills/launch-github-project/scripts/check_secrets.py ../target-project --json
python skills/launch-github-project/scripts/check_links.py ../target-project
python skills/launch-github-project/scripts/review_public_surface.py ../target-project --strict
python skills/launch-github-project/scripts/build_release_bundle.py ../target-project --output /tmp/project-release.zip
```

Then invoke the Skill in a compatible client:

```text
Use $launch-github-project to prepare this project for GitHub. Start read-only,
classify the project, ask only grouped questions when a decision changes the
artifacts, and do not publish remotely without my explicit approval.
```

## Design principles

1. Evidence before positioning: observed facts, inference, risk and missing decisions stay separate.
2. Type before template: a dataset needs a data card; a Skill needs trigger and behavior evidence; a portfolio needs outcomes and responsibility.
3. Goal before distribution: choose the smallest useful channel set for the user's desired result instead of applying a calendar formula.
4. Public surface before remote: review the exact staged tree, archive contents, asset rights, claims, Git identity and unsigned visitor experience before publication.
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
