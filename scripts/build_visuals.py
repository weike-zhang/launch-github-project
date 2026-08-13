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
    image = ImageOps.fit(source, (1600, 640), method=Image.Resampling.LANCZOS, centering=(0.55, 0.5))
    image = darken_left(image)
    draw = ImageDraw.Draw(image)
    rounded_label(draw, (86, 54), "GITHUB LAUNCH FINISHER", "#263650", AMBER)
    draw.text((84, 126), "Launch", font=font(76, True), fill=WHITE)
    draw.text((84, 208), "GitHub Project", font=font(66, True), fill=WHITE)
    draw.text((90, 315), "Find what stops a new user.", font=font(31, True), fill="#D9E3F0")
    draw.text((90, 360), "Finish the public release around it.", font=font(28), fill="#D9E3F0")
    draw.line((90, 428, 640, 428), fill="#52637A", width=2)
    draw.text((90, 458), "README", font=font(19, True), fill=AMBER)
    draw.text((196, 458), "VISUALS", font=font(19, True), fill=AMBER)
    draw.text((310, 458), "INSTALL", font=font(19, True), fill=AMBER)
    draw.text((414, 458), "RELEASE", font=font(19, True), fill=AMBER)
    draw.text((530, 458), "SOURCE ZIP", font=font(19, True), fill=MINT)
    draw.text((90, 535), "First pass is read-only. You approve edits and GitHub actions.", font=font(22), fill=SLATE)
    return image.convert("RGB")


def build_hero_zh() -> Image.Image:
    source = Image.open(ASSETS / "hero-art.png").convert("RGB")
    image = ImageOps.fit(source, (1600, 640), method=Image.Resampling.LANCZOS, centering=(0.55, 0.5))
    image = darken_left(image)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((70, 43, 374, 94), radius=24, fill="#263650")
    draw.text((91, 55), "GitHub 发布收尾", font=zh_font(22, True), fill=AMBER)
    draw.text((84, 126), "Launch", font=font(70, True), fill=WHITE)
    draw.text((84, 204), "GitHub Project", font=font(61, True), fill=WHITE)
    draw.text((90, 315), "先找出最劝退新用户的地方", font=zh_font(32, True), fill="#D9E3F0")
    draw.text((90, 360), "再把发布材料一项项补齐", font=zh_font(28), fill="#D9E3F0")
    draw.line((90, 428, 680, 428), fill="#52637A", width=2)
    labels = [(90, "README", AMBER), (215, "配图", AMBER), (310, "安装入口", AMBER), (450, "Release", AMBER), (575, "发布包", MINT)]
    for x, label, color in labels:
        draw.text((x, 458), label, font=zh_font(22, True), fill=color)
    draw.text((90, 535), "第一轮只读。改文件、操作 GitHub 都由你确认。", font=zh_font(22), fill=SLATE)
    return image.convert("RGB")


def build_activation_proof() -> Image.Image:
    image = Image.new("RGB", (1400, 760), NAVY)
    draw = ImageDraw.Draw(image)
    draw.text((70, 56), "A Codex test run showed that the audit was too noisy", font=font(42, True), fill=WHITE)
    draw.text(
        (72, 122),
        "The target was a tiny notes CLI. The installed Skill dependency was not the product.",
        font=font(25),
        fill=SLATE,
    )
    cards = [(70, 205, 640, 650), (760, 205, 1330, 650)]
    for card in cards:
        draw.rounded_rectangle(card, radius=28, fill=PANEL, outline="#2C3B53", width=2)

    rounded_label(draw, (104, 240), "BEFORE THE FIX", "#39231F", CORAL)
    draw.text((105, 315), "Primary type", font=font(23), fill=SLATE)
    draw.text((105, 354), "Agent Skill", font=font(36, True), fill=CORAL)
    draw.text((105, 435), "6 blockers", font=font(31, True), fill=WHITE)
    draw.text((340, 435), "6 warnings", font=font(31, True), fill=WHITE)
    draw.text((105, 500), "Installed dependency scanned as product", font=font(23), fill="#FFD5CA")
    draw.text((105, 545), "Scanner matched its own rule source", font=font(23), fill="#FFD5CA")

    rounded_label(draw, (794, 240), "AFTER THE FIX", "#16372F", MINT)
    draw.text((795, 315), "Installed Skill", font=font(23), fill=SLATE)
    draw.text((795, 354), "excluded from target", font=font(34, True), fill=MINT)
    draw.text((795, 435), "1 real blocker", font=font(31, True), fill=WHITE)
    draw.text((1085, 435), "0 warnings", font=font(31, True), fill=WHITE)
    draw.text((795, 500), "Local lock path remains visible", font=font(23), fill="#D8F7EB")
    draw.text((795, 545), "Codex still catches the false README claim", font=font(23), fill="#D8F7EB")

    draw.line((656, 427, 744, 427), fill=AMBER, width=8)
    draw.polygon([(744, 427), (720, 411), (720, 443)], fill=AMBER)
    draw.text((72, 695), "Same fixture and host: dependency noise removed, real blocker preserved.", font=font(22), fill=SLATE)
    return image


def main() -> None:
    hero = build_hero()
    hero.save(ASSETS / "hero.png", optimize=True)
    hero_zh = build_hero_zh()
    hero_zh.save(ASSETS / "hero.zh-CN.png", optimize=True)
    social = ImageOps.fit(hero, (1280, 640), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    social.save(ASSETS / "social-preview.png", optimize=True)
    activation = build_activation_proof()
    activation.save(ASSETS / "activation-proof.png", optimize=True)
    for name in (
        "hero.png",
        "hero.zh-CN.png",
        "social-preview.png",
        "activation-proof.png",
    ):
        print(ASSETS / name)


if __name__ == "__main__":
    main()
