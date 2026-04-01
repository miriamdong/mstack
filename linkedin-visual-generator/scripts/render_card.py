#!/usr/bin/env python3
"""
Virio LinkedIn Visual Generator
Renders 1080x1080 PNG cards in Virio's brand style.

Usage:
    python render_card.py --spec spec.json --output output.png

Spec format (list card):
{
  "type": "list",
  "section_label": "HOT TAKE",
  "topic_label": "Open-Source GTM",
  "headline": "GitHub stars ≠ pipeline.",
  "subhead": "Here's what breaks after Series B — and what you need instead.",
  "items": [
    {"num": "001", "title": "Social proof signal", "desc": "Stars tell VCs and early buyers you're real."},
    {"num": "002", "title": "Dev-first credibility", "desc": "Engineers trust what engineers use."},
    ...
  ],
  "footnote": "Works until Series B. Then it doesn't.",
  "examples": "Teleport · Skyflow"
}
"""

import json
import argparse
import random
import sys
from PIL import Image, ImageDraw, ImageFont

# ── Font paths ────────────────────────────────────────────────────────────────
FONT_BOLD    = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def fb(size): return ImageFont.truetype(FONT_BOLD, size)
def fr(size): return ImageFont.truetype(FONT_REGULAR, size)

# ── Virio Brand Palette ───────────────────────────────────────────────────────
BG_LEFT  = (216, 205, 184)   # warm sand
BG_RIGHT = (196, 202, 194)   # cool mist
INK      = (26,  23,  20)    # near-black
INK_MED  = (90,  80,  68)    # mid brown
INK_SOFT = (122, 112, 98)    # muted warm grey

W, H = 1080, 1080

def make_canvas():
    """Create base canvas with gradient + grain."""
    img = Image.new("RGBA", (W, H))
    draw = ImageDraw.Draw(img)

    # Horizontal gradient
    for x in range(W):
        t = x / W
        r = int(BG_LEFT[0]*(1-t) + BG_RIGHT[0]*t)
        g = int(BG_LEFT[1]*(1-t) + BG_RIGHT[1]*t)
        b = int(BG_LEFT[2]*(1-t) + BG_RIGHT[2]*t)
        draw.line([(x,0),(x,H)], fill=(r,g,b,255))

    # Grain texture
    grain = Image.new("RGBA", (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(grain)
    rng = random.Random(42)
    for _ in range(W*H//4):
        gd.point(
            (rng.randint(0, W-1), rng.randint(0, H-1)),
            fill=(rng.randint(0,255), rng.randint(0,255), rng.randint(0,255), rng.randint(0,13))
        )
    return Image.alpha_composite(img, grain)

def paste_rounded(base, box, radius, fill_rgba):
    ov = Image.new("RGBA", base.size, (0,0,0,0))
    ImageDraw.Draw(ov).rounded_rectangle(box, radius=radius, fill=fill_rgba)
    return Image.alpha_composite(base, ov)

def text_width(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[2] - bb[0]

def text_height(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[3] - bb[1]

def wrap_text(draw, text, font, max_width):
    """Wrap text to fit within max_width. Returns list of lines."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if text_width(draw, test, font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def render_list_card(spec, output_path):
    img = make_canvas()
    ML, MR, MT, MB = 72, 72, 58, 54
    CW = W - ML - MR

    draw = ImageDraw.Draw(img)
    f_lbl = fr(20)

    # ── Top bar ──────────────────────────────────────────────────────────────
    section = f"[ {spec.get('section_label', 'INSIGHT')} ]"
    topic   = spec.get('topic_label', '')
    topbar_left = f"{section}  ·  {topic}" if topic else section
    draw.text((ML, MT), topbar_left, font=f_lbl, fill=(*INK_SOFT, 255))

    brand = "VIRIO"
    bb = draw.textbbox((0,0), brand, font=fb(19))
    draw.text((W - MR - (bb[2]-bb[0]), MT), brand, font=fb(19), fill=(*INK_SOFT, 255))

    # ── Headline ─────────────────────────────────────────────────────────────
    y = MT + 52
    headline = spec.get('headline', '')
    f_h = fb(88)

    # Handle multi-line headline if needed
    hl_lines = wrap_text(draw, headline, f_h, CW)
    for line in hl_lines:
        draw.text((ML, y), line, font=f_h, fill=(*INK, 255))
        y += text_height(draw, line, f_h) - 4
    y += 6

    # ── Subhead ──────────────────────────────────────────────────────────────
    subhead = spec.get('subhead', '')
    if subhead:
        f_sub = fr(25)
        sub_lines = wrap_text(draw, subhead, f_sub, CW)
        for line in sub_lines:
            draw.text((ML, y), line, font=f_sub, fill=(*INK_MED, 255))
            y += text_height(draw, line, f_sub) + 2
        y += 20
    else:
        y += 16

    # ── Items ─────────────────────────────────────────────────────────────────
    items = spec.get('items', [])
    BOTTOM_H = 44
    y_bot    = H - MB - BOTTOM_H
    items_h  = y_bot - y - 8

    n = len(items)
    if n == 0:
        n = 1
    IGAP   = 10
    item_h = (items_h - (n-1)*IGAP) // n

    f_num = fr(17)
    f_rt  = fb(22)
    f_rd  = fr(20)

    for i, item in enumerate(items):
        alpha = 20 + i * 4  # slight depth variation
        img = paste_rounded(img, [ML, y, ML+CW, y+item_h], 14, (*INK, alpha))
        d = ImageDraw.Draw(img)

        num   = item.get('num', f'{i+1:03d}')
        title = item.get('title', '')
        desc  = item.get('desc', '')

        d.text((ML+18, y+12), f"[ {num} ]", font=f_num, fill=(*INK_SOFT, 255))
        d.text((ML+18, y+36), title, font=f_rt, fill=(*INK, 255))
        if desc:
            # Wrap description
            desc_lines = wrap_text(d, desc, f_rd, CW - 36)
            dy = y + 66
            for line in desc_lines:
                d.text((ML+18, dy), line, font=f_rd, fill=(*INK_MED, 255))
                dy += text_height(d, line, f_rd) + 2

        y += item_h + IGAP

    # ── Bottom bar ────────────────────────────────────────────────────────────
    # Layout: [footnote ············ e.g. examples] [Virio]
    # Footnote + examples share the left ~80%, Virio is pinned right.
    draw = ImageDraw.Draw(img)
    f_ft = fr(19)
    f_br = fb(19)
    by   = y_bot + 14

    footnote = spec.get('footnote', '')
    examples = spec.get('examples', '')
    virio    = "Virio"

    # Right: Virio — always pinned
    bb_v  = draw.textbbox((0,0), virio, font=f_br)
    vw    = bb_v[2] - bb_v[0]
    vx    = W - MR - vw
    draw.text((vx, by), virio, font=f_br, fill=(*INK_MED, 255))

    right_edge = vx - 24  # safe boundary before Virio

    # Build left-side text: footnote  ·  examples (combined if both present)
    if footnote and examples:
        left_txt = f"{footnote}   ·   {examples}"
    elif footnote:
        left_txt = footnote
    elif examples:
        left_txt = f"e.g. {examples}"
    else:
        left_txt = ""

    if left_txt:
        # Truncate only if it would collide with Virio
        while text_width(draw, left_txt, f_ft) > (right_edge - ML) and len(left_txt) > 12:
            left_txt = left_txt[:-4] + "..."
        draw.text((ML, by), left_txt, font=f_ft, fill=(*INK_MED, 255))

    # ── Save ──────────────────────────────────────────────────────────────────
    img.convert("RGB").save(output_path, "PNG")
    print(f"Saved: {output_path}")


RENDERERS = {
    "list": render_list_card,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec",   required=True, help="Path to JSON spec file")
    parser.add_argument("--output", required=True, help="Output PNG path")
    args = parser.parse_args()

    with open(args.spec) as f:
        spec = json.load(f)

    card_type = spec.get("type", "list")
    renderer  = RENDERERS.get(card_type)

    if not renderer:
        print(f"Unknown card type: {card_type}. Supported: {list(RENDERERS.keys())}", file=sys.stderr)
        sys.exit(1)

    renderer(spec, args.output)

if __name__ == "__main__":
    main()
