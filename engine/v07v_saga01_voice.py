"""Ep. 1 with narration (voice 6). Same visuals as v07_saga01.py, time-warped to the voice."""
import narrate, v07_saga01 as ep

SEGMENTS = [
    (0.0, 4.0, "Before the gods, before the world, there was only a gap."),
    (4.0, 7.6, "Ginnungagap. The yawning void."),
    (7.6, 11.6, "Fire to the south. Ice to the north."),
    (11.6, 15.2, "Where they met, the ice melted. From the drops, a giant woke. Eemeer."),
    (15.2, 19.2, "From the thaw came a cow, Ow-dumbla. Eemeer drank her milk."),
    (19.2, 23.4, "She licked the salty ice for three days. Out came Booree, the first of the gods."),
    (23.4, 27.2, "Booree's grandson: Odin."),
    (27.2, 31.0, "His first act? Murder."),
]

if __name__ == "__main__":
    d = narrate.render_voiced("out/v07v_saga01.mp4", ep.DUR, ep.frame, SEGMENTS, seed=17, bpm=58)
    print("duration", round(d, 2))
