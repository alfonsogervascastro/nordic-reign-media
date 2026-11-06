"""The Norse Saga, Ep. 4 — Ask and Embla. Sources: Prose Edda, Gylfaginning 9; Völuspá 17–18.
Art: Lorenz Frølich (1895), "Odin, Lóðurr and Hœnir create Ask and Embla"."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 33.2
SRC = "../images/froelich_ask_embla_1895.jpg"
FULL = nr.Painting(SRC, 1000, 660, cy=900, focus=(0.5, 0.45), zoom=0.08, feather=0.10)
GODS = nr.Painting(SRC, 980, 560, cy=880, crop=(230, 60, 760, 330), zoom=0.10, feather=0.12)
END = nr.TattooEnd("../tattoos/out/ep04_ask_embla/ep04_ask_embla_gold.png", t0=30.0)
HORIZON = 1240

def shore(img, t, op):
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    xs = np.arange(0, W + 8, 8)
    for k, (col, amp, yoff, sp) in enumerate([((28, 40, 58), 14, 0, 0.9), ((20, 30, 44), 18, 80, 1.3), ((14, 21, 31), 22, 180, 1.7)]):
        ys = HORIZON + yoff + amp * np.sin(xs / 90.0 + t * sp + k)
        d.polygon(list(zip(xs, ys)) + [(W, H), (0, H)], fill=col + (int(255 * op),))
        d.line(list(zip(xs, ys)), fill=(70, 90, 115, int(160 * op)), width=3)
    img.alpha_composite(lay)

def gifts(img, t, op):
    """Three gold rings, one per god's gift (atmosphere)."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i, t0 in enumerate([8.2, 12.2, 15.2]):
        k = op * ease((t - t0) / 0.9)
        if k <= 0:
            continue
        cx = W / 2 + (i - 1) * 300
        r = 60 + 70 * k
        d.ellipse([cx - r, 940 - r, cx + r, 940 + r], outline=GOLD + (int(230 * k),), width=6)
    glow = lay.filter(ImageFilter.GaussianBlur(16))
    img.alpha_composite(glow)
    img.alpha_composite(lay)

cards = [
    Card(-0.8, 4.0, 330, [T("The first humans", 72), T("were two pieces of wood.", 64, GOLD)]),
    Card(0.4, 4.0, 1300, [B("Art: Lorenz Frølich, 1895", 30)]),
    Card(4.2, 8.0, 330, [B("On the seashore, Odin and his brothers", 50, LIGHT), B("found two trees.", 58, LIGHT)]),
    Card(8.2, 12.0, 330, [B("The first gave them", 54), T("breath and life,", 66, GOLD)]),
    Card(12.2, 15.0, 330, [B("the second", 54), T("mind and movement,", 66, GOLD)]),
    Card(15.2, 18.4, 330, [B("the third", 54), T("faces, speech,", 66, GOLD), T("hearing and sight.", 66, GOLD)]),
    Card(18.6, 22.4, 330, [T("ASK", 104, LIGHT), B('"ash tree"', 48)]),
    Card(19.6, 22.4, 1240, [T("EMBLA", 104, GOLD), B("nobody knows for sure:", 44), B("elm? a vine?", 44)]),
    Card(22.6, 26.0, 330, [B("The gods gave them Midgard.", 56, LIGHT), B("Every human comes from them.", 52)]),
    Card(26.2, 29.8, 330, [B("But the gods were about", 56, LIGHT), T("to fight their first war.", 64, GOLD)]),
    Card(27.4, 29.8, 1460, [B("Episode 5: Saturday  ·  " + nr.HANDLE, 40)]),
    Card(23.0, 26.0, 1460, [B("Source: Prose Edda, Gylfaginning; Völuspá", 32)]),
]

LABEL = nr.Label("THE NORSE SAGA", "EP. 4")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    FULL.draw(img, t, 0.0, window(t, -1.0, 8.2, 0.6), dur=8.2)
    shore(img, t, window(t, 7.8, 18.6, 0.8))
    gifts(img, t, window(t, 8.0, 18.6, 0.6))
    GODS.draw(img, t, 18.4, window(t, 18.4, 30.0, 0.6), dur=11.6)
    for c in cards:
        c.draw(img, t)
    END.draw(img, t)

SEGMENTS = [
    (0.0, 4.2, "The first humans were two pieces of wood."),
    (4.2, 8.2, "On the seashore, Odin and his brothers found two trees."),
    (8.2, 12.2, "The first gave them breath and life,"),
    (12.2, 15.2, "the second, mind and movement,"),
    (15.2, 18.6, "the third, faces, speech, hearing and sight."),
    (18.6, 22.6, "The man was Ask: ash tree. The woman, Embla. Nobody knows for sure what her name means."),
    (22.6, 26.2, "The gods gave them Midgard. Every human comes from them."),
    (26.2, 30.0, "But the gods were about to fight their first war."),
    (30.0, 33.2, "This chapter, as a tattoo."),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 16.5, 20.5, 24.0, 32.0]:
            nr.still(f"stills/v13_{s}.png", s, frame, seed=41)
    else:
        import narrate
        print("duration", round(narrate.render_voiced("out/v13v_saga04.mp4", DUR, frame, SEGMENTS, seed=41, bpm=60), 2))
