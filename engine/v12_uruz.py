"""RUNE 2/24 — Uruz. The three rune poems disagree: aurochs (Old English), slag (Old Norwegian), drizzle (Old Icelandic)."""
import sys
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, ease, window

DUR = 25.0
SX, SY, SW, SH = (W - 460) / 2, 520, 460, 660
AUROCHS = nr.Painting("../images/hamiltonsmith_aurochs_1827.jpg", 980, 600, cy=930, focus=(0.3, 0.5))

cards = [
    Card(0.2, 3.6, 300, [T("Nobody agrees", 68), T("what this rune means.", 68, GOLD)]),
    Card(3.8, 21.0, 1250, [T("URUZ", 100, GOLD)]),
    Card(4.1, 21.0, 1380, [B("Elder Futhark  ·  the sound U", 42)]),
    Card(5.6, 9.0, 300, [B("Its original name is lost.", 54, LIGHT), B("\"Uruz\" is a modern reconstruction.", 50)]),
    Card(9.2, 13.6, 300, [T("OLD ENGLISH POEM", 38, GOLD), B("the aurochs:", 56, LIGHT), B("a wild ox with great horns", 48)]),
    Card(9.6, 13.6, 1470, [B("Aurochs, after a 16th-century painting", 30)]),
    Card(13.8, 16.6, 300, [T("OLD NORWEGIAN POEM", 38, GOLD), B("slag:", 56, LIGHT), B("what comes from bad iron", 48)]),
    Card(16.8, 19.6, 300, [T("OLD ICELANDIC POEM", 38, GOLD), B("drizzle:", 56, LIGHT), B("\"the weeping of the clouds\"", 48)]),
    Card(19.8, 22.4, 300, [T("MODERN", 38, MIST), B("Strength, vitality.", 54, LIGHT), B("A 20th-century reading.", 46)]),
    Card(22.6, 25.0, 300, [T("Ox, slag or rain?", 64)]),
    Card(23.1, 25.0, 420, [B("Next Monday: THURISAZ  ·  " + nr.HANDLE, 38)]),
]

LABEL = nr.Label("RUNE", "2 / 24")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    slab = window(t, 3.0, 25.0, 0.8) * (1 - window(t, 9.0, 13.8, 0.5))
    nr.draw_slab(img, SX, SY, SW, SH, slab)
    p = ease((t - 3.4) / 2.4)
    if slab > 0:
        from PIL import Image
        import numpy as np
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        nr.draw_rune(lay, "uruz", SX + 70, SY + 70, SW - 140, SH - 140, p, width=34)
        a = np.asarray(lay, np.float32).copy(); a[..., 3] *= slab
        img.alpha_composite(Image.fromarray(a.astype(np.uint8)))
    AUROCHS.draw(img, t, 9.0, window(t, 9.0, 13.8, 0.5), dur=4.8)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [2.0, 7.0, 11.5, 15.0, 18.0, 23.5]:
            nr.still(f"stills/v12_{s}.png", s, frame, seed=37)
    else:
        nr.render("out/v12_uruz.mp4", DUR, frame, seed=37, bpm=60)
