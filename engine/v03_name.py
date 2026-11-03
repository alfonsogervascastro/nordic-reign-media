import sys
from PIL import Image, ImageDraw
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, ease, window

DUR = 19.5
NAME = "Astrid"
GLYPHS = nr.transliterate(NAME)

SLAB_X, SLAB_Y, SLAB_W, SLAB_H = 70, 560, W - 140, 520
STEP = 148
BOX_W, BOX_H = 104, 250
START = 0.9
EACH = 0.75

cards = [
    Card(0.2, 3.8, 300, [T("What your name", 72), T("looks like in runes", 72)]),
    Card(4.0, 19.5, 300, [[B("This is ", 58, LIGHT), T(NAME.upper(), 62, GOLD)]]),
    Card(4.5, 19.5, 400, [B("in the oldest runic alphabet", 46)]),
    Card(11.0, 15.8, 1180, [B("Elder Futhark, used c. 150–800 AD.", 44), B("Runes spell sounds, not letters.", 44)]),
    Card(16.0, 19.5, 1180, [T("Comment your name.", 64)]),
    Card(16.5, 19.5, 1290, [B("I'll carve the best ones next.", 50, GOLD)]),
    Card(17.0, 19.5, 1380, [B(nr.HANDLE, 40)]),
]

LABEL = nr.Label("YOUR NAME IN RUNES")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    nr.draw_slab(img, SLAB_X, SLAB_Y, SLAB_W, SLAB_H, window(t, 0.3, 19.5, 0.6))
    n = len(GLYPHS)
    x0 = W / 2 - (n - 1) * STEP / 2
    for i, (letter, rune) in enumerate(GLYPHS):
        p = ease((t - (START + i * EACH)) / 0.75)
        cx = x0 + i * STEP
        nr.draw_rune(img, rune, cx - BOX_W / 2, SLAB_Y + 90, BOX_W, BOX_H, p, width=16)
        op = window(t, START + i * EACH + 0.5, 19.5)
        if op > 0:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            f = nr.font("body", 46)
            bb = d.textbbox((0, 0), letter, font=f)
            d.text((cx - (bb[2] - bb[0]) / 2, SLAB_Y + 395), letter, font=f, fill=MIST + (int(255 * op),))
            img.alpha_composite(lay)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [2.6, 7.0, 13.0, 18.5]:
            nr.still(f"stills/v03_{s}.png", s, frame, seed=8)
    else:
        nr.render("out/v03_name.mp4", DUR, frame, seed=8, bpm=60)
