#!/usr/bin/env python3
"""Validate Launch GitHub Project fixture and release integrity."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "docs/FIRST-GITHUB-LAUNCH.zh-CN.md",
    "assets/hero.png",
    "assets/hero.zh-CN.png",
    "assets/hero-art.png",
    "assets/audit-proof.png",
    "assets/social-preview.png",
    "assets/audit-proof.zh-CN.png",
    "assets/activation-proof.png",
    "assets/ASSET-NOTICE.md",
    "assets/launch-flow.svg",
    "skills/launch-github-project/SKILL.md",
    "skills/launch-github-project/references/public-surface-review.md",
    "skills/launch-github-project/references/adoption-and-trust.md",
    "skills/launch-github-project/references/chinese-public-copy.md",
    "skills/launch-github-project/references/release-page.md",
    "skills/launch-github-project/scripts/audit_repository.py",
    "skills/launch-github-project/scripts/check_secrets.py",
    "skills/launch-github-project/scripts/check_links.py",
    "skills/launch-github-project/scripts/review_public_surface.py",
    "skills/launch-github-project/scripts/build_release_bundle.py",
    "skills/launch-github-project/scripts/generate_release_page.py",
    "skills/launch-github-project/assets/release/release-page.json",
    "tests/test_release_tools.py",
    "tests/test_public_copy.py",
    "evals/results/codex-first-audit-v0.2.0.md",
    "examples/self-audit-bundle-safety.md",
    "release/v0.1.2.json",
    "release/v0.1.2.md",
    "release/v0.2.0.json",
    "release/v0.2.0.md",
]


def main() -> int:
    with (ROOT / "evals/trigger-prompts.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    scenarios = [
        json.loads(line)
        for line in (ROOT / "evals/scenarios.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    rubric = json.loads((ROOT / "evals/rubric.json").read_text(encoding="utf-8"))
    true_count = sum(row["should_trigger"] == "true" for row in rows)
    false_count = sum(row["should_trigger"] == "false" for row in rows)
    types = {item["type"] for item in scenarios}
    checks = {
        "trigger_prompt_count": len(rows) == 24,
        "trigger_balance": true_count == 12 and false_count == 12,
        "scenario_count": len(scenarios) == 9,
        "scenario_schema": all(
            {"id", "type", "goal", "prompt", "required", "forbidden"} <= set(item)
            for item in scenarios
        ),
        "type_route_coverage": {
            "software",
            "agent-skill",
            "dataset",
            "research",
            "design-resource",
            "portfolio",
            "general",
        }
        <= types,
        "rubric_weights_sum_to_one": math.isclose(
            sum(item["weight"] for item in rubric["dimensions"]), 1.0, abs_tol=1e-9
        ),
        "required_release_files": all((ROOT / path).is_file() for path in REQUIRED_FILES),
    }
    passed = sum(checks.values())
    result = {
        "suite": "launch-github-project-fixture-integrity",
        "version": "0.2.0",
        "checks": checks,
        "passed_checks": passed,
        "total_checks": len(checks),
        "all_passed": all(checks.values()),
        "interpretation": "Structure, route coverage and release-integrity checks only; no model quality, reach or popularity is scored.",
    }
    output = ROOT / "evals/results/fixture-integrity.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
