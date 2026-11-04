"""Words from the North — Tolkien's dwarves come from the Völuspá's list of dwarves (Dvergatal, st. 10–16).
Middle-earth = Old English middangeard, cognate of Old Norse Miðgarðr."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr, scenes
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 31.6
NAMES = ["Durinn", "Þorinn", "Þráinn", "Dvalinn", "Bívurr", "Bávurr", "Bömburr",
         "Nóri", "Óri", "Dóri", "Óinn", "Glóinn", "Fíli", "Kíli"]
MOUNT = scenes.Mountains(seed=11, horizon=1470)

def names_grid(img, t, op):
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = nr.font("title", 58)
    for i, n in enumerate(NAMES):
        k = op * ease((t - 9.2 - i * 0.45) / 0.4)
        if k <= 0:
            continue
        col, row = i % 2, i // 2
        x = 300 if col == 0 else W - 300
        y = 480 + row * 96 + (1 - k) * 16
        bb = d.textbbox((0, 0), n, font=f)
        c = GOLD if n in ("Durinn", "Þorinn") else LIGHT
        d.text((x - (bb[2] - bb[0]) / 2, y), n, font=f, fill=c + (int(255 * k),))
    img.alpha_composite(lay)

def forge(img, t, op):
    """Warm light from a door in the mountain (atmosphere)."""
    if op <= 0:
        return
    flick = 0.85 + 0.15 * np.sin(t * 7.0) * np.sin(t * 3.1)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([W / 2 - 220, 1440, W / 2 + 220, 1720], fill=(235, 140, 60, int(120 * op * flick)))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(60)))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    fc = (240, 170, 90, int(230 * op * flick))
    dd.rectangle([W / 2 - 46, 1600, W / 2 + 46, 1670], fill=fc)
    dd.pieslice([W / 2 - 46, 1554, W / 2 + 46, 1646], 180, 360, fill=fc)
    img.alpha_composite(lay)

cards = [
    Card(0.2, 4.0, 520, [T("Tolkien didn't invent", 70), T("his dwarves' names.", 70, GOLD)]),
    Card(1.5, 4.0, 800, [B("He found them in a Norse poem", 52, LIGHT), B("written down 750 years ago.", 52, LIGHT)]),
    Card(4.2, 8.8, 520, [T("Völuspá", 96, GOLD), B('"The Prophecy of the Seeress"', 50, LIGHT)]),
    Card(5.4, 8.8, 820, [B("Among the gods and giants,", 50), B("it lists the dwarves by name.", 50)]),
    Card(9.0, 17.0, 330, [B("Stanzas 10–16:", 48, MIST)]),
    Card(17.2, 20.8, 520, [B("Even his surname is there:", 52, LIGHT)]),
    Card(17.8, 20.8, 700, [T("Eikinskjaldi", 96, GOLD), B('"Oak-shield"  →  Thorin Oakenshield', 50, LIGHT)]),
    Card(21.0, 24.6, 520, [B("And one more name on the list:", 52, LIGHT)]),
    Card(21.6, 24.6, 700, [T("Gandálfr", 104, GOLD), B('probably "wand-elf"', 50, LIGHT)]),
    Card(24.8, 28.4, 480, [B("Even Middle-earth:", 54, LIGHT)]),
    Card(25.3, 28.4, 640, [T("middangeard", 76), B("Old English", 40)]),
    Card(25.9, 28.4, 860, [T("Miðgarðr", 76, GOLD), B("Old Norse: the world of humans", 40)]),
    Card(26.5, 28.4, 1080, [B("Same word, same idea.", 46)]),
    Card(28.6, 31.6, 600, [T("Which name", 74), T("did you spot first?", 74, GOLD)]),
    Card(29.3, 31.6, 880, [B("Source: Poetic Edda, Völuspá 10–16", 36), B(nr.HANDLE, 40)]),
]

LABEL = nr.Label("WORDS FROM THE NORTH")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    m = window(t, 0.0, 31.6, 0.8)
    if m > 0:
        MOUNT.draw(img, t, op=m)
        forge(img, t, m)
    names_grid(img, t, window(t, 9.0, 17.0, 0.5))
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [2.5, 7.0, 15.5, 19.5, 23.0, 27.5]:
            nr.still(f"stills/v09_{s}.png", s, frame, seed=29)
    else:
        nr.render("out/v09_tolkien.mp4", DUR, frame, seed=29, bpm=66)
