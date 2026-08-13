#!/usr/bin/env python3
"""Install Project Publisher, its companion Skill and dependency guard."""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "runtime" / "dependencies.json"
HOOK_COMMAND_MARKER = "project-publisher/hooks/dependency_guard.py"


def _same_tree(left: Path, right: Path) -> bool:
    comparison = filecmp.dircmp(left, right, ignore=["__pycache__", ".DS_Store"])
    if comparison.left_only or comparison.right_only or comparison.funny_files:
        return False
    if any(not filecmp.cmp(left / name, right / name, shallow=False) for name in comparison.common_files):
        return False
    return all(_same_tree(left / name, right / name) for name in comparison.common_dirs)


def _replace_skill(source: Path, target: Path, mode: str, allow_replace: bool) -> str:
    if target.is_symlink() and target.resolve() == source.resolve() and mode == "link":
        return "already_linked"
    if target.is_dir() and not target.is_symlink() and mode == "copy" and _same_tree(source, target):
        return "already_copied"
    if target.exists() or target.is_symlink():
        if not allow_replace:
            raise FileExistsError(f"refusing to replace existing installation: {target}")
        backup = target.with_name(f"{target.name}.backup-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}")
        if backup.exists() or backup.is_symlink():
            raise FileExistsError(f"backup path already exists: {backup}")
        target.replace(backup)
    target.parent.mkdir(parents=True, exist_ok=True)
    if mode == "link":
        target.symlink_to(source, target_is_directory=True)
    else:
        staging = Path(tempfile.mkdtemp(prefix=f".{target.name}-", dir=target.parent))
        shutil.rmtree(staging)
        shutil.copytree(source, staging, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
        staging.replace(target)
    return "installed"


def _hook_group(command: str) -> dict[str, object]:
    return {
        "hooks": [
            {
                "type": "command",
                "command": command,
                "timeout": 5,
                "statusMessage": "Checking Project Publisher dependencies",
            }
        ]
    }


def _install_hook(home: Path, source: Path, mode: str, allow_replace: bool) -> dict[str, str]:
    runtime_root = home / ".codex" / "project-publisher"
    hook_target = runtime_root / "hooks" / "dependency_guard.py"
    hook_target.parent.mkdir(parents=True, exist_ok=True)
    if hook_target.exists() or hook_target.is_symlink():
        same_link = hook_target.is_symlink() and hook_target.resolve() == source.resolve()
        same_file = hook_target.is_file() and filecmp.cmp(source, hook_target, shallow=False)
        if not (same_link if mode == "link" else same_file):
            if not allow_replace:
                raise FileExistsError(f"refusing to replace existing hook: {hook_target}")
            hook_target.unlink()
    if not hook_target.exists():
        if mode == "link":
            hook_target.symlink_to(source)
        else:
            shutil.copy2(source, hook_target)

    hooks_path = home / ".codex" / "hooks.json"
    hooks_path.parent.mkdir(parents=True, exist_ok=True)
    if hooks_path.exists():
        config = json.loads(hooks_path.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError(f"hook configuration must be an object: {hooks_path}")
    else:
        config = {"description": "User lifecycle hooks.", "hooks": {}}
    hooks = config.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError(f"hooks field must be an object: {hooks_path}")
    groups = hooks.setdefault("UserPromptSubmit", [])
    if not isinstance(groups, list):
        raise ValueError(f"UserPromptSubmit hooks must be a list: {hooks_path}")
    command = f'python3 "{hook_target}"'
    present = any(HOOK_COMMAND_MARKER in json.dumps(group) for group in groups)
    if not present:
        groups.append(_hook_group(command))
        if hooks_path.exists():
            backup = hooks_path.with_suffix(".json.pre-launch-backup")
            if not backup.exists():
                shutil.copy2(hooks_path, backup)
        temporary = hooks_path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(hooks_path)
    return {
        "status": "installed_pending_trust",
        "path": str(hook_target),
        "config": str(hooks_path),
    }


def _tool_status(manifest: dict[str, object]) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for item in manifest.get("tools", []):
        if not isinstance(item, dict):
            continue
        commands = [str(value) for value in item.get("commands", [])]
        found = next((shutil.which(command) for command in commands if shutil.which(command)), None)
        version = None
        compatible = True
        minimum = item.get("minimumVersion")
        if found and minimum:
            completed = subprocess.run(
                [found, "--version"],
                check=False,
                capture_output=True,
                text=True,
            )
            version_text = (completed.stdout or completed.stderr).strip()
            parts = version_text.split()
            version = parts[-1] if parts else None
            try:
                actual_tuple = tuple(int(value) for value in str(version).split(".")[:2])
                minimum_tuple = tuple(int(value) for value in str(minimum).split(".")[:2])
                compatible = actual_tuple >= minimum_tuple
            except ValueError:
                compatible = False
        result[str(item["id"])] = {
            "status": "available" if found and compatible else "incompatible" if found else "missing",
            "required": bool(item.get("required")),
            "path": found,
            "version": version,
            "minimumVersion": minimum,
            "neededWhen": item.get("neededWhen"),
            "alternatives": item.get("alternatives", []),
        }
    return result


def install(args: argparse.Namespace) -> tuple[int, dict[str, object]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    home = args.home.expanduser().resolve()
    skill_root = home / ".agents" / "skills"
    state: dict[str, object] = {
        "schemaVersion": 1,
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "mode": args.mode,
        "skills": {},
        "tools": _tool_status(manifest),
        "hook": {"status": "not_attempted"},
    }
    errors: list[str] = []
    for item in manifest["skills"]:
        name = item["id"]
        source = ROOT / item["source"]
        target = skill_root / name
        try:
            status = _replace_skill(source, target, args.mode, args.yes)
            state["skills"][name] = {"status": status, "path": str(target)}
        except (OSError, ValueError) as exc:
            state["skills"][name] = {"status": "failed", "error": str(exc), "path": str(target)}
            errors.append(f"{name}: {exc}")

    if args.with_hook:
        try:
            state["hook"] = _install_hook(
                home,
                ROOT / manifest["hook"]["source"],
                args.mode,
                args.yes,
            )
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            state["hook"] = {"status": "failed", "error": str(exc)}
            errors.append(f"dependency-guard: {exc}")
    else:
        state["hook"] = {
            "status": "declined",
            "impact": "The main Skill must surface dependency gaps without Hook assistance.",
        }

    required_missing = [
        name
        for name, item in state["tools"].items()
        if item["required"] and item["status"] != "available"
    ]
    errors.extend(f"required tool missing: {name}" for name in required_missing)
    state["result"] = "failed" if errors else "ready_pending_hook_trust" if args.with_hook else "ready_without_hook"
    state["errors"] = errors

    state_path = home / ".codex" / "project-publisher" / "install-state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state["statePath"] = str(state_path)
    return (1 if errors else 0), state


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Project Publisher, Humanizer and the dependency guard, then verify required tools."
    )
    parser.add_argument("--mode", choices=("copy", "link"), default="copy")
    parser.add_argument("--without-hook", dest="with_hook", action="store_false")
    parser.add_argument("--yes", action="store_true", help="replace an existing different installation")
    parser.add_argument("--json", action="store_true", help="print the machine-readable install state")
    parser.add_argument("--home", type=Path, default=Path.home(), help=argparse.SUPPRESS)
    parser.set_defaults(with_hook=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    code, state = install(args)
    if args.json:
        print(json.dumps(state, ensure_ascii=False, indent=2))
    else:
        print(f"Project Publisher install result: {state['result']}")
        for name, item in state["skills"].items():
            print(f"- Skill {name}: {item['status']}")
        for name, item in state["tools"].items():
            print(f"- Tool {name}: {item['status']}")
        print(f"- Hook dependency-guard: {state['hook']['status']}")
        if state["hook"]["status"] == "installed_pending_trust":
            print("Open /hooks in Codex, review dependency-guard, and trust it before relying on it.")
        for error in state["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Install state: {state['statePath']}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
