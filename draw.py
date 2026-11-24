#!/usr/bin/env python3
"""THE DAILY ORBIT - poster renderer for Tuesday 24 November 2026.

Draws a one-page broadsheet (1024x1024) that sums up the day's world
news: a masthead, a strip of the day's key numbers, three hero stories,
a 27-card grid of the remaining stories, a schematic dot-matrix world
map with pins, and a DATE CHECK box explaining the date discipline.

Rendering is fully deterministic: fixed geometry, fixed fonts, no
randomness, no timestamps. Two runs produce byte-identical entry.png.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
W = H = 1024
PAPER = (246, 240, 226)
CARD_BG = (255, 252, 244)
INK = (26, 22, 16)
FAINT = (96, 88, 74)
RULE = (60, 52, 40)
RED = (163, 22, 33)
NAVY = (23, 58, 94)
GOLD = (166, 124, 22)
BAND_DARK = (30, 27, 22)
TAG_TUE = (163, 22, 33)
TAG_CTX = (110, 100, 84)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

_cache = {}


def fnt(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def text_w(dr, s, font):
    return dr.textlength(s, font=font)


def wrap(dr, s, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(dr, trial, font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(dr, x, y, s, font, fill, width, leading, max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(dr, s, font, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        dr.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def centered(dr, cx, y, s, font, fill):
    dr.text((cx - text_w(dr, s, font) / 2, y), s, font=font, fill=fill)


# ---------------------------------------------------------------- content
HEROES = [
    {
        "place": "ULLEUNGDO, SOUTH KOREA",
        "tag": "TUE",
        "color": RED,
        "head": "AIR ALERT AT 07:52, LIFTED IN 3 MINUTES",
        "body": ("Russian military jets entered the KADIZ off Ulleungdo. "
                 "An evacuation alert went out at 07:52 and was lifted "
                 "about three minutes later. Seoul's JCS: no airspace "
                 "violation; ROK fighters scrambled."),
    },
    {
        "place": "GENEVA, SWITZERLAND",
        "tag": "TUE",
        "color": NAVY,
        "head": "YOUNGEST WORLD CHESS FINAL OPENS",
        "body": ("Champion Gukesh meets challenger Sindarov - both are "
                 "20, the youngest title match in history. Game 1 at "
                 "15:00 CET, Sindarov with White; 14 games, a $2.5M "
                 "prize fund."),
    },
    {
        "place": "WALL STREET",
        "tag": "MON",
        "color": GOLD,
        "head": "HUANG RETURNS - NVIDIA LEAPS 31%",
        "body": ("Nvidia's board reinstated Jensen Huang as CEO, 11 days "
                 "after he quit. Shares jumped 31% - $952B added in a "
                 "day; the Nasdaq rose 6.5%, its best day since "
                 "April 2025."),
    },
]

# (place, day tag, headline, one-breath summary)
CARDS = [
    ("SERANG", "TUE", "Factory-fire search goes on",
     "24 dead, ~30 missing after Saturday's Cikande blaze; DNA ID takes 2-3 weeks."),
    ("POLAND", "MON", "Kh-101s confirmed, AWACS sent",
     "All 3 objects were Russian missiles; NATO reinforces, no Article 4."),
    ("CRICKET", "MON", "India-NZ Test ends in a draw",
     "India's 720/9 declared is a record in NZ; the hosts hold out on day five."),
    ("COP31", "MON", "Climate talks end in letdown",
     "Guterres 'deeply disappointed'; focus shifts to COP32 in Addis Ababa."),
    ("IRAN", "MON", "Singer lashed 74 times",
     "A singer and four production staff each received 74 lashes."),
    ("GERMANY", "MON", "Bundeswehr adopts Kyiv's Delta",
     "Letter of intent: Germany will use Ukraine's battle-management system."),
    ("TEHRAN", "MON", "Iran vows 'all tools' vs blockade",
     "Foreign ministry spokesman answers the US naval blockade threat."),
    ("IOWA", "MON", "Trump halts lead-azide blasts",
     "Army ordered to pause detonating toxic explosive stockpiles."),
    ("LIBYA", "SUN", "Ukraine sinks Russian corvette",
     "Naval drones hit the ship at Benghazi; Zelenskyy confirms the strike."),
    ("WASHINGTON", "MON", "Trump clears Huang on security",
     "President assures Nvidia its CEO is no national-security threat."),
    ("SANCTIONS", "MON", "US hits Iran shadow banking",
     "Dozens of parties sanctioned over Tehran's covert finance network."),
    ("MURMANSK", "MON", "Governor held in graft probe",
     "Regional governor detained on suspicion of embezzlement."),
    ("GAZA", "MON", "Strike kills UNRWA staffer",
     "At least three dead in an Israeli strike, incl. a UN agency worker."),
    ("ORBIT", "TUE", "Nukes in orbit 'within weeks'?",
     "Western intelligence warns Russia could orbit nuclear weapons soon."),
    ("ZAMBIA", "TUE", "Opposition chief charged",
     "Leader accused of plotting to overthrow the government."),
    ("THE HAGUE", "TUE", "Tajikistan quits the ICC",
     "Fourth state to leave the court, after a US diplomatic push."),
    ("DHAKA", "TUE", "Bangladesh vows Hasina arrest",
     "Government promises to detain the ex-PM on her return from India."),
    ("DENMARK", "MON", "Court backs 'ghetto law'",
     "High court upholds the hardline immigration statute."),
    ("DELHI", "TUE", "Modi opens AI park at IIT Patna",
     "A 400-crore-rupee research park inaugurated by the prime minister."),
    ("ARUNACHAL", "TUE", "India-China commanders talk",
     "Border commanders meet to ease tensions along the frontier."),
    ("GODHRA", "TUE", "Bail on medical grounds",
     "Supreme Court grants bail in the Godhra case, citing health."),
    ("DYMER", "MON", "Rescue search continues",
     "1-2 dead, 14-15 missing, including two children."),
    ("BALTIC", "SAT", "Sparta II still ablaze",
     "Russian cargo ship burns in the Gulf of Finland after drone hits."),
    ("LISBON", "TUE", "March on parliament",
     "CGTP unions protest as inflation runs at 3.8%."),
    ("TONIGHT", "TUE", "Supermoon meets the Pleiades",
     "The full moon crosses the Seven Sisters in tonight's sky."),
    ("GAZA REPORT", "TUE", "Oxfam: poisoned for decades",
     "Air, soil and water contamination documented in a new report."),
    ("TURIN", "SUN", "Alcaraz takes ATP Finals",
     "First year-end title for the Spaniard, beating Zverev in the final."),
]

STATS = [
    ("+31%", "NVIDIA IN A DAY"),
    ("$952B", "VALUE ADDED"),
    ("24", "DEAD AT SERANG"),
    ("3 MIN", "THE ALERT STOOD"),
    ("$2.5M", "CHESS PRIZE FUND"),
    ("+1,448", "DOW POINTS"),
]

# Schematic dot-matrix world: '#' is land. Rough shapes only.
MAP_ROWS = [
    "                                                  ",
    "  #######          ######################         ",
    " #########        ########################       ",
    "  ########         ######################         ",
    "   ######    ##     #################             ",
    "    ####    ########    ###########    ##         ",
    "     ##    ##########      #######    ####        ",
    "          ############       #####   ######       ",
    "           ##########         ###   ########      ",
    "            ########           ##    ########     ",
    "             ######                   ######      ",
    "              ####                     ####       ",
    "               ##                                   ",
]
# (col, row) pins on the schematic map
PINS = [(6, 2), (23, 4), (24, 3), (30, 1), (27, 5), (30, 5),
        (32, 4), (35, 5), (43, 3), (39, 7)]
PIN_LEGEND = ("PINS: IOWA, LISBON, GENEVA, MURMANSK, BENGHAZI, GAZA, "
              "TEHRAN, DELHI, ULLEUNGDO, SERANG")

DATE_CHECK = (
    "DATE CHECK - This page sums up Tuesday 24 November 2026. Stories "
    "tagged TUE happened, or were first reported, today. Items tagged "
    "MON, SUN or SAT are background from the days just before, included "
    "only where today's story needs them - never passed off as today's "
    "news."
)


# ---------------------------------------------------------------- drawing
MARGIN = 30


def masthead(dr):
    centered(dr, W / 2, 26, "ONE PAGE - THE WHOLE DAY - EVERY CONTINENT",
             fnt(SANS, 11), FAINT)
    centered(dr, W / 2, 44, "THE DAILY ORBIT", fnt(SERIF_B, 62), INK)
    dr.line([(MARGIN, 122), (W - MARGIN, 122)], fill=INK, width=3)
    dr.line([(MARGIN, 127), (W - MARGIN, 127)], fill=INK, width=1)
    # date band
    dr.rectangle([MARGIN, 134, W - MARGIN, 168], fill=BAND_DARK)
    centered(dr, W / 2, 140, "TUESDAY  -  24 NOVEMBER 2026",
             fnt(SANS_B, 20), (250, 246, 235))
    dr.text((W - MARGIN - text_w(dr, "VOL. II - NO. 24", fnt(SANS, 10)),
             176), "VOL. II - NO. 24", font=fnt(SANS, 10), fill=FAINT)
    dr.text((MARGIN, 176), "SOURCES: REUTERS - AP - KBS - CHESS.COM - TOI",
            font=fnt(SANS, 10), fill=FAINT)


def stats_strip(dr):
    y0, y1 = 194, 252
    dr.rectangle([MARGIN, y0, W - MARGIN, y1], outline=RULE, width=1)
    colw = (W - 2 * MARGIN) / len(STATS)
    for i, (num, label) in enumerate(STATS):
        cx = MARGIN + colw * (i + 0.5)
        centered(dr, cx, y0 + 8, num, fnt(SERIF_B, 25), RED if i % 2 == 0 else NAVY)
        centered(dr, cx, y0 + 40, label, fnt(SANS_B, 8), FAINT)
        if i:
            x = MARGIN + colw * i
            dr.line([(x, y0 + 8), (x, y1 - 8)], fill=(205, 196, 178), width=1)


def hero(dr, x, y, w, h, item):
    dr.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=RULE, width=1)
    dr.rectangle([x, y, x + w, y + 26], fill=item["color"])
    dr.text((x + 10, y + 7), item["place"], font=fnt(SANS_B, 10),
            fill=(255, 255, 255))
    tag = item["tag"]
    tw = text_w(dr, tag, fnt(SANS_B, 10))
    dr.text((x + w - 10 - tw, y + 7), tag, font=fnt(SANS_B, 10),
            fill=(255, 255, 255))
    yy = block(dr, x + 10, y + 36, item["head"], fnt(SERIF_B, 16), INK,
               w - 20, 20)
    dr.line([(x + 10, yy + 2), (x + 52, yy + 2)], fill=item["color"], width=2)
    block(dr, x + 10, yy + 9, item["body"], fnt(SANS, 11), (52, 47, 38),
          w - 20, 15)


def heroes(dr):
    y, h, gap = 264, 196, 12
    w = (W - 2 * MARGIN - 2 * gap) / 3
    for i, item in enumerate(HEROES):
        hero(dr, MARGIN + i * (w + gap), y, w, h, item)


def cards(dr):
    y0, rows, gap = 482, 9, 5
    cols = 3
    cw = (W - 2 * MARGIN - (cols - 1) * gap) / cols
    ch = 40
    head_f, body_f, tag_f = fnt(SANS_B, 11), fnt(SANS, 9), fnt(SANS_B, 8)
    for idx, (place, tag, head, body) in enumerate(CARDS):
        r, c = divmod(idx, cols)
        x = MARGIN + c * (cw + gap)
        y = y0 + r * (ch + gap)
        dr.rectangle([x, y, x + cw, y + ch], fill=CARD_BG,
                     outline=(205, 196, 178), width=1)
        tag_col = TAG_TUE if tag == "TUE" else TAG_CTX
        dr.text((x + 7, y + 4), place + " ", font=tag_f, fill=tag_col)
        px = x + 7 + text_w(dr, place + " ", tag_f)
        dr.text((px, y + 4), "- " + head, font=head_f, fill=INK)
        tw = text_w(dr, tag, tag_f)
        dr.text((x + cw - 6 - tw, y + 4), tag, font=tag_f, fill=tag_col)
        block(dr, x + 7, y + 18, body, body_f, (62, 56, 46), cw - 13, 11,
              max_lines=2)


def world_map(dr, x, y):
    cell = 6
    dot_f = (150, 138, 112)
    for r, row in enumerate(MAP_ROWS):
        for c, ch in enumerate(row):
            if ch == "#":
                cx, cy = x + c * cell, y + r * cell
                dr.ellipse([cx + 1, cy + 1, cx + 4, cy + 4], fill=dot_f)
    for c, r in PINS:
        cx, cy = x + c * cell + 3, y + r * cell + 3
        dr.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED,
                   outline=(255, 252, 244), width=1)
    ly = y + len(MAP_ROWS) * cell + 5
    dr.text((x, ly), "WHERE TODAY HAPPENED - SCHEMATIC MAP, DRAWN IN PYTHON",
            font=fnt(SANS_B, 9), fill=FAINT)
    dr.text((x, ly + 13), PIN_LEGEND, font=fnt(SANS, 8), fill=FAINT)


def bottom_band(dr):
    y = 898
    dr.line([(MARGIN, y - 8), (W - MARGIN, y - 8)], fill=INK, width=2)
    world_map(dr, MARGIN + 4, y)
    # date check box on the right
    bx = 520
    dr.rectangle([bx, y, W - MARGIN, y + 92], fill=(238, 230, 210),
                 outline=RULE, width=1)
    dr.text((bx + 12, y + 9), "HOW TO READ THE TAGS",
            font=fnt(SANS_B, 11), fill=RED)
    block(dr, bx + 12, y + 28, DATE_CHECK, fnt(SANS, 10), (52, 47, 38),
          W - MARGIN - bx - 24, 13, max_lines=5)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    dr = ImageDraw.Draw(img)
    dr.rectangle([8, 8, W - 8, H - 8], outline=INK, width=2)
    dr.rectangle([14, 14, W - 14, H - 14], outline=(150, 138, 112), width=1)
    masthead(dr)
    stats_strip(dr)
    heroes(dr)
    centered(dr, W / 2, 464, "- THE REST OF THE DAY -", fnt(SANS_B, 11),
             FAINT)
    cards(dr)
    bottom_band(dr)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
