"""Brand carousels (1080x1350) for Instagram / TikTok photo posts.

Usage:
  python3 carousel.py tattoo ep02_ymir     -> ../2026-11/carousels/tattoo_ep02_ymir_N.jpg
  python3 carousel.py myths                -> ../2026-11/carousels/myths_vikings-never_N.jpg
Tattoo carousels need the design generated first (tattoos/out/<slug>/, not in the repo).
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
import nr

nr.W, nr.H = 1080, 1350
W, H = nr.W, nr.H
T, B, GOLD, LIGHT, MIST = nr.T, nr.B, nr.GOLD, nr.LIGHT, nr.MIST
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../2026-11/carousels")

def base(seed=4):
    return nr.Background(seed).render(2.0)

def footer(img, n, total):
    nr.draw_lines(img, [B(f"{n} / {total}   ·   {nr.HANDLE}", 30)], H - 80, 1.0)

def label(img, text):
    nr.draw_lines(img, [T(text, 32, GOLD)], 70, 1.0)
    d = ImageDraw.Draw(img)
    d.line([(W / 2 - 40, 122), (W / 2 + 40, 122)], fill=GOLD + (170,), width=2)

def swipe(img):
    nr.draw_lines(img, [T("SWIPE TO READ", 34, GOLD)], H - 150, 1.0)

def gold_png(path, size):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im, np.float32)
    alpha = np.clip(np.abs(a - np.array([14, 17, 22], np.float32)).max(axis=2) / 60.0, 0, 1)
    out = Image.fromarray(np.dstack([a, alpha * 255]).astype(np.uint8))
    out.thumbnail((size, size), Image.LANCZOS)
    return out

def save(img, name):
    os.makedirs(OUT, exist_ok=True)
    img.convert("RGB").save(os.path.join(OUT, name), quality=90)
    print(name)

# ---------------------------------------------------------------- tattoo carousel
TATTOO = {
    "ep02_ymir": dict(ep=2, title="YMIR'S WORLD", hook=["The world was made", "from a giant."],
                      source=["“Out of Ymir's flesh was fashioned the earth,", "and the ocean out of his blood;",
                              "of his bones the hills, of his hair the trees,", "of his skull the heavens high.”",
                              ("Grímnismál 40 · trans. H. A. Bellows (1923)", 30)]),
    "ep03_yggdrasil": dict(ep=3, title="YGGDRASIL", hook=["Nine worlds", "hang on one tree."],
                           source=["“An ash I know, Yggdrasil its name,", "with water white is the great tree wet;",
                                   "thence come the dews that fall in the dales,", "green by Urth's well does it ever grow.”",
                                   ("Völuspá 19 · trans. H. A. Bellows (1923)", 30)]),
    "ep04_ask_embla": dict(ep=4, title="ASK & EMBLA", hook=["The first humans", "were two trees."],
                           source=["“Soul they had not, sense they had not,", "heat nor motion, nor goodly hue;",
                                   "soul gave Othin, sense gave Hönir,", "heat gave Lothur and goodly hue.”",
                                   ("Völuspá 18 · trans. H. A. Bellows (1923)", 30)]),
    "ep05_aesir_vanir": dict(ep=5, title="THE FIRST WAR", hook=["The first war", "began with a spear."],
                             source=["“On the host his spear did Othin hurl,", "then in the world did war first come;",
                                     "the wall that girdled the gods was broken,", "and the field by the warlike Wanes was trodden.”",
                                     ("Völuspá 24 · trans. H. A. Bellows (1923)", 30)]),
    "ep06_nine_nights": dict(ep=6, title="NINE NIGHTS", hook=["He hung nine nights", "to win the runes."],
                             source=["“I ween that I hung on the windy tree,", "hung there for nights full nine;",
                                     "with the spear I was wounded, and offered I was", "to Othin, myself to myself.”",
                                     ("Hávamál 138 · trans. H. A. Bellows (1923)", 30)]),
    "ep07_ravens": dict(ep=7, title="THOUGHT & MEMORY", hook=["Odin sends two ravens", "out every day."],
                        source=["“O'er Mithgarth Hugin and Munin both", "each day set forth to fly;",
                                "for Hugin I fear lest he come not home,", "but for Munin my care is more.”",
                                ("Grímnismál 20 · trans. H. A. Bellows (1923)", 30)]),
}

def tattoo(slug):
    cfg = TATTOO[slug]
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../tattoos/out/{slug}")
    gold = gold_png(f"{d}/{slug}_gold.png", 760)
    total = 5
    # 1 cover
    img = base(11); label(img, f"THE NORSE SAGA · EPISODE {cfg['ep']}")
    nr.draw_lines(img, [T(cfg["hook"][0], 66, LIGHT), T(cfg["hook"][1], 66, GOLD)], 190, 1.0, gap=10)
    img.alpha_composite(gold, (int(W / 2 - gold.width / 2), 420))
    swipe(img); footer(img, 1, total); save(img, f"tattoo_{slug}_1.jpg")
    # 2 the story card (already branded)
    card = Image.open(f"{d}/{slug}_card.png").convert("RGBA").resize((W, H))
    save(card, f"tattoo_{slug}_2.jpg")
    # 3 stencil preview (low-res, watermarked: the full-size stencil is the paid product)
    img = Image.new("RGBA", (W, H), (244, 241, 234, 255))
    st = Image.open(f"{d}/{slug}_white.png").convert("RGBA"); st.thumbnail((820, 820), Image.LANCZOS)
    img.alpha_composite(st, (int(W / 2 - st.width / 2), 300))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
    f = nr.font("title", 58)
    for k in range(-2, 6):
        dd.text((-200 + k * 260, 200 + k * 180), "NORDIC REIGN", font=f, fill=(20, 20, 20, 28))
    img.alpha_composite(lay.rotate(30, resample=Image.BICUBIC))
    nr.draw_lines(img, [T("STENCIL-READY", 44, (30, 34, 40))], 110, 1.0)
    nr.draw_lines(img, [B("Clean lines your artist can transfer as is.", 38, (70, 74, 80))], 180, 1.0)
    nr.draw_lines(img, [B(f"3 / {total}   ·   {nr.HANDLE}", 30, (90, 94, 100))], H - 80, 1.0)
    save(img, f"tattoo_{slug}_3.jpg")
    # 4 the source
    img = base(13); label(img, "THE SOURCE")
    lines = [B(s, 46, LIGHT) if isinstance(s, str) else B(s[0], s[1]) for s in cfg["source"]]
    nr.draw_lines(img, lines, 420, 1.0, gap=18)
    footer(img, 4, total); save(img, f"tattoo_{slug}_4.jpg")
    # 5 call to action
    img = base(17); label(img, cfg["title"])
    nr.draw_lines(img, [T("Which chapter", 66, LIGHT), T("would you wear?", 66, GOLD)], 420, 1.0, gap=10)
    nr.draw_lines(img, [B("Save this for your next tattoo.", 46, LIGHT),
                        B(f"Episode {cfg['ep']} is on our profile.", 42)], 700, 1.0, gap=16)
    footer(img, 5, total); save(img, f"tattoo_{slug}_5.jpg")

# ---------------------------------------------------------------- myth vs history
MYTHS = [
    ("Horned helmets", ["No Viking Age helmet with horns", "has ever been found. The horns", "came from an 1876 opera costume."],
     "Gjermundbu helmet (10th c.); Wagner's Ring, 1876"),
    ("Drinking from skulls", ["A 17th-century mistranslation.", "The poem said “the curved branches", "of skulls”: a kenning for horns."],
     "Krákumál; Ole Worm, Runer (1636)"),
    ("“Viking” as a people", ["Víkingr meant a sea raider.", "Fara í víking: to go raiding.", "Most Norse people were farmers."],
     "Old Norse usage, sagas and runestones"),
    ("The “Valknut”", ["The knot is on Viking Age picture stones,", "but that name is modern.", "Nobody knows what they called it."],
     "Stora Hammars I picture stone, Gotland"),
    ("The Vegvísir compass", ["It comes from an Icelandic", "magic manuscript written in 1860,", "800 years after the Vikings."],
     "Huld Manuscript (1860)"),
]

def myths():
    total = len(MYTHS) + 2
    img = base(21); label(img, "MYTH VS HISTORY")
    nr.draw_lines(img, [T("5 things", 86, LIGHT), T("Vikings never did", 76, GOLD)], 420, 1.0, gap=14)
    nr.draw_lines(img, [B("(or never called them that)", 44)], 660, 1.0)
    swipe(img); footer(img, 1, total); save(img, "myths_vikings-never_1.jpg")
    for k, (title, body, src) in enumerate(MYTHS, start=2):
        img = base(21 + k); label(img, f"MYTH {k - 1}")
        nr.draw_lines(img, [T(title, 72, GOLD)], 330, 1.0)
        nr.draw_lines(img, [B(s, 50, LIGHT) for s in body], 520, 1.0, gap=16)
        nr.draw_lines(img, [B("Source: " + src, 32)], 900, 1.0)
        footer(img, k, total); save(img, f"myths_vikings-never_{k}.jpg")
    img = base(29); label(img, "MYTH VS HISTORY")
    nr.draw_lines(img, [T("Which one", 76, LIGHT), T("did you believe?", 76, GOLD)], 420, 1.0, gap=12)
    nr.draw_lines(img, [B("Send this to someone who still", 46, LIGHT), B("pictures horns on every Viking.", 46, LIGHT)],
                  720, 1.0, gap=14)
    footer(img, total, total); save(img, "myths_vikings-never_7.jpg")

# ---------------------------------------------------------------- were Vikings tattooed?
def tattooed():
    total = 7
    designs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../tattoos/out")
    img = base(31); label(img, "MYTH VS HISTORY")
    nr.draw_lines(img, [T("Were Vikings", 90, LIGHT), T("tattooed?", 90, GOLD)], 400, 1.0, gap=14)
    nr.draw_lines(img, [B("There is exactly one eyewitness.", 50, LIGHT)], 680, 1.0)
    swipe(img); footer(img, 1, total); save(img, "tattoos_were-vikings-tattooed_1.jpg")
    slides = [
        ("THE EYEWITNESS", "Ibn Fadlan, 922",
         ["An Arab envoy from Baghdad met", "the Rus, traders from the north,", "on the river Volga."],
         "Ibn Fadlan, Risala (922)"),
        ("WHAT HE WROTE", "From toes to neck",
         ["Each man, he says, was marked from", "the tips of his toes to his neck", "with dark green trees and figures."],
         "Ibn Fadlan, Risala (paraphrased)"),
        ("THE CATCH", "Tattoos or paint?",
         ["His Arabic word could mean tattoos,", "or designs drawn on the skin.", "Scholars still disagree."],
         "Translations and commentary on the Risala"),
        ("THE BODIES", "No skin survives",
         ["Viking Age bodies were burned or decayed.", "Not one tattooed Viking has ever", "been found. Not one untattooed either."],
         "Viking Age burial archaeology"),
    ]
    for k, (lab, title, body, src) in enumerate(slides, start=2):
        img = base(31 + k); label(img, lab)
        nr.draw_lines(img, [T(title, 72, GOLD)], 330, 1.0)
        nr.draw_lines(img, [B(x, 50, LIGHT) for x in body], 520, 1.0, gap=16)
        nr.draw_lines(img, [B("Source: " + src, 32)], 900, 1.0)
        footer(img, k, total); save(img, f"tattoos_were-vikings-tattooed_{k}.jpg")
    img = base(37); label(img, "THE VERDICT")
    nr.draw_lines(img, [T("Possible.", 80, LIGHT), T("Not proven.", 80, GOLD)], 330, 1.0, gap=12)
    nr.draw_lines(img, [B("Vegvísir, Valknut and rune tattoos", 48, LIGHT), B("are modern designs inspired by the past.", 48, LIGHT)],
                  600, 1.0, gap=14)
    footer(img, 6, total); save(img, "tattoos_were-vikings-tattooed_6.jpg")
    img = base(39); label(img, "THE NORSE SAGA")
    picks = ["ep06_nine_nights", "ep07_ravens", "ep02_ymir"]
    for i, sl in enumerate(picks):
        g = gold_png(f"{designs}/{sl}/{sl}_gold.png", 300)
        img.alpha_composite(g, (int(W / 2 - 480 + i * 330 - g.width / 2 + 150), 230))
    nr.draw_lines(img, [T("Ours are modern too.", 64, LIGHT)], 600, 1.0)
    nr.draw_lines(img, [B("Every chapter of The Norse Saga", 48, LIGHT), B("ends with its own knotwork design.", 48, LIGHT)],
                  700, 1.0, gap=14)
    nr.draw_lines(img, [T("Would you get one?", 60, GOLD), B("Yes, no, or already have one?", 44)], 900, 1.0, gap=16)
    footer(img, 7, total); save(img, "tattoos_were-vikings-tattooed_7.jpg")

# ---------------------------------------------------------------- Vikings in America
def vinland():
    total = 7
    img = base(41); label(img, "MYTH VS HISTORY")
    nr.draw_lines(img, [T("Vikings reached", 84, LIGHT), T("America.", 96, GOLD)], 400, 1.0, gap=14)
    nr.draw_lines(img, [B("Almost 500 years before Columbus.", 50, LIGHT), B("The proof, and the hoax.", 46)], 680, 1.0, gap=14)
    swipe(img); footer(img, 1, total); save(img, "vinland_vikings-in-america_1.jpg")
    slides = [
        ("THE SAGAS", "Vinland",
         ["Two Icelandic sagas tell how", "Leif Eriksson sailed west", "around the year 1000."],
         "Grænlendinga saga; Eiríks saga rauða"),
        ("THE SITE", "L'Anse aux Meadows",
         ["Newfoundland, found in 1960", "by Helge and Anne Stine Ingstad:", "Norse turf halls, iron rivets, a bronze pin."],
         "Parks Canada; UNESCO World Heritage (1978)"),
        ("THE DATE", "Exactly 1021",
         ["Wood cut with iron blades.", "Its tree rings carry the mark", "of a solar storm from 993."],
         "Kuitems et al., Nature (2021)"),
        ("THE CLUE", "Butternuts",
         ["Nuts found at the site", "don't grow that far north.", "The Norse went further south."],
         "Excavation finds, L'Anse aux Meadows"),
        ("THE HOAX", "Kensington Runestone",
         ["Found in Minnesota in 1898.", "Its runes and words are too modern:", "most scholars call it a fake."],
         "Runological studies of the stone"),
    ]
    for k, (lab, title, body, src) in enumerate(slides, start=2):
        img = base(41 + k); label(img, lab)
        nr.draw_lines(img, [T(title, 72, GOLD)], 330, 1.0)
        nr.draw_lines(img, [B(x, 50, LIGHT) for x in body], 520, 1.0, gap=16)
        nr.draw_lines(img, [B("Source: " + src, 32)], 900, 1.0)
        footer(img, k, total); save(img, f"vinland_vikings-in-america_{k}.jpg")
    img = base(49); label(img, "MYTH VS HISTORY")
    nr.draw_lines(img, [T("Would you have", 80, LIGHT), T("sailed west with Leif?", 70, GOLD)], 420, 1.0, gap=12)
    nr.draw_lines(img, [B("Yes or no, in the comments.", 48, LIGHT)], 720, 1.0)
    footer(img, total, total); save(img, "vinland_vikings-in-america_7.jpg")

if __name__ == "__main__":
    if sys.argv[1] == "tattoo":
        tattoo(sys.argv[2])
    elif sys.argv[1] == "tattooed":
        tattooed()
    elif sys.argv[1] == "vinland":
        vinland()
    else:
        myths()
