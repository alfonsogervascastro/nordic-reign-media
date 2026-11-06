"""RUNE 3/24 — Thurisaz. Norwegian and Icelandic rune poems: þurs, a giant; Old English poem: þorn, thorn.
The letter þ survives in Icelandic, and in the 'Ye' of 'Ye Olde' (a misread þe)."""
import sys
import numpy as np
from PIL import Image
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, ease, window

DUR = 26.0
SX, SY, SW, SH = (W - 460) / 2, 560, 460, 660
GIANT = nr.Painting("../images/froelich_ymir_killed_1895.jpg", 1000, 520, cy=920, crop=(20, 280, 890, 700), zoom=0.08, feather=0.12)

cards = [
    Card(-0.8, 3.6, 300, [T("This rune is still", 72), T("in use today.", 72, GOLD)]),
    Card(3.8, 22.0, 1290, [T("THURISAZ", 96, GOLD)]),
    Card(4.1, 22.0, 1410, [B("Elder Futhark  ·  the sound TH", 42)]),
    Card(4.8, 8.6, 300, [B("Its name is reconstructed:", 54, LIGHT), B('*þurisaz, "giant".', 54, GOLD)]),
    Card(8.8, 12.6, 300, [T("NORSE RUNE POEMS", 38, GOLD), B("a giant who torments women,", 50, LIGHT), B('"dweller in the cliffs"', 50)]),
    Card(9.2, 12.6, 1460, [B("Art: Lorenz Frølich, 1895", 30)]),
    Card(12.8, 16.2, 300, [T("OLD ENGLISH POEM", 38, GOLD), B("not a giant: þorn, a thorn,", 50, LIGHT), B('"exceedingly sharp"', 50)]),
    Card(16.4, 22.0, 300, [B("That name stuck. Icelanders", 52, LIGHT), B("still write þ every day,", 52, LIGHT), B('and the "Ye" in "Ye Olde Shoppe"', 46), B("is a misread þe: \"the\".", 46, GOLD)]),
    Card(22.2, 26.0, 300, [T("Giant or thorn?", 72)]),
    Card(22.7, 26.0, 430, [B("Next Monday: ANSUZ  ·  " + nr.HANDLE, 38)]),
]

LABEL = nr.Label("RUNE", "3 / 24")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    slab = window(t, -1.0, 26.0, 0.8) * (1 - window(t, 8.6, 12.8, 0.5))
    nr.draw_slab(img, SX, SY, SW, SH, slab)
    if slab > 0:
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        nr.draw_rune(lay, "thurisaz", SX + 70, SY + 70, SW - 140, SH - 140, ease((t + 2.4) / 2.4), width=34)
        a = np.asarray(lay, np.float32).copy(); a[..., 3] *= slab
        img.alpha_composite(Image.fromarray(a.astype(np.uint8)))
    GIANT.draw(img, t, 8.6, window(t, 8.6, 12.8, 0.5), dur=4.2)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 10.5, 19.0]:
            nr.still(f"stills/v17_{s}.png", s, frame, seed=59)
    else:
        nr.render("out/v17_thurisaz.mp4", DUR, frame, seed=59, bpm=60)
