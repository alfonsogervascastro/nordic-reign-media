"""Listing photos for the tattoo pack (Etsy: 4:3, 3000x2250). Output: tattoos/pack/etsy/ (not in the repo).
Run after designs.py / designs_saga.py / make_pack.py:  python3 etsy_images.py
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
import nr  # noqa: E402

W, H = 3000, 2250
nr.W, nr.H = W, H
OUT = os.path.join(HERE, "pack", "etsy")
GOLD, LIGHT, MIST = nr.GOLD, nr.LIGHT, nr.MIST
T, B = nr.T, nr.B

ORDER = ["prologue_gleipnir", "ep01_ginnungagap", "ep02_ymir", "ep03_yggdrasil", "ep04_ask_embla",
         "ep05_aesir_vanir", "ep06_nine_nights", "ep07_ravens", "ep08_mead", "ep09_sleipnir",
         "ep10_lokis_children", "ep11_fenrir_bound", "ep12_mjolnir", "ep13_bride", "ep14_illusions",
         "ep15_jormungandr", "ep16_idunn", "ep17_baldr", "ep18_loki_bound", "ep19_fimbulvetr",
         "ep20_ragnarok", "ep21_thor_serpent", "ep22_rebirth"]

def bg(seed=5):
    return nr.Background(seed).render(2.0)

def gold(slug, size):
    im = Image.open(os.path.join(HERE, "out", slug, f"{slug}_gold.png")).convert("RGB")
    a = np.asarray(im, np.float32)
    alpha = np.clip(np.abs(a - np.array([14, 17, 22], np.float32)).max(axis=2) / 60.0, 0, 1)
    g = Image.fromarray(np.dstack([a, alpha * 255]).astype(np.uint8))
    g.thumbnail((size, size), Image.LANCZOS)
    return g

def watermark(img, alpha=26):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = nr.font("title", 90)
    for y in range(-400, img.height + 400, 420):
        for x in range(-600, img.width + 600, 1100):
            d.text((x, y), "NORDIC REIGN", font=f, fill=(255, 255, 255, alpha))
    img.alpha_composite(lay.rotate(25, resample=Image.BICUBIC))

def save(img, name):
    os.makedirs(OUT, exist_ok=True)
    img.convert("RGB").save(os.path.join(OUT, name), quality=92)
    print(name)

def cover():
    img = bg(5)
    picks = ["prologue_gleipnir", "ep03_yggdrasil", "ep06_nine_nights", "ep07_ravens", "ep12_mjolnir",
             "ep15_jormungandr", "ep18_loki_bound", "ep20_ragnarok", "ep22_rebirth"]
    cell = 520
    x0, y0 = 1500 - 1.5 * 600, 520
    for k, s in enumerate(picks):
        r, c = divmod(k, 3)
        g = gold(s, cell)
        img.alpha_composite(g, (int(x0 + c * 600 + (600 - g.width) / 2 - 300 + 300), int(y0 + r * 560)))
    nr.draw_lines(img, [T("23 NORSE MYTHOLOGY TATTOO DESIGNS", 110, LIGHT)], 150, 1.0)
    nr.draw_lines(img, [B("Original knotwork · stencil-ready · from the first giant to Ragnarök", 66, GOLD)], 310, 1.0)
    nr.draw_lines(img, [B("Digital download: 49-page PDF + 23 PNG stencils (3000 px)", 56, MIST)], 2140, 1.0)
    watermark(img, 14)
    save(img, "01_cover.jpg")

def inside():
    pdf = os.path.join(HERE, "pack", "NordicReign_NorseSaga_TattooPack.pdf")
    tmp = os.path.join(OUT, "_p")
    os.makedirs(OUT, exist_ok=True)
    subprocess.run(["pdftoppm", "-r", "60", "-f", "1", "-l", "8", "-jpeg", pdf, tmp], check=True)
    pages = sorted(f for f in os.listdir(OUT) if f.startswith("_p"))
    img = bg(7)
    nr.draw_lines(img, [T("WHAT YOU GET", 100, GOLD)], 130, 1.0)
    picks = [pages[0], pages[3], pages[4], pages[7]]
    pw = 640
    for k, p in enumerate(picks):
        pg = Image.open(os.path.join(OUT, p)).convert("RGBA")
        pg = pg.resize((pw, int(pg.height * pw / pg.width)), Image.LANCZOS)
        x = 1500 - (4 * pw + 3 * 60) / 2 + k * (pw + 60)
        sh = Image.new("RGBA", (pg.width + 40, pg.height + 40), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle([20, 20, pg.width + 20, pg.height + 20], fill=(0, 0, 0, 150))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (int(x - 10), 340))
        img.alpha_composite(pg, (int(x), 350))
    nr.draw_lines(img, [B("• A 49-page PDF: each design with its myth, its source in the Eddas, and a full-page stencil", 60, LIGHT),
                        B("• 23 high-resolution PNG stencils with transparent background, ready for your artist", 60, LIGHT),
                        B("• Personal use licence: get them tattooed, print them for your wall", 60, LIGHT)], 1620, 1.0, gap=34)
    watermark(img, 14)
    save(img, "02_whats_inside.jpg")
    for p in pages:
        os.remove(os.path.join(OUT, p))

def design(slug, n):
    card = Image.open(os.path.join(HERE, "out", slug, f"{slug}_card.png")).convert("RGBA")
    card = card.resize((int(card.width * 2050 / card.height), 2050), Image.LANCZOS)
    img = bg(11 + n)
    img.alpha_composite(card, (int(1500 - card.width / 2), 100))
    watermark(img, 22)
    save(img, f"{n:02d}_{slug}.jpg")

if __name__ == "__main__":
    cover()
    inside()
    for n, s in enumerate(["ep06_nine_nights", "prologue_gleipnir", "ep03_yggdrasil", "ep07_ravens",
                           "ep12_mjolnir", "ep15_jormungandr", "ep20_ragnarok", "ep22_rebirth"], start=3):
        design(s, n)
