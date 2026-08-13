# Public install verification for v0.3.0

Date: 2026-08-13. Repository: `weike-zhang/project-publisher`. Scope: public default branch after the repository rename, tested from temporary clean directories.

## Public clone and integrated installer

```bash
git clone --depth 1 https://github.com/weike-zhang/project-publisher.git project-publisher
python3 project-publisher/scripts/install.py --home <temporary-home> --json
```

Observed result:

- `project-publisher`: installed;
- bundled `humanizer`: installed;
- Python 3.10.11 and Git: available;
- dependency guard: `installed_pending_trust`;
- overall result: `ready_pending_hook_trust`;
- errors: none.

The temporary home kept this verification separate from the user's real Skills and Hook configuration. `installed_pending_trust` means the files and Hook configuration were created; it does not mean Codex trusted the Hook automatically.

## Public Skills CLI discovery

```bash
npx -y skills@latest add weike-zhang/project-publisher \
  --agent codex --skill project-publisher humanizer --copy -y
```

The CLI found both Skills and copied them to a clean project's `.agents/skills/` directory. Both `project-publisher/SKILL.md` and `humanizer/SKILL.md` were present after installation.

This verifies repository discovery and installation. It does not prove Hook trust, model behavior, adoption or compatibility with other Agent Skills hosts.
