"""HÁVAMÁL — stanza 47. Bellows translation (1923, public domain). Voice: Kokoro am_michael (Old Norse line silent).
Art: Georg von Rosen, Odin the Wanderer (1886); Robert Engels, Odin at the Well of Wisdom (1903)."""
import sys
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, window

DUR = 29.0
SRC = "../images/rosen_odin_wanderer_1886.jpg"
ODIN = nr.Painting(SRC, 760, 900, cy=1080, focus=(0.5, 0.25))
FACE = nr.Painting(SRC, 700, 700, cy=1060, crop=(120, 20, 400, 300), zoom=0.10, feather=0.12)
PAIR = nr.Painting("../images/engels_odin_mimir_well_1903.jpg", 700, 880, cy=1150, zoom=0.08, feather=0.10)

cards = [
    Card(-0.8, 4.2, 330, [T("Odin on loneliness:", 72), T("the cure is one friend.", 66, GOLD)]),
    Card(0.4, 4.2, 1600, [B("Art: Georg von Rosen, 1886", 30)]),
    Card(4.4, 8.8, 330, [T("Ungr var ek forðum,", 62, GOLD), T("fór ek einn saman", 62, GOLD), B("… maðr er manns gaman.", 52, LIGHT)]),
    Card(5.0, 8.8, 1600, [B("Hávamál 47, in Old Norse", 34)]),
    Card(9.0, 14.6, 330, [B("Young was I once,", 62, LIGHT), B("and wandered alone,", 62, LIGHT), B("And nought of the road I knew;", 54)]),
    Card(14.8, 20.0, 330, [T("Rich did I feel", 70, GOLD), T("when a comrade I found,", 62, GOLD), B("For man is man's delight.", 56, LIGHT)]),
    Card(15.4, 20.0, 1600, [B("Translation: H. A. Bellows, 1923", 32)]),
    Card(20.2, 25.0, 330, [B("Advice from a god who walks", 54, LIGHT), B("the worlds alone, in a grey cloak,", 50, LIGHT), T("with only two ravens.", 62, GOLD)]),
    Card(25.2, 29.0, 330, [T("Who is your comrade?", 70), B("Send this to them.", 54, GOLD)]),
    Card(25.8, 29.0, 1600, [B(nr.HANDLE, 40)]),
]

LABEL = nr.Label("HÁVAMÁL", "47")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    ODIN.draw(img, t, 0.0, window(t, -1.0, 4.6, 0.6), dur=4.6)
    FACE.draw(img, t, 4.4, window(t, 4.4, 9.2, 0.6), dur=4.8)
    ODIN.draw(img, t, 9.0, window(t, 9.0, 15.0, 0.6), dur=6.0)
    PAIR.draw(img, t, 14.8, window(t, 14.8, 20.4, 0.6), dur=5.6)
    FACE.draw(img, t, 20.2, window(t, 20.2, 25.4, 0.6), dur=5.2)
    PAIR.draw(img, t, 25.2, window(t, 25.2, 29.0, 0.6), dur=3.8)
    for c in cards:
        c.draw(img, t)

SEGMENTS = [
    (0.0, 4.4, "Odin on loneliness: the cure is one friend."),
    (4.4, 9.0, ""),
    (9.0, 14.8, "Young was I once, and wandered alone, and nought of the road I knew;"),
    (14.8, 20.2, "Rich did I feel when a comrade I found, for man is man's delight."),
    (20.2, 25.2, "Advice from a god who walks the worlds alone, in a grey cloak, with only two ravens."),
    (25.2, 29.0, "Who is your comrade? Send this to them."),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 12.0, 17.5, 22.5, 27.0]:
            nr.still(f"stills/v25_{s}.png", s, frame, seed=79)
    else:
        import narrate
        print("duration", round(narrate.render_voiced("out/v25v_havamal47.mp4", DUR, frame, SEGMENTS, seed=79, bpm=56), 2))
