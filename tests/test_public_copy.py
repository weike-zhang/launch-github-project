from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicCopyContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_readmes_lead_to_first_success_and_direct_evidence(self):
        english = self.read("README.md")
        chinese = self.read("README.zh-CN.md")

        self.assertEqual(re.findall(r"^## (.+)$", english, flags=re.MULTILINE)[0], "Install and invoke")
        self.assertEqual(re.findall(r"^## (.+)$", chinese, flags=re.MULTILINE)[0], "安装并调用")
        for text in (english, chinese):
            self.assertIn("$launch-github-project", text)
            self.assertIn("examples/self-audit-bundle-safety.md", text)
            self.assertIn("evals/results/model-comparison.md", text)
            self.assertIn("SECURITY.md", text)
            self.assertRegex(text, r"(?i)(compatibility|兼容性)")
            self.assertRegex(text, r"(?i)(permissions and limits|权限与限制)")

    def test_public_guide_contains_no_author_profile_setup_draft(self):
        guide = self.read("docs/FIRST-GITHUB-LAUNCH.zh-CN.md")
        stale_markers = [
            "mumian" + "wei",
            "你已经决定" + "使用展示名",
            (
                "计划把"
                "登录名改成"
            ),
            "建议资料" + "先采用",
        ]
        for marker in stale_markers:
            self.assertNotIn(marker, guide)
        self.assertIn("<owner>/<repository>", guide)
        self.assertIn("generate_release_page.py", guide)
        self.assertIn("并非所有项目都需要 GitHub Release", guide)
        self.assertIn("普通目标项目里不会自动出现这组路径", guide)
        self.assertIn("gh release create", guide)
        self.assertIn("<default-branch>", guide)

    def test_pilot_publishes_exact_input_and_bounds_the_claim(self):
        readme = self.read("README.md")
        comparison = self.read("evals/results/model-comparison.md")

        self.assertIn("## Exact prompt", comparison)
        self.assertIn("Do not use a day-by-day calendar", comparison)
        self.assertNotIn("Complete distribution pilot", readme)
        self.assertIn("host-level behavior is not yet claimed as broadly verified", readme)

    def test_install_docs_keep_remote_actions_behind_authorization(self):
        english = self.read("docs/INSTALL.md")
        chinese = self.read("docs/INSTALL.zh-CN.md")

        self.assertIn("explicit authorization", english)
        self.assertIn("明确授权", chinese)
        self.assertNotIn("only prepares local materials", english)
        self.assertNotIn("只准备本地发布材料", chinese)


if __name__ == "__main__":
    unittest.main()
