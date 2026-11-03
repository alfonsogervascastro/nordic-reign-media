import sys
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, ease, window

DUR = 21.0
SX, SY, SW, SH = (W - 460) / 2, 520, 460, 660

cards = [
    Card(0.2, 3.4, 300, [T("This rune meant wealth.", 64)]),
    Card(1.3, 3.4, 400, [B("Just not the kind you think.", 52)]),
    Card(3.6, 20.6, 1250, [T("FEHU", 100, GOLD)]),
    Card(3.9, 20.6, 1380, [B("Rune 1 of 24 · Elder Futhark", 42)]),
    Card(5.6, 9.6, 270, [T("Its name means CATTLE.", 58)]),
    Card(6.4, 9.6, 370, [B("For Norse farmers, cattle", 50), B("were wealth you could move.", 50)]),
    Card(9.9, 14.6, 230, [T("HISTORICAL", 38, GOLD), B("The medieval rune poems:", 50, LIGHT),
                          B("wealth brings comfort, but strife among kin.", 46)]),
    Card(14.9, 18.0, 260, [T("MODERN", 38, MIST), B("20th-century readings:", 50, LIGHT),
                           B("abundance, new beginnings.", 50)]),
    Card(18.2, 21.0, 230, [T("Would you tattoo it?", 60)]),
    Card(18.8, 21.0, 340, [B("Next Monday: URUZ · " + nr.HANDLE, 40)]),
]

def frame(img, t):
    nr.draw_slab(img, SX, SY, SW, SH, window(t, 2.6, 21.0, 0.8))
    p = ease((t - 3.0) / 2.4)
    nr.draw_rune(img, "fehu", SX + 70, SY + 70, SW - 140, SH - 140, p, width=34)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [12.0]:
            nr.still(f"stills/v06_{s}.png", s, frame, seed=7)
    else:
        nr.render("out/v06_fehu.mp4", DUR, frame, seed=7, bpm=60)
