"""MYTH vs HISTORY — correction: the bathing video softened the chronicle (comment by @fakehistoryhunter, 21 Nov 2026).
Latin from R. Vaughan's edition (Camden Third Series 90, 1958) as quoted by fakehistoryhunter.net (16 Jul 2026):
"unde et matronarum castitati insidiabantur, et filias etiam nobilium concubinarum nomine detinebant."
Chronicle written 1220-1258 by an anonymous monk of St Albans (once attributed to John of Wallingford), on the
St Brice's Day massacre of 1002. New hook design: big text and movement from frame 0, series label from 2 s."""
import sys
from PIL import Image, ImageDraw
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, ease, window

DUR = 27.0

def struck(img, t):
    """The line from the old video, struck through from 0.3 s."""
    op = window(t, -1.0, 3.4, 0.4)
    if op <= 0:
        return
    y = 900
    nr.draw_lines(img, [B("“and stole the local", 58, MIST), B("women's hearts”", 58, MIST)], y, op, gap=6)
    k = ease((t - 0.3) / 0.8)
    if k <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for yy, half in ((y + 34, 300), (y + 104, 230)):
        x0 = W / 2 - half
        d.line([(x0, yy), (x0 + 2 * half * k, yy)], fill=GOLD + (int(255 * op),), width=9)
    img.alpha_composite(lay)

cards = [
    Card(-0.8, 3.4, 300, [T("I got this one wrong.", 80), T("A viewer called me out.", 64, GOLD)]),
    Card(3.6, 8.6, 360, [B("The chronicle, in Latin:", 46), B("matronarum castitati", 60, GOLD), B("insidiabantur", 60, GOLD)]),
    Card(4.4, 8.6, 820, [B("“they lay in wait for the chastity", 50, LIGHT), B("of married women”", 50, LIGHT)]),
    Card(8.8, 13.8, 360, [B("filias etiam nobilium", 60, GOLD), B("concubinarum nomine detinebant", 54, GOLD)]),
    Card(9.6, 13.8, 820, [B("“and held even nobles' daughters,", 50, LIGHT), B("under the name of concubines”", 50, LIGHT)]),
    Card(14.0, 18.6, 420, [T("Not seduction.", 84), T("Held.", 84, GOLD)]),
    Card(18.8, 23.2, 330, [B("Written by an unnamed monk", 50, LIGHT), B("at St Albans, 1220–1258,", 50, LIGHT),
                           B("about Danes killed in a massacre", 50, LIGHT), B("two centuries earlier.", 50, LIGHT)]),
    Card(23.4, 27.0, 330, [B("What still stands:", 46), T("Saturday = washing day.", 64, GOLD),
                           B("Thanks, @fakehistoryhunter.", 46, LIGHT)]),
    Card(24.4, 27.0, 900, [T("What should I fact-check next?", 56)]),
]

LABEL = nr.Label("MYTH vs HISTORY", "CORRECTION")

def frame(img, t):
    if t >= 2.0:
        LABEL.draw(img, t - 2.0, DUR - 2.0)
    struck(img, t)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 1.5, 6.0, 11.0, 16.0, 21.0, 25.5]:
            nr.still(f"stills/v34_{s}.png", s, frame, seed=48)
    else:
        nr.render("out/v34_correction.mp4", DUR, frame, seed=48, bpm=66)
