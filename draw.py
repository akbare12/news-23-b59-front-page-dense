#!/usr/bin/env python3
"""news-23 b59 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"

def f(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: f("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: f("DejaVuSans-Bold.ttf", s)
SANS = lambda s: f("DejaVuSans.ttf", s)

BLACK = (17, 17, 17)
WHITE = (255, 255, 255)
GOLD = (212, 160, 23)
GOLD_L = (232, 185, 35)
RED = (185, 28, 28)
TEAL = (13, 148, 136)
TEAL_D = (15, 118, 110)
BLUE = (37, 99, 235)
NAVY = (11, 30, 58)
PURPLE = (124, 58, 237)
GREEN = (21, 128, 61)
CREAM = (250, 247, 232)
GRAY = (107, 114, 128)
LGRAY = (229, 231, 235)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

def tw(font, s):
    return d.textlength(s, font=font)

def wrap(text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(font, t) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(x, y, label, color):
    """Small rounded-ish chip; returns width."""
    ft = SANS_B(8)
    w = int(tw(ft, label)) + 10
    d.rectangle([x, y, x + w, y + 12], fill=color)
    d.text((x + 5, y + 2), label, font=ft, fill=WHITE)
    return w

# ---------------- masthead ----------------
d.rectangle([0, 0, W, 56], fill=BLACK)
d.text((14, 8), "THE WORLD TODAY", font=SERIF_B(34), fill=WHITE)
d.text((W - 14 - tw(SANS_B(15), "MONDAY 23 NOVEMBER 2026"), 20),
       "MONDAY 23 NOVEMBER 2026", font=SANS_B(15), fill=GOLD_L)

# ---------------- kicker ----------------
d.text((14, 60), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
       font=SANS_B(13), fill=RED)

# ---------------- number strip: 2 rows x 5 cols ----------------
nums = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", BLUE),
    ("11,762", "EBOLA CASES, DRC", GREEN), ("10T won", "SEOUL STABILISATION FUND", (180, 130, 29)),
    ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE),
    ("$450M", "SKUBAL DEAL", PURPLE), ("165", "RUSSIAN MISSILES/WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", BLUE), ("264 kg", "EXPLOSIVES SEIZED", (180, 130, 29)),
    ("$107.3B", "ANTHROPIC IPO", PURPLE),
]
cw = W // 5
for i, (num, lab, col) in enumerate(nums):
    r, c = divmod(i, 5)
    x = c * cw + 12
    y = 80 + r * 31
    d.text((x, y), num, font=SANS_B(19), fill=col)
    d.text((x, y + 21), lab, font=SANS_B(9), fill=BLACK)

# ---------------- region bar ----------------
regs = [("ASIA-PACIFIC 7", TEAL, 168), ("AMERICAS 8", BLUE, 168),
        ("MIDDLE EAST 6", (180, 130, 29), 168), ("EUROPE 5", PURPLE, 168),
        ("AFRICA 3", RED, 168), ("WORLD 2", GRAY, 184)]
x = 0
for name, col, w in regs:
    d.rectangle([x, 142, x + w, 160], fill=col)
    d.text((x + 8, 145), name, font=SANS_B(11), fill=WHITE)
    x += w

# ---------------- UTC strip ----------------
d.text((14, 164), "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
       font=SANS(11), fill=BLACK)
d.text((W - 14 - tw(SANS(10), "~ APPROX"), 165), "~ APPROX", font=SANS(10), fill=GRAY)

# ---------------- hero scenes ----------------
HX = [14, 352, 690]
HW = 320
HY = 182
SC_H = 118

def scene_kospi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # skyline: solid buildings with lit windows
    import random
    rnd = random.Random(7)
    bx = x + 8
    while bx < x + w - 30:
        bw = rnd.randint(22, 38)
        bh = rnd.randint(34, h - 30)
        by = y + h - bh
        d.rectangle([bx, by, bx + bw, y + h], fill=(23, 48, 88))
        for wy in range(by + 6, y + h - 6, 10):
            for wx in range(bx + 4, bx + bw - 4, 9):
                if rnd.random() < 0.45:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 6
    # chart line
    pts = [(x + 14, y + 52), (x + 60, y + 30), (x + 110, y + 58), (x + 160, y + 34),
           (x + 210, y + 44), (x + 260, y + 20), (x + 306, y + 26)]
    d.line(pts, fill=(255, 170, 60), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 190, 90), outline=(255, 255, 255))
    d.text((x + 12, y + 8), "-3.3%", font=SANS_B(30), fill=(255, 80, 80))

def scene_guterres(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=TEAL_D)
    yy = y + 14
    for ln in ["150 DELEGATES", "BACK A RISK", "FRAMEWORK"]:
        d.text((x + 12, yy), ln, font=SANS_B(24), fill=GOLD_L)
        yy += 30
    # globe
    cx, cy, r = x + w - 30, y + h - 34, 22
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=WHITE, width=1)
    d.line([cx - r, cy, cx + r, cy], fill=WHITE, width=1)
    d.line([cx - r + 8, cy - r + 12, cx + r - 8, cy - r + 12], fill=WHITE, width=1)
    d.line([cx - r + 8, cy + r - 12, cx + r - 8, cy + r - 12], fill=WHITE, width=1)

def scene_power(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CREAM)
    d.text((x + 12, y + 8), "NARROWEST SINCE 2018", font=SANS_B(12), fill=BLACK)
    d.text((x + w - 12 - tw(SANS_B(12), "GAP 5.3"), y + 8), "GAP 5.3", font=SANS_B(12), fill=(180, 130, 29))
    bars = [("78.9", "US", NAVY, 70), ("73.6", "CHINA", RED, 64), ("40.5", "INDIA", (180, 130, 29), 38)]
    bx = x + 30
    for val, lab, col, bh in bars:
        d.text((bx + 18 - tw(SANS_B(15), val) // 2, y + 34), val, font=SANS_B(15), fill=BLACK)
        d.rectangle([bx, y + 54, bx + 56, y + 54 + bh], fill=col)
        d.text((bx + 28 - tw(SANS_B(10), lab) // 2, y + 54 + bh - 16), lab, font=SANS_B(10), fill=WHITE)
        bx += 92

scenes = [scene_kospi, scene_guterres, scene_power]
for sx, fn in zip(HX, scenes):
    fn(sx, HY, HW, SC_H)

heroes = [
    ("KOSPI 4,708.54   \u00b7   -161 PTS", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", "REPORTED", BLUE),
    ("UN   \u00b7   BRIDGETOWN", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "UNITED NATIONS", "REPORTED", BLUE),
    ("ASIA POWER INDEX 2026", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED", BLUE),
]
for i, (bar, head, body, src, chip_lab, chip_col) in enumerate(heroes):
    x = HX[i]
    # black label bar under scene
    d.rectangle([x, HY + SC_H, x + HW, HY + SC_H + 18], fill=BLACK)
    d.text((x + 8, HY + SC_H + 3), bar, font=SANS_B(10), fill=WHITE)
    # headline (2 lines max), clear of the strip above
    hy = HY + SC_H + 24
    hlines = wrap(head, SANS_B(19), HW)
    for j, ln in enumerate(hlines[:2]):
        d.text((x, hy + j * 20), ln, font=SANS_B(19), fill=BLACK)
    by = hy + len(hlines[:2]) * 20 + 3
    blines = wrap(body, SANS(11), HW)
    for j, ln in enumerate(blines[:2]):
        d.text((x, by + j * 13), ln, font=SANS(11), fill=BLACK)
    sy = by + len(blines[:2]) * 13 + 5
    d.text((x, sy), src, font=SANS(10), fill=GRAY)
    chip(x + HW - 62, sy - 1, chip_lab, chip_col)

# ---------------- MORE OF THE DAY bar ----------------
d.rectangle([0, 414, W, 434], fill=BLACK)
d.text((14, 418), "MORE OF THE DAY  \u2014  10 STORIES", font=SANS_B(13), fill=WHITE)

# ---------------- cards: 2 rows x 5 cols ----------------
cards = [
    ("AMERICAS", TEAL, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED", BLUE),
    ("FBI", RED, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", BLUE),
    ("WHITE HOUSE", (180, 130, 29), "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", BLUE),
    ("MARKETS", BLUE, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED", BLUE),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", BLUE),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED", BLUE),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED", BLUE),
    ("TECH", PURPLE, "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED", BLUE),
    ("EUROPE", PURPLE, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM", RED),
    ("SPACE", GRAY, "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", RED),
]
CW2 = 204
CH2 = 71
for i, (cat, tcol, head, body, src, chip_lab, chip_col) in enumerate(cards):
    r, c = divmod(i, 5)
    x = c * CW2 + 4
    y = 438 + r * CH2
    # tab header
    d.rectangle([x, y, x + CW2 - 8, y + 16], fill=tcol)
    d.text((x + 6, y + 3), cat, font=SANS_B(9), fill=WHITE)
    d.text((x + CW2 - 8 - 12 - tw(SANS_B(9), str(i + 1)), y + 3), str(i + 1), font=SANS_B(9), fill=WHITE)
    hlines = wrap(head, SANS_B(11), CW2 - 12)
    for j, ln in enumerate(hlines[:2]):
        d.text((x, y + 19 + j * 13), ln, font=SANS_B(11), fill=BLACK)
    d.text((x, y + 46), body, font=SANS(9), fill=BLACK)
    d.text((x, y + 60), src, font=SANS(8), fill=GRAY)
    chip(x + CW2 - 8 - 62, y + 59, chip_lab, chip_col)

# ---------------- map + ALSO bars ----------------
d.rectangle([0, 580, 336, 600], fill=BLACK)
d.text((14, 584), "WHERE IT HAPPENED", font=SANS_B(12), fill=WHITE)
d.rectangle([344, 580, W, 600], fill=BLACK)
d.text((358, 584), "ALSO ON MONDAY", font=SANS_B(12), fill=WHITE)

# map: simplified continents
d.rectangle([14, 606, 322, 780], fill=(245, 245, 240))
for gx in range(14, 322, 12):
    d.line([gx, 606, gx, 780], fill=(235, 235, 228), width=1)
for gy in range(606, 780, 12):
    d.line([14, gy, 322, gy], fill=(235, 235, 228), width=1)
d.ellipse([30, 640, 170, 760], fill=(190, 225, 170))   # Americas blob
d.ellipse([170, 620, 300, 730], fill=(190, 225, 170))  # Eurasia blob
d.ellipse([90, 752, 200, 786], fill=(190, 225, 170))   # SE Asia / Oceania blob
pins = [(44, 664, 1), (86, 742, 2), (252, 636, 3), (52, 700, 4), (110, 668, 5),
        (236, 700, 6), (66, 640, 7), (40, 724, 8), (76, 748, 9), (150, 752, 10),
        (196, 648, 11), (222, 664, 12), (262, 660, 13)]
for px, py, n in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    d.text((px - 3 if n < 10 else px - 6, py - 6), str(n), font=SANS_B(9), fill=WHITE)
d.text((14, 786), "Pins 1\u201313:  1 Seoul  \u00b7  2 Bridgetown  \u00b7  3 Beijing", font=SANS(9), fill=BLACK)
d.text((14, 798), "4 Washington  \u00b7  5 New York  \u00b7  6 Tehran  \u00b7  7 Chicago", font=SANS(9), fill=BLACK)
d.text((14, 810), "8 SF  \u00b7  9 Denver  \u00b7  10 Austin  \u00b7  11 Warsaw  \u00b7  12 Kyiv  \u00b7  13 Moscow", font=SANS(9), fill=BLACK)

# ALSO list: 18 items, 2 columns x 9
also = [
    "Paris: 100+ back 2% billionaire tax", "Manchester: 12,000 cleared",
    "Zelenskyy: 165 missiles in a week", "COP31: the day after pact rejected",
    "Benghazi: UN demands port probe", "Israel unity talks resume",
    "Gaza: two killed in Israeli strike", "West Bank settler attacks",
    "Iran war: no deal in sight", "Lebanon seizes 264 kg explosives",
    "Bahrain: strike hits plant, 2 hurt", "Sudan: defences down drones",
    "DRC: fighting traps Ebola teams", "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits in exam row", "SK Telecom -7.3% as hype cools",
    "China eases margin rules", "Seoul readies 10T-won fund",
]
for i, item in enumerate(also):
    col = i // 9
    row = i % 9
    x = 358 + col * 330
    y = 610 + row * 22
    d.text((x, y), f"{14 + i}. {item}", font=SANS(11), fill=BLACK)

# ---------------- DATE CHECK ----------------
d.rectangle([10, 826, W - 10, 916], outline=RED, width=2)
d.text((20, 832), "DATE CHECK", font=SANS_B(13), fill=RED)
d.text((W - 20 - tw(SANS_B(9), "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY"), 835),
       "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", font=SANS_B(9), fill=RED)
dc1 = "LEFT OUT \u2014 NOT 23 NOV:  Democrats reach 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)  \u00b7  EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar ruling (19 Nov)"
for j, ln in enumerate(wrap(dc1, SANS(11), W - 40)):
    d.text((20, 854 + j * 14), ln, font=SANS(11), fill=BLACK)
d.text((20, 886), "NOT YET:  Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
       font=SANS(11), fill=BLACK)

# ---------------- footer ----------------
d.text((14, 924), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=SANS(10), fill=GRAY)
d.text((14, 940), "CHIPS: REPORTED = confirmed by wires  \u00b7  CLAIM = one side's claim, not independently confirmed  \u00b7  ONGOING = still developing.",
       font=SANS(10), fill=GRAY)
d.text((14, 956), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=SANS(10), fill=GRAY)

# ---------------- bottom strip ----------------
d.rectangle([0, 990, W, 1024], fill=BLACK)
bt = "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((W - tw(SANS_B(14), bt)) // 2, 1001), bt, font=SANS_B(14), fill=GOLD_L)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
