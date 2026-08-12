#!/usr/bin/env python3
"""Scan text files for secret and privacy patterns without printing matched values."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

IGNORED_DIRS = {".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__", ".next", ".cache"}
MAX_FILE_BYTES = 2_000_000
PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(r"\bgh[opusr]_[A-Za-z0-9]{20,}\b"),
    "openai_style_key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "generic_secret_assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}"
    ),
    "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "cn_phone_number": re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)"),
    "cn_id_like": re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\d)"),
}


def text_files(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS)
        for name in sorted(files):
            path = Path(current) / name
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    continue
                sample = path.read_bytes()[:4096]
            except OSError:
                continue
            if b"\x00" in sample:
                continue
            yield path


def scan(root: Path) -> dict[str, object]:
    findings: list[dict[str, object]] = []
    files_scanned = 0
    for path in text_files(root):
        files_scanned += 1
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line_no, line in enumerate(lines, start=1):
            for kind, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append({"file": str(path.relative_to(root)), "line": line_no, "type": kind})
    return {
        "root": str(root.resolve()),
        "files_scanned": files_scanned,
        "finding_count": len(findings),
        "findings": findings,
        "safe_to_publish": not findings,
        "note": "Pattern matches require human review. Matched values are intentionally redacted.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f"not a directory: {args.root}")
    result = scan(args.root)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Files scanned: {result['files_scanned']}")
        print(f"Findings: {result['finding_count']}")
        for item in result["findings"]:
            print(f"{item['file']}:{item['line']} [{item['type']}]")
    return 0 if result["safe_to_publish"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
