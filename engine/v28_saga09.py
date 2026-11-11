"""The Norse Saga, Ep. 9 — the wall of Asgard and the birth of Sleipnir. Source: Prose Edda, Gylfaginning 42; Völuspá 25–26.
Art: Oluf O. Bagge, Yggdrasil (1847); Mårten Eskil Winge, Tor's Fight with the Giants (1872);
Lorenz Frølich, Odin on Sleipnir (1895). Soundtrack: Inside the Lie (instrumental) by Nordic Reign. Voice: Kokoro am_michael."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 40.0
TREE = "../images/bagge_yggdrasil_1847.jpg"
WINGE = "../images/winge_thor_giants_1872.jpg"
ASGARD = nr.Painting(TREE, 1000, 560, cy=980, crop=(60, 250, 860, 560), zoom=0.10, feather=0.12)
THOR = nr.Painting(WINGE, 760, 1000, cy=1080, crop=(150, 0, 1280, 1300), zoom=0.08, feather=0.10)
HAMMER = nr.Painting(WINGE, 860, 760, cy=1020, crop=(250, 0, 1150, 800), zoom=0.10, feather=0.12)
SLEIPNIR = nr.Painting("../images/froelich_odin_ravens_1895.jpg", 820, 720, cy=1000, zoom=0.08, feather=0.10)
ODIN = nr.Painting("../images/rosen_odin_wanderer_1886.jpg", 700, 900, cy=1060, focus=(0.5, 0.25))
END = nr.TattooEnd("../tattoos/out/ep09_sleipnir/ep09_sleipnir_gold.png", t0=36.8)

def wall(img, t, op, t0, t1):
    """Stone courses rising row by row, faster and faster (the stallion does twice the work)."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rows = int(14 * ease((t - t0) / (t1 - t0)) ** 0.7)
    for r in range(rows):
        y = 1500 - r * 52
        off = 60 if r % 2 else 0
        for x in range(60 - off, W - 40, 120):
            d.rectangle([x + 4, y - 46, x + 116, y], fill=(52, 58, 68, int(255 * op)), outline=(90, 100, 115, int(255 * op)))
    img.alpha_composite(lay)

def winter(img, t, op):
    """Snow falling: the deal had to be done in one winter."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rng = np.random.default_rng(9)
    for i in range(90):
        x0, sp, ph = rng.uniform(0, W), rng.uniform(60, 140), rng.uniform(0, 20)
        y = 300 + ((t * sp + ph * 80) % 1500)
        x = x0 + 20 * np.sin(t + ph)
        r = rng.uniform(2, 5)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(214, 226, 238, int(200 * op)))
    img.alpha_composite(lay)

cards = [
    Card(-0.8, 4.0, 330, [T("Odin's eight-legged horse", 64), T("was born from a lie.", 70, GOLD)]),
    Card(0.4, 4.0, 1600, [B("Art: Oluf O. Bagge, 1847", 30)]),
    Card(4.2, 8.8, 330, [B("A builder offered the gods", 54, LIGHT), B("a wall around Asgard", 54, LIGHT), T("in a single winter.", 64, GOLD)]),
    Card(9.0, 13.2, 330, [B("His price: the goddess Freyja,", 52, LIGHT), T("the sun and the moon.", 66, GOLD)]),
    Card(13.4, 17.6, 330, [B("Loki told the gods:", 54, LIGHT), B("let him use his horse.", 54, LIGHT), B("The stallion did twice his work.", 50)]),
    Card(17.8, 21.6, 330, [T("Three days from summer,", 66), T("the wall was almost done.", 64, GOLD)]),
    Card(21.8, 25.6, 330, [B("So Loki turned himself", 56, LIGHT), B("into a mare", 56, LIGHT), B("and led the stallion away.", 52)]),
    Card(25.8, 29.6, 330, [B("The builder raged: he was a giant.", 50, LIGHT), T("Thor came home", 66), T("and paid him with the hammer.", 58, GOLD)]),
    Card(26.2, 29.6, 1640, [B("Art: Mårten Eskil Winge, 1872", 30)]),
    Card(29.8, 33.6, 330, [B("Months later, Loki gave birth", 52, LIGHT), B("to a grey foal with eight legs:", 50, LIGHT), T("Sleipnir, Odin's horse.", 62, GOLD)]),
    Card(30.2, 33.6, 1600, [B("Source: Prose Edda, Gylfaginning 42", 32)]),
    Card(33.8, 36.6, 330, [T("Would you trust Loki?", 70), B("Yes or no.", 54, GOLD)]),
    Card(34.2, 36.6, 1640, [B("Episode 10: Wednesday  ·  " + nr.HANDLE, 40)]),
]

LABEL = nr.Label("THE NORSE SAGA", "EP. 9")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    ASGARD.draw(img, t, 0.0, window(t, -1.0, 4.4, 0.5), dur=4.4)
    winter(img, t, window(t, 4.2, 21.8, 0.6))
    wall(img, t, window(t, 4.2, 9.2, 0.5), 4.2, 9.0)
    ODIN.draw(img, t, 9.0, window(t, 9.0, 13.4, 0.5), dur=4.4)
    wall(img, t, window(t, 13.2, 21.8, 0.5), 13.2, 21.4)
    ASGARD.draw(img, t, 21.6, window(t, 21.6, 25.8, 0.5), dur=4.2)
    THOR.draw(img, t, 25.6, window(t, 25.6, 29.8, 0.5), dur=4.2)
    SLEIPNIR.draw(img, t, 29.6, window(t, 29.6, 33.8, 0.5), dur=4.2)
    HAMMER.draw(img, t, 33.6, window(t, 33.6, 37.0, 0.5), dur=3.4)
    for c in cards:
        c.draw(img, t)
    END.draw(img, t)

SEGMENTS = [
    (0.0, 4.2, "Odin's eight-legged horse was born from a lie."),
    (4.2, 9.0, "A builder offered the gods a wall around Asgard, in a single winter."),
    (9.0, 13.4, "His price: the goddess Freya, the sun, and the moon."),
    (13.4, 17.8, "Loki told the gods: let him use his horse. The stallion did twice his work."),
    (17.8, 21.8, "Three days from summer, the wall was almost done."),
    (21.8, 25.8, "So Loki turned himself into a mare, and led the stallion away."),
    (25.8, 29.8, "The builder raged: he was a giant. Thor came home, and paid him with the hammer."),
    (29.8, 33.8, "Months later, Loki gave birth to a grey foal with eight legs: Sleipnir, Odin's horse."),
    (33.8, 36.8, "Would you trust Loki?"),
    (36.8, 40.0, "This chapter, as a tattoo."),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.5, 11.0, 15.5, 20.0, 23.5, 27.5, 31.5, 35.0, 38.5]:
            nr.still(f"stills/v28_{s}.png", s, frame, seed=97)
    else:
        import narrate
        d = narrate.render_voiced("out/v28v_saga09.mp4", DUR, frame, SEGMENTS, seed=97, bpm=60,
                                  music="../audio/inside-the-lie.mp3", music_start=0.0)
        print("duration", round(d, 2))
