from __future__ import annotations

import json
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

        self.assertEqual(re.findall(r"^## (.+)$", english, flags=re.MULTILINE)[0], "A real failure it caught")
        self.assertEqual(re.findall(r"^## (.+)$", chinese, flags=re.MULTILINE)[0], "一次自审发现的越界打包漏洞")
        self.assertIn("assets/hero.png", english)
        self.assertIn("assets/audit-proof.png", english)
        self.assertIn("assets/hero.zh-CN.png", chinese)
        self.assertIn("assets/audit-proof.zh-CN.png", chinese)
        for text in (english, chinese):
            self.assertIn("$launch-github-project", text)
            self.assertIn("examples/self-audit-bundle-safety.md", text)
            self.assertIn("evals/results/model-comparison.md", text)
            self.assertIn("SECURITY.md", text)
            self.assertRegex(text, r"(?i)(compatibility|兼容性)")
            self.assertRegex(text, r"(?i)(permissions and limits|权限与限制)")

    def test_readmes_put_the_existing_hero_before_long_prose(self):
        english = self.read("README.md")
        chinese = self.read("README.zh-CN.md")

        for text, hero in (
            (english, 'src="assets/hero.png"'),
            (chinese, 'src="assets/hero.zh-CN.png"'),
        ):
            self.assertLess(text.index(hero), text.index("```bash"))
            opening = text.split("```bash", 1)[0]
            self.assertEqual(opening.count("<img "), 4)
            self.assertLess(opening.index("<strong>"), opening.index("<a href="))

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
        self.assertIn("Other Agent Skills hosts", readme)

    def test_public_visuals_are_shipped_pngs(self):
        for relative in (
            "assets/hero.png",
            "assets/hero.zh-CN.png",
            "assets/social-preview.png",
            "assets/audit-proof.png",
            "assets/audit-proof.zh-CN.png",
            "assets/activation-proof.png",
            "assets/hero-art.png",
        ):
            data = (ROOT / relative).read_bytes()
            self.assertGreater(len(data), 10_000, relative)
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n", relative)

    def test_install_docs_keep_remote_actions_behind_authorization(self):
        english = self.read("docs/INSTALL.md")
        chinese = self.read("docs/INSTALL.zh-CN.md")

        self.assertIn("explicit authorization", english)
        self.assertIn("明确授权", chinese)
        self.assertNotIn("only prepares local materials", english)
        self.assertNotIn("只准备本地发布材料", chinese)

    def test_chinese_readme_rejects_translationese_and_manufactured_punchlines(self):
        chinese = self.read("README.zh-CN.md")
        stale_phrases = [
            (
                "不代表陌生人来到 GitHub 后"
                "能看懂、敢信、会用"
            ),
            (
                "陌生访客"
                "能看懂、能试用、能验证"
            ),
            "可理解、" + "可试用、可验证",
            "别让一个能打的项目",
            "别先听我吹",
            "不是讲概念",
            "回归测试把修复钉死",
            "哪些绝不吹",
            "想贡献？别夸",
        ]
        for phrase in stale_phrases:
            self.assertNotIn(phrase, chinese)
        opening = chinese.split("```bash", 1)[0]
        self.assertIn("代码写完了，发布页却还没收尾", opening)
        self.assertIn("找不到入口就走了", opening)
        prose = [
            part
            for part in chinese.split("\n\n")
            if "\n" not in part and not part.startswith(("<", "```", "|", "#"))
        ]
        self.assertLessEqual(max(map(len, prose)), 240)

    def test_humanizer_is_locked_and_used_as_a_bounded_copy_pass(self):
        lock = json.loads(self.read("skills-lock.json"))
        skill = self.read("skills/launch-github-project/SKILL.md")
        patterns = self.read("skills/launch-github-project/references/readme-patterns.md")

        self.assertEqual(lock["skills"]["humanizer"]["source"], "blader/humanizer")
        self.assertIn("$humanizer", skill)
        self.assertIn("Preserve commands, links, version numbers", skill)
        self.assertIn("never authorizes invented facts", patterns)

    def test_visible_image_copy_rejects_framework_slogans(self):
        source = self.read("scripts/build_visuals.py")
        stale = [
            "RELEASE WITH EVIDENCE",
            'draw.text((90, 540), "AUDIT"',
            'draw.text((224, 540), "PROVE"',
            'draw.text((362, 540), "PACKAGE"',
            'draw.text((528, 540), "VERIFY"',
            "别让好项目死在发布页",
            "让人看懂、试得动、查得到证据",
            "先审项目 · 再拿证据",
            "不是演示：它真抓到过",
            "BEFORE · NOISY",
            "AFTER · SIGNAL",
        ]
        for phrase in stale:
            self.assertNotIn(phrase, source)


if __name__ == "__main__":
    unittest.main()
