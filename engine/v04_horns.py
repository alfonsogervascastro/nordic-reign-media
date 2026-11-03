import sys, math
from PIL import Image, ImageDraw
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 24.0
CX, CY = W / 2, 1060

def bez(p0, p1, p2, n=24):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]

def helmet(img, t):
    op = window(t, 0.3, 21.0, 0.6)
    if op <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = MIST + (int(255 * op),)
    d.arc([CX - 175, CY - 290, CX + 175, CY + 250], 180, 360, fill=c, width=13)       # dome
    d.rounded_rectangle([CX - 182, CY - 28, CX + 182, CY + 8], radius=8, outline=c, width=10)  # brim band
    d.line([(CX, CY - 290), (CX, CY - 28)], fill=c, width=9)                             # ridge
    d.ellipse([CX - 135, CY + 14, CX - 22, CY + 84], outline=c, width=11)                # spectacle guard
    d.ellipse([CX + 22, CY + 14, CX + 135, CY + 84], outline=c, width=11)
    d.line([(CX, CY + 8), (CX, CY + 120)], fill=c, width=12)                             # nasal
    img.alpha_composite(lay)
    # horns: shown at the hook, gone by 3.2 s, back in gold for the opera
    h1 = 1 - ease((t - 2.4) / 0.8) if t < 8 else 0
    h2 = window(t, 13.0, 17.2, 0.6)
    for k, col in ((h1, MIST), (h2, GOLD)):
        if k <= 0:
            continue
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        for s in (-1, 1):
            pts = bez((CX + s * 165, CY - 110), (CX + s * 320, CY - 140), (CX + s * 300, CY - 360))
            d.line(pts, fill=col + (int(255 * k * op),), width=20, joint="curve")
        img.alpha_composite(lay)

cards = [
    Card(0.2, 3.6, 300, [T("Vikings never wore", 72), T("horned helmets.", 72)]),
    Card(1.4, 3.6, 500, [B("Not one has ever been found.", 54, GOLD)]),
    Card(3.8, 8.0, 300, [T("The only near-complete", 60), T("Viking helmet ever found", 60)]),
    Card(4.6, 8.0, 1290, [B("Gjermundbu, Norway. 10th century.", 50), B("No horns.", 54, GOLD)]),
    Card(8.2, 12.6, 330, [T("So where did", 72), T("the horns come from?", 72)]),
    Card(12.8, 17.2, 300, [T("1876. An opera.", 80, GOLD)]),
    Card(13.4, 17.2, 1290, [B("Costume designer Carl Emil Doepler", 48, LIGHT),
                            B("gave them horns for Wagner's Ring cycle.", 48, LIGHT)]),
    Card(17.4, 21.0, 300, [B("Horned helmets did exist:", 56, LIGHT), B("in the Bronze Age,", 56, LIGHT),
                           B("about 1,700 years earlier.", 56, GOLD)]),
    Card(21.2, 24.0, 760, [T("Vikings? Never.", 84)]),
    Card(21.8, 24.0, 920, [B("Follow for more myths, debunked", 48)]),
    Card(22.2, 24.0, 1000, [B(nr.HANDLE, 42)]),
]

LABEL = nr.Label("MYTH vs HISTORY")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    helmet(img, t)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [1.5, 6.0, 15.0, 19.0]:
            nr.still(f"stills/v04_{s}.png", s, frame, seed=11)
    else:
        nr.render("out/v04_horns.mp4", DUR, frame, seed=11, bpm=64)
