"""WORDS FROM THE NORTH — Odin's name. Óðinn < Proto-Germanic *Wōdanaz, from *wōðaz 'frenzied, inspired';
Old Norse óðr 'frantic' (adj.) and 'mind, poetry, inspiration' (noun); Óðrerir, the vessel of the mead of poetry (Ep. 8);
Old English wōd 'mad'; German Wut 'rage'. Adam of Bremen (c. 1075): "Wodan, id est furor". Soundtrack: Born in the Dark."""
import sys
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, window

DUR = 25.0
SRC = "../images/rosen_odin_wanderer_1886.jpg"
ODIN = nr.Painting(SRC, 760, 900, cy=1080, focus=(0.5, 0.25))
FACE = nr.Painting(SRC, 760, 760, cy=1060, crop=(120, 20, 400, 300), zoom=0.10, feather=0.12)
THOR = nr.Painting("../images/winge_thor_giants_1872.jpg", 860, 760, cy=1060, crop=(0, 900, 1280, 1851), zoom=0.10, feather=0.12)

cards = [
    Card(-0.8, 4.0, 330, [T("Odin's name means", 72), T("fury.", 96, GOLD)]),
    Card(0.4, 4.0, 1620, [B("Art: Georg von Rosen, 1886", 30)]),
    Card(4.2, 8.6, 330, [B("Old Norse", 52, LIGHT), T("Óðinn", 100, GOLD), B('from óðr: "frantic, raging"', 52, LIGHT)]),
    Card(8.8, 13.0, 330, [B("But óðr also meant", 54, LIGHT), T("mind, poetry, inspiration.", 60, GOLD)]),
    Card(13.2, 17.4, 330, [B("The pot of the mead of poetry", 50, LIGHT), B("was called", 50, LIGHT), T("Óðrerir", 90, GOLD), B('"stirrer of inspiration".', 50)]),
    Card(17.6, 21.6, 330, [B("Old English wōd: mad.", 54, LIGHT), B("German still says", 54, LIGHT), T("Wut: rage.", 80, GOLD)]),
    Card(18.0, 21.6, 1620, [B("Art: Mårten Eskil Winge, 1872", 30)]),
    Card(21.8, 25.0, 330, [B('A monk wrote it in 1075: "Wodan, that is, fury."', 44, LIGHT), T("Fury or poetry:", 68), T("which is more Odin?", 66, GOLD)]),
    Card(22.2, 25.0, 1620, [B("Adam of Bremen, Gesta IV · " + nr.HANDLE, 32)]),
]

LABEL = nr.Label("WORDS FROM THE NORTH")

def frame(img, t):
    LABEL.draw(img, t, DUR)
    ODIN.draw(img, t, 0.0, window(t, -1.0, 4.4, 0.5), dur=4.4)
    FACE.draw(img, t, 4.2, window(t, 4.2, 8.8, 0.5), dur=4.6)
    ODIN.draw(img, t, 8.6, window(t, 8.6, 13.2, 0.5), dur=4.6)
    FACE.draw(img, t, 13.0, window(t, 13.0, 17.6, 0.5), dur=4.6)
    THOR.draw(img, t, 17.4, window(t, 17.4, 21.8, 0.5), dur=4.4)
    ODIN.draw(img, t, 21.6, window(t, 21.6, 25.0, 0.5), dur=3.4)
    for c in cards:
        c.draw(img, t)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for s in [0.0, 6.0, 11.0, 15.0, 19.5, 23.5]:
            nr.still(f"stills/v30_{s}.png", s, frame, seed=101)
    else:
        nr.render("out/v30_odin_name.mp4", DUR, frame, seed=101, bpm=60)
