"""Hávamál 76 with narration (voice 6). The Old Norse lines stay silent, to be read on screen."""
import narrate, v11_havamal76 as ep

SEGMENTS = [
    (0.0, 4.6, "The oldest advice about being remembered."),
    (4.6, 9.6, "Hah-vah-mahl, the Sayings of the High One, is advice spoken in the voice of Odin, written down in Iceland around twelve seventy."),
    (9.6, 14.8, ""),
    (14.8, 17.6, "Cattle die, and kinsmen die, and so one dies one's self;"),
    (17.6, 20.0, "but a noble name will never die,"),
    (20.0, 23.8, "if good renown one gets."),
    (23.8, 27.6, "Fay is the word behind the rune Fay-hoo. Cattle. Wealth. Wealth dies. Names don't."),
    (27.6, 30.0, "What would you want to be remembered for?"),
]

if __name__ == "__main__":
    d = narrate.render_voiced("out/v11v_havamal76.mp4", ep.DUR, ep.frame, SEGMENTS, seed=31, bpm=56)
    print("duration", round(d, 2))
