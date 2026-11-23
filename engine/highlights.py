"""Instagram highlight covers and one intro story per highlight.
Instagram shows the centre of the cover as a small circle, so the icon is a single gold rune centred in a ring.
Usage:  python3 highlights.py   ->  ../highlights/<slug>_cover.jpg (cover) and <slug>_intro.jpg (first story)
"""
import os
from PIL import Image, ImageDraw
import nr
from nr import T, B, GOLD, LIGHT, MIST, W, H

# slug, highlight name (as typed in the app), rune icon, intro lines (title, gold subtitle, body lines)
HIGHLIGHTS = [
    ("saga", "SAGA", "dagaz", ("THE NORSE SAGA", "From the void to Ragnarök"),
     ["The Norse myths, in order,", "from the Eddas.", "New episode every", "Wednesday and Saturday."]),
    ("runes", "RUNES", "fehu", ("RUNES", "The Elder Futhark, one by one"),
     ["A new rune every Monday.", "Your name in runes", "every Tuesday:", "drop it in the comments."]),
    ("words", "WORDS", "ansuz", ("WORDS FROM THE NORTH", "Old Norse in your language"),
     ["Sky, egg, Tuesday, Tolkien.", "The Norse words", "you already speak.", "Every Thursday."]),
    ("history", "HISTORY", "raidho", ("MYTH vs HISTORY", "What the sources really say"),
     ["Horned helmets, baths,", "berserkers, real graves.", "Myth or history,", "every Friday."]),
    ("havamal", "HÁVAMÁL", "kenaz", ("HÁVAMÁL", "The sayings of Odin"),
     ["One stanza every Sunday,", "in Old Norse and in", "Bellows' 1923 translation."]),
    ("music", "MUSIC", "laguz", ("ORIGINAL MUSIC", "Before the End Begins"),
     ["Viking metal for the saga.", "Ten tracks, on Spotify,", "YouTube and everywhere.", "Link in bio."]),
]

nr.RUNES.setdefault("kenaz", [[(0.72, 0.2), (0.28, 0.5)], [(0.28, 0.5), (0.72, 0.8)]])
CX, CY = W // 2, H // 2

def ring(img, cx, cy, r, op=1.0):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(43, 48, 56, int(235 * op)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(224, 164, 74, int(255 * op)), width=10)
    d.ellipse([cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26], outline=(224, 164, 74, int(90 * op)), width=3)
    img.alpha_composite(lay)

def icon(img, rune, cx, cy, r):
    ring(img, cx, cy, r)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    h = r * 1.1
    w = h * 0.62
    nr.draw_rune(lay, rune, cx - w / 2, cy - h / 2, w, h, 1.0, width=max(14, int(r / 9)))
    img.alpha_composite(lay)

def cover(rune):
    img = nr.Background(5).render(1.0)
    icon(img, rune, CX, CY, 400)
    return img.convert("RGB")

def intro(rune, title, body):
    img = nr.Background(5).render(1.0)
    icon(img, rune, CX, 640, 230)
    nr.draw_lines(img, [T(title[0], 84 if len(title[0]) <= 16 else 66, LIGHT), T(title[1], 58, GOLD)], 980, 1.0, gap=18)
    nr.draw_lines(img, [B(t, 52, LIGHT) for t in body], 1250, 1.0, gap=12)
    nr.draw_lines(img, [B(nr.HANDLE, 38)], 1700, 1.0)
    return img.convert("RGB")

if __name__ == "__main__":
    out = os.path.join("..", "highlights")
    os.makedirs(out, exist_ok=True)
    for slug, name, rune, title, body in HIGHLIGHTS:
        cover(rune).save(os.path.join(out, f"{slug}_cover.jpg"), quality=92)
        intro(rune, title, body).save(os.path.join(out, f"{slug}_intro.jpg"), quality=92)
        print(slug)
