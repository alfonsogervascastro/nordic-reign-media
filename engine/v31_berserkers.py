"""MYTH vs HISTORY — berserkers and mushrooms. Ynglinga saga 6 (Snorri, c. 1230): Odin's men went without mail,
mad as dogs or wolves, bit their shields, strong as bears or bulls. Fly-agaric theory: Samuel Ödmann, 1784
(speculation, no Norse source). Henbane theory: K. Fatur, J. Ethnopharmacology 2019 (also speculation).
Art: Mårten Eskil Winge, Tor's Fight with the Giants (1872). Soundtrack: Chains Beneath the Mountain."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 28.0
WINGE = "../images/winge_thor_giants_1872.jpg"
FULL = nr.Painting(WINGE, 700, 1000, cy=1080, zoom=0.08, feather=0.10)
FIGHT = nr.Painting(WINGE, 900, 800, cy=1040, crop=(0, 900, 1280, 1851), zoom=0.10, feather=0.12)
TOP = nr.Painting(WINGE, 860, 800, cy=1040, crop=(150, 0, 1280, 1000), zoom=0.10, feather=0.12)

def shields(img, t, op):
    """A row of round shields (atmosphere)."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(4):
        cx = 170 + i * 250
        k = ease((t - 9.0 - i * 0.25) / 0.5)
        r = 110 * k
        if r <= 0:
            continue
        d.ellipse([cx - r, 1050 - r, cx + r, 1050 + r], fill=(43, 48, 56, int(255 * op)), outline=GOLD + (int(255 * op),), width=6)
        d.ellipse([cx - r * 0.22, 1050 - r * 0.22, cx + r * 0.22, 1050 + r * 0.22], fill=GOLD + (int(230 * op),))
    img.alpha_composite(lay)

cards = [
    Card(-0.8, 4.0, 330, [T("Berserkers on", 76), T("magic mushrooms?", 76, GOLD)]),
    Card(0.4, 4.0, 1620, [B("Art: Mårten Eskil Winge, 1872", 30)]),
    Card(4.2, 8.6, 330, [B("Snorri, c. 1230: Odin's men fought", 50, LIGHT), B("without armour, mad as wolves,", 50, LIGHT), T("strong as bears.", 66, GOLD)]),
    Card(8.8, 12.8, 330, [T("They bit their shields.", 70), B("Berserkr: probably “bear-shirt”.", 50, LIGHT)]),
    Card(9.2, 12.8, 1560, [B("Source: Ynglinga saga 6", 32)]),
    Card(13.0, 17.2, 330, [B("The mushroom idea?", 56, LIGHT), B("A Swedish priest, Samuel Ödmann,", 50, LIGHT), T("in 1784.", 74, GOLD)]),
    Card(17.4, 21.6, 330, [T("No Norse source", 70), T("mentions mushrooms.", 70, GOLD), B("Not one.", 54, LIGHT)]),
    Card(21.8, 25.0, 330, [B("A 2019 study suggested henbane.", 50, LIGHT), B("Also a guess.", 54, GOLD)]),
    Card(25.2, 28.0, 330, [T("Mushrooms, henbane,", 66), T("or pure rage?", 70, GOLD)]),
    Card(25.6, 28.0, 1620, [B(nr.HANDLE, 40)]),
]

LABEL = nr.Label("MYTH vs HISTORY")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    FULL.draw(img, t, 0.0, window(t, -1.0, 4.4, 0.5), dur=4.4)
    FIGHT.draw(img, t, 4.2, window(t, 4.2, 8.8, 0.5), dur=4.6)
    shields(img, t, window(t, 8.8, 13.0, 0.5))
    TOP.draw(img, t, 12.8, window(t, 12.8, 17.4, 0.5), dur=4.6)
    FIGHT.draw(img, t, 17.2, window(t, 17.2, 21.8, 0.5), dur=4.6)
    TOP.draw(img, t, 21.6, window(t, 21.6, 25.2, 0.5), dur=3.6)
    FULL.draw(img, t, 25.0, window(t, 25.0, 28.0, 0.5), dur=3.0)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 10.5, 15.0, 19.5, 23.5, 27.0]:
            nr.still(f"stills/v31_{s}.png", s, frame, seed=103)
    else:
        nr.render("out/v31_berserkers.mp4", DUR, frame, seed=103, bpm=60)
