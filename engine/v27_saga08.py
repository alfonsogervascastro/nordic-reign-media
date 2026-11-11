"""The Norse Saga, Ep. 8 — Kvasir and the mead of poetry. Source: Prose Edda, Skáldskaparmál 1 (G57–58).
Art: Georg von Rosen, Odin the Wanderer (1886); Gotland picture stone detail often read as Odin, Suttungr and Gunnlöð.
No song for this episode: generated background. Voice: Kokoro am_michael."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 40.0
ODIN = nr.Painting("../images/rosen_odin_wanderer_1886.jpg", 700, 900, cy=1060, focus=(0.5, 0.25))
FACE = nr.Painting("../images/rosen_odin_wanderer_1886.jpg", 700, 700, cy=1040, crop=(120, 20, 400, 300), zoom=0.10, feather=0.12)
STONE = nr.Painting("../images/odin_suttungr_gunnlod.jpg", 980, 560, cy=1000, zoom=0.08, feather=0.10)
END = nr.TattooEnd("../tattoos/out/ep08_mead/ep08_mead_gold.png", t0=36.8)

def vat(img, t, op):
    """A cauldron glowing gold: the vat of spit, then the mead."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    glow = 0.6 + 0.4 * np.sin(t * 2.0)
    d.ellipse([W / 2 - 330, 900, W / 2 + 330, 1060], fill=GOLD + (int(170 * op * glow),))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(60)))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.pieslice([W / 2 - 300, 760, W / 2 + 300, 1360], 0, 180, fill=(43, 48, 56, int(255 * op)))
    d.ellipse([W / 2 - 300, 1000, W / 2 + 300, 1120], fill=(224, 164, 74, int(230 * op)))
    d.arc([W / 2 - 300, 1000, W / 2 + 300, 1120], 0, 360, fill=(255, 220, 160, int(255 * op)), width=6)
    img.alpha_composite(lay)

def mountain(img, t, op):
    """A black mountain with a thin gold tunnel boring into it (Odin's auger, Rati)."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.polygon([(40, 1500), (420, 760), (620, 900), (820, 700), (1040, 1500)], fill=(22, 26, 33, int(255 * op)))
    d.line([(420, 760), (620, 900), (820, 700)], fill=(90, 100, 115, int(255 * op)), width=4)
    k = ease((t - 16.6) / 3.0)
    if k > 0:
        d.line([(540, 1500), (540, 1500 - 520 * k)], fill=GOLD + (int(255 * op),), width=8)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10)))
    img.alpha_composite(lay)

def drops(img, t, op, t0):
    """Gold drops falling: the mead spat into the gods' vessels, and the few that fell behind."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    rng = np.random.default_rng(5)
    for i in range(40):
        x = rng.uniform(260, W - 260)
        ph = rng.uniform(0, 1.6)
        y = 700 + ((t - t0 + ph) * 520) % 900
        r = rng.uniform(5, 11)
        d.ellipse([x - r, y - r * 1.4, x + r, y + r], fill=GOLD + (int(230 * op),))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(4)))
    img.alpha_composite(lay)

cards = [
    Card(-0.8, 4.0, 330, [T("Poetry was made", 74), T("from spit.", 84, GOLD)]),
    Card(0.4, 4.0, 1600, [B("Art: Georg von Rosen, 1886", 30)]),
    Card(4.2, 9.0, 330, [B("To seal the peace, the gods and the Vanir", 46, LIGHT), B("all spat into one vat.", 52, LIGHT), B("From it they made Kvasir,", 52), T("the wisest man alive.", 60, GOLD)]),
    Card(9.2, 13.0, 330, [B("Two dwarves killed him", 56, LIGHT), B("and brewed his blood with honey:", 50, LIGHT), T("the mead of poetry.", 66, GOLD)]),
    Card(13.2, 16.4, 330, [B("A giant, Suttungr, took it", 54, LIGHT), B("and hid it inside a mountain.", 54)]),
    Card(16.6, 20.2, 330, [T("So Odin bored a hole", 66), T("and slid in as a snake.", 66, GOLD)]),
    Card(20.4, 24.6, 330, [B("Three nights with the giant's", 52, LIGHT), B("daughter, Gunnlöð.", 52, LIGHT), T("Three drinks. Every drop.", 62, GOLD)]),
    Card(20.8, 24.6, 1560, [B("Gotland picture stone, often read as this scene", 30)]),
    Card(24.8, 28.6, 330, [B("Then he flew home as an eagle,", 52, LIGHT), B("with Suttungr chasing him", 52, LIGHT), B("as an eagle too.", 52)]),
    Card(28.8, 33.4, 330, [B("He spat the mead into the gods' vessels.", 46, LIGHT), B("But a few drops fell out behind:", 50, LIGHT), T("the bad poets' share.", 64, GOLD)]),
    Card(29.2, 33.4, 1600, [B("Source: Prose Edda, Skáldskaparmál", 32)]),
    Card(33.6, 36.6, 330, [T("Which share", 76), T("did you get?", 76, GOLD)]),
    Card(34.0, 36.6, 1640, [B("Episode 9: Saturday  ·  " + nr.HANDLE, 40)]),
]

LABEL = nr.Label("THE NORSE SAGA", "EP. 8")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    ODIN.draw(img, t, 0.0, window(t, -1.0, 4.4, 0.5), dur=4.4)
    vat(img, t, window(t, 4.2, 9.4, 0.6))
    FACE.draw(img, t, 9.2, window(t, 9.2, 13.4, 0.5), dur=4.2)
    drops(img, t, window(t, 9.2, 13.2, 0.5), 9.2)
    mountain(img, t, window(t, 13.0, 20.4, 0.6))
    STONE.draw(img, t, 20.2, window(t, 20.2, 24.8, 0.5), dur=4.6)
    FACE.draw(img, t, 24.6, window(t, 24.6, 28.8, 0.5), dur=4.2)
    drops(img, t, window(t, 28.6, 33.6, 0.5), 28.6)
    ODIN.draw(img, t, 33.4, window(t, 33.4, 37.0, 0.5), dur=3.6)
    for c in cards:
        c.draw(img, t)
    END.draw(img, t)

SEGMENTS = [
    (0.0, 4.2, "Poetry was made from spit."),
    (4.2, 9.2, "To seal the peace, the gods and the Vanir all spat into one vat. From it they made Kvasir, the wisest man alive."),
    (9.2, 13.2, "Two dwarves killed him, and brewed his blood with honey: the mead of poetry."),
    (13.2, 16.6, "A giant, Suttung, took it, and hid it inside a mountain."),
    (16.6, 20.4, "So Odin bored a hole, and slid in as a snake."),
    (20.4, 24.8, "Three nights with the giant's daughter, Goonloth. Three drinks. Every drop."),
    (24.8, 28.8, "Then he flew home as an eagle, with Suttung chasing him as an eagle too."),
    (28.8, 33.6, "He spat the mead into the gods' vessels. But a few drops fell out behind: the bad poets' share."),
    (33.6, 36.8, "Which share did you get?"),
    (36.8, 40.0, "This chapter, as a tattoo."),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.5, 11.0, 15.0, 18.5, 22.5, 26.5, 31.0, 35.0, 38.5]:
            nr.still(f"stills/v27_{s}.png", s, frame, seed=89)
    else:
        import narrate
        print("duration", round(narrate.render_voiced("out/v27v_saga08.mp4", DUR, frame, SEGMENTS, seed=89, bpm=58), 2))
