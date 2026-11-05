"""Ep. 2 with narration (Kokoro). Same visuals as v08_saga02.py, time-warped to the voice."""
import sys
import narrate, v08_saga02 as ep

SEGMENTS = [
    (0.0, 4.2, "Odin and his brothers, Vili and Vay, killed the giant Eemeer."),
    (4.2, 8.6, "So much blood poured from him that every frost giant drowned. All but one. Bergelmeer."),
    (8.6, 12.8, "Then they built the world from his body."),
    (12.8, 15.0, "His blood became the sea,"),
    (15.0, 17.4, "his flesh the earth, his bones the mountains."),
    (17.4, 19.6, "His skull became the sky, held up by four dwarves."),
    (19.6, 21.8, "His brains, the clouds."),
    (21.8, 25.2, "And with his eyebrows, they walled in Midgard."),
    (25.2, 27.6, "A home for humans who did not exist yet."),
    (27.6, 31.2, "But what holds all the worlds together?"),
    (31.2, 34.4, "This chapter, as a tattoo."),
]

if __name__ == "__main__":
    voice = sys.argv[1] if len(sys.argv) > 1 else None
    d = narrate.render_voiced("out/v08v_saga02.mp4", ep.DUR, ep.frame, SEGMENTS, seed=19, bpm=60, voice=voice)
    print("duration", round(d, 2))
