"""WORDS FROM THE NORTH — Týr: Old Norse týr 'god' (pl. tívar), from Proto-Germanic *Tīwaz, same Indo-European root as
Latin deus and Greek Zeus. Romans equated him with Mars: dies Martis -> Tiw's day, Tuesday (martes, mardi)."""
import sys
import numpy as np
from PIL import Image
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, ease, window

DUR = 25.0
SRC = "../images/bauer_tyr_fenrir_1911.jpg"
TYR = nr.Painting(SRC, 1000, 600, cy=960, crop=(0, 427, 733, 855), zoom=0.08, feather=0.10)
SX, SY, SW, SH = (W - 380) / 2, 640, 380, 560

cards = [
    Card(-0.8, 3.8, 330, [T("This god's name", 74), T('just means "god".', 74, GOLD)]),
    Card(0.4, 3.8, 1500, [B("Art: John Bauer, 1911", 30)]),
    Card(4.0, 8.6, 330, [T("TÝR", 110, GOLD), B('Old Norse týr: "a god"', 52, LIGHT)]),
    Card(8.8, 13.4, 330, [B("It comes from the same ancient root", 50, LIGHT), B("as Latin", 50, LIGHT), T("deus", 76, GOLD), B("and Greek", 50, LIGHT), T("Zeus", 76, GOLD)]),
    Card(13.6, 18.4, 330, [B("The Romans thought he was Mars.", 52, LIGHT), B("Mars's day, dies Martis,", 52), B("became Tiw's day:", 52)]),
    Card(14.8, 18.4, 1500, [T("Tuesday", 90, GOLD), B("martes · mardi · martedì", 46, LIGHT)]),
    Card(18.6, 22.0, 330, [B("His rune is TIWAZ.", 56, LIGHT), B("He lost his hand to the wolf Fenrir", 48), B("to keep the gods' word.", 48)]),
    Card(22.2, 25.0, 330, [T("Odin, Thor or Loki:", 70), T("whose name is next?", 70, GOLD)]),
    Card(22.8, 25.0, 560, [B(nr.HANDLE, 40)]),
]

LABEL = nr.Label("WORDS FROM THE NORTH")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    TYR.draw(img, t, 0.0, window(t, -1.0, 8.8, 0.6), dur=8.8)
    TYR.draw(img, t, 18.4, window(t, 18.4, 25.0, 0.6), dur=6.6)
    sl = window(t, 8.6, 18.6, 0.6)
    if sl > 0:
        nr.draw_slab(img, SX, SY + 260, SW, SH, sl)
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        nr.draw_rune(lay, "tiwaz", SX + 60, SY + 320, SW - 120, SH - 120, ease((t - 8.8) / 1.6), width=30)
        a = np.asarray(lay, np.float32).copy(); a[..., 3] *= sl
        img.alpha_composite(Image.fromarray(a.astype(np.uint8)))
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 11.0, 16.0, 20.0]:
            nr.still(f"stills/v18_{s}.png", s, frame, seed=61)
    else:
        nr.render("out/v18_tyr.mp4", DUR, frame, seed=61, bpm=66)
