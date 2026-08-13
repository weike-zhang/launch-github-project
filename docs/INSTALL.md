# Install

Verified requirements for this release:

- Git to download and inspect repositories;
- Python 3.10 or newer for the integrated installer and bundled audit, Release-page and packaging scripts;
- Node.js and `npx` only for the Skills-only alternative.

## Recommended

The commands below become public after the authorized repository rename to `project-publisher`. Until then, use the current local checkout; the new remote path is not claimed as published.

```bash
git clone https://github.com/weike-zhang/project-publisher.git
python3 project-publisher/scripts/install.py
```

This integrated path installs Project Publisher and its bundled Humanizer companion together, verifies the required command-line tools, installs the dependency-guard Hook, and records every component state. Open `/hooks` in Codex after installation, review `dependency-guard`, and trust it if you accept its source. Codex does not allow an installer to grant that trust for you.

Project Publisher invokes Humanizer only after the factual draft is stable, using file or embedded mode. The main Skill rechecks dependencies at the stage where they are needed. If installation failed, the user declined the Hook, or the active host does not expose a companion, Project Publisher must report the affected proof and fallback instead of silently skipping it.

The integrated path is verified from the current local candidate and its extracted Release ZIP: both Skills installed, required tools passed preflight, the Hook was registered as pending trust, and a second run remained idempotent. It is not a publicly released path until the next version is published. The previous Skills-only v0.2.0 path was verified after publication with Codex CLI `0.147.0-alpha.6.5` in a clean project. Start a new Codex task in the target project after installation, then invoke:

```text
Use $project-publisher to review this project before I publish or update it.
Start read-only. Tell me the biggest reason a new visitor may not understand or
try it. Do not edit files or perform remote actions.
```

Compare the first response with the saved [activation check](../evals/results/codex-first-audit-v0.2.0.md). Other clients and versions remain unverified unless named in the compatibility table.

For an existing checkout, update and replace only the managed Project Publisher components:

```bash
git -C project-publisher pull --ff-only
python3 project-publisher/scripts/install.py --yes
```

The installer preserves a timestamped backup before replacing a different Skill installation. Its state is written to `~/.codex/project-publisher/install-state.json`.

## Skills-only alternative

```bash
npx skills add weike-zhang/project-publisher \
  --agent codex --skill project-publisher humanizer -g -y
```

This installs both Skills but does not install the dependency-guard Hook or run the integrated tool preflight. Use it only when the host or administrator manages Hooks separately.

## Local checkout

For continuous local development, link both Skills and the Hook to this checkout:

```bash
python3 scripts/install.py --mode link --yes
```

Edits in the checkout are then visible to new Codex tasks without reinstalling. Changed Hooks still require review because Codex binds trust to the current Hook definition.

## Local validation

```bash
python3 -m unittest discover -s tests -v
python3 skills/project-publisher/scripts/audit_repository.py . --json
python3 skills/project-publisher/scripts/check_secrets.py . --json
python3 skills/project-publisher/scripts/check_links.py .
python3 skills/project-publisher/scripts/review_public_surface.py . --strict
python3 skills/project-publisher/scripts/generate_release_page.py . --check-all
python3 evals/validate_fixtures.py
```

The release bundle rejects symbolic links and non-regular filesystem entries instead of following or silently packaging them.

The Skill is local-first and performs no remote action merely because it was installed or invoked. Repository creation, pushes, visibility changes, Releases and external posts require an exact target plus explicit authorization; use a dedicated GitHub workflow for those authorized actions.
