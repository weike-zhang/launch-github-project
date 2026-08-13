# Install

Verified requirements for this release:

- Node.js and `npx` for the Skills CLI install path;
- Python 3.12 for the bundled audit, Release-page and packaging scripts.

## Recommended

```bash
npx skills add weike-zhang/launch-github-project \
  --agent codex --skill launch-github-project -g -y
```

The public global command above was verified after v0.2.0 was published: Codex CLI `0.147.0-alpha.6.5` loaded the GitHub-installed Skill in a clean project and completed a first audit in a read-only sandbox. The local release candidate had already passed the same project-level path before publication. Start a new Codex task in the target project after installation, then invoke:

```text
Use $launch-github-project to audit this project for GitHub.
Start read-only. Do not edit files or perform remote actions.
```

Compare the first response with the saved [activation check](../evals/results/codex-first-audit-v0.2.0.md). Other clients and versions remain unverified unless named in the compatibility table.

For an existing global installation:

```bash
npx skills update launch-github-project -g -y
```

## Local checkout

From this repository's parent directory, install the local Skill checkout with the same Skills CLI:

```bash
npx skills add ./launch-github-project \
  --agent codex --skill launch-github-project --copy -y
```

This avoids depending on a client-specific local-plugin command. You can also copy `skills/launch-github-project/` into a client's Agent Skills directory and restart the client.

## Local validation

```bash
python3 -m unittest discover -s tests -v
python3 skills/launch-github-project/scripts/audit_repository.py . --json
python3 skills/launch-github-project/scripts/check_secrets.py . --json
python3 skills/launch-github-project/scripts/check_links.py .
python3 skills/launch-github-project/scripts/review_public_surface.py . --strict
python3 skills/launch-github-project/scripts/generate_release_page.py . --check-all
python3 evals/validate_fixtures.py
```

The release bundle rejects symbolic links and non-regular filesystem entries instead of following or silently packaging them.

The Skill is local-first and performs no remote action merely because it was installed or invoked. Repository creation, pushes, visibility changes, Releases and external posts require an exact target plus explicit authorization; use a dedicated GitHub workflow for those authorized actions.
