"""HÁVAMÁL — stanza 55. Bellows translation (1923, public domain). Twist: Odin gave an eye for a drink from Mímir's well
(Gylfaginning 15; Völuspá 28)."""
import sys
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, window

DUR = 28.4
SRC = "../images/rosen_odin_wanderer_1886.jpg"
ODIN = nr.Painting(SRC, 760, 900, cy=1080, focus=(0.5, 0.25))
FACE = nr.Painting(SRC, 700, 700, cy=1060, crop=(120, 20, 400, 300), zoom=0.10, feather=0.12)

cards = [
    Card(-0.8, 4.2, 330, [T("Odin's advice:", 74), T("don't be too wise.", 74, GOLD)]),
    Card(0.4, 4.2, 1560, [B("Art: Georg von Rosen, 1886", 30)]),
    Card(4.4, 8.6, 330, [T("Meðalsnotr", 70, GOLD), T("skyli manna hverr,", 64, GOLD), T("æva til snotr sé", 64, GOLD)]),
    Card(5.0, 8.6, 1560, [B("Hávamál 55, in Old Norse", 34)]),
    Card(8.8, 15.0, 330, [B("A measure of wisdom", 62, LIGHT), B("each man shall have,", 62, LIGHT), B("but never too much let him know;", 54)]),
    Card(15.2, 20.4, 330, [T("for the wise man's heart", 62, GOLD), T("is seldom happy,", 62, GOLD), B("if wisdom too great he has won.", 54, LIGHT)]),
    Card(16.0, 20.4, 1560, [B("Translation: H. A. Bellows, 1923", 32)]),
    Card(20.6, 25.0, 330, [B("Strange advice from a god", 58, LIGHT), T("who gave an eye", 72, GOLD), B("for one drink from Mímir's well.", 52, LIGHT)]),
    Card(25.2, 28.4, 330, [T("Would you trade", 72), T("an eye for wisdom?", 72, GOLD)]),
    Card(25.8, 28.4, 520, [B("Yes or no, in the comments.", 48), B(nr.HANDLE, 40)]),
]

LABEL = nr.Label("HÁVAMÁL", "55")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    ODIN.draw(img, t, 0.0, window(t, -1.0, 15.2, 0.6), dur=15.2)
    FACE.draw(img, t, 15.0, window(t, 15.0, 25.2, 0.6), dur=10.2)
    for c in cards:
        c.draw(img, t)

SEGMENTS = [
    (0.0, 4.4, "Odin's advice: don't be too wise."),
    (4.4, 8.8, ""),
    (8.8, 15.2, "A measure of wisdom each man shall have, but never too much let him know;"),
    (15.2, 20.6, "for the wise man's heart is seldom happy, if wisdom too great he has won."),
    (20.6, 25.2, "Strange advice, from a god who gave an eye for one drink from Meemeer's well."),
    (25.2, 28.4, "Would you trade an eye for wisdom?"),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 12.0, 18.0, 23.0]:
            nr.still(f"stills/v16_{s}.png", s, frame, seed=53)
    else:
        import narrate
        print("duration", round(narrate.render_voiced("out/v16v_havamal55.mp4", DUR, frame, SEGMENTS, seed=53, bpm=56), 2))
