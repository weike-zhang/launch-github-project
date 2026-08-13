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
INSTALLED_SKILL_DIRS = {Path(".agents/skills"), Path(".claude/skills"), Path(".codex/skills")}
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
    Path("skills/project-publisher/scripts/review_public_surface.py"),
    Path("skills/project-publisher/references/public-surface-review.md"),
    Path("skills/project-publisher/references/repository-standard.md"),
    Path("skills/project-publisher/references/chinese-public-copy.md"),
    Path("skills/project-publisher/references/readme-patterns.md"),
    Path("tests/test_public_copy.py"),
    Path("tests/test_release_tools.py"),
}
TEXT_RULES = [
    (
        "pending_public_rights",
        "blocker",
        re.compile(
            r"(?i)(before (?:the first )?public (?:push|release)|must be confirmed before public|"
            r"not licensed public assets?|公开\s*(?:Push|发布)前.*确认)"
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
    (
        "author_identity_setup",
        "warning",
        re.compile(
            r"(?i)(plan(?:ned)? to change (?:the )?(?:GitHub )?user(?:name|name)|"
            r"change (?:the )?GitHub user(?:name|name) before|"
            r"计划把.*登录名改成|推荐先把 GitHub 登录名改为)"
        ),
    ),
    (
        "translationese_public_copy",
        "warning",
        re.compile(
            r"(?:不代表.{0,24}(?:能|能够)看懂.{0,16}(?:敢信|信任).{0,16}会用|"
            r"陌生(?:访客|用户).{0,20}能看懂.{0,16}能试用.{0,16}能验证|"
            r"变成.{0,24}可理解.{0,16}可试用.{0,16}可验证)"
        ),
    ),
    (
        "manufactured_public_copy",
        "warning",
        re.compile(
            r"(?:别让.{0,30}死在|别先听我吹|不是讲概念[:：]|"
            r"哪些绝不吹|想贡献[?？].{0,12}别夸|代码能跑.{0,12}只是及格)"
        ),
    ),
    (
        "maintainer_first_proof_heading",
        "warning",
        re.compile(r"^(?:#{2,4})\s*(?:一次|本次).{0,12}(?:自审|审计|测试).{0,12}(?:发现|结果)", re.MULTILINE),
    ),
]
HERO_IMAGE_PATTERN = re.compile(
    r"(?:<img\b[^>]*\bsrc=[\"'](?P<html>[^\"']+)[\"'][^>]*>|"
    r"!\[[^\]]*\]\((?P<markdown>[^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\))",
    re.IGNORECASE,
)
HERO_NAME_PATTERN = re.compile(r"(?i)(?:^|[-_/])(hero|banner|cover|masthead)(?:[-_.?/]|$)")
MAX_CONTENT_BEFORE_HERO = 320
STRONG_TAGLINE_PATTERN = re.compile(r"<strong>(?P<text>.*?)</strong>", re.IGNORECASE | re.DOTALL)
METHOD_WORD_PATTERN = re.compile(
    r"(?i)(?:\b(?:audit|check|inspect|review|validate|verify|optimize)\w*\b|"
    r"检查|核对|复核|审计|验证|验一遍|优化)"
)
VISIBLE_RESULT_PATTERN = re.compile(
    r"(?i)(?:\b(?:user|reader|visitor|result|report|finding|problem|blocker|"
    r"readme|visual|install|release page|bundle|source zip|preview)\w*\b|"
    r"用户|读者|访客|帮你|拿到|得到|问题|缺口|阻断|报告|清单|"
    r"README|配图|安装|Release|发布包|文件|预览|修复)"
)


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


def find_buried_hero(text: str) -> int | None:
    """Return the line of a hero placed after a long README introduction."""
    for match in HERO_IMAGE_PATTERN.finditer(text):
        source = match.group("html") or match.group("markdown") or ""
        if not HERO_NAME_PATTERN.search(source):
            continue
        prefix = text[: match.start()]
        visible_prefix = re.sub(r"<[^>]+>|[`#*_>|\[\]()]", " ", prefix)
        visible_prefix = re.sub(r"\s+", " ", visible_prefix).strip()
        if len(visible_prefix) > MAX_CONTENT_BEFORE_HERO or "```" in prefix:
            return text.count("\n", 0, match.start()) + 1
        return None
    return None


def find_method_only_tagline(text: str) -> int | None:
    """Return the line of a centered tagline that names methods but no visible result."""
    match = STRONG_TAGLINE_PATTERN.search(text[:4000])
    if match is None:
        return None
    tagline = re.sub(r"<[^>]+>", " ", match.group("text"))
    if len(METHOD_WORD_PATTERN.findall(tagline)) < 2:
        return None
    if VISIBLE_RESULT_PATTERN.search(tagline):
        return None
    return text.count("\n", 0, match.start()) + 1


def scan(root: Path) -> dict[str, object]:
    findings: list[dict[str, object]] = []
    root_git = root / ".git"
    candidate_paths = git_candidate_paths(root)
    for current, dirs, files in os.walk(root):
        base = Path(current)
        kept_dirs: list[str] = []
        for name in sorted(dirs):
            path = base / name
            relative_dir = path.relative_to(root)
            if relative_dir in INSTALLED_SKILL_DIRS:
                continue
            if path.is_symlink():
                if candidate_paths is None or relative_dir in candidate_paths:
                    findings.append(finding("blocker", "symbolic_link", path, root))
                continue
            if name == ".git":
                if path != root_git:
                    findings.append(finding("blocker", "nested_git_repository", path, root))
                continue
            if name == "__pycache__":
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
            if path.is_symlink():
                findings.append(finding("blocker", "symbolic_link", path, root))
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
            if relative_path.parent == Path(".") and relative_path.name.lower().startswith("readme"):
                hero_line = find_buried_hero(text)
                if hero_line is not None:
                    findings.append(finding("warning", "hero_below_long_intro", path, root, hero_line))
                tagline_line = find_method_only_tagline(text)
                if tagline_line is not None:
                    findings.append(finding("warning", "method_only_tagline", path, root, tagline_line))
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
            "visual necessity plus rendered fonts, glyphs, labels and units",
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
        (root / "outside.txt").symlink_to(Path(directory).parent / "outside.txt")
        (root / "README.md").write_text(
            "<p><strong>Check the repository, validate the claims, review before launch.</strong></p>\n"
            "Before public release these are local release candidates.\n"
            "I planned to change the GitHub username before launch.\n"
            "本地能跑不代表陌生用户能看懂、敢信、会用。\n"
            "别先听我吹，直接看证据。\n"
            + ("Long introduction. " * 24)
            + "\n![Hero](assets/hero.png)\n",
            encoding="utf-8",
        )
        result = scan(root)
        categories = {item["category"] for item in result["blockers"] + result["warnings"]}
        expected = {
            "generated_or_machine_file",
            "editor_workspace",
            "pending_public_rights",
            "symbolic_link",
            "author_identity_setup",
            "translationese_public_copy",
            "manufactured_public_copy",
            "hero_below_long_intro",
            "method_only_tagline",
        }
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
