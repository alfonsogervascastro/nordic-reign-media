"""The Norse Saga, Ep. 7 — Odin's eye in Mímir's well, and the ravens Huginn and Muninn.
Sources: Prose Edda, Gylfaginning 15 (the pledge of the eye) and 38 (the ravens); Völuspá 28; Grímnismál 20.
Art: Robert Engels, Odin at the Well of Wisdom (1903); Lorenz Frølich, Odin with Sleipnir and the ravens (1895);
Oluf O. Bagge, Yggdrasil (1847). Soundtrack: Odin's Sacrifice (instrumental) by Nordic Reign. Voice: Kokoro am_michael."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 39.0
WELL = "../images/engels_odin_mimir_well_1903.jpg"
FULL = nr.Painting(WELL, 760, 1000, cy=1060, zoom=0.08, feather=0.10)
ODIN = nr.Painting(WELL, 900, 760, cy=1020, crop=(0, 560, 640, 1100), zoom=0.10, feather=0.12)
MIMIR = nr.Painting(WELL, 900, 760, cy=1020, crop=(0, 0, 960, 700), zoom=0.10, feather=0.12)
ROOTS = nr.Painting("../images/bagge_yggdrasil_1847.jpg", 900, 760, cy=1000, crop=(230, 640, 730, 999), zoom=0.10, feather=0.12)
RAVENS = nr.Painting("../images/froelich_odin_ravens_1895.jpg", 820, 720, cy=1000, zoom=0.08, feather=0.10)
RAVEN_L = nr.Painting("../images/froelich_odin_ravens_1895.jpg", 820, 720, cy=1000, crop=(0, 0, 180, 150), zoom=0.10, feather=0.12)
END = nr.TattooEnd("../tattoos/out/ep07_ravens/ep07_ravens_gold.png", t0=35.8)

def well_eye(img, t, op):
    """Deep water with one gold glint at the bottom: the eye left as a pledge (atmosphere only)."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(6):
        r = 120 + i * 70 + 20 * np.sin(t * 1.5 + i)
        d.ellipse([W / 2 - r * 1.8, 1050 - r * 0.6, W / 2 + r * 1.8, 1050 + r * 0.6],
                  outline=(120, 160, 200, int(90 * op)), width=4)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(6)))
    k = ease((t - 13.6) / 1.2)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([W / 2 - 70, 1050 - 32, W / 2 + 70, 1050 + 32], fill=GOLD + (int(230 * op * k),))
    d.ellipse([W / 2 - 14, 1050 - 30, W / 2 + 14, 1050 + 30], fill=(14, 17, 22, int(255 * op * k)))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(18)))
    img.alpha_composite(lay)

cards = [
    Card(-0.8, 4.0, 330, [T("Odin paid for wisdom", 70), T("with an eye.", 80, GOLD)]),
    Card(0.4, 4.0, 1620, [B("Art: Robert Engels, 1903", 30)]),
    Card(4.2, 8.6, 330, [B("At the roots of Yggdrasil", 54, LIGHT), B("lies the well of Mímir,", 54, LIGHT), B("the wisest being in the worlds.", 50)]),
    Card(8.8, 12.6, 330, [B("Odin asked for one drink.", 56, LIGHT), T("The price: one eye.", 70, GOLD)]),
    Card(12.8, 16.8, 330, [B("He paid it.", 60, LIGHT), B("The eye still lies", 54, LIGHT), B("at the bottom of the well.", 54)]),
    Card(13.2, 16.8, 1560, [B("Völuspá 28; Gylfaginning 15", 32)]),
    Card(17.0, 20.4, 330, [T("But one eye", 74), T("can't watch nine worlds.", 66, GOLD)]),
    Card(20.6, 25.0, 330, [B("So every dawn, two ravens fly out:", 50, LIGHT), T("Huginn, “Thought”", 64, GOLD), T("Muninn, “Memory”", 64, GOLD)]),
    Card(21.0, 25.0, 1520, [B("Art: Lorenz Frølich, 1895", 30)]),
    Card(25.2, 29.0, 330, [B("By breakfast they are back,", 54, LIGHT), B("whispering everything they saw", 50, LIGHT), B("into his ears.", 50)]),
    Card(29.2, 32.6, 330, [B("And Odin admits he fears for Thought,", 48, LIGHT), T("but fears more for Memory.", 60, GOLD)]),
    Card(29.6, 32.6, 1560, [B("Grímnismál 20; Gylfaginning 38", 32)]),
    Card(32.8, 35.6, 330, [T("Thought or Memory:", 72), T("which would you keep?", 66, GOLD)]),
    Card(33.2, 35.6, 1640, [B("Episode 8: Wednesday  ·  " + nr.HANDLE, 40)]),
]

LABEL = nr.Label("THE NORSE SAGA", "EP. 7")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    FULL.draw(img, t, 0.0, window(t, -1.0, 4.4, 0.5), dur=4.4)
    ROOTS.draw(img, t, 4.2, window(t, 4.2, 8.8, 0.5), dur=4.6)
    ODIN.draw(img, t, 8.6, window(t, 8.6, 12.8, 0.5), dur=4.2)
    well_eye(img, t, window(t, 12.6, 17.0, 0.5))
    MIMIR.draw(img, t, 16.8, window(t, 16.8, 20.6, 0.5), dur=3.8)
    RAVENS.draw(img, t, 20.4, window(t, 20.4, 25.2, 0.5), dur=4.8)
    RAVEN_L.draw(img, t, 25.0, window(t, 25.0, 29.2, 0.5), dur=4.2)
    FULL.draw(img, t, 29.0, window(t, 29.0, 33.0, 0.6), dur=4.0)
    MIMIR.draw(img, t, 32.8, window(t, 32.8, 36.0, 0.5), dur=3.2)
    for c in cards:
        c.draw(img, t)
    END.draw(img, t)

SEGMENTS = [
    (0.0, 4.2, "Odin paid for wisdom with an eye."),
    (4.2, 8.8, "At the roots of Yggdrasil lies the well of Meemeer, the wisest being in the worlds."),
    (8.8, 12.8, "Odin asked for one drink. The price: one eye."),
    (12.8, 17.0, "He paid it. The eye still lies at the bottom of the well."),
    (17.0, 20.6, "But one eye can't watch nine worlds."),
    (20.6, 25.2, "So every dawn, two ravens fly out. Hoogin, Thought. And Moonin, Memory."),
    (25.2, 29.2, "By breakfast they are back, whispering everything they saw into his ears."),
    (29.2, 32.8, "And Odin admits he fears for Thought, but fears more for Memory."),
    (32.8, 35.8, "Thought, or Memory. Which would you keep?"),
    (35.8, 39.0, "This chapter, as a tattoo."),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 10.5, 15.0, 18.5, 22.5, 27.0, 31.0, 34.0, 37.5]:
            nr.still(f"stills/v24_{s}.png", s, frame, seed=73)
    else:
        import narrate
        d = narrate.render_voiced("out/v24v_saga07.mp4", DUR, frame, SEGMENTS, seed=73, bpm=60,
                                  music="../audio/odins-sacrifice.mp3", music_start=0.0)
        print("duration", round(d, 2))
