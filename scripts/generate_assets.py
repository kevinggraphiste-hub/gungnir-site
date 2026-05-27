#!/usr/bin/env python3
"""Génère les assets statiques :
- favicon.ico (16+32+48)
- apple-touch-icon.png (180×180)
- assets/img/og/default.jpg (1200×630, image OG par défaut)

À relancer si le logo source change. Sortie commitée.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent
LOGO = ROOT / "assets/img/gungnir-logo.png"

ANTHRACITE = (17, 17, 17)
BRONZE     = "#b89468"
CREAM      = "#f4f1ea"
SCARLET    = "#c21c27"

FONT_BOLD  = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_REG   = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_MONO  = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def square_logo(size: int) -> Image.Image:
    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((size, size), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), ANTHRACITE + (255,))
    off = ((size - logo.width) // 2, (size - logo.height) // 2)
    canvas.paste(logo, off, logo)
    return canvas


def gen_apple_touch_icon():
    img = square_logo(180).convert("RGB")
    img.save(ROOT / "apple-touch-icon.png", "PNG", optimize=True)
    print("  apple-touch-icon.png (180×180)")


def gen_favicon_ico():
    sizes = [16, 32, 48]
    icons = [square_logo(s) for s in sizes]
    icons[0].save(ROOT / "favicon.ico", format="ICO", sizes=[(s, s) for s in sizes])
    print(f"  favicon.ico ({'+'.join(str(s) for s in sizes)})")


def gen_og_default():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), ANTHRACITE)
    draw = ImageDraw.Draw(img)

    logo = Image.open(LOGO).convert("RGBA")
    logo.thumbnail((420, 420), Image.LANCZOS)
    img.paste(logo, (90, (H - logo.height) // 2), logo)

    title_font = ImageFont.truetype(FONT_BOLD, 92)
    tag_font   = ImageFont.truetype(FONT_REG, 42)
    url_font   = ImageFont.truetype(FONT_MONO, 26)

    tx = 560
    draw.text((tx, 180), "GUNGNIR", fill=CREAM, font=title_font)
    draw.text((tx, 290), "L'assistant IA qui apprend", fill=BRONZE, font=tag_font)
    draw.text((tx, 340), "votre métier — souverain.", fill=BRONZE, font=tag_font)
    draw.text((tx, 460), "scarletwolf.cloud", fill=SCARLET, font=url_font)

    draw.rectangle([(0, H - 8), (W, H)], fill=SCARLET)

    (ROOT / "assets/img/og").mkdir(parents=True, exist_ok=True)
    img.save(ROOT / "assets/img/og/default.jpg", "JPEG", quality=88, optimize=True)
    print("  assets/img/og/default.jpg (1200×630)")


if __name__ == "__main__":
    gen_apple_touch_icon()
    gen_favicon_ico()
    gen_og_default()
