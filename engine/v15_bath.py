"""MYTH vs HISTORY — were Vikings filthy? laugardagr ('washing day'); John of Wallingford's chronicle;
antler combs; counterpoint: Ibn Fadlan (922) on the Rus and their shared morning basin."""
import sys
import numpy as np
from PIL import Image, ImageDraw
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 27.0
CX, CY = W / 2, 1020

def comb(img, t, op, col):
    """Viking Age double-row antler comb, line drawing (an object, not a figure)."""
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = col + (int(255 * op),)
    w, h = 300, 54
    d.rounded_rectangle([CX - w, CY - h, CX + w, CY + h], radius=22, outline=c, width=10)
    for x in np.linspace(CX - w + 30, CX + w - 30, 7):
        d.ellipse([x - 9, CY - 9, x + 9, CY + 9], outline=c, width=5)       # rivets
    n = 34
    for i in range(n):
        x = CX - w + 24 + i * (2 * w - 48) / 33
        d.line([(x, CY - h), (x, CY - h - 120)], fill=c, width=7)
        d.line([(x, CY + h), (x, CY + h + 120)], fill=c, width=7)
    img.alpha_composite(lay)

def water(img, t, op):
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(5):
        r = ((t * 120 + i * 90) % 450)
        a = int(200 * op * (1 - r / 450))
        d.ellipse([CX - r * 1.6, 1380 - r * 0.35, CX + r * 1.6, 1380 + r * 0.35], outline=(120, 160, 200, a), width=4)
    img.alpha_composite(lay)

cards = [
    Card(-0.8, 3.6, 330, [T("Vikings had a day", 74), T("just for bathing.", 74, GOLD)]),
    Card(3.8, 8.4, 330, [B("Old Norse: laugardagr,", 54, LIGHT), B('"washing day".', 54, GOLD)]),
    Card(4.6, 8.4, 1380, [B("Still Saturday today:", 46), T("lördag · lørdag · laugardagur", 46, LIGHT)]),
    Card(8.6, 13.2, 330, [B("Their combs, carved from antler,", 52, LIGHT), B("are among the commonest finds", 52, LIGHT), B("in Viking Age sites.", 52, LIGHT)]),
    Card(13.4, 18.4, 330, [B("An English chronicle complained", 50, LIGHT), B("that the Danes combed their hair daily,", 46, LIGHT), B("bathed on Saturdays", 52, GOLD), B("and stole the local women's hearts.", 46)]),
    Card(18.6, 23.4, 330, [T("But...", 80, GOLD), B("In 922, Ibn Fadlan watched the Rus", 48, LIGHT), B("wash every morning", 52, LIGHT), B("all in the same bowl of water.", 52, LIGHT)]),
    Card(23.6, 27.0, 400, [T("Clean or filthy?", 80)]),
    Card(24.2, 27.0, 600, [B("Vote in the comments.", 52, GOLD), B(nr.HANDLE, 40)]),
]

LABEL = nr.Label("MYTH vs HISTORY")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    comb(img, t, window(t, -1.0, 18.6, 0.6), MIST if t < 13.4 else GOLD)
    water(img, t, window(t, 18.4, 27.0, 0.8))
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 15.0, 21.0]:
            nr.still(f"stills/v15_{s}.png", s, frame, seed=47)
    else:
        nr.render("out/v15_bath.mp4", DUR, frame, seed=47, bpm=66)
