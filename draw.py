#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: one infographic summing up the world
news of Monday 23 November 2026.

Built from real reporting dated 23 November 2026 (BBC, CNN, Reuters,
Al Jazeera, The Hindu, Airways Magazine / Skeyes, market wires):
  1. COP31 climate talks in Antalya collapse with no deal (BBC/CNN/Reuters).
  2. Democrats clinch their largest US House majority since 1992 (BBC).
  3. A 7-year-old boy is pulled alive from rubble after a Russian drone
     strike in Ukraine that killed 10 (BBC/Al Jazeera).
  4. Belgium's airports shut as air-traffic controllers join a national
     anti-austerity strike (Skeyes/Brussels Airport via Airways Mag).
  5. Asian stock markets tumble on AI-bubble fears; Kospi -4% (wires).
  6. FIFA confirms the UK as host of the 2035 Women's World Cup (BBC/Reuters).
Footer: Indonesia factory fire and the Vanuatu M6.5 quake (Al Jazeera/USGS).

Output: 1024x1024 PNG, deterministic (no timestamps, fixed fonts).
Run: python3 draw.py  ->  writes entry.png next to this script.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

BLACK = (17, 17, 17)
WHITE = (255, 255, 255)
RED = (200, 16, 46)
DARK = (51, 51, 51)
RULE = (200, 200, 200)

STORIES = [
    ("CLIMATE", (27, 122, 61), "COP31 COLLAPSES \u2014 NO CLIMATE DEAL",
     "Talks in Antalya end after two weeks; fossil-fuel wording blocked."),
    ("USA", (29, 78, 216), "DEMOCRATS' BIGGEST HOUSE WIN SINCE 1992",
     "North Carolina flip gives the party at least 258 House seats."),
    ("UKRAINE", (185, 28, 28), "BOY, 7, PULLED ALIVE FROM RUBBLE",
     "Russian drone strike kills 10; the child was trapped 14 hours."),
    ("EUROPE", (109, 40, 217), "BELGIUM GROUNDED BY NATIONAL STRIKE",
     "Air-traffic controllers walk out; Brussels flights halted 7am\u20139pm."),
    ("MARKETS", (180, 83, 9), "ASIAN MARKETS TUMBLE ON AI-BUBBLE FEARS",
     "Seoul's Kospi falls 4%; Shanghai slides below 3,500."),
    ("SPORT", (15, 118, 110), "UK TO HOST 2035 WOMEN'S WORLD CUP",
     "FIFA confirms the four-nation bid \u2014 first UK World Cup since 1966."),
]

FOOTER = [
    "ALSO TODAY:  Indonesia factory fire \u2014 24 body bags recovered, dozens missing",
    "M 6.5 quake hits the Vanuatu region  \u2022  Nepal PM begins India visit",
]


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, f, max_w):
    """Shrink the font until the text fits max_w; returns (font, text)."""
    size = f.size
    while size > 18 and draw.textlength(text, font=f) > max_w:
        size -= 1
        f = ImageFont.truetype(f.path, size)
    return f


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # --- Masthead: black band with the title -------------------------------
    d.rectangle([0, 0, W, 108], fill=BLACK)
    f_title = font(BOLD, 68)
    d.text((W // 2, 54), "WORLD NEWS", font=f_title, fill=WHITE, anchor="mm")

    # --- Date band: red, the day this image sums up -----------------------
    d.rectangle([0, 108, W, 170], fill=RED)
    f_date = font(BOLD, 42)
    d.text((W // 2, 139), "MONDAY, 23 NOVEMBER 2026", font=f_date,
           fill=WHITE, anchor="mm")

    # --- Six stories, one row each ----------------------------------------
    y = 170
    row_h = 124
    for i, (tag, colour, headline, context) in enumerate(STORIES):
        # tag pill
        f_tag = font(BOLD, 20)
        tag_w = int(d.textlength(tag, font=f_tag)) + 28
        d.rounded_rectangle([28, y + 12, 28 + tag_w, y + 42],
                            radius=15, fill=colour)
        d.text((28 + tag_w // 2, y + 27), tag, font=f_tag,
               fill=WHITE, anchor="mm")
        # headline (one line, shrunk only if it would overflow)
        f_head = font(BOLD, 36)
        f_head = fit(d, headline, f_head, W - 56)
        d.text((28, y + 52), headline, font=f_head, fill=BLACK)
        # one line of context
        f_ctx = font(REG, 24)
        f_ctx = fit(d, context, f_ctx, W - 56)
        d.text((28, y + 94), context, font=f_ctx, fill=DARK)
        # divider rule (not after the last row)
        if i < len(STORIES) - 1:
            d.line([28, y + row_h - 1, W - 28, y + row_h - 1],
                   fill=RULE, width=2)
        y += row_h

    # --- Footer band: two more stories of the day -------------------------
    d.rectangle([0, y, W, H], fill=BLACK)
    f_foot = font(REG, 21)
    d.text((28, y + 22), FOOTER[0], font=f_foot, fill=WHITE)
    d.text((28, y + 56), FOOTER[1], font=f_foot, fill=WHITE)
    d.text((W - 28, y + 56), "23 NOV 2026", font=font(BOLD, 21),
           fill=(255, 210, 0), anchor="ra")

    # thin outer frame
    d.rectangle([0, 0, W - 1, H - 1], outline=BLACK, width=6)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
