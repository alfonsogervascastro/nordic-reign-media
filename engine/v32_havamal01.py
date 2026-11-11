"""HÁVAMÁL — stanza 1. Bellows translation (1923, public domain). Voice: Kokoro am_michael (Old Norse line silent).
Art: Georg von Rosen, Odin the Wanderer (1886); Oluf O. Bagge, Yggdrasil (1847)."""
import sys
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, window

DUR = 29.0
SRC = "../images/rosen_odin_wanderer_1886.jpg"
ODIN = nr.Painting(SRC, 760, 900, cy=1080, focus=(0.5, 0.25))
FACE = nr.Painting(SRC, 700, 700, cy=1060, crop=(120, 20, 400, 300), zoom=0.10, feather=0.12)
HALL = nr.Painting("../images/bagge_yggdrasil_1847.jpg", 1000, 560, cy=1000, crop=(60, 250, 860, 560), zoom=0.10, feather=0.12)

cards = [
    Card(-0.8, 4.2, 330, [T("Odin's first rule:", 76), T("check the doors.", 76, GOLD)]),
    Card(0.4, 4.2, 1600, [B("Art: Georg von Rosen, 1886", 30)]),
    Card(4.4, 8.8, 330, [T("Gáttir allar,", 66, GOLD), T("áðr gangi fram…", 66, GOLD)]),
    Card(5.0, 8.8, 1600, [B("Hávamál 1, the very first stanza, in Old Norse", 32)]),
    Card(9.0, 14.6, 330, [B("Within the gates ere a man shall go,", 52, LIGHT), B("(Full warily let him watch,)", 52, LIGHT), B("Full long let him look about him;", 52)]),
    Card(14.8, 20.0, 330, [T("For little he knows", 66, GOLD), T("where a foe may lurk,", 66, GOLD), B("And sit in the seats within.", 54, LIGHT)]),
    Card(15.4, 20.0, 1600, [B("Translation: H. A. Bellows, 1923", 32)]),
    Card(20.2, 25.0, 330, [B("A world of feuds and halls,", 54, LIGHT), B("where a guest could be", 54, LIGHT), T("an enemy at the table.", 62, GOLD)]),
    Card(25.2, 29.0, 330, [T("Do you sit", 76), T("facing the door?", 72, GOLD)]),
    Card(25.8, 29.0, 1600, [B("Yes or no  ·  " + nr.HANDLE, 40)]),
]

LABEL = nr.Label("HÁVAMÁL", "1")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    ODIN.draw(img, t, 0.0, window(t, -1.0, 4.6, 0.6), dur=4.6)
    FACE.draw(img, t, 4.4, window(t, 4.4, 9.2, 0.6), dur=4.8)
    HALL.draw(img, t, 9.0, window(t, 9.0, 15.0, 0.6), dur=6.0)
    FACE.draw(img, t, 14.8, window(t, 14.8, 20.4, 0.6), dur=5.6)
    HALL.draw(img, t, 20.2, window(t, 20.2, 25.4, 0.6), dur=5.2)
    ODIN.draw(img, t, 25.2, window(t, 25.2, 29.0, 0.6), dur=3.8)
    for c in cards:
        c.draw(img, t)

SEGMENTS = [
    (0.0, 4.4, "Odin's first rule: check the doors."),
    (4.4, 9.0, ""),
    (9.0, 14.8, "Within the gates ere a man shall go, full warily let him watch, full long let him look about him;"),
    (14.8, 20.2, "For little he knows where a foe may lurk, and sit in the seats within."),
    (20.2, 25.2, "A world of feuds and halls, where a guest could be an enemy at the table."),
    (25.2, 29.0, "Do you sit facing the door?"),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 12.0, 17.5, 22.5, 27.0]:
            nr.still(f"stills/v32_{s}.png", s, frame, seed=107)
    else:
        import narrate
        print("duration", round(narrate.render_voiced("out/v32v_havamal01.mp4", DUR, frame, SEGMENTS, seed=107, bpm=56), 2))
