"""Extra reel: "Pause to find your rune" — the 24 Elder Futhark runes flash past,
each with its (reconstructed) name and literal meaning. Engagement game, not divination."""
import sys
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, ease, window

nr.RUNES.setdefault("algiz", [[(0.5, 0), (0.5, 1)], [(0.5, 0.45), (0.18, 0.05)], [(0.5, 0.45), (0.82, 0.05)]])

RUNES = [("fehu", "FEHU", "cattle, wealth"), ("uruz", "URUZ", "aurochs, a wild ox (?)"),
         ("thurisaz", "THURISAZ", "giant · or thorn"), ("ansuz", "ANSUZ", "a god"),
         ("raidho", "RAIDHO", "ride, journey"), ("kaunan", "KAUNAN", "ulcer · or torch"),
         ("gebo", "GEBO", "gift"), ("wunjo", "WUNJO", "joy"), ("hagalaz", "HAGALAZ", "hail"),
         ("naudiz", "NAUDIZ", "need"), ("isa", "ISA", "ice"), ("jera", "JERA", "year, harvest"),
         ("eihwaz", "EIHWAZ", "yew tree"), ("perthro", "PERTHRO", "meaning unknown"),
         ("algiz", "ALGIZ", "elk (?)"), ("sowilo", "SOWILO", "sun"), ("tiwaz", "TIWAZ", "the god Týr"),
         ("berkano", "BERKANO", "birch"), ("ehwaz", "EHWAZ", "horse"), ("mannaz", "MANNAZ", "man, human"),
         ("laguz", "LAGUZ", "water, lake"), ("ingwaz", "INGWAZ", "the god Ing"),
         ("othala", "OTHALA", "inherited land"), ("dagaz", "DAGAZ", "day")]

T0, STEP = 1.7, 0.55
T_END = T0 + STEP * len(RUNES)          # 14.9 s
DUR = T_END + 4.6                       # 19.5 s
SX, SY, SW, SH = (W - 460) / 2, 560, 460, 620

cards = [
    Card(-0.8, T0 - 0.05, 330, [T("PAUSE THE VIDEO", 70, LIGHT)]),
    Card(-0.8, T0 - 0.05, 440, [T("TO FIND YOUR RUNE", 70, GOLD)]),
    Card(T_END, DUR + 1, 360, [T("What did you get?", 70)]),
    Card(T_END + 0.3, DUR + 1, 470, [B("Comment your rune.", 54, LIGHT)]),
    Card(T_END + 0.6, DUR + 1, 1240, [B("Names are modern reconstructions.", 40),
                                      B("Meanings: rune poems and reconstructions.", 40),
                                      B("Follow for one rune every Monday · " + nr.HANDLE, 36, GOLD)], gap=14),
]
LABEL = nr.Label("FIND YOUR RUNE")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    # hook: a rune already on screen at frame 0, so the first frame has an image
    if t < T0:
        nr.draw_slab(img, SX, SY + 60, SW, SH, 1.0)
        nr.draw_rune(img, "ansuz", SX + 80, SY + 140, SW - 160, SH - 160, 1.0, width=34, glow=0.6)
    elif t < T_END:
        k = min(int((t - T0) / STEP), len(RUNES) - 1)
        key, name, meaning = RUNES[k]
        nr.draw_slab(img, SX, SY, SW, SH, 1.0)
        nr.draw_rune(img, key, SX + 80, SY + 80, SW - 160, SH - 160, 1.0, width=34)
        nr.draw_lines(img, [T(f"{k + 1} / 24", 34, MIST)], 440, 1.0)
        nr.draw_lines(img, [T(name, 84, GOLD), B(meaning, 54, LIGHT)], 1240, 1.0, gap=18)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 3.0, 9.6, 16.5]:
            nr.still(f"stills/v19_{s}.png", s, frame, seed=71)
    else:
        nr.render("out/v19_find_your_rune.mp4", DUR, frame, seed=71,
                  music="../audio/thunder-of-the-gods.mp3", music_start=3.0)
