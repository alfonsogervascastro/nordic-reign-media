import sys
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, ease, window

DUR = 24.5

DAYS = [("TUES", "Týr's day", "God of war and oaths"),
        ("WEDNES", "Woden's day", "Odin, the All-Father"),
        ("THURS", "Thor's day", "God of thunder"),
        ("FRI", "Frigg's day", "Odin's wife, queen of Asgard")]

cards = [
    Card(0.2, 3.4, 640, [T("Your week is named", 70), T("after Norse gods.", 70)]),
    Card(1.4, 3.4, 880, [B("Well, four days of it.", 56, GOLD)]),
]
for i, (pre, god, desc) in enumerate(DAYS):
    a = 3.6 + i * 3.4
    b = a + 3.2
    cards.append(Card(a, b, 700, [[T(pre, 112, GOLD), T("DAY", 112, LIGHT)]]))
    cards.append(Card(a + 0.4, b, 900, [B(god, 64, LIGHT)]))
    cards.append(Card(a + 0.7, b, 1000, [B(desc, 48)]))
cards += [
    Card(3.6, 16.8, 1440, [B("Via Old English: Tiw, Woden, Thunor, Frige", 34)]),
    Card(17.2, 20.6, 700, [T("SATURDAY?", 100)]),
    Card(17.8, 20.6, 900, [B("Saturn. That one's Roman.", 60, GOLD)]),
    Card(20.8, 24.5, 680, [T("Which day", 76), T("were you born?", 76)]),
    Card(21.6, 24.5, 930, [B("Comment it. Follow for more.", 50)]),
    Card(22.0, 24.5, 1010, [B(nr.HANDLE, 42)]),
]

LABEL = nr.Label("WORDS FROM THE NORTH")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    for i in range(len(DAYS)):
        a = 3.6 + i * 3.4
        nr.draw_rule(img, 650, window(t, a + 0.2, a + 3.2), 220)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [2.6, 5.5, 9.0, 18.8, 23.2]:
            nr.still(f"stills/v02_{s}.png", s, frame, seed=5)
    else:
        nr.render("out/v02_days.mp4", DUR, frame, seed=5, bpm=70)
