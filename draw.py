#!/usr/bin/env python3
"""Render the 24 November 2026 news poster (1024x1024 PNG).

Written from scratch for the news-image-20261124 edition. All facts come
from NEWS-RESEARCH-20261124.md. Pillow is only needed here; the shipped
main.py is pure stdlib and just copies the rendered entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (247, 242, 232)
INK = (20, 24, 31)
INK_SOFT = (74, 80, 92)
RED = (178, 39, 30)
BLUE = (29, 78, 137)
GOLD = (176, 124, 24)
CARD = (255, 253, 247)
LINE = (196, 186, 168)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, color, max_w, leading):
    """Draw wrapped paragraph, return y just below the last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- data
HEROES = [
    {
        "kicker": "ULLEUNGDO  •  KOREA",
        "color": RED,
        "head": "Russian jets trigger an air-raid scare off Ulleungdo",
        "body": "Seoul orders islanders to shelter at 07:52 on Tuesday "
                "after aircraft approach Ulleungdo; the warning is "
                "lifted three minutes later. The military says jets "
                "entered the air-defence zone — no airspace violation.",
    },
    {
        "kicker": "WALL STREET  •  MARKETS",
        "color": BLUE,
        "head": "Huang is back — Nvidia soars 31% in a day",
        "body": "Reinstated as CEO 11 days after resigning, Jensen Huang "
                "sparks the best Wall Street day since April 2025: "
                "Nasdaq +6.5%, S&P 500 +4.7%, Dow +1,448 points.",
    },
    {
        "kicker": "GENEVA  •  CHESS",
        "color": GOLD,
        "head": "Game 1: Gukesh defends his crown against Sindarov",
        "body": "The youngest title match in history opens at 15:00 CET: "
                "both players are 20, over 14 games for a $2.5M prize "
                "fund. Sindarov, the challenger, has White.",
    },
]

STATS = [
    ("31%", "Nvidia's one-day jump\non Huang's return"),
    ("$952B", "added in a day —\nbest since 2003"),
    ("24", "dead confirmed in\nSerang, ~30 missing"),
    ("3 min", "Ulleungdo air-raid\nwarning lasted"),
    ("$2.5M", "chess title prize\nfund in Geneva"),
    ("194", "parties at COP31 —\nno fossil-fuel text"),
]

# (place, day-tag, headline, subline)
CARDS = [
    ("SERANG", "TUE", "Search goes on in Serang on Tuesday",
     "600 rescuers; DNA takes 2–3 weeks."),
    ("BRUSSELS", "MON", "NATO sends AWACS to Poland after the missile fall",
     "All 3 objects confirmed Kh-101."),
    ("WELLINGTON", "MON", "India–New Zealand Test ends in a draw",
     "India 720/9 dec; NZ hold on."),
    ("CLIMATE", "MON", "COP31 flop draws backlash and Pacific despair",
     "Guterres disappointed; COP32 next."),
    ("TEHRAN", "MON", "Iran flogs a singer and her team, 74 lashes each",
     "Sentences reported by Iranian site."),
    ("BERLIN", "MON", "Germany to use Kyiv's Delta battle tool",
     "Letter of intent signed with Kyiv."),
    ("TEHRAN", "MON", "Iran vows 'all tools' against US naval blockade",
     "Foreign ministry spokesman Baghaei."),
    ("IOWA", "MON", "Trump halts Army detonation of toxic lead azide",
     "Orders a pause in Iowa this week."),
    ("LIBYA", "SUN", "Ukraine sinks a Russian warship in a Libyan port",
     "Maritime drones; Zelenskyy confirms."),
    ("WASHINGTON", "MON", "Trump: Huang poses no national security threat",
     "Assurance given to Nvidia."),
    ("WASHINGTON", "MON", "US sanctions dozens tied to Iran shadow banking",
     "New sanctions round on networks."),
    ("RUSSIA", "MON", "Murmansk governor detained over embezzlement",
     "Regional governor held by police."),
    ("GAZA", "MON", "Israeli strikes kill three in Gaza, incl. UNRWA worker",
     "UNRWA confirms its staffer killed."),
    ("SPACE", "TUE", "Russia 'could put a nuclear weapon in space in weeks'",
     "Western intelligence warns."),
    ("LUSAKA", "TUE", "Zambia opposition leader charged over coup plot",
     "Charged with seeking to overthrow govt."),
    ("THE HAGUE", "TUE", "Tajikistan becomes fourth country to quit the ICC",
     "Follows the US diplomatic push."),
    ("DHAKA", "TUE", "Bangladesh vows to capture Hasina after India return",
     "Vow follows her return from India."),
    ("COPENHAGEN", "MON", "Denmark's top court backs hardline 'ghetto law'",
     "Immigration law upheld by court."),
    ("DELHI", "TUE", "Modi opens AI centre at IIT Patna",
     "Launches Rs 400-crore research park."),
    ("ARUNACHAL", "TUE", "India, China hold military talks in Arunachal",
     "Commanders meet to ease tensions."),
    ("DELHI", "TUE", "Supreme Court grants bail to Godhra convict",
     "Bail granted on medical grounds."),
    ("TURIN", "SUN", "Alcaraz wins maiden ATP Finals title",
     "Beats Zverev in the Turin final."),
    ("DYMER", "MON", "Dymer rescue continues after drone strike",
     "1–2 dead, 14–15 missing."),
    ("BALTIC", "MON", "Sparta II still burning in the Gulf of Finland",
     "Hit by drones Sat; fire may last days."),
    ("LISBON", "TUE", "Lisbon demo heads to parliament on Tuesday",
     "CGTP rally; inflation 3.8%."),
    ("SCIENCE", "TUE", "Supermoon meets the Seven Sisters tonight",
     "Supermoon aligns with the Pleiades."),
    ("GAZA", "TUE", "Oxfam: Gaza's air, soil and water poisoned for decades",
     "Toxic contamination report out today."),
]

# Dot-matrix map: rough continent blobs as ellipses in map coords.
# Map inner area in pixels: 584 wide x 96 tall (dots step 12).
BLOBS = [
    # (cx, cy, rx, ry) in 0..584 x 0..96 map space
    (70, 52, 62, 36),    # North America
    (128, 84, 32, 14),   # Central America
    (182, 70, 24, 24),   # South America
    (298, 34, 32, 22),   # Europe
    (318, 66, 40, 28),   # Africa
    (428, 40, 88, 30),   # Asia
    (516, 86, 28, 12),   # Oceania
]
# (label, px, py, label_dx, label_dy) — label offset keeps text in-bounds
PINS = [
    ("Helsinki", 312, 12, 8, -6),
    ("Brussels", 292, 28, -64, 10),
    ("Dymer", 316, 30, 8, -6),
    ("Geneva", 296, 44, -58, 12),
    ("Gaza", 352, 58, 8, -6),
    ("Lusaka", 330, 80, 8, -6),
    ("Delhi", 442, 54, 8, 10),
    ("Ulleungdo", 508, 44, -72, -6),
    ("Serang", 488, 88, -52, -6),
]

DATE_CHECK = (
    "DATE CHECK — Tuesday is only hours old in most time zones, so "
    "verified all-Tuesday news is still thin. The leads are confirmed "
    "Tuesday events; Monday items are marked MON — context only, never "
    "presented as 24 Nov news."
)


# ---------------------------------------------------------------- draw
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Frame
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([22, 22, W - 23, H - 23], outline=LINE, width=1)

    # ---- Masthead
    d.text((W // 2, 34), "THE DAILY ORBIT", font=font(SERIF, 56),
           fill=INK, anchor="ma")
    rule(d, 60, 108, W - 60, RED, 3)
    d.text((W // 2, 118), "TUESDAY 24 NOVEMBER 2026   •   30 STORIES   •   ONE PAGE",
           font=font(SANS_B, 15), fill=INK_SOFT, anchor="ma")

    # ---- Hero row: three columns
    hx, hy, hw, hh, gap = 40, 146, 304, 190, 16
    for i, hero in enumerate(HEROES):
        x = hx + i * (hw + gap)
        d.rounded_rectangle([x, hy, x + hw, hy + hh], radius=6,
                            fill=CARD, outline=LINE, width=1)
        d.rectangle([x, hy, x + hw, hy + 6], fill=hero["color"])
        y = hy + 18
        d.text((x + 14, y), hero["kicker"], font=font(SANS_B, 12),
               fill=hero["color"])
        y += 22
        y = para(d, (x + 14, y), hero["head"], font(SANS_B, 19), INK,
                 hw - 28, 22)
        y += 6
        end_y = para(d, (x + 14, y), hero["body"], font(SANS, 12), INK_SOFT,
                     hw - 28, 15)
        if end_y > hy + hh - 6:
            print("WARNING hero", i, "overflow:", end_y, "vs", hy + hh)

    # ---- Stats strip
    sy, sh = 348, 72
    sw = (W - 80 - 5 * 10) / 6
    for i, (num, label) in enumerate(STATS):
        x = 40 + i * (sw + 10)
        d.rounded_rectangle([x, sy, x + sw, sy + sh], radius=6,
                            fill=INK, outline=INK)
        d.text((x + sw / 2, sy + 8), num, font=font(SANS_B, 24),
               fill=(255, 255, 255), anchor="ma")
        for j, line in enumerate(label.split("\n")):
            d.text((x + sw / 2, sy + 40 + j * 13), line,
                   font=font(SANS, 10), fill=(214, 210, 198), anchor="ma")

    # ---- Dot-matrix map
    mx0, my0, mx1, my1 = 40, 450, 640, 570
    d.text((mx0, 430), "WHERE IT HAPPENED — 9 PINS",
           font=font(SANS_B, 12), fill=INK)
    d.rounded_rectangle([mx0, my0, mx1, my1], radius=6,
                        fill=CARD, outline=LINE, width=1)
    ox, oy = mx0 + 8, my0 + 8
    for gx in range(0, 584, 12):
        for gy in range(0, 96, 12):
            inside = any(((gx - cx) / rx) ** 2 + ((gy - cy) / ry) ** 2 <= 1
                         for cx, cy, rx, ry in BLOBS)
            if inside:
                d.ellipse([ox + gx - 2, oy + gy - 2, ox + gx + 2, oy + gy + 2],
                          fill=(150, 158, 172))
    for name, px, py, ldx, ldy in PINS:
        cx, cy = ox + px, oy + py
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((cx + ldx, cy + ldy), name, font=font(SANS_B, 10), fill=RED)

    # ---- Date check box
    bx0, by0, bx1, by1 = 664, 450, 984, 570
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=6,
                        fill=(255, 244, 224), outline=GOLD, width=2)
    d.text((bx0 + 14, by0 + 12), "DATE CHECK", font=font(SANS_B, 13),
           fill=GOLD)
    end_y = para(d, (bx0 + 14, by0 + 34), DATE_CHECK, font(SANS, 11),
                 INK_SOFT, bx1 - bx0 - 28, 14)
    if end_y > by1 - 6:
        print("WARNING date-check overflow:", end_y, "vs", by1)

    # ---- Cards grid: 3 columns x 9 rows
    rule(d, 40, 582, W - 40, INK, 2)
    d.text((40, 590), "THE REST OF THE DAY — 27 MORE STORIES",
           font=font(SANS_B, 13), fill=INK)
    d.text((W - 40, 590), "4–30", font=font(SANS_B, 13), fill=RED,
           anchor="ra")
    cw = 304
    gy0 = 614
    head_f = font(SANS_B, 11)
    sub_f = font(SANS, 10)
    tag_f = font(SANS_B, 9)
    for i, (place, day, head, sub) in enumerate(CARDS):
        col, row = i % 3, i // 3
        x = 40 + col * (cw + 16)
        y = gy0 + row * 40
        d.text((x, y), f"{i + 4:>2}.", font=font(SANS_B, 11), fill=RED)
        tx = x + 26
        # Headline, wrapped to at most 2 lines inside the column.
        lines = wrap(d, head, head_f, cw - 26)[:2]
        for j, line in enumerate(lines):
            d.text((tx, y + j * 13), line, font=head_f, fill=INK)
        # Subline: place/day tag first, then the summary, truncated.
        sy2 = y + len(lines) * 13 + 2
        tag_txt = f"{place} · {day}  "
        d.text((tx, sy2), tag_txt, font=tag_f, fill=RED)
        tag_w = d.textlength(tag_txt, font=tag_f)
        avail = cw - 26 - tag_w
        shown = sub
        while shown and d.textlength(shown + "…", font=sub_f) > avail:
            shown = shown[:-1]
        if shown != sub:
            shown += "…"
        d.text((tx + tag_w, sy2), shown, font=sub_f, fill=INK_SOFT)

    # ---- Footer
    rule(d, 40, 984, W - 40, LINE, 1)
    d.text((40, 990), "THE DAILY ORBIT — drawn from verified wire reporting; "
                        "weekend items are marked with their day.",
           font=font(SANS, 10), fill=INK_SOFT)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
