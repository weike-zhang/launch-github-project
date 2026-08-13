#!/usr/bin/env python3
"""Build the launch-project hero image with deterministic typography."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]


def font(size: int, bold: bool = False):
    candidates = [
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/System/Library/Fonts/Helvetica.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default(size=size)


image = Image.new("RGB", (1600, 900), "#162033")
draw = ImageDraw.Draw(image)
for y in range(900):
    blend = y / 900
    draw.line((0, y, 1600, y), fill=tuple(round(a * (1 - blend) + b * blend) for a, b in zip((22, 32, 51), (35, 46, 67))))

draw.rounded_rectangle((92, 92, 450, 144), radius=26, fill="#29364C")
draw.text((120, 104), "OPEN-SOURCE WORKFLOW", font=font(24, True), fill="#FFB423")
draw.text((92, 226), "Launch", font=font(104, True), fill="white")
draw.text((92, 346), "GitHub Project", font=font(84, True), fill="white")
draw.text((100, 490), "Audit what exists. Prove what works.", font=font(35), fill="#DDE5F0")
draw.text((100, 540), "Package only what the project needs.", font=font(35), fill="#DDE5F0")
draw.text((100, 790), "Built by Weike Zhang", font=font(25), fill="#9EABBC")

# Repository folder + launch arrow mark.
draw.rounded_rectangle((1050, 235, 1445, 565), radius=34, fill="#FFB423", outline="#FFF3E8", width=8)
draw.polygon([(1085, 235), (1225, 235), (1260, 280), (1415, 280), (1415, 535), (1085, 535)], fill="#FFB423", outline="#FFF3E8")
draw.line((1150, 470, 1345, 275), fill="#F24B22", width=28)
draw.line((1345, 275, 1345, 390), fill="#F24B22", width=28)
draw.line((1345, 275, 1230, 275), fill="#F24B22", width=28)

image.save(ROOT / "assets" / "hero.png", optimize=True)
preview = ImageOps.fit(image, (1280, 640), method=Image.Resampling.LANCZOS)
preview.save(ROOT / "assets" / "social-preview.png", optimize=True)
print(ROOT / "assets" / "hero.png")
print(ROOT / "assets" / "social-preview.png")
