"""Builds the sellable tattoo pack: tattoos/pack/NordicReign_NorseSaga_TattooPack.pdf (+ a ZIP of the stencils).

Per design: a dark story page (gold preview + chapter story) and a white stencil page at print resolution.
Run after designs.py / designs_saga.py:  python3 make_pack.py
"""
import ast, os, io, zipfile
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "engine", "fonts")
OUT = os.path.join(HERE, "pack")
pdfmetrics.registerFont(TTFont("Cinzel", os.path.join(FONTS, "Cinzel.ttf")))
pdfmetrics.registerFont(TTFont("Garamond", os.path.join(FONTS, "EBGaramond.ttf")))

BG = (0x0E / 255, 0x11 / 255, 0x16 / 255)
GOLD = (0xE0 / 255, 0xA4 / 255, 0x4A / 255)
LIGHT = (0xD6 / 255, 0xE2 / 255, 0xEE / 255)
MIST = (0x8E / 255, 0x99 / 255, 0xA6 / 255)
INK = (0.08, 0.08, 0.08)
PW, PH = A4

ORDER = ["prologue_gleipnir", "ep01_ginnungagap", "ep02_ymir", "ep03_yggdrasil", "ep04_ask_embla",
         "ep05_aesir_vanir", "ep06_nine_nights", "ep07_ravens", "ep08_mead", "ep09_sleipnir",
         "ep10_lokis_children", "ep11_fenrir_bound", "ep12_mjolnir", "ep13_bride", "ep14_illusions",
         "ep15_jormungandr", "ep16_idunn", "ep17_baldr", "ep18_loki_bound", "ep19_fimbulvetr",
         "ep20_ragnarok", "ep21_thor_serpent", "ep22_rebirth"]
SOURCES = {"prologue_gleipnir": "Prose Edda, Gylfaginning 34", "ep01_ginnungagap": "Gylfaginning 4–6",
           "ep02_ymir": "Gylfaginning 7–8; Grímnismál 40–41", "ep03_yggdrasil": "Gylfaginning 15–16; Grímnismál 31–35",
           "ep04_ask_embla": "Gylfaginning 9; Völuspá 17–18", "ep05_aesir_vanir": "Völuspá 21–24; Ynglinga saga 4",
           "ep06_nine_nights": "Hávamál 138–139", "ep07_ravens": "Grímnismál 20; Völuspá 28",
           "ep08_mead": "Skáldskaparmál", "ep09_sleipnir": "Gylfaginning 42",
           "ep10_lokis_children": "Gylfaginning 34", "ep11_fenrir_bound": "Gylfaginning 34",
           "ep12_mjolnir": "Skáldskaparmál", "ep13_bride": "Þrymskviða", "ep14_illusions": "Gylfaginning 44–47",
           "ep15_jormungandr": "Gylfaginning 48; Hymiskviða", "ep16_idunn": "Skáldskaparmál",
           "ep17_baldr": "Gylfaginning 49", "ep18_loki_bound": "Gylfaginning 50",
           "ep19_fimbulvetr": "Gylfaginning 51", "ep20_ragnarok": "Gylfaginning 51; Völuspá 44–53",
           "ep21_thor_serpent": "Gylfaginning 51; Völuspá 56", "ep22_rebirth": "Gylfaginning 53; Völuspá 59–62"}
AI_ASSISTED = {"ep07_ravens", "ep15_jormungandr"}

def meta():
    """Title, chapter and story for every design, read from the design scripts' save_all/_figure calls."""
    out = {}
    for f in ("designs.py", "designs_saga.py"):
        for n in ast.walk(ast.parse(open(os.path.join(HERE, f)).read())):
            if isinstance(n, ast.Call) and getattr(n.func, "id", "") in ("save_all", "_figure"):
                try:
                    slug = ast.literal_eval(n.args[0])
                    args = n.args[2:5] if n.func.id == "save_all" else n.args[1:4]
                    title, chapter, story = [ast.literal_eval(a) for a in args]
                    out[slug] = (title, chapter, story)
                except Exception:
                    pass
    return out

def img_reader(path, size, mode=None):
    im = Image.open(path)
    if mode:
        im = im.convert(mode)
    im.thumbnail((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG" if im.mode in ("RGB", "L") else "PNG", quality=92)
    buf.seek(0)
    return ImageReader(buf), im.size

def fill(c, col):
    c.setFillColorRGB(*col); c.rect(0, 0, PW, PH, stroke=0, fill=1)

def centre(c, text, y, font, size, col):
    c.setFont(font, size); c.setFillColorRGB(*col)
    c.drawCentredString(PW / 2, y, text)

def fit(c, text, font, size, maxw):
    while size > 10 and pdfmetrics.stringWidth(text, font, size) > maxw:
        size -= 1
    return size

def cover(c, n):
    fill(c, BG)
    centre(c, "NORDIC REIGN", PH - 90, "Cinzel", 14, GOLD)
    centre(c, "THE NORSE SAGA", PH - 150, "Cinzel", 40, LIGHT)
    centre(c, "Tattoo Collection", PH - 185, "Garamond", 22, GOLD)
    r, (w, h) = img_reader(os.path.join(HERE, "out", "ep03_yggdrasil", "ep03_yggdrasil_gold.png"), 1800, "RGB")
    bh = PH - 360; bw = bh * w / h
    if bw > PW - 120:
        bw = PW - 120; bh = bw * h / w
    c.drawImage(r, (PW - bw) / 2, 120 + (PH - 360 - bh) / 2, bw, bh)
    centre(c, f"{n} Viking knotwork designs, one for every chapter of the myths", 80, "Garamond", 14, LIGHT)
    centre(c, "@nordicreignofficial", 55, "Garamond", 11, MIST)
    c.showPage()

def about(c, n):
    fill(c, BG)
    y = PH - 90
    centre(c, "ABOUT THIS COLLECTION", y, "Cinzel", 20, GOLD)
    paras = [
        f"The Norse Saga tells the Norse myths in order, from the void before creation to the world rising again after Ragnarök. Each chapter has its own tattoo: {n} designs in the interlaced style of Viking Age art, where every band passes alternately over and under the next.",
        "Every design carries a symbol or a story from its chapter, taken from the medieval Icelandic sources (the Poetic Edda and Snorri Sturluson's Prose Edda). The source is printed under each design. Runes are Elder Futhark.",
        "For each design you get two pages: the story page, and a black stencil page on white, ready to print for your tattoo artist. The high-resolution stencils (3000 px, transparent background) come in the ZIP file with this PDF.",
        "Your artist can scale the designs and adjust the line weight to your skin and placement. Knotwork needs some size to stay crisp: as a guide, at least 7–8 cm across for the round designs.",
        "Designs 7 (Thought & Memory) and 15 (Jörmungandr) include figure elements (the ravens, the serpent's head) that were drafted with AI assistance and then redrawn into the knotwork. All other designs are fully hand-built geometry.",
    ]
    c.setFont("Garamond", 13); c.setFillColorRGB(*LIGHT)
    y -= 50
    from reportlab.lib.utils import simpleSplit
    for p in paras:
        for line in simpleSplit(p, "Garamond", 13, PW - 150):
            c.drawString(75, y, line); y -= 18
        y -= 12
    y -= 10
    centre(c, "LICENCE (PERSONAL USE)", y, "Cinzel", 16, GOLD); y -= 32
    lic = [
        "You may get any of these designs tattooed on yourself, as many times as you like.",
        "You may print them and share them with your tattoo artist for that purpose.",
        "You may not resell or share the files, use them in commercial products or merchandise,",
        "or offer them as flash or stock designs. For any other use, contact @nordicreignofficial.",
        "© Nordic Reign. All designs are original works.",
    ]
    for line in lic:
        centre(c, line, y, "Garamond", 12.5, MIST); y -= 18
    c.showPage()

def contents(c, items):
    fill(c, BG)
    centre(c, "CONTENTS", PH - 90, "Cinzel", 20, GOLD)
    y = PH - 140
    for i, (slug, (title, chapter, _)) in enumerate(items):
        ch = chapter.split("·")[-1].strip()
        page = 4 + i * 2
        c.setFont("Garamond", 12.5); c.setFillColorRGB(*MIST)
        c.drawString(80, y, ch)
        c.setFont("Cinzel", 12.5); c.setFillColorRGB(*LIGHT)
        c.drawString(190, y, title)
        c.setFont("Garamond", 12.5); c.setFillColorRGB(*GOLD)
        c.drawRightString(PW - 80, y, str(page))
        y -= 26
    c.showPage()

def design_pages(c, slug, title, chapter, story):
    d = os.path.join(HERE, "out", slug)
    # story page
    fill(c, BG)
    centre(c, chapter.upper(), PH - 80, "Cinzel", 12, GOLD)
    centre(c, title, PH - 120, "Cinzel", fit(c, title, "Cinzel", 30, PW - 100), LIGHT)
    r, (w, h) = img_reader(os.path.join(d, f"{slug}_gold.png"), 1800, "RGB")
    bw = PW - 120; bh = bw * h / w
    if bh > 470:
        bh = 470; bw = bh * w / h
    block = bh + 40 + 22 * len(story) + 40
    top = PH - 160 - max(0, (PH - 230 - block) / 2)
    c.drawImage(r, (PW - bw) / 2, top - bh, bw, bh)
    y = top - bh - 40
    for line in story:
        centre(c, line, y, "Garamond", 15, LIGHT); y -= 22
    y -= 14
    centre(c, "Source: " + SOURCES.get(slug, "Poetic Edda; Prose Edda"), y, "Garamond", 11, MIST)
    if slug in AI_ASSISTED:
        centre(c, "Figure element drafted with AI assistance, redrawn into the knotwork.", y - 16, "Garamond", 9.5, MIST)
    centre(c, "Nordic Reign  ·  The Norse Saga Tattoo Collection", 36, "Garamond", 9.5, MIST)
    c.showPage()
    # stencil page
    fill(c, (1, 1, 1))
    st = Image.open(os.path.join(d, f"{slug}_white.png")).convert("L")
    st.thumbnail((2000, 2000), Image.LANCZOS)
    buf = io.BytesIO(); st.save(buf, "PNG", optimize=True); buf.seek(0)
    w, h = st.size
    bw = PW - 80; bh = bw * h / w
    if bh > PH - 130:
        bh = PH - 130; bw = bh * w / h
    c.drawImage(ImageReader(buf), (PW - bw) / 2, (PH - bh) / 2 + 10, bw, bh)
    c.setFont("Cinzel", 10); c.setFillColorRGB(*INK)
    c.drawCentredString(PW / 2, 34, f"{title}  ·  STENCIL")
    c.setFont("Garamond", 8.5); c.setFillColorRGB(0.45, 0.45, 0.45)
    c.drawCentredString(PW / 2, 22, "© Nordic Reign · personal-use licence")
    c.showPage()

def main():
    os.makedirs(OUT, exist_ok=True)
    m = meta()
    items = [(s, m[s]) for s in ORDER if s in m and os.path.exists(os.path.join(HERE, "out", s))]
    missing = [s for s in ORDER if s not in dict(items)]
    if missing:
        print("missing:", missing)
    pdf = os.path.join(OUT, "NordicReign_NorseSaga_TattooPack.pdf")
    c = canvas.Canvas(pdf, pagesize=A4)
    c.setTitle("The Norse Saga · Tattoo Collection"); c.setAuthor("Nordic Reign")
    cover(c, len(items)); about(c, len(items)); contents(c, items)
    for slug, (title, chapter, story) in items:
        design_pages(c, slug, title, chapter, story)
    c.save()
    z = os.path.join(OUT, "NordicReign_NorseSaga_Stencils.zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, (slug, (title, _, _)) in enumerate(items):
            zf.write(os.path.join(HERE, "out", slug, f"{slug}_stencil.png"), f"{i:02d}_{slug}_stencil.png")
        zf.writestr("LICENCE.txt", "Personal-use licence. You may get these designs tattooed on yourself and share them with your tattoo artist for that purpose. No resale, redistribution, merchandise, flash or stock use. (c) Nordic Reign.\n")
    print(pdf, os.path.getsize(pdf) // 1024, "KB;", z, os.path.getsize(z) // 1024, "KB")

if __name__ == "__main__":
    main()
