#!/usr/bin/env python3
"""Review files that would create public trust, privacy or release-hygiene problems."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


IGNORED_DIRS = {".venv", "venv", "node_modules", "dist", "build", ".next", ".cache"}
BLOCKED_NAMES = {".DS_Store", "Thumbs.db"}
BLOCKED_SUFFIXES = {".pyc", ".pyo"}
EDITOR_SUFFIXES = {".code-workspace"}
MAINTAINER_PLAN_NAMES = {
    "launch-copy.md",
    "launch-copy.zh-CN.md",
    "distribution-plan.md",
    "distribution-plan.zh-CN.md",
    "repository-metadata.md",
}
MAX_TEXT_BYTES = 2_000_000
TEXT_RULE_EXEMPT_PATHS = {
    Path("skills/launch-github-project/scripts/review_public_surface.py"),
    Path("skills/launch-github-project/references/public-surface-review.md"),
    Path("skills/launch-github-project/references/repository-standard.md"),
}
TEXT_RULES = [
    (
        "pending_public_rights",
        "blocker",
        re.compile(
            r"(?i)(before (?:the first )?public (?:push|release)|must be confirmed before public|"
            r"local release candidates?|not licensed public assets?|公开\s*(?:Push|发布)前.*确认|"
            r"本地发布候选)"
        ),
    ),
    (
        "internal_generation_process",
        "warning",
        re.compile(r"(?i)(AI image-edit attempt|rejected AI (?:image )?attempt|prompt below)"),
    ),
    (
        "unresolved_public_copy",
        "warning",
        re.compile(r"(?i)(\bTODO\b|\bTBD\b|replace before (?:launch|release)|发布时应替换|中文发布文案草案)"),
    ),
    (
        "machine_specific_path",
        "blocker",
        re.compile(r"(?:/Users/[^/\s]+/|/home/[^/\s]+/|[A-Za-z]:\\Users\\[^\\\s]+\\)"),
    ),
]


def finding(severity: str, category: str, path: Path, root: Path, line: int | None = None) -> dict[str, object]:
    item: dict[str, object] = {
        "severity": severity,
        "category": category,
        "file": str(path.relative_to(root)),
    }
    if line is not None:
        item["line"] = line
    return item


def git_candidate_paths(root: Path) -> set[Path] | None:
    """Return tracked and non-ignored untracked files when root is a Git repository."""
    if not (root / ".git").exists():
        return None
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        return None
    return {Path(item.decode("utf-8")) for item in result.stdout.split(b"\0") if item}


def scan(root: Path) -> dict[str, object]:
    findings: list[dict[str, object]] = []
    root_git = root / ".git"
    candidate_paths = git_candidate_paths(root)
    for current, dirs, files in os.walk(root):
        base = Path(current)
        kept_dirs: list[str] = []
        for name in sorted(dirs):
            path = base / name
            if name == ".git":
                if path != root_git:
                    findings.append(finding("blocker", "nested_git_repository", path, root))
                continue
            if name == "__pycache__":
                relative_dir = path.relative_to(root)
                if candidate_paths is None or any(relative_dir in item.parents for item in candidate_paths):
                    findings.append(finding("blocker", "generated_cache", path, root))
                continue
            if name in IGNORED_DIRS:
                continue
            kept_dirs.append(name)
        dirs[:] = kept_dirs

        for name in sorted(files):
            path = base / name
            relative_path = path.relative_to(root)
            if candidate_paths is not None and relative_path not in candidate_paths:
                continue
            if name in BLOCKED_NAMES or path.suffix in BLOCKED_SUFFIXES:
                findings.append(finding("blocker", "generated_or_machine_file", path, root))
                continue
            if path.suffix in EDITOR_SUFFIXES:
                findings.append(finding("warning", "editor_workspace", path, root))
            if name in MAINTAINER_PLAN_NAMES:
                findings.append(finding("warning", "maintainer_only_plan", path, root))
            try:
                if path.stat().st_size > MAX_TEXT_BYTES:
                    continue
                sample = path.read_bytes()
            except OSError:
                continue
            if b"\x00" in sample:
                continue
            text = sample.decode("utf-8", errors="replace")
            if relative_path not in TEXT_RULE_EXEMPT_PATHS:
                for line_no, line in enumerate(text.splitlines(), start=1):
                    for category, severity, pattern in TEXT_RULES:
                        if pattern.search(line):
                            findings.append(finding(severity, category, path, root, line_no))
            if (
                "evals" in path.parts
                and "results" in path.parts
                and path.name.startswith("deterministic")
                and re.search(r'"score"\s*:', text)
            ):
                findings.append(finding("warning", "fixture_check_presented_as_score", path, root))

    blockers = [item for item in findings if item["severity"] == "blocker"]
    warnings = [item for item in findings if item["severity"] == "warning"]
    return {
        "root": str(root.resolve()),
        "blocker_count": len(blockers),
        "warning_count": len(warnings),
        "blockers": blockers,
        "warnings": warnings,
        "automated_gate_passed": not blockers,
        "manual_checks_required": [
            "asset rights and final reuse terms",
            "claims linked to methods and sanitized raw evidence",
            "public Git authors, contributors and history",
            "repository metadata, social preview and Release assets",
            "unsigned visitor verification after publication",
        ],
        "note": "Passing the automated gate does not complete the required manual checks.",
        "scope": "tracked and non-ignored Git candidates" if candidate_paths is not None else "all local files",
    }


def self_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / ".DS_Store").write_bytes(b"test")
        (root / "demo.code-workspace").write_text("{}", encoding="utf-8")
        (root / "README.md").write_text(
            "Before public release these are local release candidates.\n", encoding="utf-8"
        )
        result = scan(root)
        categories = {item["category"] for item in result["blockers"] + result["warnings"]}
        expected = {"generated_or_machine_file", "editor_workspace", "pending_public_rights"}
        if not expected <= categories:
            raise AssertionError(f"self-test failed: {sorted(categories)}")
    print("self-test passed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--strict", action="store_true", help="also fail when warnings remain")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.root is None or not args.root.is_dir():
        parser.error("root must be an existing directory")
    result = scan(args.root.resolve())
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Blockers: {result['blocker_count']}")
        print(f"Warnings: {result['warning_count']}")
        for item in result["blockers"] + result["warnings"]:
            location = f"{item['file']}:{item['line']}" if "line" in item else item["file"]
            print(f"{item['severity']}: {location} [{item['category']}]")
    return 1 if result["blocker_count"] or (args.strict and result["warning_count"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
