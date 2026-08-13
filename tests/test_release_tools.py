from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "launch-github-project" / "scripts"


def load_script(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bundle = load_script("build_release_bundle")
public_surface = load_script("review_public_surface")
release_page = load_script("generate_release_page")
audit_repository = load_script("audit_repository")


class ReleaseBundleTests(unittest.TestCase):
    def test_rejects_file_symlink_that_points_outside_project(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "project"
            root.mkdir()
            (root / "README.md").write_text("safe\n", encoding="utf-8")
            outside = base / "outside.txt"
            outside.write_text("must not be archived\n", encoding="utf-8")
            (root / "outside.txt").symlink_to(outside)

            with self.assertRaisesRegex(ValueError, "symbolic link"):
                bundle.build(root, base / "release.zip")

    def test_rejects_directory_symlink_that_points_outside_project(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "project"
            root.mkdir()
            outside = base / "private"
            outside.mkdir()
            (outside / "secret.txt").write_text("must not be archived\n", encoding="utf-8")
            (root / "private").symlink_to(outside, target_is_directory=True)

            with self.assertRaisesRegex(ValueError, "symbolic link"):
                bundle.build(root, base / "release.zip")

    def test_build_is_deterministic_and_excludes_local_state(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "project"
            root.mkdir()
            (root / "README.md").write_text("hello\n", encoding="utf-8")
            (root / ".env").write_text("TOKEN=private\n", encoding="utf-8")
            installed = root / ".agents" / "skills" / "humanizer"
            installed.mkdir(parents=True)
            (installed / "SKILL.md").write_text("dependency\n", encoding="utf-8")
            (root / "skills-lock.json").write_text('{"version": 1}\n', encoding="utf-8")
            first = base / "first.zip"
            second = base / "second.zip"

            bundle.build(root, first)
            bundle.build(root, second)

            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(
                    archive.namelist(),
                    ["project/README.md", "project/skills-lock.json"],
                )


class PublicSurfaceTests(unittest.TestCase):
    def test_symbolic_link_is_a_blocker(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "project"
            root.mkdir()
            outside = base / "outside.txt"
            outside.write_text("private\n", encoding="utf-8")
            (root / "outside.txt").symlink_to(outside)

            result = public_surface.scan(root)

            self.assertEqual(result["blocker_count"], 1)
            self.assertEqual(result["blockers"][0]["category"], "symbolic_link")

    def test_installed_project_skill_is_not_scanned_as_project_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installed = root / ".agents" / "skills" / "launch-github-project"
            installed.mkdir(parents=True)
            (root / "README.md").write_text("A small CLI.\n", encoding="utf-8")
            (installed / "rules.md").write_text(
                "Before public "
                "release this must be confirmed.\n",
                encoding="utf-8",
            )

            result = public_surface.scan(root)

            self.assertEqual(result["blocker_count"], 0)

    def test_historical_release_candidate_evidence_is_not_pending_work(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "The local release candidate passed before publication.\n",
                encoding="utf-8",
            )

            result = public_surface.scan(root)

            self.assertEqual(result["blocker_count"], 0)

    def test_manufactured_chinese_punchline_is_a_warning(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.zh-CN.md").write_text(
                "别先听我吹，直接看证据。\n",
                encoding="utf-8",
            )

            result = public_surface.scan(root)

            self.assertEqual(result["warning_count"], 1)
            self.assertEqual(
                result["warnings"][0]["category"],
                "manufactured_public_copy",
            )

    def test_warns_when_an_existing_hero_is_buried_below_long_prose(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "# Example\n\n"
                + ("This paragraph explains the project before showing its visual. " * 8)
                + "\n\n![Project hero](assets/hero.png)\n",
                encoding="utf-8",
            )

            result = public_surface.scan(root)

            self.assertIn("hero_below_long_intro", {item["category"] for item in result["warnings"]})

    def test_allows_a_hero_at_the_start_of_the_readme(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                '<img src="assets/hero.png" alt="Project outcome">\n\n'
                "# Example\n\nA concise outcome.\n",
                encoding="utf-8",
            )

            result = public_surface.scan(root)

            self.assertNotIn("hero_below_long_intro", {item["category"] for item in result["warnings"]})


class AuditRepositoryTests(unittest.TestCase):
    def test_installed_skill_does_not_change_target_project_type(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installed = root / ".agents" / "skills" / "launch-github-project"
            installed.mkdir(parents=True)
            (installed / "SKILL.md").write_text("installed dependency\n", encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")

            result = audit_repository.audit(root)

            self.assertEqual(result["primary_type"], "software")


class ReleasePageTests(unittest.TestCase):
    def spec(self) -> dict[str, object]:
        return {
            "project_name": "Example Skill",
            "version": "1.2.3",
            "title": "A safer update",
            "summary": "This release closes a verified packaging defect.",
            "highlights": ["Rejects unsafe entries before reading them."],
            "install_or_update": ["npx skills add owner/example -g"],
            "verification": ["`python -m unittest` — 2 tests passed."],
            "compatibility": ["Python 3.12 verified."],
            "limitations": ["This is not a general sandbox."],
            "visuals": [
                {
                    "alt": "A release audit stopping an unsafe path",
                    "url": "https://example.com/audit-proof.png",
                    "caption": "Observed failure, blocker and corrected release state.",
                }
            ],
            "upgrade_if": ["You publish a downloadable release."],
            "defer_if": ["You only need the previous security fix."],
            "release_asset": "example-v1.2.3.zip",
        }

    def test_renders_decision_sections_from_structured_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / ".codex-plugin" / "plugin.json"
            manifest.parent.mkdir()
            manifest.write_text('{"version": "1.2.3"}\n', encoding="utf-8")

            result = release_page.render(root, self.spec())

            self.assertIn("# Example Skill v1.2.3 — A safer update", result)
            self.assertIn("## Install or update", result)
            self.assertIn("## Verification", result)
            self.assertIn("## Visual proof", result)
            self.assertIn("## Should I update?", result)
            self.assertIn("![A release audit stopping an unsafe path]", result)
            self.assertIn("## Known limitations", result)
            self.assertIn("example-v1.2.3.zip", result)

    def test_rejects_manifest_version_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / ".codex-plugin" / "plugin.json"
            manifest.parent.mkdir()
            manifest.write_text('{"version": "1.2.2"}\n', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "does not match plugin manifest"):
                release_page.render(root, self.spec())

    def test_rejects_unresolved_placeholder(self):
        with tempfile.TemporaryDirectory() as directory:
            spec = self.spec()
            spec["summary"] = "TO" + "DO: explain this release"

            with self.assertRaisesRegex(ValueError, "unresolved placeholder"):
                release_page.render(Path(directory), spec)

    def test_rejects_incomplete_visual(self):
        with tempfile.TemporaryDirectory() as directory:
            spec = self.spec()
            spec["visuals"] = [{"alt": "Proof", "url": "https://example.com/proof.png"}]

            with self.assertRaisesRegex(ValueError, "caption"):
                release_page.render(Path(directory), spec)

    def test_rejects_one_sided_upgrade_guidance(self):
        with tempfile.TemporaryDirectory() as directory:
            spec = self.spec()
            del spec["defer_if"]

            with self.assertRaisesRegex(ValueError, "provided together"):
                release_page.render(Path(directory), spec)

    def test_check_all_rejects_stale_generated_page(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_dir = root / "release"
            release_dir.mkdir()
            (release_dir / "v1.2.3.json").write_text(
                json.dumps(self.spec()), encoding="utf-8"
            )
            (release_dir / "v1.2.3.md").write_text("stale\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "generated Release page is stale"):
                release_page.check_all(root)

    def test_check_all_allows_history_but_aligns_latest_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release_dir = root / "release"
            release_dir.mkdir()
            manifest = root / ".codex-plugin" / "plugin.json"
            manifest.parent.mkdir()
            manifest.write_text('{"version": "1.2.10"}\n', encoding="utf-8")

            for version in ("1.2.9", "1.2.10"):
                spec = self.spec()
                spec["version"] = version
                spec_path = release_dir / f"v{version}.json"
                output = release_dir / f"v{version}.md"
                spec_path.write_text(json.dumps(spec), encoding="utf-8")
                output.write_text(
                    release_page.render(root, spec, validate_manifest=False),
                    encoding="utf-8",
                )

            self.assertEqual(len(release_page.check_all(root)), 2)


if __name__ == "__main__":
    unittest.main()
