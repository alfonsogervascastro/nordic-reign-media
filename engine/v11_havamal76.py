"""HÁVAMÁL — stanza 76. Old Norse text + Bellows translation (1923, public domain)."""
import sys
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, window

DUR = 30.0
ODIN = nr.Painting("../images/rosen_odin_wanderer_1886.jpg", 820, 940, cy=1050, focus=(0.5, 0.25))

cards = [
    Card(0.2, 4.4, 330, [T("The oldest advice", 68), T("about being remembered.", 64, GOLD)]),
    Card(1.0, 4.4, 1540, [B("Art: Georg von Rosen, 1886", 30)]),
    Card(4.6, 9.4, 330, [B("Hávamál, \"the Sayings of the High One\",", 46, LIGHT), B("is advice spoken in the voice of Odin,", 46), B("written down in Iceland around 1270.", 46)]),
    Card(9.6, 14.6, 560, [T("Deyr fé,", 72, GOLD), T("deyja frændr,", 72, GOLD), T("deyr sjalfr it sama...", 72, GOLD)]),
    Card(10.6, 14.6, 1060, [B("Stanza 76, in Old Norse", 40)]),
    Card(14.8, 23.6, 420, [B("Cattle die, and kinsmen die,", 60, LIGHT), B("and so one dies one's self;", 60, LIGHT)]),
    Card(17.6, 23.6, 680, [T("but a noble name", 74, GOLD), T("will never die,", 74, GOLD)]),
    Card(20.0, 23.6, 940, [B("if good renown one gets.", 60, LIGHT)]),
    Card(21.0, 23.6, 1480, [B("Translation: H. A. Bellows, 1923", 32)]),
    Card(23.8, 27.4, 520, [B("\"Fé\" is the word behind", 54, LIGHT), B("the rune FEHU: cattle, wealth.", 54, LIGHT)]),
    Card(24.6, 27.4, 760, [B("Wealth dies. Names don't.", 54, GOLD)]),
    Card(27.6, 30.0, 560, [T("What would you", 72), T("want to be remembered for?", 64, GOLD)]),
    Card(28.2, 30.0, 860, [B(nr.HANDLE, 40)]),
]

LABEL = nr.Label("HÁVAMÁL", "76")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    ODIN.draw(img, t, 0.2, max(window(t, 0.2, 9.6, 0.6), 0.16 * window(t, 9.0, 30.0, 1.2)), dur=9.4)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [2.5, 7.0, 12.5, 21.5, 26.0, 29.0]:
            nr.still(f"stills/v11_{s}.png", s, frame, seed=31)
    else:
        nr.render("out/v11_havamal76.mp4", DUR, frame, seed=31, bpm=56)
