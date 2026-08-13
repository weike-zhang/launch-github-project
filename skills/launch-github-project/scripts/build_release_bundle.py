#!/usr/bin/env python3
"""Build a deterministic, safety-filtered ZIP of a project directory."""

from __future__ import annotations

import argparse
import json
import os
import stat
import zipfile
from pathlib import Path

EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".cache", ".next",
    ".grounded-ai-mentor", ".launch-github-project", "dist", "build",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".private.md", ".local.md"}
EXCLUDED_NAMES = {".DS_Store", ".env", ".env.local", ".env.production", "mascot-source.png"}
EXCLUDED_PATHS = {("evals", "results", "runs")}


def include(path: Path, root: Path, output: Path) -> bool:
    rel = path.relative_to(root)
    if path.resolve() == output.resolve():
        return False
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if any(tuple(rel.parts[: len(prefix)]) == prefix for prefix in EXCLUDED_PATHS):
        return False
    if path.name in EXCLUDED_NAMES:
        return False
    return not any(path.name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES)


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def collect(root: Path, output: Path) -> list[Path]:
    files: list[Path] = []
    unsafe_entries: list[str] = []
    for current, dirs, names in os.walk(root):
        base = Path(current)
        kept_dirs: list[str] = []
        for name in sorted(dirs):
            path = base / name
            if name in EXCLUDED_DIRS:
                continue
            if path.is_symlink():
                unsafe_entries.append(f"symbolic link: {path.relative_to(root)}")
                continue
            kept_dirs.append(name)
        dirs[:] = kept_dirs
        for name in sorted(names):
            path = base / name
            if not include(path, root, output):
                continue
            if path.is_symlink():
                unsafe_entries.append(f"symbolic link: {path.relative_to(root)}")
                continue
            try:
                mode = path.lstat().st_mode
            except OSError as error:
                unsafe_entries.append(f"unreadable entry: {path.relative_to(root)} ({error})")
                continue
            if not stat.S_ISREG(mode):
                unsafe_entries.append(f"non-regular file: {path.relative_to(root)}")
                continue
            if not is_within(path, root):
                unsafe_entries.append(f"path outside root: {path.relative_to(root)}")
                continue
            files.append(path)
    if unsafe_entries:
        preview = "; ".join(unsafe_entries[:10])
        if len(unsafe_entries) > 10:
            preview += f"; and {len(unsafe_entries) - 10} more"
        raise ValueError(f"refusing to bundle unsafe filesystem entries: {preview}")
    return files


def build(root: Path, output: Path) -> dict[str, object]:
    if output.exists() and output.is_dir():
        raise ValueError(f"output must be a ZIP file, not a directory: {output}")
    if is_within(output, root):
        raise ValueError("output must be outside the project root to keep bundles reproducible")
    files = collect(root, output)
    output.parent.mkdir(parents=True, exist_ok=True)
    top = root.name
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            arcname = Path(top) / path.relative_to(root)
            info = zipfile.ZipInfo(str(arcname), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if os.access(path, os.X_OK) else 0o644) << 16
            archive.writestr(info, path.read_bytes())
    return {"root": str(root.resolve()), "output": str(output.resolve()), "file_count": len(files), "bytes": output.stat().st_size}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f"not a directory: {args.root}")
    try:
        result = build(args.root.resolve(), args.output.resolve())
    except ValueError as error:
        parser.error(str(error))
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Created {result['output']} with {result['file_count']} files ({result['bytes']} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
