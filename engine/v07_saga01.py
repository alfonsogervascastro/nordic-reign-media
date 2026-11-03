"""The Norse Saga, Ep. 1 — Ginnungagap to Odin. Source: Prose Edda, Gylfaginning 4–6.

Illustrated with code-drawn silhouette scenes (cliffs of the void, fire and ice,
Ymir's eyes, Auðumbla, Búri in the ice, Odin the wanderer) and a slow camera push.
"""
import sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 31.0
DARK = (8, 10, 14, 255)
RIM = (52, 60, 74, 255)
ICEC = (200, 225, 245)

def glow_layer(cx, cy, r, col, strength=210):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a = strength * np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (r * r)) * 1.6)
    out = np.zeros((H, W, 4), np.float32)
    out[..., :3] = col
    out[..., 3] = a
    return out

def put(img, arr, op):
    if op <= 0:
        return
    a = arr.copy(); a[..., 3] *= op
    img.alpha_composite(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)))

FIRE = glow_layer(330, 1180, 300, (235, 140, 60))
ICE = glow_layer(W - 330, 1180, 300, ICEC)
MEET = glow_layer(W / 2, 1150, 260, (230, 200, 160), 170)
PALE = glow_layer(W / 2, 1080, 420, (150, 175, 200), 150)
MOON = glow_layer(W / 2, 880, 260, (236, 196, 130), 230)

L_CLIFF = [(0, 700), (240, 740), (330, 880), (290, 1010), (390, 1180), (340, 1380), (430, 1600), (390, 1920), (0, 1920)]
R_CLIFF = [(W - x, y) for x, y in L_CLIFF]

def cliffs(d):
    for poly in (L_CLIFF, R_CLIFF):
        d.polygon(poly, fill=DARK)
        d.line(poly[:-1], fill=RIM, width=4)

def eyes(d, cx, cy, open_k, op):
    for ex in (cx - 120, cx + 120):
        hw, hh = 78, 34 * max(0.04, open_k)
        d.ellipse([ex - hw, cy - hh, ex + hw, cy + hh], fill=ICEC + (int(255 * op),))
        d.ellipse([ex - 9, cy - hh * 0.9, ex + 9, cy + hh * 0.9], fill=(10, 14, 20, int(255 * op)))

SS = 2  # supersampling for smooth silhouettes

def _smooth(draw_fn):
    big = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(big), SS)
    return big.resize((W, H), Image.LANCZOS)

def _cow(d, k):
    q = lambda pts: [(x * k, y * k) for x, y in pts]
    e = lambda x0, y0, x1, y1: [x0 * k, y0 * k, x1 * k, y1 * k]
    d.ellipse(e(400, 1035, 780, 1185), fill=DARK)                      # body
    d.ellipse(e(640, 1020, 790, 1150), fill=DARK)                      # rump
    d.polygon(q([(430, 1060), (360, 1040), (330, 1085), (360, 1140), (440, 1150)]), fill=DARK)   # neck
    d.ellipse(e(255, 1030, 385, 1115), fill=DARK)                      # head
    d.ellipse(e(232, 1060, 300, 1120), fill=DARK)                      # muzzle
    for x, lean in ((440, -6), (480, 4), (700, -4), (745, 6)):        # tapered legs
        d.polygon(q([(x - 15, 1150), (x + 15, 1150), (x + 9 + lean, 1262), (x - 9 + lean, 1262)]), fill=DARK)
    d.polygon(q([(285, 1045), (300, 1040), (288, 1000), (270, 990)]), fill=DARK)   # horns
    d.polygon(q([(335, 1040), (352, 1046), (360, 1004), (348, 990)]), fill=DARK)
    d.line(q([(785, 1080), (812, 1150), (806, 1200)]), fill=DARK, width=7 * k, joint="curve")   # tail

def _buri(d, k):
    e = lambda x0, y0, x1, y1: [x0 * k, y0 * k, x1 * k, y1 * k]
    g = GOLD + (255,)
    d.ellipse(e(498, 930, 582, 1035), fill=g)                          # head
    d.rectangle(e(522, 1025, 558, 1070), fill=g)                       # neck
    d.chord(e(410, 1055, 670, 1320), 180, 360, fill=g)                 # shoulders and chest
    d.rectangle(e(440, 1186, 640, 1300), fill=g)

COW = _smooth(_cow)
BURI = _smooth(_buri).filter(ImageFilter.GaussianBlur(4))

def cow_scene(lay):
    lay.alpha_composite(COW)

def ice_block(lay, reveal):
    a = np.asarray(BURI, np.float32).copy(); a[..., 3] *= reveal
    glow = Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(30))
    lay.alpha_composite(glow)
    lay.alpha_composite(Image.fromarray(a.astype(np.uint8)))
    ice = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ice)
    d.polygon([(390, 870), (690, 860), (712, 1325), (372, 1335)], fill=ICEC + (95,), outline=ICEC + (210,))
    for p, q in (((420, 930), (520, 1050)), ((670, 950), (600, 1120)), ((400, 1230), (560, 1190)), ((690, 1200), (620, 1300))):
        d.line([p, q], fill=ICEC + (170,), width=3)
    lay.alpha_composite(ice)

def wanderer(d):
    d.polygon([(470, 905), (610, 905), (690, 1360), (390, 1360)], fill=DARK)          # cloak
    d.ellipse([515, 845, 565, 915], fill=DARK)                                        # head
    d.ellipse([430, 830, 650, 870], fill=DARK)                                        # hat brim
    d.polygon([(490, 850), (500, 770), (580, 770), (590, 850)], fill=DARK)            # hat crown
    d.line([(660, 800), (700, 1360)], fill=DARK, width=12)                            # staff
    d.rectangle([380, 1355, 700, 1380], fill=DARK)

def scene(t):
    """Returns the illustration layer for time t (drawn behind the text)."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # 1. the void between cliffs + 2. fire and ice
    s12 = window(t, 0.2, 15.0, 0.6)
    if s12 > 0:
        meet = ease((t - 9.6) / 1.8)
        put(lay, FIRE, window(t, 7.6, 15.0, 0.8) * (1 - 0.5 * meet))
        put(lay, ICE, window(t, 7.6, 15.0, 0.8) * (1 - 0.5 * meet))
        put(lay, MEET, window(t, 9.6, 15.0, 0.8) * meet)
        d = ImageDraw.Draw(lay)
        if 11.4 < t < 15.0:                        # drops falling where they meet
            for i in range(14):
                y = 820 + ((t * 260 + i * 97) % 520)
                x = W / 2 + ((i * 53) % 160) - 80
                d.ellipse([x - 4, y - 7, x + 4, y + 7], fill=ICEC + (int(200 * s12),))
        if 12.4 < t < 15.0:
            eyes(d, W / 2, 1060, ease((t - 12.6) / 0.9), window(t, 12.4, 15.0, 0.4))
        cliffs(d)
        if s12 < 1:
            a = np.asarray(lay, np.float32).copy(); a[..., 3] *= s12
            lay = Image.fromarray(a.astype(np.uint8))
    # 3. Auðumbla on the ice
    s3 = window(t, 15.0, 19.2, 0.6)
    if s3 > 0:
        l3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        put(l3, PALE, 1.0)
        ImageDraw.Draw(l3).rectangle([0, 1262, W, H], fill=(46, 58, 74, 255))
        cow_scene(l3)
        _fade_into(lay, l3, s3)
    # 4. Búri in the ice
    s4 = window(t, 19.0, 23.4, 0.6)
    if s4 > 0:
        l4 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        put(l4, PALE, 0.7)
        ImageDraw.Draw(l4).rectangle([0, 1320, W, H], fill=(46, 58, 74, 255))
        ice_block(l4, ease((t - 20.2) / 2.2))
        _fade_into(lay, l4, s4)
    # 5. Odin the wanderer
    s5 = window(t, 23.2, 27.2, 0.6)
    if s5 > 0:
        l5 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ODIN_ART.draw(l5, t, 23.2, 1.0, dur=4.0)
        _fade_into(lay, l5, s5)
    # 6. Ymir's eyes close
    s6 = window(t, 27.2, 31.0, 0.5)
    if s6 > 0:
        l6 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        eyes(ImageDraw.Draw(l6), W / 2, 1100, 1 - ease((t - 28.2) / 0.5), 1.0)
        _fade_into(lay, l6, s6)
    return lay

def _fade_into(base, layer, op):
    a = np.asarray(layer, np.float32).copy(); a[..., 3] *= op
    base.alpha_composite(Image.fromarray(a.astype(np.uint8)))

def camera(lay, t):
    """Slow push-in, restarting gently for each scene."""
    starts = [0.2, 15.0, 19.0, 23.2, 27.2]
    s = max(x for x in starts if x <= t) if t >= 0.2 else 0.2
    z = 1 + 0.07 * ease((t - s) / 6.0)
    if z <= 1.001:
        return lay
    w2, h2 = int(W * z), int(H * z)
    big = lay.resize((w2, h2), Image.BILINEAR)
    x0, y0 = (w2 - W) // 2, int((h2 - H) * 0.55)
    return big.crop((x0, y0, x0 + W, y0 + H))

cards = [
    Card(0.3, 3.8, 330, [T("Before the gods,", 70), T("before the world,", 70)]),
    Card(1.6, 3.8, 540, [B("there was only a gap.", 58, GOLD)]),
    Card(4.0, 7.4, 330, [T("GINNUNGAGAP", 92, LIGHT)]),
    Card(4.5, 7.4, 460, [B('"the yawning void"', 54)]),
    Card(7.6, 11.4, 330, [T("Fire to the south.", 64, GOLD), T("Ice to the north.", 64, LIGHT)]),
    Card(11.6, 15.0, 330, [B("Where they met, the ice melted.", 54, LIGHT), B("From the drops, a giant woke:", 54, LIGHT)]),
    Card(12.6, 15.0, 500, [T("YMIR", 120, GOLD)]),
    Card(15.2, 19.0, 330, [B("From the thaw came a cow,", 56, LIGHT), T("AUÐUMBLA", 84, GOLD),
                           B("Ymir drank her milk.", 52)]),
    Card(19.2, 23.2, 330, [B("She licked the salty ice", 56, LIGHT), B("for three days.", 56, LIGHT)]),
    Card(20.6, 23.2, 1440, [B("Out came Búri,", 60, GOLD), B("the first of the gods.", 52)]),
    Card(23.4, 27.0, 330, [B("Búri's grandson:", 58, LIGHT)]),
    Card(24.0, 27.0, 440, [T("ODIN", 130, GOLD)]),
    Card(27.2, 31.0, 330, [T("His first act?", 74)]),
    Card(27.9, 31.0, 450, [T("Murder.", 96, GOLD)]),
    Card(23.6, 27.0, 1530, [B("Art: Georg von Rosen, Odin the Wanderer, 1886", 30)]),
    Card(28.8, 31.0, 1450, [B("Episode 2: Wednesday  ·  " + nr.HANDLE, 42)]),
]

ODIN_ART = nr.Painting("../images/rosen_odin_wanderer_1886.jpg", 760, 900, cy=1060, focus=(0.5, 0.25))

LABEL = nr.Label("THE NORSE SAGA", "EP. 1")

def frame(img, t):
    img.alpha_composite(camera(scene(t), t))
    if 28.5 < t < 29.1:                            # the strike: a brief gold flash
        k = 1 - abs(t - 28.8) / 0.3
        img.alpha_composite(Image.new("RGBA", (W, H), GOLD + (int(70 * k),)))
    LABEL.draw(img, t, DUR)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [2.6, 6.0, 9.0, 13.8, 17.0, 22.0, 25.5, 29.8]:
            nr.still(f"stills/v07_{s}.png", s, frame, seed=17)
    else:
        nr.render("out/v07_saga01.mp4", DUR, frame, seed=17, bpm=58)
