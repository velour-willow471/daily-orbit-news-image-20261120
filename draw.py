#!/usr/bin/env python3
"""Render THE DAILY ORBIT front page for Friday, 20 November 2026.

A single 1024x1024 broadsheet-style image summarising the day's verified
world news. Built only with Pillow: rules, columns, kickers, bylines and
small line illustrations drawn by hand. Run: python3 draw.py
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
GREY = (92, 88, 80)
LIGHT = (226, 220, 203)
RED = (154, 26, 26)
BLUE = (28, 58, 102)
TEAL = (18, 96, 92)

FONT_DIR = "/usr/share/fonts/truetype/noto"
SERIF_BLACK = f"{FONT_DIR}/NotoSerif-Black.ttf"
SERIF_BOLD = f"{FONT_DIR}/NotoSerif-Bold.ttf"
SERIF_REG = f"{FONT_DIR}/NotoSerif-Regular.ttf"
SERIF_IT = f"{FONT_DIR}/NotoSerif-Italic.ttf"
SANS_BOLD = f"{FONT_DIR}/NotoSans-Bold.ttf"
SANS_REG = f"{FONT_DIR}/NotoSans-Regular.ttf"
SANS_COND_BOLD = f"{FONT_DIR}/NotoSans-CondensedBold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, max_w, leading, fill=INK):
    for ln in wrap(draw, text, font, max_w):
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def centered(draw, y, text, font, fill=INK):
    w = draw.textlength(text, font=font)
    draw.text(((W - w) / 2, y), text, font=font, fill=fill)
    return y


def rule(draw, y, x0=28, x1=996, thick=1, fill=INK):
    draw.rectangle([x0, y, x1, y + thick - 1], fill=fill)


def story(draw, x, y, col_w, kicker, headline, body, hsize=15, bsize=11):
    """Draw one story block; returns y after the block."""
    if kicker:
        draw.text((x, y), kicker.upper(), font=F(SANS_BOLD, 8), fill=RED)
        y += 12
    y = para(draw, x, y, headline, F(SERIF_BOLD, hsize), col_w, hsize + 3)
    y += 2
    y = para(draw, x, y, body, F(SERIF_REG, bsize), col_w, bsize + 4)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- folio line ----
    d.text((28, 14), "Vol. IX  •  No. 324", font=F(SANS_REG, 9), fill=GREY)
    d.text((430, 14), "www.dailyorbit.example", font=F(SANS_REG, 9), fill=GREY)
    r = "Price $2.00  •  Late Edition"
    d.text((996 - d.textlength(r, font=F(SANS_REG, 9)), 14), r,
           font=F(SANS_REG, 9), fill=GREY)
    rule(d, 30, thick=1)
    rule(d, 33, thick=3)

    # ---- masthead ----
    centered(d, 40, "THE DAILY ORBIT", F(SERIF_BLACK, 62))
    centered(d, 108, "All the world, on one page  •  Independent since 2017",
             F(SERIF_IT, 11), fill=GREY)
    rule(d, 130, thick=1)
    # date bar
    d.rectangle([28, 133, 996, 155], fill=INK)
    d.text((38, 138), "Friday, 20 November 2026", font=F(SANS_BOLD, 12), fill=PAPER)
    mid = "WORLD NEWS  •  ONE DAY, ONE IMAGE"
    d.text(((W - d.textlength(mid, font=F(SANS_BOLD, 10))) / 2, 139), mid,
           font=F(SANS_BOLD, 10), fill=(210, 200, 175))
    tail = "20 NOV 2026"
    d.text((986 - d.textlength(tail, font=F(SANS_BOLD, 12)), 138), tail,
           font=F(SANS_BOLD, 12), fill=PAPER)

    # ---- MAIN STORY ----
    y = 164
    d.text((28, y), "CLIMATE SUMMIT  •  BELEM TALKS CLOSE", font=F(SANS_BOLD, 10), fill=RED)
    y += 16
    y = para(d, 28, y, "COP31 wraps in turmoil as climate",
             F(SERIF_BLACK, 34), 640, 38)
    y = para(d, 28, y, "texts branded an \u201coutrage\u201d",
             F(SERIF_BLACK, 34), 640, 38)
    y += 2
    y = para(d, 28, y,
             "Fossil-fuel transition eliminated from near-final deal; "
             "Pacific nations face the reality of a warming world.",
             F(SERIF_IT, 13), 640, 17, fill=(50, 48, 44))
    y += 4
    d.text((28, y), "By Orbit Staff  •  BELEM", font=F(SANS_BOLD, 8), fill=GREY)
    y += 13
    body_main = (
        "The COP31 climate summit closed in turmoil after near-final texts "
        "dropped any commitment to transition away from fossil fuels. "
        "Delegates and campaigners branded the outcome an \u201coutrage\u201d, "
        "while Pacific island nations \u2014 for whom sea-level rise is "
        "existential \u2014 said they must now face that reality with far "
        "less help than they were promised."
    )
    y = para(d, 28, y, body_main, F(SERIF_REG, 11), 640, 15)

    # illustration: globe + thermometer, top-right of main story
    bx0, by0, bx1, by1 = 692, 164, 996, 330
    d.rectangle([bx0, by0, bx1, by1], outline=INK, width=1)
    d.rectangle([bx0, by0, bx1, by0 + 20], fill=BLUE)
    d.text((bx0 + 8, by0 + 4), "THE PLANET AT COP31", font=F(SANS_BOLD, 9), fill=PAPER)
    cx, cy, rr = 800, 262, 42
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=TEAL, width=3)
    d.ellipse([cx - 14, cy - rr, cx + 14, cy + rr], outline=TEAL, width=1)
    d.line([cx - rr, cy, cx + rr, cy], fill=TEAL, width=1)
    d.line([cx - rr + 8, cy - 22, cx + rr - 8, cy - 22], fill=TEAL, width=1)
    d.line([cx - rr + 8, cy + 22, cx + rr - 8, cy + 22], fill=TEAL, width=1)
    # thermometer
    tx = 900
    d.rectangle([tx, 205, tx + 12, 285], outline=RED, width=2)
    d.rectangle([tx + 2, 235, tx + 10, 283], fill=RED)
    d.ellipse([tx - 6, 278, tx + 18, 302], fill=RED)
    d.text((862, 306), "Talks overheat as the", font=F(SERIF_IT, 9), fill=GREY)
    d.text((862, 317), "phase-out disappears.", font=F(SERIF_IT, 9), fill=GREY)

    rule(d, 342, thick=2)
    rule(d, 346, thick=1)

    # ---- three columns of secondary stories ----
    col_x = [28, 352, 676]
    col_w = 304
    ys = [356, 356, 356]

    # Column 1
    x = col_x[0]
    yy = story(d, x, ys[0], col_w, "Diplomacy • Shenzhen",
               "After Shenzhen: Trump, Putin and Xi draw pushback at home",
               "The camaraderie of Donald Trump, Vladimir Putin and Xi Jinping "
               "after their Shenzhen meeting drew pushback at home, even as "
               "China, the United States and Russia issued a joint peace "
               "declaration.", hsize=15)
    yy += 6
    d.line([x, yy, x + col_w, yy], fill=GREY, width=1)
    yy += 8
    yy = story(d, x, yy, col_w, "Markets • Debut",
               "Anthropic joins the giants in stock-market debut",
               "Anthropic became one of the world's most valuable public "
               "companies after its stock-market debut, a landmark listing "
               "for the artificial-intelligence industry.", hsize=14)
    ys[0] = yy

    # Column 2
    x = col_x[1]
    yy = story(d, x, ys[1], col_w, "War & Peace • Ukraine",
               "Europe ready for talks with Russia on ending the war",
               "Europe signalled it is ready for talks with Russia on ending "
               "the Ukraine war. Kyiv and Moscow exchanged drone attacks amid "
               "peace talks in Abu Dhabi, and Putin ruled out a sea or energy "
               "truce after the Crimea Bridge was hit again.", hsize=15)
    yy += 6
    d.line([x, yy, x + col_w, yy], fill=GREY, width=1)
    yy += 8
    yy = story(d, x, yy, col_w, "Oceans • Mining",
               "US auctions first deep-sea mining leases",
               "The United States auctioned its first-ever deep-sea mining "
               "leases, pressing ahead despite a court ruling against the "
               "plan and warnings from marine scientists.", hsize=14)
    ys[1] = yy

    # Column 3
    x = col_x[2]
    yy = story(d, x, ys[2], col_w, "Gulf • Oil",
               "Iran steps up Hormuz tanker attacks as oil slides",
               "Iran intensified attacks on tankers in the Strait of Hormuz "
               "just as oil prices slid. In Washington, the US Senate "
               "rejected an Iran war-powers resolution 51\u201348.", hsize=15)
    yy += 6
    d.line([x, yy, x + col_w, yy], fill=GREY, width=1)
    yy += 8
    yy = story(d, x, yy, col_w, "Technology • Chips",
               "880,000 AI chips for China spark calls for hearings",
               "Records show Washington approved about 880,000 advanced AI "
               "chips for Chinese firms. Lawmakers demanded hearings, and "
               "California targeted Nvidia in a China chip probe.", hsize=14)
    ys[2] = yy

    # vertical column rules
    mid_y = max(ys) + 4
    for vx in (340, 664):
        d.line([vx, 356, vx, mid_y], fill=LIGHT, width=2)

    y = mid_y + 6
    rule(d, y, thick=2)
    y += 8

    # ---- Around the world in brief ----
    d.rectangle([28, y, 996, y + 22], fill=INK)
    d.text((38, y + 5), "AROUND THE WORLD IN BRIEF", font=F(SANS_BOLD, 11), fill=PAPER)
    d.text((700, y + 5), "20 NOVEMBER 2026", font=F(SANS_BOLD, 11), fill=(210, 200, 175))
    y += 30
    briefs = [
        ("HEALTH —", "Antibiotics are failing and patients are running out of "
         "options, the UN warns, as drug-resistant infections spread."),
        ("INDIA —", "Cyclone Akvan makes landfall on the Andhra\u2013Odisha "
         "coast, bringing destructive winds and flooding rains."),
        ("ESTONIA —", "Estonia will close its border with Russia from "
         "December, citing security concerns along the frontier."),
        ("SPAIN —", "A general strike disrupts ports and factories across "
         "Spain in a nationwide day of industrial action."),
        ("CLIMATE TECH —", "Meta re-evaluates its 2030 net-zero target amid "
         "the vast energy demands of its AI buildout."),
        ("APEC —", "APEC ministers issue a joint statement in Shenzhen after "
         "a week of trade and security talks."),
        ("CINCINNATI —", "Beloved zoo hippo Fiona dies after swallowing a "
         "hat; tributes pour in for the city's favourite animal."),
    ]
    bx = [28, 352, 676]
    # briefs in 3 columns: 3 / 2 / 2
    groups = [briefs[0:3], briefs[3:5], briefs[5:7]]
    brief_bottom = y
    for ci, group in enumerate(groups):
        byy = y
        for head, txt in group:
            byy = para(d, bx[ci], byy, head + " " + txt, F(SERIF_REG, 10.5 if False else 10),
                       col_w, 14)
            byy += 7
        brief_bottom = max(brief_bottom, byy)
    y = brief_bottom + 2
    rule(d, y, thick=1)
    y += 8

    # ---- markets & weather ticker ----
    d.rectangle([28, y, 996, 1024 - 28], fill=(30, 30, 30))
    d.text((40, y + 8), "MARKETS", font=F(SANS_BOLD, 10), fill=(240, 200, 90))
    d.text((40, y + 26),
           "OIL  Slides as Hormuz risk rises  •  ANTHROPIC  Soars on debut  •  "
           "CHIPS  Nvidia in focus",
           font=F(SANS_REG, 10), fill=PAPER)
    d.text((40, y + 44), "WEATHER", font=F(SANS_BOLD, 10), fill=(140, 200, 240))
    d.text((40, y + 62),
           "ANDHRA\u2013ODISHA  Cyclone Akvan landfall  •  BELEM  Hot, humid  •  "
           "ABU DHABI  Clear  •  SHENZHEN  Mild",
           font=F(SANS_REG, 10), fill=PAPER)
    d.text((40, y + 82),
           "The Daily Orbit  •  Friday, 20 November 2026  •  One day. One page. "
           "Every story above happened today.",
           font=F(SERIF_IT, 9), fill=(190, 185, 170))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}: {os.path.getsize(out)} bytes, {img.size}")


if __name__ == "__main__":
    main()
