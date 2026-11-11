"""REAL VIKINGS — Birka grave Bj 581 (Sweden, 10th c.). Excavated 1878 by Hjalmar Stolpe; plan drawing published 1889.
Weapons, two horses, a gaming set. DNA (Hedenstierna-Jonson et al., Am. J. Phys. Anthropol. 2017): female.
Follow-up and reply to critics: Price et al., Antiquity 2019. Interpretation as a warrior is debated.
Art: Hjalmar Stolpe's plan of Bj 581 (1889, public domain). Soundtrack: Before the End Begins."""
import sys
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, window

DUR = 31.0
SRC = "../images/stolpe_birka_bj581_1889.jpg"
FULL = nr.Painting(SRC, 600, 960, cy=1090, zoom=0.06, feather=0.08)
BODY = nr.Painting(SRC, 900, 900, cy=1040, crop=(60, 150, 900, 900), zoom=0.10, feather=0.10)
DETAIL = nr.Painting(SRC, 860, 860, cy=1040, crop=(200, 330, 820, 950), zoom=0.10, feather=0.10)
HORSES = nr.Painting(SRC, 980, 640, cy=1000, crop=(20, 960, 940, 1480), zoom=0.10, feather=0.10)

cards = [
    Card(-0.8, 4.0, 330, [T("A Viking warrior's grave.", 66), T("Then the DNA came back.", 66, GOLD)]),
    Card(0.4, 4.0, 1600, [B("Grave Bj 581, drawn by Hjalmar Stolpe, 1889", 30)]),
    Card(4.2, 8.4, 330, [B("Birka, Sweden, 10th century.", 54, LIGHT), B("Dug up in 1878.", 54)]),
    Card(8.6, 13.0, 330, [B("Sword, axe, spears,", 56, LIGHT), B("armour-piercing arrows, two shields", 50, LIGHT), T("and two horses.", 66, GOLD)]),
    Card(13.2, 16.6, 330, [B("For 130 years,", 56, LIGHT), B("everyone assumed:", 56, LIGHT), T("a man.", 80, GOLD)]),
    Card(16.8, 20.6, 330, [T("2017: DNA.", 76), B("Two X chromosomes. No Y.", 54, LIGHT), T("A woman.", 80, GOLD)]),
    Card(20.8, 24.6, 330, [B("But was she a warrior?", 58, LIGHT), B("Critics: weapons in a grave", 50), B("don't prove she fought.", 50)]),
    Card(24.8, 28.0, 330, [B("She was buried with", 54, LIGHT), T("a war-game board", 66, GOLD), B("which some read as a commander's sign.", 44, LIGHT)]),
    Card(25.2, 28.0, 1600, [B("Hedenstierna-Jonson et al. 2017; Price et al., Antiquity 2019", 28)]),
    Card(28.2, 31.0, 330, [T("Warrior or not?", 76), B("Tell us what you think.", 52, GOLD)]),
    Card(28.8, 31.0, 1600, [B(nr.HANDLE, 40)]),
]

LABEL = nr.Label("REAL VIKINGS")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    FULL.draw(img, t, 0.0, window(t, -1.0, 4.4, 0.6), dur=4.4)
    DETAIL.draw(img, t, 4.2, window(t, 4.2, 8.6, 0.6), dur=4.4)
    BODY.draw(img, t, 8.4, window(t, 8.4, 11.0, 0.5), dur=2.6)
    HORSES.draw(img, t, 10.8, window(t, 10.8, 13.2, 0.5), dur=2.4)
    BODY.draw(img, t, 13.0, window(t, 13.0, 17.0, 0.6), dur=4.0)
    DETAIL.draw(img, t, 16.8, window(t, 16.8, 21.0, 0.6), dur=4.2)
    HORSES.draw(img, t, 20.8, window(t, 20.8, 24.8, 0.6), dur=4.0)
    FULL.draw(img, t, 24.6, window(t, 24.6, 31.0, 0.6), dur=6.4)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 9.5, 12.0, 15.0, 18.5, 22.5, 26.5, 30.0]:
            nr.still(f"stills/v23_{s}.png", s, frame, seed=71)
    else:
        nr.render("out/v23_birka.mp4", DUR, frame, seed=71, bpm=60)
