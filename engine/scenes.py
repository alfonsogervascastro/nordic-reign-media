"""Code-drawn silhouette scenes for Nordic Reign (no external images needed).

Each scene draws layered silhouettes (mountains, trees, ships, ravens) over the
standard background, with a slow parallax camera so the picture moves.
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr
from nr import W, H, GOLD, LIGHT

def _ridge(seed, base_y, amp, rough=0.55, n=9):
    rng = random.Random(seed)
    pts = [base_y + rng.uniform(-amp, amp), base_y + rng.uniform(-amp, amp)]
    step = amp
    for _ in range(n):
        nxt = []
        for i in range(len(pts) - 1):
            nxt += [pts[i], (pts[i] + pts[i + 1]) / 2 + rng.uniform(-step, step)]
        nxt.append(pts[-1])
        pts = nxt
        step *= rough
    return pts

class Mountains:
    """Three parallax mountain layers, darker toward the viewer."""
    def __init__(self, seed=1, horizon=1300):
        self.layers = []
        cols = [(30, 36, 46), (22, 26, 34), (12, 14, 19)]
        for k, col in enumerate(cols):
            prof = _ridge(seed + k, horizon + k * 110, 260 - k * 50)
            prof = [prof[0]] + prof + [prof[-1]]
            wext = W + 400
            xs = np.linspace(0, wext, len(prof))
            img = Image.new("RGBA", (wext, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            poly = [(x, y) for x, y in zip(xs, prof)] + [(wext, H), (0, H)]
            d.polygon(poly, fill=col + (255,))
            self.layers.append((img, 20 + k * 45))
    def draw(self, img, t, op=1.0):
        for layer, speed in self.layers:
            x = -int(200 - 200 * math.sin(t * 0.05) * 0) - int((t * speed) % 200)
            if op < 1:
                a = np.asarray(layer, np.float32).copy(); a[..., 3] *= op
                layer = Image.fromarray(a.astype(np.uint8))
            img.alpha_composite(layer, (0, 0), (-x, 0, -x + W, H))

def tree(d, x, y, length, angle, depth, width, rng, col):
    if depth == 0 or length < 6:
        return
    x2 = x + length * math.cos(angle)
    y2 = y - length * math.sin(angle)
    d.line([(x, y), (x2, y2)], fill=col, width=max(1, int(width)))
    for da in (rng.uniform(0.25, 0.55), -rng.uniform(0.25, 0.55)):
        tree(d, x2, y2, length * rng.uniform(0.66, 0.78), angle + da, depth - 1, width * 0.68, rng, col)

def yggdrasil(seed=4, col=(8, 10, 14, 255)):
    """A big world-tree silhouette with roots, as an RGBA layer."""
    rng = random.Random(seed)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, base = W / 2, 1360
    d.polygon([(cx - 60, base), (cx + 60, base), (cx + 30, base - 380), (cx - 30, base - 380)], fill=col)
    for a in (math.pi / 2 + 0.05, math.pi / 2 - 0.35, math.pi / 2 + 0.4, math.pi / 2 - 0.7, math.pi / 2 + 0.75):
        tree(d, cx, base - 360, 230, a, 9, 34, rng, col)
    for a in (-math.pi / 2 + 0.3, -math.pi / 2 - 0.3, -math.pi / 2 + 0.8, -math.pi / 2 - 0.8):
        tree(d, cx, base - 20, 140, a, 6, 26, rng, col)
    return img

def moon(img, cx, cy, r, op):
    if op <= 0:
        return
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    glow = np.clip(1 - dist / (r * 4), 0, 1) ** 2 * 120 * op
    disc = np.clip((r - dist) / 3, 0, 1) * 235 * op
    a = np.maximum(glow, disc)
    lay = np.zeros((H, W, 4), np.float32)
    lay[..., :3] = (236, 196, 130)
    lay[..., 3] = a
    img.alpha_composite(Image.fromarray(lay.astype(np.uint8)))

def raven(d, x, y, s, flap, col=(8, 10, 14, 255)):
    wing = s * (0.4 + 0.6 * abs(math.sin(flap)))
    d.polygon([(x - s, y - wing), (x - s * 0.2, y), (x, y + s * 0.15), (x + s * 0.2, y), (x + s, y - wing),
               (x + s * 0.25, y + s * 0.18), (x, y + s * 0.35), (x - s * 0.25, y + s * 0.18)], fill=col)
