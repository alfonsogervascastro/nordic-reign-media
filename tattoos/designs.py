"""Nordic Reign tattoo designs — one per episode of The Norse Saga, in Viking knotwork.

Outputs per design (in tattoos/out/<slug>/):
  <slug>_stencil.png   black linework on transparent, 3000 px (for the tattoo artist)
  <slug>_white.png     same on white
  <slug>_gold.png      brand preview, gold on storm charcoal
  <slug>_card.png      1080x1350 social card with the story
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from knots import Knot, torus_knot, circle, braid, on_paper, recolor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
import nr  # rune geometry and fonts

INK = (12, 12, 12)

def rune_layer(size_wh, rune, x, y, w, h, width):
    """Solid black rune strokes on a transparent layer."""
    W, H = size_wh
    S = 3
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    r = width * S / 2
    for stroke in nr.RUNES[rune]:
        pts = [((x + px * w) * S, (y + py * h) * S) for px, py in stroke]
        d.line(pts, fill=INK + (255,), width=int(width * S), joint="curve")
        for p in pts:
            d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=INK + (255,))
    return lay.resize((W, H), Image.LANCZOS)

def save_all(slug, img, title, chapter, story):
    out = os.path.join(HERE, "out", slug)
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(out, f"{slug}_stencil.png"))
    on_paper(img).save(os.path.join(out, f"{slug}_white.png"))
    gold = recolor(img)
    gold.save(os.path.join(out, f"{slug}_gold.png"))
    card(gold, title, chapter, story).save(os.path.join(out, f"{slug}_card.png"))

def card(gold, title, chapter, story):
    Wc, Hc = 1080, 1350
    c = Image.new("RGB", (Wc, Hc), (14, 17, 22))
    g = gold.copy()
    g.thumbnail((900, 640))
    c.paste(g, ((Wc - g.width) // 2, 250 + (640 - g.height) // 2))
    d = ImageDraw.Draw(c)
    def center(text, y, f, col):
        bb = d.textbbox((0, 0), text, font=f)
        d.text(((Wc - (bb[2] - bb[0])) / 2, y), text, font=f, fill=col)
        return y + (bb[3] - bb[1])
    center(chapter.upper(), 90, nr.font("title", 30), nr.GOLD)
    center(title, 140, nr.font("title", 64), nr.LIGHT)
    y = 940
    for line in story:
        y = center(line, y, nr.font("body", 38), nr.MIST) + 18
    center("Save it for your next tattoo  ·  " + nr.HANDLE, 1270, nr.font("body", 30), nr.GOLD)
    return c

# ------------------------------------------------------------------ designs
def gleipnir():
    """Prologue — armband. A three-strand plait (the ribbon) runs into a ring
    holding Tiwaz, the rune of Týr, who gave his hand so the wolf could be bound."""
    Wd, Hd = 3600, 1000
    k = Knot(Wd, Hd)
    cx, cy, rr = Wd / 2, Hd / 2, 300
    for c in braid(60, cx - rr + 10, cy, 220, 760, 3, n=3000):
        k.add(c, closed=False)
    for c in braid(cx + rr - 10, Wd - 60, cy, 220, 760, 3, n=3000, phase=math.pi):
        k.add(c, closed=False)
    k.add(circle(cx, cy, rr, 2400))
    for y in (110, Hd - 110):
        k.add(np.stack([np.linspace(40, Wd - 40, 1500), np.full(1500, y)], 1), closed=False)
    img = k.render(band=96, line=18)
    img.alpha_composite(rune_layer((Wd, Hd), "tiwaz", cx - 120, cy - 170, 240, 340, 46))
    save_all("prologue_gleipnir", img, "GLEIPNIR", "The Norse Saga · Prologue",
             ["The ribbon of six impossible things", "that held the wolf Fenrir.",
              "At its heart, Tiwaz: the rune of Týr,", "who gave his hand to keep the oath."])

def ginnungagap():
    """Ep. 1 — rosette around an empty centre (the void), framed by a ring.
    Isa (ice) above, Kenaz (the torch) below: ice from the north, fire from the south."""
    S = 3000
    k = Knot(S)
    k.add(torus_knot(3, 8, S / 2, S / 2, 760, 300, n=5200, rot=-np.pi / 2))
    k.add(circle(S / 2, S / 2, 1340, 3000))
    img = k.render(band=110, line=20)
    img.alpha_composite(rune_layer((S, S), "isa", S / 2 - 50, S / 2 - 1200 - 65, 100, 130, 34))
    img.alpha_composite(rune_layer((S, S), "kaunan", S / 2 - 70, S / 2 + 1200 - 65, 140, 130, 34))
    save_all("ep01_ginnungagap", img, "GINNUNGAGAP", "The Norse Saga · Episode 1",
             ["Ice from the north, fire from the south,", "and between them the yawning void",
              "where everything began.", "Isa above, Kenaz below."])

def ymir():
    """Ep. 2 — four-lobed knot bound by a ring: the world the gods made from Ymir.
    Four lobes for sky, sea, land and mountains (his skull, blood, flesh and bones)."""
    S = 3000
    k = Knot(S)
    k.add(torus_knot(3, 4, S / 2, S / 2, 740, 360, n=4800, rot=-np.pi / 2))
    k.add(circle(S / 2, S / 2, 1330, 3000))
    img = k.render(band=118, line=22)
    save_all("ep02_ymir", img, "YMIR'S WORLD", "The Norse Saga · Episode 2",
             ["His skull became the sky, his blood the sea,", "his flesh the land, his bones the mountains.",
              "Four loops, one body:", "the world was made from a giant."])

def _ai_ink(path, keep=0.8):
    """Load an AI-generated black-on-white drawing as an opaque ink layer (outside made transparent)."""
    from scipy import ndimage
    a = np.asarray(Image.open(path).convert("L"))
    ink = a < 128
    lab, _ = ndimage.label(~ink)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    outside = np.isin(lab, list(border))
    rgb = np.where(ink[..., None], INK[0], 255).astype(np.uint8).repeat(3, 2)
    im = Image.fromarray(np.dstack([rgb, (~outside).astype(np.uint8) * 255]))
    im = im.crop(im.getbbox())
    return im.crop((0, 0, im.width, int(im.height * keep)))

def jormungandr():
    """Ep. 15 — the World Serpent around Midgard. Braided knotwork body (engine) + Viking dragon head
    (AI-assisted, Qwen-Image, see ai/README.md)."""
    Wd, Hd = 3000, 3300
    cy = Hd / 2 + 260
    k = Knot(Wd, Hd)
    k.add(torus_knot(2, 21, Wd / 2, cy, 960, 110, n=9000, rot=-np.pi / 2))
    k.add(circle(Wd / 2, cy, 520, 2400))
    img = k.render(band=120, line=54, gap=26)
    head = _ai_ink(os.path.join(HERE, "ai", "serpent_head_1.png"))
    hw = 1250
    head = head.resize((hw, int(head.height * hw / head.width)), Image.LANCZOS)
    top = cy - 960 - 110
    img.alpha_composite(head, (int(Wd / 2 - hw * 0.58), int(top - head.height * 0.72)))
    save_all("ep15_jormungandr", img, "JÖRMUNGANDR", "The Norse Saga · Episode 15",
             ["Loki's child, thrown into the sea by Odin,", "grew until it lay around all of Midgard",
              "and bit its own tail.", "At Ragnarök it rises to face Thor."])

if __name__ == "__main__":
    which = sys.argv[1:] or ["gleipnir", "ginnungagap", "ymir"]
    for name in which:
        globals()[name]()
        print("done", name)
