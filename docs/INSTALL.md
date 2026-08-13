# Install

## Recommended

```bash
npx skills add weike-zhang/launch-github-project --skill launch-github-project -g
```

## Local checkout

From this repository's parent directory, install the local Skill checkout with the same Skills CLI:

```bash
npx skills add ./launch-github-project --skill launch-github-project -g
```

This avoids depending on a client-specific local-plugin command. You can also copy `skills/launch-github-project/` into a client's Agent Skills directory and restart the client.

## Local validation

```bash
python -m unittest discover -s tests -v
python skills/launch-github-project/scripts/audit_repository.py . --json
python skills/launch-github-project/scripts/check_secrets.py . --json
python skills/launch-github-project/scripts/check_links.py .
python skills/launch-github-project/scripts/review_public_surface.py . --strict
python evals/validate_fixtures.py
```

The release bundle rejects symbolic links and non-regular filesystem entries instead of following or silently packaging them.

The Skill only prepares local materials. It does not create or modify a GitHub repository.
