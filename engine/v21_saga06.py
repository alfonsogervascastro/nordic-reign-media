"""The Norse Saga, Ep. 6 — Nine nights on the tree: Odin wins the runes. Source: Hávamál 138–139
(Bellows 1923 numbers them 139–140). Art: Oluf O. Bagge, Yggdrasil (1847); Georg von Rosen, Odin the Wanderer (1886).
Soundtrack: Nine Days Below (instrumental) by Nordic Reign. Voice: Kokoro am_michael."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr
nr.RUNES.setdefault("algiz", [[(0.5, 0), (0.5, 1)], [(0.5, 0.45), (0.18, 0.05)], [(0.5, 0.45), (0.82, 0.05)]])
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 38.0
TREE = "../images/bagge_yggdrasil_1847.jpg"
ODIN_SRC = "../images/rosen_odin_wanderer_1886.jpg"
FULL = nr.Painting(TREE, 760, 840, cy=1030, zoom=0.08, feather=0.10)
TRUNK = nr.Painting(TREE, 900, 820, cy=1000, crop=(250, 300, 650, 760), zoom=0.10, feather=0.12)
ROOTS = nr.Painting(TREE, 900, 760, cy=1000, crop=(230, 640, 730, 999), zoom=0.10, feather=0.12)
ODIN = nr.Painting(ODIN_SRC, 700, 900, cy=1060, focus=(0.5, 0.25))
FACE = nr.Painting(ODIN_SRC, 700, 700, cy=1040, crop=(120, 20, 400, 300), zoom=0.10, feather=0.12)
END = nr.TattooEnd("../tattoos/out/ep06_nine_nights/ep06_nine_nights_gold.png", t0=34.8)
RUNE_ORDER = ["fehu", "uruz", "thurisaz", "ansuz", "raidho", "kaunan", "gebo", "wunjo", "hagalaz",
              "naudiz", "isa", "jera", "eihwaz", "perthro", "algiz", "sowilo", "tiwaz", "berkano",
              "ehwaz", "mannaz", "laguz", "ingwaz", "othala", "dagaz"]

def nights(img, t, op):
    """Nine tally marks carved one by one: the nine nights."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x0, y = W / 2 - 4 * 70, 1440
    for i in range(9):
        k = ease((t - (8.6 + i * 0.32)) / 0.3)
        if k <= 0:
            continue
        x = x0 + i * 70
        d.line([x, y, x, y + 110 * k], fill=GOLD + (int(255 * op),), width=10)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(8)))
    img.alpha_composite(lay)

def dark(img, t, op):
    """The abyss under the tree: a cold glow far below."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    r = 260 + 40 * np.sin(t * 1.3)
    d.ellipse([W / 2 - r * 1.6, 1250 - r, W / 2 + r * 1.6, 1250 + r], fill=(120, 150, 190, int(110 * op)))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(90)))

def runes(img, t, op, t0):
    """The 24 runes rise out of the dark, one after another, and glow."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cols, size = 6, 120
    x0 = W / 2 - (cols - 1) * 150 / 2
    for i, r in enumerate(RUNE_ORDER):
        k = ease((t - (t0 + i * 0.14)) / 0.5)
        if k <= 0:
            continue
        cx = x0 + (i % cols) * 150
        cy = 760 + (i // cols) * 200 + 40 * (1 - k)
        nr.draw_rune(lay, r, cx - size / 3, cy, size * 0.66, size * 1.2, k, width=11)
    a = np.asarray(lay, np.float32).copy(); a[..., 3] *= op
    img.alpha_composite(Image.fromarray(a.astype(np.uint8)))

cards = [
    Card(-0.8, 4.0, 330, [T("Odin hanged himself.", 72), T("On purpose.", 76, GOLD)]),
    Card(0.4, 4.0, 1560, [B("Art: Georg von Rosen, 1886", 30)]),
    Card(4.2, 8.4, 330, [B("Nine nights on Yggdrasil,", 56, LIGHT), B("the tree that holds the worlds,", 52, LIGHT), B("wounded by his own spear.", 52)]),
    Card(4.6, 8.4, 1560, [B("Art: Oluf O. Bagge, Yggdrasil, 1847", 30)]),
    Card(8.6, 12.6, 330, [B("A sacrifice, he says:", 52, LIGHT), T("“myself to myself.”", 70, GOLD)]),
    Card(12.8, 16.8, 330, [B("No bread. No drink.", 60, LIGHT), B("He stared down into the dark.", 52)]),
    Card(17.0, 20.4, 330, [T("On the ninth night,", 70), T("he saw them.", 76, GOLD)]),
    Card(20.6, 25.0, 330, [B("He took up the runes,", 58, LIGHT), T("screaming,", 70, GOLD), B("and fell back from the tree.", 52)]),
    Card(25.2, 30.4, 330, [B("The Norse believed writing itself", 50, LIGHT), B("was won by a god's sacrifice.", 50, LIGHT), T("That is why the runes are Odin's.", 54, GOLD)]),
    Card(25.6, 30.4, 1560, [B("Source: Hávamál 138–139 (trans. Bellows, 1923)", 30)]),
    Card(30.6, 34.6, 330, [T("Would you hang", 72), T("nine nights for that?", 72, GOLD)]),
    Card(31.2, 34.6, 1460, [B("Episode 7: Saturday  ·  " + nr.HANDLE, 40)]),
]

LABEL = nr.Label("THE NORSE SAGA", "EP. 6")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    ODIN.draw(img, t, 0.0, window(t, -1.0, 4.2, 0.5), dur=4.2)
    FULL.draw(img, t, 4.0, window(t, 4.0, 8.6, 0.5), dur=4.6)
    TRUNK.draw(img, t, 8.4, window(t, 8.4, 12.8, 0.5), dur=4.4)
    nights(img, t, window(t, 8.4, 12.8, 0.4))
    ROOTS.draw(img, t, 12.6, window(t, 12.6, 17.0, 0.5), dur=4.4)
    dark(img, t, window(t, 14.0, 25.2, 0.8))
    runes(img, t, window(t, 17.0, 25.2, 0.5), 17.2)
    FACE.draw(img, t, 25.0, window(t, 25.0, 30.6, 0.6), dur=5.6)
    FULL.draw(img, t, 30.4, window(t, 30.4, 35.0, 0.6), dur=4.6)
    for c in cards:
        c.draw(img, t)
    END.draw(img, t)

SEGMENTS = [
    (0.0, 4.2, "Odin hanged himself. On purpose."),
    (4.2, 8.6, "Nine nights on Yggdrasil, the tree that holds the worlds, wounded by his own spear."),
    (8.6, 12.8, "A sacrifice, he says: myself, to myself."),
    (12.8, 17.0, "No bread. No drink. He stared down into the dark."),
    (17.0, 20.6, "On the ninth night, he saw them."),
    (20.6, 25.2, "He took up the runes, screaming, and fell back from the tree."),
    (25.2, 30.6, "The Norse believed writing itself was won by a god's sacrifice. That is why the runes are Odin's."),
    (30.6, 34.8, "Would you hang nine nights for that?"),
    (34.8, 38.0, "This chapter, as a tattoo."),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 10.5, 15.0, 19.5, 23.0, 28.0, 32.0, 36.5]:
            nr.still(f"stills/v21_{s}.png", s, frame, seed=61)
    else:
        import narrate
        d = narrate.render_voiced("out/v21v_saga06.mp4", DUR, frame, SEGMENTS, seed=61, bpm=60,
                                  music="../audio/nine-days-below.mp3", music_start=2.0)
        print("duration", round(d, 2))
