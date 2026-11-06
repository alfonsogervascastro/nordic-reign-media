"""The Norse Saga, Ep. 5 — the Æsir–Vanir war. Sources: Völuspá 21–24; Ynglinga saga 4; Skáldskaparmál (Kvasir).
Art: Lorenz Frølich (1895), Odin throws his spear over the Vanir."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 34.2
SRC = "../images/froelich_aesir_vanir_war_1895.jpg"
FULL = nr.Painting(SRC, 1000, 660, cy=980, focus=(0.75, 0.3), zoom=0.08, feather=0.10)
ODIN = nr.Painting(SRC, 620, 860, cy=1110, crop=(330, 0, 800, 737), zoom=0.10, feather=0.12)
ARMY = nr.Painting(SRC, 980, 700, cy=980, crop=(0, 150, 620, 640), zoom=0.10, feather=0.12)
END = nr.TattooEnd("../tattoos/out/ep05_aesir_vanir/ep05_aesir_vanir_gold.png", t0=31.0)

def fire(img, t, op):
    """Rising embers and a low red glow (atmosphere for Gullveig's burning)."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([W / 2 - 420, 1250, W / 2 + 420, 1750], fill=(200, 80, 30, int(150 * op)))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(80)))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rng = np.random.default_rng(3)
    for i in range(60):
        x0, sp, ph = rng.uniform(200, W - 200), rng.uniform(80, 200), rng.uniform(0, 10)
        y = 1650 - ((t * sp + ph * 100) % 900)
        x = x0 + 30 * np.sin(t * 2 + ph)
        r = rng.uniform(2, 5)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(240, 160, 70, int(220 * op)))
    img.alpha_composite(lay)

def heads(img, t, op):
    """Two gold rings joined: the truce and the exchange of hostages (atmosphere)."""
    if op <= 0:
        return
    k = ease((t - 19.4) / 1.0)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for cx in (W / 2 - 150 * k, W / 2 + 150 * k):
        d.ellipse([cx - 230, 1000 - 230, cx + 230, 1000 + 230], outline=GOLD + (int(230 * op),), width=7)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(14)))
    img.alpha_composite(lay)

cards = [
    Card(-0.8, 4.0, 330, [T("The first war", 76), T("began with a fire.", 70, GOLD)]),
    Card(0.4, 4.0, 1420, [B("Art: Lorenz Frølich, 1895", 30)]),
    Card(4.2, 8.6, 330, [B("A woman called Gullveig came to the gods.", 46, LIGHT), B("They pierced her with spears", 52, LIGHT), B("and burned her.", 52, LIGHT)]),
    Card(8.8, 12.0, 330, [T("Three times.", 80, GOLD), B("Three times she was reborn.", 52, LIGHT)]),
    Card(12.2, 15.8, 330, [B("Her people, the Vanir, went to war.", 52, LIGHT), B("Odin threw his spear over them:", 52)]),
    Card(13.6, 15.8, 560, [T("the first war in the world.", 60, GOLD)]),
    Card(16.0, 19.2, 330, [B("Neither side could win.", 56, LIGHT), B("The wall of Asgard fell.", 56, LIGHT)]),
    Card(19.4, 23.4, 330, [T("So they made peace", 70), B("and swapped hostages:", 52, LIGHT), B("Njörðr and Freyr went to the gods.", 46)]),
    Card(23.6, 27.2, 330, [B("The Vanir cut off", 56, LIGHT), B("the head of wise Mímir", 56, LIGHT), B("and sent it back to Odin.", 52)]),
    Card(27.4, 30.8, 330, [B("Odin kept the head alive", 56, LIGHT), T("to whisper secrets to him.", 62, GOLD)]),
    Card(28.6, 30.8, 1460, [B("Episode 6: Wednesday  ·  " + nr.HANDLE, 40)]),
    Card(24.0, 27.2, 1460, [B("Source: Völuspá 21–24; Ynglinga saga 4", 32)]),
]

LABEL = nr.Label("THE NORSE SAGA", "EP. 5")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    FULL.draw(img, t, 0.0, window(t, -1.0, 4.2, 0.5), dur=4.2)
    fire(img, t, window(t, 4.0, 12.2, 0.8))
    ODIN.draw(img, t, 12.0, window(t, 12.0, 16.0, 0.5), dur=4.0)
    ARMY.draw(img, t, 16.0, window(t, 16.0, 19.4, 0.5), dur=3.4)
    heads(img, t, window(t, 19.2, 27.4, 0.6))
    FULL.draw(img, t, 27.2, window(t, 27.2, 31.0, 0.6), dur=3.8)
    for c in cards:
        c.draw(img, t)
    END.draw(img, t)

SEGMENTS = [
    (0.0, 4.2, "The first war began with a fire."),
    (4.2, 8.8, "A woman called Gullveig came to the gods. They pierced her with spears, and burned her."),
    (8.8, 12.2, "Three times. Three times she was reborn."),
    (12.2, 16.0, "Her people, the Vanir, went to war. Odin threw his spear over them: the first war in the world."),
    (16.0, 19.4, "Neither side could win. The wall of Asgard fell."),
    (19.4, 23.6, "So they made peace, and swapped hostages."),
    (23.6, 27.4, "The Vanir cut off the head of wise Meemeer, and sent it back to Odin."),
    (27.4, 31.0, "Odin kept the head alive, to whisper secrets to him."),
    (31.0, 34.2, "This chapter, as a tattoo."),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 13.5, 17.5, 21.5, 33.0]:
            nr.still(f"stills/v14_{s}.png", s, frame, seed=43)
    else:
        import narrate
        print("duration", round(narrate.render_voiced("out/v14v_saga05.mp4", DUR, frame, SEGMENTS, seed=43, bpm=60), 2))
