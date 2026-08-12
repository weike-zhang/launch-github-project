# Install

## Recommended

```bash
npx skills add weike-zhang/launch-github-project --skill launch-github-project -g
```

## Local checkout

From this repository's parent directory, Codex users may also install the local plugin:

```bash
codex plugin install ./launch-github-project
```

If your client does not support plugin installation, copy `skills/launch-github-project/` into its Agent Skills directory and restart the client.

## Local validation

```bash
python skills/launch-github-project/scripts/audit_repository.py . --json
python skills/launch-github-project/scripts/check_secrets.py . --json
python skills/launch-github-project/scripts/check_links.py .
python skills/launch-github-project/scripts/review_public_surface.py . --strict
python evals/validate_fixtures.py
```

The Skill only prepares local materials. It does not create or modify a GitHub repository.
