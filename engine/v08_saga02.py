"""The Norse Saga, Ep. 2 — the world made from Ymir. Sources: Prose Edda, Gylfaginning 7–8; Grímnismál 40–41."""
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr, scenes
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 34.4
YMIR = nr.Painting("../images/froelich_ymir_killed_1895.jpg", 1000, 500, cy=900, crop=(20, 280, 890, 700), focus=(0.5, 0.5), zoom=0.06, feather=0.12)
END = nr.TattooEnd("../tattoos/out/ep02_ymir/ep02_ymir_gold.png", t0=31.2)
HORIZON = 1300

def sea(img, t, op):
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    xs = np.arange(0, W + 8, 8)
    for k, (col, amp, yoff, sp) in enumerate([((28, 40, 58), 14, 0, 0.9), ((20, 30, 44), 18, 70, 1.3), ((14, 21, 31), 22, 160, 1.7)]):
        ys = HORIZON + 40 + yoff + amp * np.sin(xs / 90.0 + t * sp + k)
        poly = list(zip(xs, ys)) + [(W, H), (0, H)]
        d.polygon(poly, fill=col + (int(255 * op),))
        d.line(list(zip(xs, ys)), fill=(70, 90, 115, int(160 * op)), width=3)
    img.alpha_composite(lay)

def flood(img, t, op):
    """Blood flood: the water line rises, drowning the giants."""
    if op <= 0:
        return
    level = H - ease((t - 4.2) / 3.5) * 900
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    xs = np.arange(0, W + 8, 8)
    ys = level + 26 * np.sin(xs / 70.0 + t * 2.2)
    d.polygon(list(zip(xs, ys)) + [(W, H), (0, H)], fill=(70, 22, 22, int(200 * op)))
    d.line(list(zip(xs, ys)), fill=(150, 60, 50, int(220 * op)), width=4)
    img.alpha_composite(lay)

def dome(img, t, op):
    if op <= 0:
        return
    k = ease((t - 17.4) / 1.4)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.arc([80, HORIZON - 760, W - 80, HORIZON + 760], 180, 180 + 180 * k, fill=GOLD + (int(220 * op),), width=6)
    img.alpha_composite(lay)
    names = [("Vestri", 120, HORIZON - 60), ("Norðri", 330, HORIZON - 640), ("Austri", W - 120, HORIZON - 60), ("Suðri", W - 330, HORIZON - 640)]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = nr.font("body", 40)
    for i, (n, x, y) in enumerate(names):
        o = op * ease((t - 18.4 - i * 0.25) / 0.5)
        bb = d.textbbox((0, 0), n, font=f)
        d.text((x - (bb[2] - bb[0]) / 2, y), n, font=f, fill=LIGHT + (int(255 * o),))
    img.alpha_composite(lay)

RIDGE = None
def land(img, t, op):
    """Earth and mountains: a ridge line that draws in from the left, filled below."""
    global RIDGE
    if op <= 0:
        return
    if RIDGE is None:
        rng = np.random.default_rng(7)
        xs = np.linspace(-40, W + 40, 15)
        ys = HORIZON - 30 - np.abs(rng.normal(0, 1, len(xs))) * 45
        ys[[3, 4, 10, 11]] -= [150, 100, 170, 110]
        sys.path.insert(0, "../tattoos")
        from knots import chaikin
        RIDGE = [tuple(p) for p in chaikin(np.stack([xs, ys], 1), 3, closed=False)]
    k = ease((t - 15.0) / 1.6)
    n = max(2, int(len(RIDGE) * k))
    pts = RIDGE[:n]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.polygon(pts + [(pts[-1][0], H), (pts[0][0], H)], fill=(26, 31, 40, int(255 * op)))
    d.line(pts, fill=(142, 153, 166, int(200 * op)), width=4, joint="curve")
    img.alpha_composite(lay)

def shaping(img, t, op):
    """A gold ring that opens at the centre: the world taking shape."""
    if op <= 0:
        return
    k = ease((t - 8.8) / 3.0)
    r = 80 + 420 * k
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([W / 2 - r, 960 - r, W / 2 + r, 960 + r], outline=GOLD + (int(230 * op),), width=5)
    img.alpha_composite(lay)
    nr_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(nr_glow).ellipse([W / 2 - r, 960 - r, W / 2 + r, 960 + r], outline=GOLD + (int(120 * op),), width=30)
    img.alpha_composite(nr_glow.filter(ImageFilter.GaussianBlur(18)))

def clouds(img, t, op):
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(7):
        x = (i * 190 + t * 40) % (W + 400) - 200
        y = 760 + (i % 3) * 110
        d.ellipse([x - 200, y - 50, x + 200, y + 50], fill=(150, 165, 185, int(70 * op)))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(26)))

def wall(img, t, op):
    if op <= 0:
        return
    k = ease((t - 21.8) / 1.2)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).arc([200, HORIZON - 90, W - 200, HORIZON + 150], 0, 360 * k, fill=GOLD + (int(255 * op),), width=8)
    img.alpha_composite(lay)

cards = [
    Card(-0.8, 4.0, 330, [T("Our world is made", 70), T("from a dead giant.", 70, GOLD)]),
    Card(1.4, 4.0, 1290, [B("Odin and his brothers, Vili and Vé,", 44, LIGHT), B("killed Ymir, the first giant.", 44, LIGHT)]),
    Card(0.6, 4.0, 1460, [B("Art: Lorenz Frølich, 1895", 30)]),
    Card(4.2, 8.4, 330, [B("So much blood poured from him", 56, LIGHT), B("that every frost giant drowned.", 56, LIGHT)]),
    Card(6.2, 8.4, 560, [T("All but one: Bergelmir.", 58, GOLD)]),
    Card(8.6, 12.6, 330, [T("Then they built", 70), T("the world from his body.", 70, GOLD)]),
    Card(12.8, 15.0, 330, [B("His blood became the sea,", 60, LIGHT)]),
    Card(15.0, 17.2, 330, [B("his flesh the earth,", 60, LIGHT), B("his bones the mountains.", 60, LIGHT)]),
    Card(17.4, 19.6, 330, [B("His skull became the sky,", 60, LIGHT), B("held up by four dwarves.", 52)]),
    Card(19.6, 21.6, 330, [B("His brains, the clouds.", 60, LIGHT)]),
    Card(21.8, 25.0, 330, [B("And with his eyebrows", 60, LIGHT), T("they walled in Midgard.", 64, GOLD)]),
    Card(23.0, 25.0, 1480, [B("Source: Prose Edda, Gylfaginning; Grímnismál", 32)]),
    Card(25.2, 31.0, 330, [B("A home for humans", 60, LIGHT), B("who did not exist yet.", 60, LIGHT)]),
    Card(27.6, 31.0, 800, [T("But what holds", 64), T("all the worlds together?", 64, GOLD)]),
    Card(28.6, 31.0, 1010, [B("Episode 3: Saturday  ·  " + nr.HANDLE, 40)]),
]

LABEL = nr.Label("THE NORSE SAGA", "EP. 2")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    YMIR.draw(img, t, 0.0, window(t, -1.0, 4.4, 0.5), dur=4.4)
    flood(img, t, window(t, 4.2, 8.6, 0.6))
    shaping(img, t, window(t, 8.6, 12.8, 0.6))
    clouds(img, t, window(t, 19.4, 27.4, 0.8))
    land(img, t, window(t, 14.8, 31.2, 0.6))
    sea(img, t, window(t, 12.6, 31.2, 0.8))
    dome(img, t, window(t, 17.2, 27.4, 0.6))
    wall(img, t, window(t, 21.6, 27.4, 0.6))
    for c in cards:
        c.draw(img, t)
    END.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [2.5, 7.0, 10.5, 16.0, 19.0, 23.5, 29.0, 33.0]:
            nr.still(f"stills/v08_{s}.png", s, frame, seed=19)
    else:
        nr.render("out/v08_saga02.mp4", DUR, frame, seed=19, bpm=60)
