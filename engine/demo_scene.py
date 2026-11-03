"""Demo still: Yggdrasil under a gold moon with ravens and mountains."""
import math
from PIL import Image, ImageDraw
import nr, scenes
from nr import T, B, GOLD, LIGHT, W, H

mount = scenes.Mountains(seed=3)
TREE = scenes.yggdrasil()

def frame(img, t):
    scenes.moon(img, W * 0.68, 620, 95, 1.0)
    mount.draw(img, t)
    img.alpha_composite(TREE)
    d = ImageDraw.Draw(img)
    for i, (x, y, s) in enumerate([(640, 560, 30), (760, 650, 24), (860, 540, 20)]):
        scenes.raven(d, x + t * 4, y, s, t * 6 + i)
    nr.Label("THE NORSE SAGA", "EP. 3").draw(img, t, 20)
    nr.draw_lines(img, [T("One tree holds", 70), T("nine worlds.", 70, GOLD)], 300, 1.0)
    nr.draw_lines(img, [B("Its name: Yggdrasil.", 54, LIGHT)], 1560, 1.0)

if __name__ == "__main__":
    nr.still("stills/demo_yggdrasil.png", 6.0, frame, seed=21)
