#!/usr/bin/env python3
"""Check local links and images in Markdown files without fetching the web."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

IGNORED_DIRS = {".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__"}
INSTALLED_SKILL_DIRS = {Path(".agents/skills"), Path(".claude/skills"), Path(".codex/skills")}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def markdown_files(root: Path):
    for current, dirs, files in os.walk(root):
        base = Path(current)
        dirs[:] = sorted(
            d
            for d in dirs
            if d not in IGNORED_DIRS
            and (base / d).relative_to(root) not in INSTALLED_SKILL_DIRS
        )
        for name in sorted(files):
            path = Path(current) / name
            if not path.is_symlink() and name.lower().endswith((".md", ".mdx")):
                yield path


def target_path(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if "{{" in target or "}}" in target:
        return None
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split(maxsplit=1)[0]
    parsed = urlparse(target)
    if parsed.scheme or target.startswith("//") or target.startswith("#") or not target:
        return None
    clean = unquote(parsed.path)
    return (source.parent / clean).resolve()


def check(root: Path) -> dict[str, object]:
    broken: list[dict[str, object]] = []
    checked = 0
    for source in markdown_files(root):
        text = source.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            for match in LINK_RE.finditer(line):
                raw = match.group(1)
                resolved = target_path(source, raw)
                if resolved is None:
                    continue
                checked += 1
                if not resolved.exists():
                    broken.append(
                        {
                            "file": str(source.relative_to(root)),
                            "line": line_no,
                            "target": raw,
                        }
                    )
    return {"root": str(root.resolve()), "local_links_checked": checked, "broken": broken, "valid": not broken}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f"not a directory: {args.root}")
    result = check(args.root)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Local links checked: {result['local_links_checked']}")
        for item in result["broken"]:
            print(f"{item['file']}:{item['line']} -> {item['target']}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
