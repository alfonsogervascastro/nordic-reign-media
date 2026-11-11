"""RUNE 4/24 — Ansuz. Reconstructed *ansuz 'god' (one of the Æsir). Old Icelandic rune poem: óss = the god
(Odin: 'aged Gautr, prince of Asgard, lord of Valhalla'). Old Norwegian poem: óss = river mouth, 'the way of most
journeys'. Old English poem: ōs = 'the source of all speech'. Soundtrack: Thunder of the Gods."""
import sys
import numpy as np
from PIL import Image
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, ease, window

DUR = 26.0
SX, SY, SW, SH = (W - 460) / 2, 560, 460, 660
ODIN = nr.Painting("../images/rosen_odin_wanderer_1886.jpg", 560, 640, cy=930, focus=(0.5, 0.2))

cards = [
    Card(-0.8, 3.6, 300, [T("This rune is", 72), T("Odin's own.", 76, GOLD)]),
    Card(3.8, 22.0, 1290, [T("ANSUZ", 96, GOLD)]),
    Card(4.1, 22.0, 1410, [B("Elder Futhark  ·  the sound A", 42)]),
    Card(4.8, 8.6, 300, [B("Its name is reconstructed:", 54, LIGHT), B('*ansuz, "a god".', 54, GOLD)]),
    Card(8.8, 12.6, 300, [T("ICELANDIC RUNE POEM", 38, GOLD), B('"aged Gautr, prince of Asgard,', 48, LIGHT), B('lord of Valhalla": Odin.', 48)]),
    Card(9.2, 12.6, 1560, [B("Art: Georg von Rosen, 1886", 30)]),
    Card(12.8, 16.2, 300, [T("NORWEGIAN RUNE POEM", 38, GOLD), B("not a god: a river mouth,", 50, LIGHT), B('"the way of most journeys"', 50)]),
    Card(16.4, 22.0, 300, [T("OLD ENGLISH POEM", 38, GOLD), B("a mouth again,", 50, LIGHT), B('"the source of all speech".', 50, GOLD)]),
    Card(22.2, 26.0, 300, [T("Would you wear", 72), T("Odin's rune?", 72, GOLD)]),
    Card(22.7, 26.0, 470, [B("Next Monday: RAIDHO  ·  " + nr.HANDLE, 38)]),
]

LABEL = nr.Label("RUNE", "4 / 24")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    slab = window(t, -1.0, 26.0, 0.8) * (1 - window(t, 8.6, 12.8, 0.5))
    nr.draw_slab(img, SX, SY, SW, SH, slab)
    if slab > 0:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        nr.draw_rune(lay, "ansuz", SX + 70, SY + 70, SW - 140, SH - 140, ease((t + 2.4) / 2.4), width=34)
        a = np.asarray(lay, np.float32).copy(); a[..., 3] *= slab
        img.alpha_composite(Image.fromarray(a.astype(np.uint8)))
    ODIN.draw(img, t, 8.6, window(t, 8.6, 12.8, 0.5), dur=4.2)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 10.5, 14.5, 19.0, 24.0]:
            nr.still(f"stills/v26_{s}.png", s, frame, seed=83)
    else:
        nr.render("out/v26_ansuz.mp4", DUR, frame, seed=83, bpm=60)
