import sys
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, window

DUR = 23.0
WORDS = [("WINDOW", 'Old Norse "vindauga"', '"wind-eye"'),
         ("SKY", 'Old Norse "ský"', '"cloud"'),
         ("EGG", 'Old Norse "egg"', "it beat Old English \"ey\""),
         ("BERSERK", 'Old Norse "berserkr"', 'probably "bear-shirt"'),
         ("THEY", 'Old Norse "þeir"', "even this one")]

cards = [
    Card(0.2, 3.6, 640, [T("You speak Old Norse", 72), T("every single day.", 72)]),
    Card(1.4, 3.6, 880, [B("Here's the proof.", 56, GOLD)]),
]
for i, (word, origin, meaning) in enumerate(WORDS):
    a = 3.8 + i * 3.2
    b = a + 3.0
    cards += [Card(a, b, 640, [T(word, 120, LIGHT)]),
              Card(a + 0.4, b, 860, [B(origin, 58, GOLD)]),
              Card(a + 0.8, b, 950, [B(meaning, 54)])]
cards += [
    Card(20.0, 23.0, 680, [T("Which one", 76), T("surprised you?", 76)]),
    Card(20.7, 23.0, 920, [B("Follow for more", 48)]),
    Card(21.1, 23.0, 1000, [B(nr.HANDLE, 42)]),
]

def frame(img, t):
    for i in range(len(WORDS)):
        a = 3.8 + i * 3.2
        nr.draw_rule(img, 600, window(t, a + 0.2, a + 3.0), 220)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [2.6, 5.5, 18.0]:
            nr.still(f"stills/v05_{s}.png", s, frame, seed=13)
    else:
        nr.render("out/v05_words.mp4", DUR, frame, seed=13, bpm=68)
