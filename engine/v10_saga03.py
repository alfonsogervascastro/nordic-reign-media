"""The Norse Saga, Ep. 3 — Yggdrasil. Sources: Prose Edda, Gylfaginning 15–16; Grímnismál 31–35.
Art: Oluf Olufsen Bagge, "Yggdrasil, The Mundane Tree" (1847), shown whole and in three details."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 38.4
SRC = "../images/bagge_yggdrasil_1847.jpg"
FULL = nr.Painting(SRC, 740, 820, cy=1040, zoom=0.08, feather=0.10)
CROWN = nr.Painting(SRC, 980, 760, cy=960, crop=(120, 0, 780, 330), zoom=0.10, feather=0.12)
DISC = nr.Painting(SRC, 1000, 560, cy=960, crop=(60, 250, 860, 560), zoom=0.10, feather=0.12)
ROOTS = nr.Painting(SRC, 900, 760, cy=960, crop=(230, 640, 730, 999), zoom=0.10, feather=0.12)
END = nr.TattooEnd("../tattoos/out/ep03_yggdrasil/ep03_yggdrasil_gold.png", t0=35.2)

def wells(img, t, op):
    """Three glowing wells, lit one by one (atmosphere only)."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    spots = [(250, 1250, (150, 175, 200), 13.0), (W / 2, 1300, (224, 164, 74), 14.6), (W - 250, 1250, (200, 225, 245), 16.2)]
    for x, y, col, t0 in spots:
        k = op * ease((t - t0) / 0.8)
        d.ellipse([x - 110, y - 34, x + 110, y + 34], fill=col + (int(170 * k),))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(22)))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for x, y, col, t0 in spots:
        k = op * ease((t - t0) / 0.8)
        d.ellipse([x - 90, y - 22, x + 90, y + 22], outline=col + (int(255 * k),), width=4)
    img.alpha_composite(lay)

cards = [
    Card(-0.8, 4.6, 330, [T("One tree", 76), T("holds all nine worlds.", 76, GOLD)]),
    Card(0.8, 4.6, 1490, [B("Art: Oluf O. Bagge, 1847", 30)]),
    Card(4.8, 8.8, 330, [B("Yggdrasil, the greatest of all trees.", 54, LIGHT), B("Its branches spread over every world", 50), B("and reach above the sky.", 50)]),
    Card(9.0, 12.6, 330, [T("Three roots.", 72), T("Three wells.", 72, GOLD)]),
    Card(12.8, 18.4, 400, [T("Hvergelmir", 60, LIGHT), B("the seething spring, in the cold mist", 42)]),
    Card(14.4, 18.4, 640, [T("Mímir's well", 60, GOLD), B("wisdom itself, among the giants", 42)]),
    Card(16.0, 18.4, 880, [T("Urðr's well", 60, LIGHT), B("where the gods hold court each day", 42)]),
    Card(18.6, 22.6, 330, [B("An eagle sits at the top.", 58, LIGHT), B("A dragon, Níðhöggr, gnaws the roots.", 52)]),
    Card(22.8, 26.8, 330, [B("And a squirrel, Ratatoskr,", 58, LIGHT), B("runs up and down the trunk", 52), B("carrying insults between them.", 52, GOLD)]),
    Card(27.0, 31.0, 330, [B("Four stags eat its leaves.", 58, LIGHT), B("Its side is rotting.", 58, LIGHT)]),
    Card(28.6, 31.0, 1460, [B("Source: Prose Edda, Gylfaginning; Grímnismál", 32)]),
    Card(31.2, 35.0, 330, [B("Every day the Norns", 58, LIGHT), B("water it from their well", 58, LIGHT), T("so it will not die.", 64, GOLD)]),
    Card(32.6, 35.0, 1300, [B("Next: the first humans,", 52, LIGHT), B("carved from two trees.", 52, LIGHT)]),
    Card(33.4, 35.0, 1480, [B("Episode 4: Wednesday  ·  " + nr.HANDLE, 40)]),
]

LABEL = nr.Label("THE NORSE SAGA", "EP. 3")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    FULL.draw(img, t, 0.0, window(t, -1.0, 9.0, 0.6), dur=9.0)
    wells(img, t, window(t, 9.0, 18.6, 0.6))
    ROOTS.draw(img, t, 9.0, window(t, 9.0, 12.8, 0.5) * 0.9, dur=3.8)
    CROWN.draw(img, t, 18.6, window(t, 18.6, 27.0, 0.6), dur=8.4)
    DISC.draw(img, t, 27.0, window(t, 27.0, 35.2, 0.6), dur=8.2)
    for c in cards:
        c.draw(img, t)
    END.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [2.5, 7.0, 11.0, 17.0, 20.5, 25.0, 30.0, 34.0]:
            nr.still(f"stills/v10_{s}.png", s, frame, seed=23)
    else:
        nr.render("out/v10_saga03.mp4", DUR, frame, seed=23, bpm=60)
