import math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 30.0

def eyes(img, t, cy, op):
    if op <= 0:
        return
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    blink = 1.0
    for bt in (5.2, 9.0):
        if bt < t < bt + 0.25:
            blink = abs((t - bt) / 0.125 - 1)
    for cx in (W / 2 - 115, W / 2 + 115):
        hw, hh = 62, 26 * max(0.08, blink)
        d.ellipse([cx - hw, cy - hh, cx + hw, cy + hh], fill=GOLD + (int(255 * op),))
        d.ellipse([cx - 7, cy - hh * 0.9, cx + 7, cy + hh * 0.9], fill=(20, 12, 6, int(255 * op)))
    glow = layer.filter(ImageFilter.GaussianBlur(26))
    ga = np.asarray(glow, np.float32).copy(); ga[..., 3] *= 2.0
    img.alpha_composite(Image.fromarray(np.clip(ga, 0, 255).astype(np.uint8)))
    img.alpha_composite(layer)

def chain(img, t, cy, op):
    if op <= 0:
        return
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    split = ease((t - 9.3) / 0.35) * 70
    n = 7
    lw, lh, step = 120, 64, 96
    x0 = W / 2 - (n - 1) * step / 2
    for i in range(n):
        cx = x0 + i * step
        dx = -split if i < n // 2 else (split if i > n // 2 else 0)
        if i == n // 2 and split > 1:
            # the broken middle link: two halves flying apart
            d.arc([cx - lw / 2 - split * 0.5, cy - lh / 2, cx + lw / 2 - split * 0.5, cy + lh / 2], 90, 270,
                  fill=MIST + (int(255 * op),), width=12)
            d.arc([cx - lw / 2 + split * 0.5, cy - lh / 2, cx + lw / 2 + split * 0.5, cy + lh / 2], 270, 90,
                  fill=MIST + (int(255 * op),), width=12)
            continue
        if i % 2 == 0:
            d.ellipse([cx + dx - lw / 2, cy - lh / 2, cx + dx + lw / 2, cy + lh / 2], outline=MIST + (int(255 * op),), width=12)
        else:
            d.line([(cx + dx - lw / 2 + 10, cy), (cx + dx + lw / 2 - 10, cy)], fill=MIST + (int(255 * op),), width=12)
    img.alpha_composite(layer)

ITEMS = ["the sound of a cat's footsteps", "the beard of a woman", "the roots of a mountain",
         "the sinews of a bear", "the breath of a fish", "the spit of a bird"]

cards = [
    Card(0.2, 3.6, 300, [T("The gods chained", 66), T("the deadliest wolf alive", 66)]),
    Card(1.3, 3.6, 500, [B("with things that don't exist.", 54, GOLD)]),
    Card(3.8, 7.6, 1180, [T("FENRIR", 120, GOLD)]),
    Card(4.4, 7.6, 1340, [B("Son of Loki. Fated to kill Odin.", 50)]),
    Card(7.8, 10.6, 360, [T("Iron chains?", 70)]),
    Card(8.4, 10.6, 470, [B("He broke two of them like thread.", 50)]),
    Card(10.8, 19.6, 300, [[T("So dwarves forged ", 58), T("GLEIPNIR", 58, GOLD)]]),
    Card(11.3, 19.6, 400, [B("a ribbon soft as silk, made of", 50)]),
]
for i, item in enumerate(ITEMS):
    cards.append(Card(12.0 + i * 1.1, 19.6, 600 + i * 118, [B(item, 56, LIGHT)]))
cards += [
    Card(19.8, 23.2, 300, [T("Fenrir only agreed", 60), T("if a god put a hand", 60), T("in his mouth.", 60)]),
    Card(21.4, 23.2, 1420, [B("Týr did. He lost it.", 58, GOLD)]),
    Card(20.0, 23.2, 1520, [B("Art: John Bauer, Tyr and Fenrir, 1911", 30)]),
    Card(23.4, 26.6, 660, [B("The Edda says that's why", 56, LIGHT), B("cats walk in silence", 56, LIGHT),
                           B("and mountains have no roots.", 56, LIGHT)]),
    Card(26.8, 30.0, 700, [T("It held.", 80), T("Until Ragnarök.", 80, GOLD)]),
    Card(27.4, 30.0, 1000, [B("Now, back to the beginning.", 52, LIGHT)]),
    Card(27.9, 30.0, 1085, [B("Episode 1: Saturday  ·  " + nr.HANDLE, 42)]),
    Card(23.4, 26.6, 1440, [B("Source: Prose Edda, Gylfaginning", 34)]),
]

TYR_ART = nr.Painting("../images/bauer_tyr_fenrir_1911.jpg", 1020, 600, cy=1000, focus=(0.5, 0.5), crop=(40, 395, 733, 800))

LABEL = nr.Label("THE NORSE SAGA", "PROLOGUE")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    eyes(img, t, 1000, window(t, 0.6, 7.6, 0.8))
    TYR_ART.draw(img, t, 19.8, window(t, 19.8, 23.2, 0.5), dur=3.4)
    chain(img, t, 900, window(t, 7.8, 10.6))
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [2.5, 5.5, 9.8, 18.5, 22.5, 25.0, 28.8]:
            nr.still(f"stills/v01_{s}.png", s, frame)
    else:
        nr.render("out/v01_gleipnir.mp4", DUR, frame, seed=3, bpm=62)
