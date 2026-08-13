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

        self.assertEqual(
            re.findall(r"^## (.+)$", english, flags=re.MULTILINE)[0],
            "Keep files from outside the project out of the release ZIP",
        )
        self.assertEqual(
            re.findall(r"^## (.+)$", chinese, flags=re.MULTILINE)[0],
            "别把项目外的文件一起发出去",
        )
        self.assertIn("assets/hero.png", english)
        self.assertIn("assets/hero.zh-CN.png", chinese)
        for text in (english, chinese):
            self.assertNotIn("audit-proof", text)
            self.assertIn("outside.txt -> /etc/hosts", text)
            self.assertIn("$project-publisher", text)
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
            self.assertEqual(opening.count("<img "), 1)
            self.assertLess(opening.index("<strong>"), opening.index("<a href="))

    def test_current_readmes_keep_only_the_hero_visual(self):
        english = self.read("README.md")
        chinese = self.read("README.zh-CN.md")

        for text in (english, chinese):
            self.assertEqual(text.count("<img "), 1)
            self.assertNotRegex(text, r"!\[[^\]]*\]\([^)]+\)")
        self.assertIn("项目已经变了", chinese)
        self.assertIn("先找出最影响传播的缺口", chinese)

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
        self.assertIn("项目已经变了", opening)
        self.assertIn("先找出哪里没跟上", opening)
        self.assertIn("审查现状、梳理名字和定位", opening)
        self.assertIn("后续更新时重新对齐", opening)
        self.assertNotIn("检查仓库，核对公开主张，发布前再验一遍", opening)
        prose = [
            part
            for part in chinese.split("\n\n")
            if "\n" not in part and not part.startswith(("<", "```", "|", "#"))
        ]
        self.assertLessEqual(max(map(len, prose)), 240)

    def test_humanizer_is_locked_and_used_as_a_bounded_copy_pass(self):
        lock = json.loads(self.read("skills-lock.json"))
        skill = self.read("skills/project-publisher/SKILL.md")
        patterns = self.read("skills/project-publisher/references/readme-patterns.md")
        orchestration = self.read(
            "skills/project-publisher/references/companion-orchestration.md"
        )
        bundled = self.read("skills/humanizer/SKILL.md")
        development_path = ROOT / ".agents/skills/humanizer/SKILL.md"

        self.assertEqual(lock["skills"]["humanizer"]["source"], "blader/humanizer")
        if development_path.is_file():
            self.assertEqual(bundled, development_path.read_text(encoding="utf-8"))
        self.assertIn("$humanizer", skill)
        self.assertIn("Preserve commands, links, version numbers", skill)
        self.assertIn("never authorizes invented facts", patterns)
        self.assertIn("name-swap test", patterns)
        self.assertIn("desire to try", patterns)
        self.assertIn("natural copy can still be generic", skill)
        self.assertIn("file mode for one file or embedded mode", orchestration)
        self.assertIn("A Skill cannot call a hook like a function", orchestration)
        self.assertIn("Do not silently install or enable anything", orchestration)

    def test_install_paths_include_companions_hook_and_runtime_disclosure(self):
        for relative in ("README.md", "README.zh-CN.md"):
            text = self.read(relative)
            self.assertIn("python3 project-publisher/scripts/install.py", text)

        for relative in ("docs/INSTALL.md", "docs/INSTALL.zh-CN.md"):
            text = self.read(relative)
            self.assertIn("python3 project-publisher/scripts/install.py", text)
            self.assertRegex(text, r"--skill project-publisher humanizer")
            self.assertIn("/hooks", text)

        manifest = json.loads(self.read(".codex-plugin/plugin.json"))
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["hooks"], "./hooks/hooks.json")
        self.assertTrue((ROOT / "skills/humanizer/SKILL.md").is_file())
        self.assertTrue((ROOT / "skills/project-publisher/SKILL.md").is_file())

        skill = self.read("skills/project-publisher/SKILL.md")
        orchestration = self.read(
            "skills/project-publisher/references/companion-orchestration.md"
        )
        self.assertIn("Never silently omit a companion pass", skill)
        self.assertIn("installed_pending_trust", orchestration)
        self.assertIn("failed, declined, disabled or untrusted", skill)

    def test_agent_skill_template_requires_a_product_specific_first_result(self):
        template = self.read("skills/project-publisher/assets/readme/agent-skill.md")
        public_review = self.read(
            "skills/project-publisher/references/public-surface-review.md"
        )

        self.assertIn("project_specific_outcome", template)
        self.assertIn("concrete_first_response_or_behavior_change", template)
        self.assertIn("low_commitment_reason_to_try_now", template)
        self.assertIn("product-blind taglines", public_review)

    def test_public_copy_requires_a_reader_purpose_not_only_motion(self):
        skill = self.read("skills/project-publisher/SKILL.md")
        patterns = self.read("skills/project-publisher/references/readme-patterns.md")
        chinese = self.read("skills/project-publisher/references/chinese-public-copy.md")
        public_review = self.read(
            "skills/project-publisher/references/public-surface-review.md"
        )

        self.assertIn("Give every public sentence", skill)
        self.assertIn("Replacing `feature` with a concrete noun", skill)
        self.assertIn("## Give every public line a job", patterns)
        self.assertIn("Try one feature", patterns)
        self.assertIn("How does login actually work?", patterns)
        self.assertIn("问一次登录流程", chinese)
        self.assertIn("登录功能到底是怎么跑起来的？", chinese)
        self.assertIn("only narrate motion", public_review)
        self.assertIn(
            "A concrete noun does not rescue an empty instruction", public_review
        )

    def test_skill_resynchronizes_the_authoritative_readme_after_changes(self):
        skill = self.read("skills/project-publisher/SKILL.md")
        patterns = self.read("skills/project-publisher/references/readme-patterns.md")
        english = self.read("README.md")
        chinese = self.read("README.zh-CN.md")

        self.assertIn("reopen every public README", skill)
        self.assertIn("edit the authoritative README in place", skill)
        self.assertIn("Do not create `README.new.md`", skill)
        self.assertIn("Re-read the existing README after implementation", patterns)
        self.assertIn("README still teaches old behavior or commands", english)
        self.assertIn("需要更新就直接覆盖旧内容", chinese)

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
            "一次自审发现的越界打包漏洞",
            'draw.text((105, 241), "1 · 修复前"',
            'draw.text((555, 241), "2 · 审计"',
            'draw.text((1005, 241), "3 · 修复后"',
        ]
        for phrase in stale:
            self.assertNotIn(phrase, source)

    def test_project_publisher_name_describes_the_durable_role(self):
        manifest = json.loads(self.read(".codex-plugin/plugin.json"))
        skill = self.read("skills/project-publisher/SKILL.md")
        naming = self.read("skills/project-publisher/references/naming-and-positioning.md")
        english = self.read("README.md")
        chinese = self.read("README.zh-CN.md")

        self.assertEqual(manifest["name"], "project-publisher")
        self.assertEqual(manifest["version"], "0.3.0")
        self.assertEqual(manifest["interface"]["displayName"], "Project Publisher")
        self.assertIn("name: project-publisher", skill)
        self.assertIn("Name the durable role or outcome", skill)
        self.assertIn("## Name the durable role, not the first demo", naming)
        self.assertIn("Speech", naming)
        self.assertIn("Grounded AI Tutor", naming)
        self.assertIn("reviews what exists, sharpens the name and position", english)
        self.assertIn("项目对外发布后的整套工作", chinese)
        for text in (english, chinese):
            self.assertNotIn("Use $launch-github-project", text)
            self.assertNotIn("remote rename not performed", text)
            self.assertNotIn("等待远程仓库改名", text)
        self.assertIn("evals/results/public-install-v0.3.0.md", english)
        self.assertIn("evals/results/public-install-v0.3.0.md", chinese)


if __name__ == "__main__":
    unittest.main()
