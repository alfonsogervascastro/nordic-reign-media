"""RUNE 5/24 — Raidho. Reconstructed *raidō 'ride, journey'. Rune poems (trans. B. Dickins, 1915):
Norwegian: riding is said to be the worst thing for horses; Icelandic: joy of the rider, speedy journey, toil of the steed;
Old English: riding seems easy to every warrior while he is indoors. Soundtrack: Forge of Svartalfheim."""
import sys
import numpy as np
from PIL import Image
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, ease, window

DUR = 26.0
SX, SY, SW, SH = (W - 460) / 2, 560, 460, 660
SLEIPNIR = nr.Painting("../images/froelich_odin_ravens_1895.jpg", 600, 540, cy=900, zoom=0.08, feather=0.10)

cards = [
    Card(-0.8, 3.6, 300, [T("This rune's poem mocks", 66), T("armchair warriors.", 72, GOLD)]),
    Card(3.8, 22.0, 1290, [T("RAIDHO", 96, GOLD)]),
    Card(4.1, 22.0, 1410, [B("Elder Futhark  ·  the sound R", 42)]),
    Card(4.8, 8.6, 300, [B("Its name is reconstructed:", 54, LIGHT), B('*raidō, "ride, journey".', 54, GOLD)]),
    Card(8.8, 12.6, 300, [T("NORWEGIAN RUNE POEM", 38, GOLD), B('"Riding is said to be', 48, LIGHT), B('the worst thing for horses."', 48)]),
    Card(9.2, 12.6, 1560, [B("Art: Lorenz Frølich, 1895", 30)]),
    Card(12.8, 16.2, 300, [T("ICELANDIC RUNE POEM", 38, GOLD), B('"joy of the rider, speedy journey,', 48, LIGHT), B('and toil of the steed."', 48)]),
    Card(16.4, 22.0, 300, [T("OLD ENGLISH POEM", 38, GOLD), B('"Riding seems easy to every warrior', 46, LIGHT), B('while he is indoors."', 50, GOLD)]),
    Card(16.8, 22.0, 1560, [B("Rune poems, trans. B. Dickins, 1915", 30)]),
    Card(22.2, 26.0, 300, [T("Rider or steed:", 72), T("which are you today?", 66, GOLD)]),
    Card(22.7, 26.0, 470, [B("Next Monday: KAUNAN  ·  " + nr.HANDLE, 38)]),
]

LABEL = nr.Label("RUNE", "5 / 24")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    slab = window(t, -1.0, 26.0, 0.8) * (1 - window(t, 8.6, 12.8, 0.5))
    nr.draw_slab(img, SX, SY, SW, SH, slab)
    if slab > 0:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        nr.draw_rune(lay, "raidho", SX + 70, SY + 70, SW - 140, SH - 140, ease((t + 2.4) / 2.4), width=34)
        a = np.asarray(lay, np.float32).copy(); a[..., 3] *= slab
        img.alpha_composite(Image.fromarray(a.astype(np.uint8)))
    SLEIPNIR.draw(img, t, 8.6, window(t, 8.6, 12.8, 0.5), dur=4.2)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 10.5, 14.5, 19.0, 24.0]:
            nr.still(f"stills/v33_{s}.png", s, frame, seed=109)
    else:
        nr.render("out/v33_raidho.mp4", DUR, frame, seed=109, bpm=60)
