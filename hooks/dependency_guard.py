#!/usr/bin/env python3
"""Tell Codex about material Project Publisher dependency gaps."""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path


PUBLISHER_MARKERS = (
    "$project-publisher",
    "project-publisher",
    "project publisher",
    "github release",
    "github launch",
    "github 发布",
    "发布材料",
    "发布到 github",
    "项目发布",
    "项目宣发",
    "项目传播",
)
REMOTE_MARKERS = (
    "push",
    "publish",
    "release create",
    "推送",
    "发布 release",
    "发布到 github",
)


def _read_input() -> dict[str, object]:
    try:
        value = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def _plugin_root() -> Path | None:
    configured = os.environ.get("PLUGIN_ROOT") or os.environ.get("CLAUDE_PLUGIN_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    candidate = Path(__file__).resolve().parents[1]
    if (candidate / "skills" / "project-publisher" / "SKILL.md").is_file():
        return candidate
    return None


def _has_humanizer(root: Path | None, cwd: Path) -> bool:
    candidates = [
        cwd / ".agents" / "skills" / "humanizer" / "SKILL.md",
        Path.home() / ".agents" / "skills" / "humanizer" / "SKILL.md",
    ]
    if root is not None:
        candidates.insert(0, root / "skills" / "humanizer" / "SKILL.md")
    return any(path.is_file() for path in candidates)


def dependency_context(prompt: str, cwd: Path) -> str | None:
    normalized = prompt.casefold()
    if not any(marker in normalized for marker in PUBLISHER_MARKERS):
        return None

    gaps: list[str] = []
    if not _has_humanizer(_plugin_root(), cwd):
        gaps.append(
            "Humanizer is not available. Before rewriting public prose, tell the user that "
            "the Humanizer pass cannot run, then use the documented manual copy checks."
        )
    if shutil.which("python3") is None:
        gaps.append(
            "python3 is unavailable. Before running a bundled audit or packaging script, "
            "tell the user which check is blocked and do not report it as passed."
        )
    if shutil.which("git") is None:
        gaps.append(
            "git is unavailable. Before relying on repository history or release alignment, "
            "tell the user that those checks are blocked."
        )
    if any(marker in normalized for marker in REMOTE_MARKERS) and shutil.which("gh") is None:
        gaps.append(
            "GitHub CLI is unavailable. Before an authorized remote mutation, verify that an "
            "active GitHub connector or publishing Skill is callable; otherwise tell the user "
            "and hand off exact manual steps."
        )
    if not gaps:
        return None
    return "Project Publisher dependency guard: " + " ".join(gaps)


def main() -> int:
    payload = _read_input()
    prompt = str(payload.get("prompt", ""))
    cwd_value = payload.get("cwd")
    cwd = Path(str(cwd_value)).expanduser() if cwd_value else Path.cwd()
    context = dependency_context(prompt, cwd)
    if context:
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "UserPromptSubmit",
                        "additionalContext": context,
                    }
                },
                ensure_ascii=False,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
