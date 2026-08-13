from __future__ import annotations

import importlib.util
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
            first = base / "first.zip"
            second = base / "second.zip"

            bundle.build(root, first)
            bundle.build(root, second)

            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(archive.namelist(), ["project/README.md"])


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


if __name__ == "__main__":
    unittest.main()
