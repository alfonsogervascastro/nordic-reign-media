"""Ep. 3 with narration (Kokoro, voice 6). Same visuals as v10_saga03.py, time-warped to the voice."""
import sys
import narrate, v10_saga03 as ep

SEGMENTS = [
    (0.0, 4.8, "One tree holds all nine worlds."),
    (4.8, 9.0, "Igdrasil. Its branches spread over every world."),
    (9.0, 12.8, "Three roots. Three wells."),
    (12.8, 14.4, "Kvergelmeer, in the cold mist."),
    (14.4, 16.0, "Meemeer's well of wisdom."),
    (16.0, 18.6, "And Urd's well, where the gods meet."),
    (18.6, 22.8, "An eagle at the top. A dragon gnawing the roots."),
    (22.8, 27.0, "And a squirrel runs between them, carrying insults."),
    (27.0, 31.2, "Four stags eat its leaves. Its side is rotting."),
    (31.2, 35.2, "Every day the Norns water it, so it will not die. Next: the first humans."),
    (35.2, 38.4, "This chapter, as a tattoo."),
]

if __name__ == "__main__":
    d = narrate.render_voiced("out/v10v_saga03.mp4", ep.DUR, ep.frame, SEGMENTS, seed=23, bpm=60)
    print("duration", round(d, 2))
