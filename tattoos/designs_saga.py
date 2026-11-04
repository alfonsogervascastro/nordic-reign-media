"""Tattoo designs for the rest of The Norse Saga (one per episode), Viking knotwork.
Geometric ones come from the knot engine; figure ones combine an AI motif (ai/*.png) with engine knotwork.

    python3 designs_saga.py            # all
    python3 designs_saga.py ep04 ep05  # some
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
from knots import Knot, torus_knot, circle, braid, ellipse, chaikin, hammer_outline
from designs import save_all, rune_layer, _ai_ink, INK, HERE

S = 3000
C = S / 2

def solid_poly(size, pts, col=INK):
    """Anti-aliased solid polygon layer."""
    W, H = size
    k = 3
    lay = Image.new("RGBA", (W * k, H * k), (0, 0, 0, 0))
    ImageDraw.Draw(lay).polygon([(x * k, y * k) for x, y in pts], fill=col + (255,))
    return lay.resize((W, H), Image.LANCZOS)

def ai_motif(name, width, keep=1.0):
    path = os.path.join(HERE, "ai", name)
    if not os.path.exists(path):
        return None
    m = _ai_ink(path, keep)
    return m.resize((width, int(m.height * width / m.width)), Image.LANCZOS)

# ------------------------------------------------------------------ geometric episodes
def ep04():
    """Ask and Embla: two tree trunks, an ash and an elm, leaning together and interlaced."""
    k = Knot(S)
    k.add(ellipse(C - 300, C, 420, 1050, rot=math.radians(-14), n=3000))
    k.add(ellipse(C + 300, C, 420, 1050, rot=math.radians(14), n=3000))
    k.add(circle(C, C, 1380, 3000))
    img = k.render(band=115, line=22)
    save_all("ep04_ask_embla", img, "ASK & EMBLA", "The Norse Saga · Episode 4",
             ["Odin and his brothers found two trees", "washed up on the shore, an ash and an elm,",
              "and gave them breath, mind and life:", "the first man and the first woman."])

def ep05():
    """The Æsir–Vanir war and truce: two interlinked rings, Gungnir across them."""
    k = Knot(S)
    k.add(circle(C - 420, C, 720, 2600))
    k.add(circle(C + 420, C, 720, 2600))
    k.add(circle(C, C, 1360, 3000))
    img = k.render(band=120, line=22)
    spear = [(C - 30, 2620), (C + 30, 2620), (C + 30, 640), (C + 95, 600), (C, 340), (C - 95, 600), (C - 30, 640)]
    img.alpha_composite(solid_poly((S, S), spear))
    save_all("ep05_aesir_vanir", img, "THE FIRST WAR", "The Norse Saga · Episode 5",
             ["Odin threw his spear over the Vanir", "and the first war in the world began.",
              "It ended in a truce:", "two families of gods, bound together."])

def ep06():
    """Nine nights on the tree: nine-lobed knot around Ansuz, Odin's rune."""
    k = Knot(S)
    k.add(torus_knot(2, 9, C, C, 900, 300, n=6000, rot=-math.pi / 2))
    k.add(circle(C, C, 1360, 3000))
    img = k.render(band=105, line=20)
    img.alpha_composite(rune_layer((S, S), "ansuz", C - 140, C - 230, 280, 460, 60))
    save_all("ep06_nine_nights", img, "NINE NIGHTS", "The Norse Saga · Episode 6",
             ["Nine nights on the windswept tree,", "wounded by a spear, given to himself.",
              "Then he took up the runes.", "Hávamál 138–139."])

def ep10():
    """Loki's children: a three-lobed knot, one lobe for each child."""
    k = Knot(S)
    k.add(torus_knot(2, 3, C, C + 60, 820, 470, n=4000, rot=-math.pi / 2))
    k.add(circle(C, C + 60, 300, 2000))
    k.add(circle(C, C, 1380, 3000))
    img = k.render(band=125, line=24)
    save_all("ep10_lokis_children", img, "BORN IN THE DARK", "The Norse Saga · Episode 10",
             ["Three children of Loki and the giantess Angrboða:", "Fenrir the wolf, Jörmungandr the serpent",
              "and Hel, queen of the dead.", "The gods feared all three."])

def _hammer(k, cx, cy, s):
    k.add(hammer_outline(cx, cy, s))
    k.add(torus_knot(2, 3, cx, cy + 0.42 * s, 0.17 * s, 0.09 * s, n=1600, rot=-math.pi / 2))

def ep12():
    """Mjölnir: the hammer of Thor, outline pendant with a knot in its head; short handle."""
    k = Knot(S)
    _hammer(k, C, C - 80, 1250)
    img = k.render(band=100, line=20)
    save_all("ep12_mjolnir", img, "MJÖLNIR", "The Norse Saga · Episode 12",
             ["Forged by the dwarves Brokkr and Eitri.", "Loki, as a fly, stung Brokkr at the bellows,",
              "so the handle came out short.", "It still never missed."])

def ep13():
    """Thor as the bride: the hammer laid in the bride's lap, inside two wedding rings."""
    k = Knot(S)
    k.add(circle(C - 330, C + 120, 900, 2600))
    k.add(circle(C + 330, C + 120, 900, 2600))
    _hammer(k, C, C - 40, 820)
    img = k.render(band=100, line=20)
    save_all("ep13_bride", img, "THE BRIDE IN THUNDER", "The Norse Saga · Episode 13",
             ["The giant Þrymr stole the hammer", "and asked for Freyja as his bride.",
              "Thor came in her veil. When they laid the hammer", "in the bride's lap, the wedding ended."])

def ep14():
    """Útgarða-Loki's illusions: a knot that is never what it seems."""
    k = Knot(S)
    k.add(torus_knot(3, 5, C, C, 820, 420, n=6000, rot=-math.pi / 2))
    k.add(circle(C, C, 1380, 3000))
    img = k.render(band=100, line=20)
    save_all("ep14_illusions", img, "HALL OF ILLUSIONS", "The Norse Saga · Episode 14",
             ["Thor drank from a horn that touched the sea,", "lifted a cat that was the World Serpent",
              "and wrestled an old woman who was Old Age.", "Nothing there was what it seemed."])

def ep16():
    """Iðunn's apples: five apples (rings) around the tree of youth."""
    k = Knot(S)
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        k.add(circle(C + 640 * math.cos(a), C + 640 * math.sin(a), 470, 2000))
    k.add(circle(C, C, 1380, 3000))
    img = k.render(band=100, line=20)
    save_all("ep16_idunn", img, "IÐUNN'S APPLES", "The Norse Saga · Episode 16",
             ["The apples that kept the gods young.", "When Loki let Iðunn be stolen,",
              "the gods grew old and grey", "until he brought her back."])

def ep17():
    """Baldr: a ring of light pierced by the mistletoe dart."""
    k = Knot(S)
    k.add(torus_knot(2, 11, C, C, 860, 230, n=7000, rot=-math.pi / 2))
    k.add(circle(C, C, 1380, 3000))
    img = k.render(band=95, line=18)
    a = math.radians(-40); L = 2350; w = 34
    dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
    x0, y0 = C - dx * L / 2, C - dy * L / 2; x1, y1 = C + dx * L / 2, C + dy * L / 2
    dart = [(x0 + nx * w, y0 + ny * w), (x1 - dx * 160 + nx * w, y1 - dy * 160 + ny * w),
            (x1 - dx * 200 + nx * 90, y1 - dy * 200 + ny * 90), (x1, y1),
            (x1 - dx * 200 - nx * 90, y1 - dy * 200 - ny * 90), (x1 - dx * 160 - nx * w, y1 - dy * 160 - ny * w),
            (x0 - nx * w, y0 - ny * w)]
    img.alpha_composite(solid_poly((S, S), dart))
    save_all("ep17_baldr", img, "BALDR", "The Norse Saga · Episode 17",
             ["Everything in the world swore not to harm him,", "except a young sprig of mistletoe.",
              "Loki made it into a dart", "and put it in a blind god's hand."])

def ep18():
    """Loki bound: an arc of interlocked chain links beneath a single drop of venom."""
    k = Knot(S)
    n = 9
    for i in range(n):
        a = math.pi * (0.10 + 0.80 * i / (n - 1))
        x, y = C - 1000 * math.cos(a), C - 150 + 900 * math.sin(a)
        tang = a + math.pi / 2
        k.add(ellipse(x, y, 230, 120, rot=tang, n=1400))
    k.add(circle(C, C, 1380, 3000))
    img = k.render(band=80, line=16)
    t = np.linspace(0, 2 * math.pi, 160, endpoint=False)
    drop = [(C + 230 * math.sin(tt) * (1 - math.cos(tt)) * 0.5, C - 120 - 330 * math.cos(tt)) for tt in t]
    img.alpha_composite(solid_poly((S, S), drop))
    save_all("ep18_loki_bound", img, "CHAINS BENEATH THE MOUNTAIN", "The Norse Saga · Episode 18",
             ["Bound beneath the mountain, venom dripping", "from a serpent above. Sigyn holds a bowl.",
              "When she empties it, he writhes", "and the whole earth shakes."])

def ep19():
    """Fimbulvetr: a six-fold winter knot around Hagalaz, the hail rune."""
    k = Knot(S)
    k.add(torus_knot(5, 6, C, C, 820, 330, n=8000, rot=-math.pi / 2))
    k.add(circle(C, C, 1380, 3000))
    img = k.render(band=85, line=17)
    img.alpha_composite(rune_layer((S, S), "hagalaz", C - 130, C - 190, 260, 380, 52))
    save_all("ep19_fimbulvetr", img, "FIMBULVETR", "The Norse Saga · Episode 19",
             ["Three winters, one after another,", "with no summer in between.",
              "The first sign", "that the end is coming."])

def ep21():
    """Ragnarök II: Thor's hammer inside the coils of the World Serpent."""
    k = Knot(S)
    k.add(torus_knot(2, 21, C, C + 120, 1080, 110, n=9000, rot=-math.pi / 2))
    _hammer(k, C, C + 60, 900)
    img = k.render(band=110, line=50, gap=24)
    save_all("ep21_thor_serpent", img, "NINE STEPS", "The Norse Saga · Episode 21",
             ["At the end, Thor kills the World Serpent.", "He walks nine steps",
              "and falls, poisoned by its venom.", "Surtr's fire takes the rest."])

def ep22():
    """The world rises again: a new sun (Dagaz) rising over a braided sea."""
    k = Knot(S)
    for c in braid(250, 2750, C + 420, 120, 620, 3, n=2600):
        k.add(c, closed=False)
    k.add(circle(C, C - 260, 560, 2400))
    k.add(circle(C, C, 1380, 3000))
    img = k.render(band=100, line=20)
    img.alpha_composite(rune_layer((S, S), "dagaz", C - 170, C - 260 - 150, 340, 300, 48))
    save_all("ep22_rebirth", img, "THE WORLD RISES AGAIN", "The Norse Saga · Episode 22",
             ["The earth rises from the sea, green again.", "Fields grow unsown.",
              "Baldr returns, and two humans", "who hid in the tree begin it all again."])

# ------------------------------------------------------------------ figure episodes (AI + engine)
def _figure(slug, title, chapter, story, motif, width, pos, knot_fn, band=110, line=22, keep=1.0):
    k = Knot(S)
    knot_fn(k)
    img = k.render(band=band, line=line)
    m = ai_motif(motif, width, keep)
    if m is None:
        print("skip (no motif)", slug); return
    img.alpha_composite(m, (int(pos[0] - m.width / 2), int(pos[1] - m.height / 2)))
    save_all(slug, img, title, chapter, story)

def ep03_ai():
    _figure("ep03_yggdrasil", "YGGDRASIL", "The Norse Saga · Episode 3",
            ["An ash so great its branches spread over the sky", "and its three roots reach three worlds.",
             "An eagle sits at the top,", "a serpent gnaws below."],
            "yggdrasil_0.png", 2300, (C, C), lambda k: k.add(circle(C, C, 1380, 3000)))

def ep07():
    _figure("ep07_ravens", "THOUGHT & MEMORY", "The Norse Saga · Episode 7",
            ["Huginn and Muninn fly over the world each day", "and whisper to Odin all they see.",
             "He gave an eye at Mímir's well", "to see even further."],
            "ravens_0.png", 2000, (C, C - 250),
            lambda k: (k.add(torus_knot(2, 5, C, C + 780, 420, 150, n=3000, rot=-math.pi / 2)),
                       k.add(circle(C, C, 1380, 3000))))

def ep08_ai():
    _figure("ep08_mead", "THE MEAD OF POETRY", "The Norse Saga · Episode 8",
            ["Brewed from the blood of Kvasir, the wisest of all beings.", "Odin stole it from the giants",
             "and spat it out in Asgard:", "whoever drinks it becomes a poet."],
            "horn_0.png", 2200, (C, C), lambda k: k.add(circle(C, C, 1380, 3000)))

def ep09_ai():
    _figure("ep09_sleipnir", "SLEIPNIR", "The Norse Saga · Episode 9",
            ["Odin's eight-legged horse,", "the fastest in all the worlds.",
             "His mother was Loki,", "who had turned himself into a mare."],
            "sleipnir_0.png", 2200, (C, C - 80),
            lambda k: (k.add(torus_knot(3, 8, C, C + 980, 260, 90, n=3000)) if False else None,
                       k.add(circle(C, C, 1380, 3000))))

def ep11_ai():
    def kn(k):
        for c in braid(380, 2620, 2150, 110, 600, 3, n=2400):
            k.add(c, closed=False)
        k.add(circle(C, C, 1380, 3000))
    _figure("ep11_fenrir_bound", "THE BINDING OF FENRIR", "The Norse Saga · Episode 11",
            ["Gleipnir held the wolf at last.", "Týr kept his hand in Fenrir's jaws",
             "as a pledge of good faith.", "He lost it."],
            "wolf_head_0.png", 1900, (C, C - 300), kn)

def ep20_ai():
    def kn(k):
        k.add(circle(C + 560, C - 520, 300, 2000))  # the sun, about to be swallowed
        k.add(circle(C, C, 1380, 3000))
    _figure("ep20_ragnarok", "RAGNARÖK", "The Norse Saga · Episode 20",
            ["The wolf breaks free.", "The sun is swallowed, the stars fall,",
             "and Fenrir's jaws open from earth to sky.", "Odin rides out to meet him."],
            "wolf_head_0.png", 2100, (C - 180, C + 150), kn)

# ------------------------------------------------------------------ geometric versions of figure episodes
def ep03():
    """Yggdrasil: a three-strand braided trunk with three crown loops and three root loops."""
    k = Knot(S)
    y0, y1 = 2080, 1080
    ys = np.linspace(y0, y1, 1400)
    tops = [(C - 520, 760, 250), (C, 560, 280), (C + 520, 760, 250)]
    bots = [(C - 480, 2330, 200), (C, 2470, 200), (C + 480, 2330, 200)]
    for i in range(3):
        ph = 2 * math.pi * i / 3
        xs = C + 120 * np.sin(2 * math.pi * (ys - y0) / 500 + ph)
        trunk = np.stack([xs, ys], 1)
        tx, ty, tr = tops[i]; bx, by, br = bots[i]
        up = chaikin([trunk[-1], ((trunk[-1, 0] + tx) / 2, y1 - 80), (tx, ty + tr)], 4, closed=False)
        dn = chaikin([(bx, by - br), ((trunk[0, 0] + bx) / 2, y0 + 60), trunk[0]], 4, closed=False)
        k.add(np.vstack([dn, trunk, up]), closed=False)
        k.add(circle(tx, ty, tr, 1600)); k.add(circle(bx, by, br, 1400))
    k.add(circle(C, C, 1380, 3000))
    img = k.render(band=95, line=19)
    save_all("ep03_yggdrasil", img, "YGGDRASIL", "The Norse Saga · Episode 3",
             ["An ash so great its branches spread over the sky", "and its three roots reach three worlds.",
              "An eagle sits at the top,", "a serpent gnaws below."])

def ep08():
    """The mead of poetry: a drinking horn outline with interlaced rim bands and a knot."""
    k = Knot(S)
    t = np.linspace(0, 1, 400)
    cxs = 650 + 1650 * t; cys = 2250 - 1500 * t + 520 * np.sin(math.pi * t)
    cl = np.stack([cxs, cys], 1)
    d = np.gradient(cl, axis=0); d /= np.linalg.norm(d, axis=1)[:, None]
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    wdt = (340 * (1 - t) + 50 * t)[:, None]
    outline = np.vstack([cl + nrm * wdt, (cl - nrm * wdt)[::-1]])
    k.add(chaikin(outline, 2))
    for tt in (0.08, 0.22):
        i = int(tt * 399)
        ang = math.atan2(d[i, 1], d[i, 0])
        k.add(ellipse(cl[i, 0], cl[i, 1], 110, wdt[i, 0] + 70, rot=ang, n=1600))
    k.add(torus_knot(2, 3, cl[230, 0], cl[230, 1], 120, 70, n=1500))
    k.add(circle(C, C, 1380, 3000))
    img = k.render(band=80, line=17)
    save_all("ep08_mead", img, "THE MEAD OF POETRY", "The Norse Saga · Episode 8",
             ["Brewed from the blood of Kvasir, the wisest of all beings.", "Odin stole it from the giants",
              "and spat it out in Asgard:", "whoever drinks it becomes a poet."])

def ep09():
    """Sleipnir: eight loops for eight legs around Ehwaz, the horse rune."""
    k = Knot(S)
    k.add(torus_knot(5, 8, C, C, 880, 300, n=8000, rot=-math.pi / 2))
    k.add(circle(C, C, 1380, 3000))
    img = k.render(band=80, line=16)
    img.alpha_composite(rune_layer((S, S), "ehwaz", C - 170, C - 190, 340, 380, 52))
    save_all("ep09_sleipnir", img, "SLEIPNIR", "The Norse Saga · Episode 9",
             ["Odin's eight-legged horse, the fastest in all the worlds.", "His mother was Loki,",
              "who had turned himself into a mare.", "Ehwaz, the horse rune, at the centre."])

def ep11():
    """The binding of Fenrir: Gleipnir closed into a ring around Tiwaz, Týr's rune."""
    k = Knot(S)
    k.add(torus_knot(3, 20, C, C, 1040, 150, n=9000, rot=-math.pi / 2))
    img = k.render(band=95, line=19)
    img.alpha_composite(rune_layer((S, S), "tiwaz", C - 230, C - 380, 460, 760, 90))
    save_all("ep11_fenrir_bound", img, "THE BINDING OF FENRIR", "The Norse Saga · Episode 11",
             ["Gleipnir held the wolf at last.", "Týr kept his hand in Fenrir's jaws",
              "as a pledge of good faith.", "He lost it."])

def ep20():
    """Ragnarök: the wolf Sköll catches the sun: the sun ring (Sowilo) caught in the larger wolf ring."""
    k = Knot(S)
    k.add(circle(C - 260, C + 120, 900, 2800))
    k.add(circle(C + 520, C - 520, 480, 2400))
    k.add(circle(C, C, 1380, 3000))
    img = k.render(band=110, line=22)
    img.alpha_composite(rune_layer((S, S), "sowilo", C + 520 - 110, C - 520 - 190, 220, 380, 52))
    save_all("ep20_ragnarok", img, "RAGNARÖK", "The Norse Saga · Episode 20",
             ["The wolf catches the sun and swallows it.", "The stars fall from the sky.",
              "Odin rides out to meet Fenrir", "and does not come back."])

ALL = ["ep03", "ep04", "ep05", "ep06", "ep07", "ep08", "ep09", "ep10", "ep11", "ep12", "ep13", "ep14",
       "ep16", "ep17", "ep18", "ep19", "ep20", "ep21", "ep22"]

if __name__ == "__main__":
    for name in sys.argv[1:] or ALL:
        globals()[name]()
        print("done", name, flush=True)
