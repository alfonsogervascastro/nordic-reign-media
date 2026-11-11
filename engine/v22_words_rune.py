"""WORDS FROM THE NORTH — 'rune'. Old Norse rún 'secret, mystery'; Gothic rūna 'mystery' (Wulfila's Bible, 4th c.);
Old English rūn 'secret, whispered counsel'; German raunen 'to whisper' (same root); Finnish runo 'poem' (an old
Germanic loan, probably). Ties in with Ep. 6 (Odin takes up the runes, Hávamál 139). Soundtrack: Inside the Lie."""
import sys
import numpy as np
from PIL import Image
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, ease, window

DUR = 25.0
SRC = "../images/rosen_odin_wanderer_1886.jpg"
FACE = nr.Painting(SRC, 760, 760, cy=1040, crop=(120, 20, 400, 300), zoom=0.10, feather=0.12)
ODIN = nr.Painting(SRC, 700, 900, cy=1060, focus=(0.5, 0.25))
SX, SY, SW, SH = 110, 640, W - 220, 520
WORD = [("R", "raidho"), ("U", "uruz"), ("N", "naudiz"), ("A", "ansuz")]

cards = [
    Card(-0.8, 4.0, 330, [T('"Rune" first meant', 72), T("secret.", 80, GOLD)]),
    Card(0.4, 4.0, 1560, [B("Art: Georg von Rosen, 1886", 30)]),
    Card(4.2, 8.8, 330, [B("In Old Norse,", 56, LIGHT), T("rún", 100, GOLD), B('meant a letter, but also', 50, LIGHT), B('"a secret", "a mystery".', 52)]),
    Card(9.0, 13.2, 330, [B("Gothic Bible, 4th century:", 50, LIGHT), T("rūna", 80, GOLD), B('"a mystery".', 52)]),
    Card(13.4, 17.4, 330, [B("Old English", 50, LIGHT), T("rūn", 80, GOLD), B('"a secret, a whispered counsel".', 48)]),
    Card(17.6, 21.6, 330, [B("And German still says", 52, LIGHT), T("raunen", 90, GOLD), B('"to whisper".', 52)]),
    Card(18.0, 21.6, 1460, [B("Same root, not a loanword", 34)]),
    Card(21.8, 25.0, 330, [B("When Odin took up the runes,", 52, LIGHT), B("he wasn't just learning letters.", 52, LIGHT), T("He was learning secrets.", 62, GOLD)]),
    Card(23.2, 25.0, 1360, [T("Which word would you", 58), T("carve in runes?", 58, GOLD), B(nr.HANDLE, 38)]),
]

LABEL = nr.Label("WORDS FROM THE NORTH")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    ODIN.draw(img, t, 0.0, window(t, -1.0, 4.2, 0.5), dur=4.2)
    sl = window(t, 4.0, 13.4, 0.6)
    if sl > 0:
        nr.draw_slab(img, SX, SY + 120, SW, SH, sl)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        step = 200
        x0 = W / 2 - 1.5 * step
        for i, (L, r) in enumerate(WORD):
            nr.draw_rune(lay, r, x0 + i * step - 60, SY + 200, 120, 280, ease((t - 4.4 - i * 0.45) / 0.6), width=18)
        a = np.asarray(lay, np.float32).copy(); a[..., 3] *= sl
        img.alpha_composite(Image.fromarray(a.astype(np.uint8)))
        nr.draw_lines(img, [B("R     U     N     A", 46)], SY + 520, sl * window(t, 6.0, 13.4, 0.4))
    FACE.draw(img, t, 13.2, window(t, 13.2, 21.8, 0.6), dur=8.6)
    ODIN.draw(img, t, 21.6, window(t, 21.6, 23.4, 0.5), dur=3.4)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.5, 11.0, 15.0, 19.5, 22.6, 24.5]:
            nr.still(f"stills/v22_{s}.png", s, frame, seed=67)
    else:
        nr.render("out/v22_rune.mp4", DUR, frame, seed=67, bpm=60)
