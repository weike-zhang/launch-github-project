#!/usr/bin/env python3
"""Build repository visuals from the project-owned source artwork."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
NAVY = "#0B1425"
PANEL = "#152238"
SLATE = "#8FA1B8"
WHITE = "#F7FAFF"
AMBER = "#FFB224"
CORAL = "#FF4A24"
MINT = "#52D6A3"


def font(size: int, bold: bool = False):
    candidates = [
        Path(
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
            if bold
            else "/System/Library/Fonts/Supplemental/Arial.ttf"
        ),
        Path("/System/Library/Fonts/Helvetica.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default(size=size)


def zh_font(size: int, bold: bool = False):
    candidates = [
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size, index=1 if bold else 0)
    return font(size, bold)


def rounded_label(draw: ImageDraw.ImageDraw, xy, text: str, fill: str, ink: str) -> None:
    x, y = xy
    label_font = font(22, True)
    box = draw.textbbox((x, y), text, font=label_font)
    width = box[2] - box[0]
    draw.rounded_rectangle((x - 16, y - 10, x + width + 16, y + 38), radius=20, fill=fill)
    draw.text((x, y), text, font=label_font, fill=ink)


def darken_left(image: Image.Image, strength: int = 220) -> Image.Image:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    pixels = overlay.load()
    width, height = image.size
    for x in range(width):
        alpha = round(max(0, strength * (1 - x / (width * 0.72))))
        for y in range(height):
            pixels[x, y] = (5, 12, 25, alpha)
    return Image.alpha_composite(image.convert("RGBA"), overlay)


def build_hero() -> Image.Image:
    source = Image.open(ASSETS / "hero-art.png").convert("RGB")
    image = ImageOps.fit(source, (1600, 800), method=Image.Resampling.LANCZOS, centering=(0.55, 0.5))
    image = darken_left(image)
    draw = ImageDraw.Draw(image)
    rounded_label(draw, (86, 76), "RELEASE WITH EVIDENCE", "#263650", AMBER)
    draw.text((84, 158), "Launch", font=font(86, True), fill=WHITE)
    draw.text((84, 252), "GitHub Project", font=font(78, True), fill=WHITE)
    draw.text((90, 374), "From a working local project", font=font(33), fill="#D9E3F0")
    draw.text((90, 420), "to a release people can trust.", font=font(33), fill="#D9E3F0")
    draw.line((90, 505, 590, 505), fill="#52637A", width=2)
    draw.text((90, 540), "AUDIT", font=font(22, True), fill=AMBER)
    draw.text((224, 540), "PROVE", font=font(22, True), fill=AMBER)
    draw.text((362, 540), "PACKAGE", font=font(22, True), fill=AMBER)
    draw.text((528, 540), "VERIFY", font=font(22, True), fill=MINT)
    draw.text((90, 615), "Agent Skill · read-only first · remote actions by approval", font=font(23), fill=SLATE)
    return image.convert("RGB")


def build_hero_zh() -> Image.Image:
    source = Image.open(ASSETS / "hero-art.png").convert("RGB")
    image = ImageOps.fit(source, (1600, 800), method=Image.Resampling.LANCZOS, centering=(0.55, 0.5))
    image = darken_left(image)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((70, 65, 374, 116), radius=24, fill="#263650")
    draw.text((91, 77), "别让好项目死在发布页", font=zh_font(22, True), fill=AMBER)
    draw.text((84, 170), "Launch", font=font(76, True), fill=WHITE)
    draw.text((84, 256), "GitHub Project", font=font(68, True), fill=WHITE)
    draw.text((90, 374), "代码能跑，只是及格", font=zh_font(34, True), fill="#D9E3F0")
    draw.text((90, 423), "让人看懂、试得动、查得到证据，才算发布", font=zh_font(30, True), fill="#D9E3F0")
    draw.line((90, 505, 590, 505), fill="#52637A", width=2)
    labels = [(90, "审计", AMBER), (224, "证明", AMBER), (362, "打包", AMBER), (528, "核验", MINT)]
    for x, label, color in labels:
        draw.text((x, 540), label, font=zh_font(24, True), fill=color)
    draw.text((90, 615), "先审项目 · 再拿证据 · 没授权不碰远程仓库", font=zh_font(24), fill=SLATE)
    return image.convert("RGB")


def build_proof() -> Image.Image:
    image = Image.new("RGB", (1400, 760), NAVY)
    draw = ImageDraw.Draw(image)
    draw.text((70, 56), "A real failure caught before release", font=font(48, True), fill=WHITE)
    draw.text(
        (72, 120),
        "The first self-audit found a path that could copy bytes from outside the project.",
        font=font(25),
        fill=SLATE,
    )

    cards = [(70, 205, 430, 650), (520, 205, 880, 650), (970, 205, 1330, 650)]
    for card in cards:
        draw.rounded_rectangle(card, radius=28, fill=PANEL, outline="#2C3B53", width=2)

    rounded_label(draw, (104, 240), "1 · BEFORE", "#39231F", CORAL)
    draw.text((105, 312), "release bundle", font=font(29, True), fill=WHITE)
    draw.text((105, 365), "project/", font=font(24), fill="#C9D4E4")
    draw.text((130, 407), "docs/", font=font(24), fill="#C9D4E4")
    draw.text((130, 449), "guide  →  /private/draft", font=font(22), fill=CORAL)
    draw.polygon([(105, 535), (130, 490), (155, 535)], fill=CORAL)
    draw.text((170, 498), "tracked symlink", font=font(22, True), fill="#FFD5CA")

    rounded_label(draw, (554, 240), "2 · AUDIT", "#3A2D17", AMBER)
    draw.text((555, 312), "BLOCKER", font=font(34, True), fill=AMBER)
    draw.text((555, 370), "Path leaves the", font=font(25), fill=WHITE)
    draw.text((555, 406), "reviewed project tree", font=font(25), fill=WHITE)
    draw.rounded_rectangle((555, 480, 845, 552), radius=16, fill="#0D1728")
    draw.text((580, 500), "package: stopped", font=font(22, True), fill=CORAL)

    rounded_label(draw, (1004, 240), "3 · AFTER", "#16372F", MINT)
    draw.text((1005, 312), "Release-ready", font=font(32, True), fill=WHITE)
    checks = [
        "symlinks rejected",
        "regression covered",
        "ZIP extracted",
        "boundary documented",
    ]
    for index, check in enumerate(checks):
        y = 375 + index * 52
        draw.ellipse((1007, y, 1035, y + 28), fill=MINT)
        draw.line((1015, y + 14, 1022, y + 21), fill=NAVY, width=4)
        draw.line((1022, y + 21, 1030, y + 8), fill=NAVY, width=4)
        draw.text((1050, y - 1), check, font=font(22), fill="#DDE8F4")

    draw.line((442, 427, 507, 427), fill=AMBER, width=8)
    draw.polygon([(507, 427), (485, 412), (485, 442)], fill=AMBER)
    draw.line((892, 427, 957, 427), fill=MINT, width=8)
    draw.polygon([(957, 427), (935, 412), (935, 442)], fill=MINT)
    draw.text((72, 695), "Observed in this repository · reproduction and remaining limits are public", font=font(22), fill=SLATE)
    return image


def build_proof_zh() -> Image.Image:
    image = Image.new("RGB", (1400, 760), NAVY)
    draw = ImageDraw.Draw(image)
    draw.text((70, 56), "不是演示：它真抓到过一个越界打包漏洞", font=zh_font(43, True), fill=WHITE)
    draw.text((72, 122), "一个藏在项目里的符号链接，差点把项目外的文件装进 ZIP。", font=zh_font(25), fill=SLATE)
    cards = [(70, 205, 430, 650), (520, 205, 880, 650), (970, 205, 1330, 650)]
    for card in cards:
        draw.rounded_rectangle(card, radius=28, fill=PANEL, outline="#2C3B53", width=2)
    draw.rounded_rectangle((88, 230, 255, 280), radius=22, fill="#39231F")
    draw.text((105, 241), "1 · 修复前", font=zh_font(22, True), fill=CORAL)
    draw.text((105, 312), "发布包", font=zh_font(31, True), fill=WHITE)
    draw.text((105, 373), "项目/", font=zh_font(24), fill="#C9D4E4")
    draw.text((130, 415), "文档/", font=zh_font(24), fill="#C9D4E4")
    draw.text((130, 457), "指南 → 私有草稿", font=zh_font(22), fill=CORAL)
    draw.polygon([(105, 535), (130, 490), (155, 535)], fill=CORAL)
    draw.text((170, 498), "被跟踪的符号链接", font=zh_font(20, True), fill="#FFD5CA")
    draw.rounded_rectangle((538, 230, 690, 280), radius=22, fill="#3A2D17")
    draw.text((555, 241), "2 · 审计", font=zh_font(22, True), fill=AMBER)
    draw.text((555, 312), "阻断发布", font=zh_font(34, True), fill=AMBER)
    draw.text((555, 377), "路径离开了", font=zh_font(25), fill=WHITE)
    draw.text((555, 415), "已审核的项目目录", font=zh_font(25), fill=WHITE)
    draw.rounded_rectangle((555, 480, 845, 552), radius=16, fill="#0D1728")
    draw.text((580, 500), "打包：已停止", font=zh_font(22, True), fill=CORAL)
    draw.rounded_rectangle((988, 230, 1140, 280), radius=22, fill="#16372F")
    draw.text((1005, 241), "3 · 修复后", font=zh_font(22, True), fill=MINT)
    draw.text((1005, 312), "可以发布", font=zh_font(32, True), fill=WHITE)
    checks = ["拒绝符号链接", "加入回归测试", "实际解压 ZIP", "公开剩余边界"]
    for index, check in enumerate(checks):
        y = 375 + index * 52
        draw.ellipse((1007, y, 1035, y + 28), fill=MINT)
        draw.line((1015, y + 14, 1022, y + 21), fill=NAVY, width=4)
        draw.line((1022, y + 21, 1030, y + 8), fill=NAVY, width=4)
        draw.text((1050, y - 1), check, font=zh_font(22), fill="#DDE8F4")
    draw.line((442, 427, 507, 427), fill=AMBER, width=8)
    draw.polygon([(507, 427), (485, 412), (485, 442)], fill=AMBER)
    draw.line((892, 427, 957, 427), fill=MINT, width=8)
    draw.polygon([(957, 427), (935, 412), (935, 442)], fill=MINT)
    draw.text((72, 695), "证据来自本仓库 · 复现过程和剩余限制均已公开", font=zh_font(22), fill=SLATE)
    return image


def build_activation_proof() -> Image.Image:
    image = Image.new("RGB", (1400, 760), NAVY)
    draw = ImageDraw.Draw(image)
    draw.text((70, 56), "One real Codex activation exposed a noisy audit", font=font(46, True), fill=WHITE)
    draw.text(
        (72, 122),
        "The target was a tiny notes CLI. The installed Skill dependency was not the product.",
        font=font(25),
        fill=SLATE,
    )
    cards = [(70, 205, 640, 650), (760, 205, 1330, 650)]
    for card in cards:
        draw.rounded_rectangle(card, radius=28, fill=PANEL, outline="#2C3B53", width=2)

    rounded_label(draw, (104, 240), "BEFORE · NOISY", "#39231F", CORAL)
    draw.text((105, 315), "Primary type", font=font(23), fill=SLATE)
    draw.text((105, 354), "Agent Skill", font=font(36, True), fill=CORAL)
    draw.text((105, 435), "6 blockers", font=font(31, True), fill=WHITE)
    draw.text((340, 435), "6 warnings", font=font(31, True), fill=WHITE)
    draw.text((105, 500), "Installed dependency scanned as product", font=font(23), fill="#FFD5CA")
    draw.text((105, 545), "Scanner matched its own rule source", font=font(23), fill="#FFD5CA")

    rounded_label(draw, (794, 240), "AFTER · SIGNAL", "#16372F", MINT)
    draw.text((795, 315), "Installed Skill", font=font(23), fill=SLATE)
    draw.text((795, 354), "excluded from target", font=font(34, True), fill=MINT)
    draw.text((795, 435), "1 real blocker", font=font(31, True), fill=WHITE)
    draw.text((1085, 435), "0 warnings", font=font(31, True), fill=WHITE)
    draw.text((795, 500), "Local lock path remains visible", font=font(23), fill="#D8F7EB")
    draw.text((795, 545), "Codex still catches the false README claim", font=font(23), fill="#D8F7EB")

    draw.line((656, 427, 744, 427), fill=AMBER, width=8)
    draw.polygon([(744, 427), (720, 411), (720, 443)], fill=AMBER)
    draw.text((72, 695), "Same fixture · same host · dependency noise removed, real blocker preserved", font=font(22), fill=SLATE)
    return image


def main() -> None:
    hero = build_hero()
    hero.save(ASSETS / "hero.png", optimize=True)
    hero_zh = build_hero_zh()
    hero_zh.save(ASSETS / "hero.zh-CN.png", optimize=True)
    social = ImageOps.fit(hero, (1280, 640), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    social.save(ASSETS / "social-preview.png", optimize=True)
    proof = build_proof()
    proof.save(ASSETS / "audit-proof.png", optimize=True)
    proof_zh = build_proof_zh()
    proof_zh.save(ASSETS / "audit-proof.zh-CN.png", optimize=True)
    activation = build_activation_proof()
    activation.save(ASSETS / "activation-proof.png", optimize=True)
    for name in (
        "hero.png",
        "hero.zh-CN.png",
        "social-preview.png",
        "audit-proof.png",
        "audit-proof.zh-CN.png",
        "activation-proof.png",
    ):
        print(ASSETS / name)


if __name__ == "__main__":
    main()
