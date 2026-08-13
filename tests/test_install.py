from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_script(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load_script("scripts/install.py", "project_publisher_installer")
guard = load_script("hooks/dependency_guard.py", "project_publisher_dependency_guard")


class InstallerTests(unittest.TestCase):
    def args(self, home: Path, **changes: object):
        values = {
            "mode": "copy",
            "with_hook": True,
            "yes": False,
            "json": True,
            "home": home,
        }
        values.update(changes)
        return type("Args", (), values)()

    def test_integrated_install_copies_both_skills_and_registers_hook(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            code, state = installer.install(self.args(home))

            self.assertEqual(code, 0)
            self.assertEqual(state["result"], "ready_pending_hook_trust")
            for name in ("project-publisher", "humanizer"):
                installed = home / ".agents" / "skills" / name / "SKILL.md"
                self.assertTrue(installed.is_file(), name)
            hooks = json.loads((home / ".codex" / "hooks.json").read_text(encoding="utf-8"))
            encoded = json.dumps(hooks)
            self.assertIn("dependency_guard.py", encoded)
            self.assertEqual(encoded.count("dependency_guard.py"), 1)
            self.assertEqual(state["hook"]["status"], "installed_pending_trust")
            self.assertTrue(
                (home / ".codex" / "project-publisher" / "install-state.json").is_file()
            )

            repeat_code, repeat_state = installer.install(self.args(home))
            self.assertEqual(repeat_code, 0)
            self.assertEqual(
                repeat_state["skills"]["project-publisher"]["status"],
                "already_copied",
            )
            repeated_hooks = json.loads(
                (home / ".codex" / "hooks.json").read_text(encoding="utf-8")
            )
            self.assertEqual(json.dumps(repeated_hooks).count("dependency_guard.py"), 1)

    def test_link_mode_tracks_the_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            code, state = installer.install(self.args(home, mode="link"))

            self.assertEqual(code, 0)
            for name in ("project-publisher", "humanizer"):
                installed = home / ".agents" / "skills" / name
                self.assertTrue(installed.is_symlink(), name)
                self.assertEqual(installed.resolve(), (ROOT / "skills" / name).resolve())
            hook = Path(state["hook"]["path"])
            self.assertTrue(hook.is_symlink())
            self.assertEqual(hook.resolve(), (ROOT / "hooks" / "dependency_guard.py").resolve())

    def test_declined_hook_is_recorded_without_failing_core_install(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            code, state = installer.install(self.args(home, with_hook=False))

            self.assertEqual(code, 0)
            self.assertEqual(state["result"], "ready_without_hook")
            self.assertEqual(state["hook"]["status"], "declined")
            persisted = json.loads(
                (home / ".codex" / "project-publisher" / "install-state.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(persisted["hook"]["status"], "declined")

    def test_existing_user_hooks_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            hooks_path = home / ".codex" / "hooks.json"
            hooks_path.parent.mkdir(parents=True)
            hooks_path.write_text(
                json.dumps(
                    {
                        "description": "existing",
                        "hooks": {"SessionStart": [{"hooks": []}]},
                    }
                ),
                encoding="utf-8",
            )

            code, _ = installer.install(self.args(home))

            self.assertEqual(code, 0)
            hooks = json.loads(hooks_path.read_text(encoding="utf-8"))["hooks"]
            self.assertIn("SessionStart", hooks)
            self.assertIn("UserPromptSubmit", hooks)
            self.assertTrue(hooks_path.with_suffix(".json.pre-launch-backup").is_file())


class DependencyGuardTests(unittest.TestCase):
    def test_irrelevant_prompt_adds_no_context(self):
        self.assertIsNone(guard.dependency_context("Explain this function", Path.cwd()))

    def test_missing_companion_and_tools_are_visible_when_publication_is_needed(self):
        def missing(command: str):
            return None

        with mock.patch.object(guard, "_plugin_root", return_value=None), mock.patch.object(
            guard, "_has_humanizer", return_value=False
        ), mock.patch.object(guard.shutil, "which", side_effect=missing):
            context = guard.dependency_context(
                "Use $project-publisher and publish to GitHub",
                Path.cwd(),
            )

        self.assertIsNotNone(context)
        self.assertIn("Humanizer is not available", context)
        self.assertIn("python3 is unavailable", context)
        self.assertIn("git is unavailable", context)
        self.assertIn("GitHub CLI is unavailable", context)
        self.assertIn("tell the user", context)


if __name__ == "__main__":
    unittest.main()
