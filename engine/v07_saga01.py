"""The Norse Saga, Ep. 1 — Ginnungagap to Odin. Source: Prose Edda, Gylfaginning 4–6."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 31.0

PADX = 300

def _glow(cx, cy, r, col):
    yy, xx = np.mgrid[0:H, 0:W + 2 * PADX].astype(np.float32)
    cx = cx + PADX
    a = 210 * np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (r * r)) * 1.6)
    out = np.zeros((H, W + 2 * PADX, 4), np.float32)
    out[..., :3] = col
    out[..., 3] = a
    return out

FIRE = _glow(170, 980, 260, (235, 140, 60))
ICE = _glow(W - 170, 980, 260, (190, 215, 240))

def glows(img, t):
    op = window(t, 7.6, 15.0, 0.8)
    if op <= 0:
        return
    meet = ease((t - 9.6) / 1.6)          # the two glows drift toward the centre
    for g, sx in ((FIRE, 1), (ICE, -1)):
        x0 = PADX - int(sx * meet * 150)
        a = g[:, x0:x0 + W].copy()
        a[..., 3] *= op
        img.alpha_composite(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = nr.font("body", 44)
    lo = int(255 * op * (1 - meet))
    for text, x in (("Múspelheim", 170), ("Niflheim", W - 170)):
        bb = d.textbbox((0, 0), text, font=f)
        d.text((x - (bb[2] - bb[0]) / 2, 1290), text, font=f, fill=MIST + (lo,))
    img.alpha_composite(lay)

cards = [
    Card(0.3, 3.8, 330, [T("Before the gods,", 70), T("before the world,", 70)]),
    Card(1.6, 3.8, 540, [B("there was only a gap.", 58, GOLD)]),
    Card(4.0, 7.4, 820, [T("GINNUNGAGAP", 92, LIGHT)]),
    Card(4.5, 7.4, 960, [B('"the yawning void"', 54)]),
    Card(7.6, 11.4, 330, [T("Fire to the south.", 64, GOLD), T("Ice to the north.", 64, LIGHT)]),
    Card(11.6, 15.0, 330, [B("Where they met, the ice melted.", 54, LIGHT), B("From the drops, a giant woke:", 54, LIGHT)]),
    Card(12.6, 15.0, 820, [T("YMIR", 130, GOLD)]),
    Card(15.2, 19.0, 700, [B("From the thaw came a cow,", 56, LIGHT), T("AUÐUMBLA", 84, GOLD),
                           B("Ymir drank her milk.", 52)]),
    Card(19.2, 23.2, 640, [B("She licked the salty ice", 56, LIGHT), B("for three days.", 56, LIGHT)]),
    Card(20.6, 23.2, 860, [B("Out came Búri,", 60, GOLD), B("the first of the gods.", 52)]),
    Card(23.4, 27.0, 700, [B("Búri's grandson:", 58, LIGHT)]),
    Card(24.0, 27.0, 820, [T("ODIN", 140, GOLD)]),
    Card(27.2, 31.0, 700, [T("His first act?", 74)]),
    Card(27.9, 31.0, 820, [T("Murder.", 96, GOLD)]),
    Card(28.8, 31.0, 1010, [B("Episode 2: Wednesday  ·  " + nr.HANDLE, 42)]),
    Card(15.2, 23.2, 1440, [B("Source: Prose Edda, Gylfaginning", 34)]),
]

LABEL = nr.Label("THE NORSE SAGA", "EP. 1")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    glows(img, t)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [2.6, 6.0, 9.0, 13.5, 17.0, 21.5, 29.5]:
            nr.still(f"stills/v07_{s}.png", s, frame, seed=17)
    else:
        nr.render("out/v07_saga01.mp4", DUR, frame, seed=17, bpm=58)
