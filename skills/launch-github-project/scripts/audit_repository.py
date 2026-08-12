#!/usr/bin/env python3
"""Read-only GitHub release-readiness and project-type signal audit."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from collections import Counter
from pathlib import Path

IGNORED_DIRS = {".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__", ".next", ".cache"}
TYPE_SIGNALS = {
    "agent-skill": {"SKILL.md", ".codex-plugin", ".claude-plugin"},
    "software": {"pyproject.toml", "package.json", "Cargo.toml", "go.mod", "requirements.txt", "Dockerfile"},
    "dataset": {"data", "dataset", "datasheet.md", "data-card.md", "schema.json", "schema.csv"},
    "course-docs": {"lessons", "course", "curriculum.md", "study-guide.md", "docs"},
    "research": {"paper.md", "methodology.md", "experiments", "notebooks", "citation.cff"},
    "design-resource": {"figma", "tokens.json", "design-tokens.json", "assets", "components"},
    "content": {"articles", "posts", "content", "bibliography.md"},
    "portfolio": {"case-studies", "portfolio", "projects"},
}


def iter_paths(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS)
        base = Path(current)
        for name in sorted(dirs):
            yield (base / name).relative_to(root), True
        for name in sorted(files):
            yield (base / name).relative_to(root), False


def git_status(root: Path) -> dict[str, object]:
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "status", "--short", "--branch"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return {"is_git_repository": False, "status": []}
    if proc.returncode != 0:
        return {"is_git_repository": False, "status": []}
    lines = proc.stdout.splitlines()
    return {"is_git_repository": True, "status": lines[:200], "status_truncated": len(lines) > 200}


def audit(root: Path) -> dict[str, object]:
    entries = list(iter_paths(root))
    normalized = {str(path).lower() for path, _ in entries}
    basenames = {path.name.lower() for path, _ in entries}
    scores: Counter[str] = Counter()
    evidence: dict[str, list[str]] = {key: [] for key in TYPE_SIGNALS}
    for project_type, signals in TYPE_SIGNALS.items():
        for signal in signals:
            signal_lower = signal.lower()
            matches = sorted(p for p in normalized if p == signal_lower or p.endswith("/" + signal_lower) or Path(p).name == signal_lower)
            if matches:
                scores[project_type] += min(3, len(matches))
                evidence[project_type].extend(matches[:5])

    ranked = [
        {"type": project_type, "score": score, "evidence": sorted(set(evidence[project_type]))}
        for project_type, score in scores.most_common()
    ]
    primary = ranked[0]["type"] if ranked else "general"
    public_files = {
        "readme": any(name.startswith("readme") for name in basenames),
        "license": any(name.startswith("license") or name == "copying" for name in basenames),
        "contributing": "contributing.md" in basenames,
        "security": "security.md" in basenames,
        "changelog": any(name.startswith("changelog") for name in basenames),
        "gitignore": ".gitignore" in basenames,
    }
    return {
        "root": str(root.resolve()),
        "primary_type": primary,
        "type_ranking": ranked,
        "public_files": public_files,
        "entry_count": len(entries),
        "git": git_status(root),
        "notes": [
            "Classification is a file-signal inference and must be checked against intended use.",
            "This audit does not prove license ownership, privacy safety, link validity, or runtime behavior.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f"not a directory: {args.root}")
    result = audit(args.root)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Primary type: {result['primary_type']}")
        print(f"Entries inspected: {result['entry_count']}")
        for key, present in result["public_files"].items():
            print(f"{key}: {'present' if present else 'missing'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
