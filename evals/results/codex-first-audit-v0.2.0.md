# Codex first-audit activation check

Status: **one verified host and public-install path; not broad compatibility evidence**.

## Post-publication check

After GitHub Release v0.2.0 was published on 2026-08-13, the public repository install path was tested separately from the local candidate:

```bash
npx skills@latest add weike-zhang/launch-github-project \
  --agent codex --skill launch-github-project --copy -g -y

codex exec --ephemeral --sandbox read-only --skip-git-repo-check \
  -C /tmp/launch-v020-public-global-test \
  'Use $launch-github-project to audit this repository for a first public GitHub launch. Do not edit files or use remote-write operations.'
```

The fixture contained only `README.md`, `notes.py` and an example `LICENSE`; it had no project-level Skill that could shadow the global install. Codex loaded `launch-github-project` from the global Skills directory, ran the bundled scanners, exercised the CLI and returned the requested read-only audit. It correctly reported that the README promised automatic persistence while `notes.py` only printed its first argument. It also rejected the placeholder license, distinguished automated results from manual decisions, and performed no edit or remote action.

The temporary global installation was removed after the check. Host startup also printed icon warnings from unrelated installed plugins; the tested Skill metadata contains neither warned field, so those messages are not attributed to this project.

## Release-candidate check

- Date: 2026-08-13
- Host: Codex CLI `0.147.0-alpha.6.5`
- Model: `gpt-5.6-sol`
- Skill build: local `0.2.0` release candidate
- Installation: project-level copy through Skills CLI
- Execution: ephemeral Codex task with a read-only sandbox
- Fixture: a three-file Python CLI prototype with a README claim that did not match runtime behavior

## Install and invoke

```bash
npx skills add /path/to/launch-github-project \
  --agent codex --skill launch-github-project --copy -y

codex exec --ephemeral --sandbox read-only -C /path/to/fixture \
  'Use $launch-github-project to audit this project for GitHub. Start read-only. Do not edit files and do not perform remote actions.'
```

The published repository form of the install command is:

```bash
npx skills add weike-zhang/launch-github-project \
  --agent codex --skill launch-github-project -g -y
```

Start a new Codex task in the target project after installation so the host reloads its Skill catalogue.

## Sanitized observed output

```text
Primary type
Software/CLI. notes.py is the executable product.

Observed
README, MIT license and one Python script exist. Syntax is valid; the documented
add command prints a confirmation but stores nothing. The directory is not yet
a Git repository.

Public gap
No genuine persistence, tests, requirements, limitations, troubleshooting or
problem-reporting path. README provides no proof beyond one command.

Release blocker
The README's “saves text notes” claim contradicts runtime behavior. The local
install lock contains a machine-specific source path and the example copyright
holder is unresolved.

Human decisions
Implement persistence or narrow the claim; confirm the copyright holder; decide
whether local Skill metadata belongs in the public project; choose repository
identity and Git history.

Action taken
Completed a read-only audit. No files were edited, no Git repository was
initialized and no remote action was performed.
```

## What this run changed

The first run exposed a real Skill defect: project-level installed dependencies under `.agents/skills/` were initially classified and scanned as if they were the target product. Version 0.2.0 excludes nested installed-Skill directories from type inference, link checks, secret checks and public-surface scanning while still reviewing `skills-lock.json`, where a local machine path may be a genuine publication blocker.

This single activation check verifies the named Codex CLI path and the read-only first response. It does not prove compatibility with every Codex version, the desktop app or other Agent Skills hosts.
