#!/usr/bin/env python3
"""Generate and validate a GitHub Release page from structured release evidence."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PLACEHOLDER = re.compile(r"(?i)(\bTODO\b|\bTBD\b|replace before (?:launch|release)|\{\{.+?\}\})")


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def require_text(data: dict[str, object], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"release spec requires non-empty text: {key}")
    if PLACEHOLDER.search(value):
        raise ValueError(f"release spec contains an unresolved placeholder: {key}")
    return value.strip()


def require_text_list(data: dict[str, object], key: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"release spec requires a non-empty list: {key}")
    items: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"release spec requires text at {key}[{index}]")
        if PLACEHOLDER.search(item):
            raise ValueError(f"release spec contains an unresolved placeholder: {key}[{index}]")
        items.append(item.strip())
    return items


def validate_versions(root: Path, version: str) -> None:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    if not manifest_path.exists():
        return
    manifest = load_json(manifest_path)
    manifest_version = manifest.get("version")
    if manifest_version != version:
        raise ValueError(
            f"release version {version!r} does not match plugin manifest {manifest_version!r}"
        )


def render(root: Path, spec: dict[str, object]) -> str:
    project_name = require_text(spec, "project_name")
    version = require_text(spec, "version")
    title = require_text(spec, "title")
    summary = require_text(spec, "summary")
    highlights = require_text_list(spec, "highlights")
    verification = require_text_list(spec, "verification")
    install = require_text_list(spec, "install_or_update")
    compatibility = require_text_list(spec, "compatibility")
    limitations = require_text_list(spec, "limitations")
    validate_versions(root, version)

    lines = [
        f"# {project_name} v{version} — {title}",
        "",
        summary,
        "",
        "## What changed",
        "",
        *(f"- {item}" for item in highlights),
        "",
        "## Install or update",
        "",
        "```bash",
        *install,
        "```",
        "",
        "## Verification",
        "",
        *(f"- {item}" for item in verification),
        "",
        "## Compatibility",
        "",
        *(f"- {item}" for item in compatibility),
        "",
        "## Known limitations",
        "",
        *(f"- {item}" for item in limitations),
        "",
    ]
    asset = spec.get("release_asset")
    if asset is not None:
        if not isinstance(asset, str) or not asset.strip() or PLACEHOLDER.search(asset):
            raise ValueError("release_asset must be non-empty text without placeholders")
        lines.extend(
            [
                "## Release asset",
                "",
                f"- `{asset.strip()}`",
                "- Verify the SHA-256 digest shown by GitHub after upload before redistributing it.",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    try:
        content = render(root, load_json(args.spec.resolve()))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))
    output = args.output.resolve()
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != content:
            parser.error(f"generated Release page is stale: {output}")
        print(f"Release page is current: {output}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(f"Created {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
