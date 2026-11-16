"""Reel covers (1080x1920) and Instagram stories for the scheduled videos.
One template for the whole grid: series label, a painting (or the rune slab), a big two-line title, the handle.
The Instagram grid shows the centre 3:4 (y 240-1680), so everything important lives there.
Usage:  python3 covers.py            -> ../<month>/covers/<date>_cover.jpg and <date>_story.jpg
"""
import os
import numpy as np
from PIL import Image, ImageDraw
import nr
from nr import T, B, GOLD, LIGHT, MIST, W, H

nr.RUNES.setdefault("algiz", [[(0.5, 0), (0.5, 1)], [(0.5, 0.45), (0.18, 0.05)], [(0.5, 0.45), (0.82, 0.05)]])
I = "../images/"
ROSEN, BAGGE, WINGE = I + "rosen_odin_wanderer_1886.jpg", I + "bagge_yggdrasil_1847.jpg", I + "winge_thor_giants_1872.jpg"

# date, series label, (title line 1, title line 2 in gold), art: painting path | ("runes", [rune names])
COVERS = [
    ("2026-11-16", "RUNE  2 / 24", ("URUZ", "Ox, slag or rain?"), ("runes", ["uruz"])),
    ("2026-11-17", "YOUR NAME IN RUNES", ("SIGRID", "in Elder Futhark"), ("name", "Sigrid")),
    ("2026-11-18", "THE NORSE SAGA  ·  EP. 4", ("The first humans", "were made of wood"), I + "froelich_ask_embla_1895.jpg"),
    ("2026-11-19", "WORDS FROM THE NORTH", ("This god's name", "just means “god”"), I + "bauer_tyr_fenrir_1911.jpg"),
    ("2026-11-20", "MYTH vs HISTORY", ("Vikings had a day", "just for bathing"), WINGE),
    ("2026-11-21", "THE NORSE SAGA  ·  EP. 5", ("The first war", "in the world"), I + "froelich_aesir_vanir_war_1895.jpg"),
    ("2026-11-22", "HÁVAMÁL  ·  55", ("Odin's advice:", "don't be too wise"), ROSEN),
    ("2026-11-23", "RUNE  3 / 24", ("THURISAZ", "Giant or thorn?"), ("runes", ["thurisaz"])),
    ("2026-11-24", "YOUR NAME IN RUNES", ("FREYA", "in Elder Futhark"), ("name", "Freya")),
    ("2026-11-25", "THE NORSE SAGA  ·  EP. 6", ("Nine nights", "on the tree"), BAGGE),
    ("2026-11-26", "WORDS FROM THE NORTH", ("“Rune”", "first meant secret"), ("name", "Runa")),
    ("2026-11-27", "REAL VIKINGS", ("A warrior's grave.", "Then came the DNA."), I + "stolpe_birka_bj581_1889.jpg"),
    ("2026-11-28", "THE NORSE SAGA  ·  EP. 7", ("Odin's eye", "and the two ravens"), I + "engels_odin_mimir_well_1903.jpg"),
    ("2026-11-29", "HÁVAMÁL  ·  47", ("Odin's cure", "for loneliness"), I + "engels_odin_mimir_well_1903.jpg"),
    ("2026-11-30", "RUNE  4 / 24", ("ANSUZ", "Odin's own rune"), ("runes", ["ansuz"])),
    ("2026-12-01", "YOUR NAME IN RUNES", ("INGRID", "in Elder Futhark"), ("name", "Ingrid")),
    ("2026-12-02", "THE NORSE SAGA  ·  EP. 8", ("Poetry was made", "from spit"), ROSEN),
    ("2026-12-03", "WORDS FROM THE NORTH", ("Odin's name", "means fury"), I + "doepler_ragnarok_1905.jpg"),
    ("2026-12-04", "MYTH vs HISTORY", ("Berserkers on", "magic mushrooms?"), WINGE),
    ("2026-12-05", "THE NORSE SAGA  ·  EP. 9", ("Odin's horse was", "born from a lie"), BAGGE),
    ("2026-12-06", "HÁVAMÁL  ·  1", ("Odin's first rule:", "check the doors"), ROSEN),
    ("2026-12-07", "RUNE  5 / 24", ("RAIDHO", "The rider's rune"), ("runes", ["raidho"])),
]

def art(img, a):
    if isinstance(a, str):
        foc = (0.0, 0.2) if "bauer_tyr" in a else (0.5, 0.4)
        P = nr.Painting(a, 1000, 960, cy=860, zoom=0.04, feather=0.10, focus=foc)
        P.draw(img, 2.0, 0.0, 1.0, dur=4.0)
        return
    kind, val = a
    runes = val if kind == "runes" else [r for _, r in nr.transliterate(val)]
    n = len(runes)
    sw = 520 if n == 1 else min(980, 150 * n + 120)
    sh = 760 if n == 1 else 520
    x, y = (W - sw) / 2, 900 - sh / 2
    nr.draw_slab(img, x, y, sw, sh, 1.0)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    if n == 1:
        nr.draw_rune(lay, runes[0], x + 90, y + 90, sw - 180, sh - 180, 1.0, width=38)
    else:
        step = (sw - 120) / n
        for i, r in enumerate(runes):
            nr.draw_rune(lay, r, x + 60 + i * step + step * 0.15, y + 90, step * 0.7, sh - 180, 1.0, width=18)
    img.alpha_composite(lay)

def shade(img, y0, y1, alpha=210):
    """Dark band behind the title so it reads on any painting."""
    a = np.zeros((H, W), np.float32)
    for y in range(int(y0), int(y1)):
        k = min((y - y0) / 120, (y1 - y) / 120, 1.0)
        a[y, :] = alpha * max(k, 0)
    lay = Image.new("RGBA", (W, H), (10, 12, 16, 0))
    lay.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(lay)

def cover(date, label, title, a, story=False):
    img = nr.Background(5).render(1.0)
    art(img, a)
    shade(img, 1160, 1580)
    nr.draw_lines(img, [T(label, 54, GOLD)], 280, 1.0)
    nr.draw_lines(img, [T(title[0], 104, LIGHT), T(title[1], 92, GOLD)], 1250, 1.0, gap=18)
    if story:
        nr.draw_lines(img, [T("NEW TODAY", 60, GOLD), B("Watch it on our profile", 44, LIGHT)], 1640, 1.0, gap=14)
    else:
        nr.draw_lines(img, [B(nr.HANDLE, 34)], 1600, 1.0)
    return img.convert("RGB")

if __name__ == "__main__":
    for date, label, title, a in COVERS:
        out = os.path.join("..", date[:7], "covers")
        os.makedirs(out, exist_ok=True)
        cover(date, label, title, a).save(os.path.join(out, f"{date}_cover.jpg"), quality=90)
        cover(date, label, title, a, story=True).save(os.path.join(out, f"{date}_story.jpg"), quality=90)
        print(date)
