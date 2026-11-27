"""Trace a public-domain line engraving of a real Viking-age object into clean tattoo linework.

Usage: python3 trace.py <src image> <out prefix> x0,y0,x1,y1 [--thicken px] [--size 3000]
Writes <prefix>.svg (vector) and <prefix>_stencil.png (black on transparent).
"""
import sys, argparse
import numpy as np
import cv2, potrace, cairosvg

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("box")
ap.add_argument("--thicken", type=float, default=0.0)
ap.add_argument("--size", type=int, default=3000)
ap.add_argument("--up", type=int, default=4)
ap.add_argument("--speck", type=int, default=60)
a = ap.parse_args()

g = cv2.imread(a.src, cv2.IMREAD_GRAYSCALE)
x0, y0, x1, y1 = map(int, a.box.split(","))
g = g[y0:y1, x0:x1]
g = cv2.resize(g, None, fx=a.up, fy=a.up, interpolation=cv2.INTER_CUBIC)
g = cv2.GaussianBlur(g, (0, 0), a.up * 0.45)
thr = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[0]
ink = (g < thr).astype(np.uint8)
if a.thicken > 0:
    k = int(round(a.thicken * a.up)) | 1
    ink = cv2.dilate(ink, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
# drop specks
n, lab, st, _ = cv2.connectedComponentsWithStats(ink, 8)
keep = np.zeros(n, bool); keep[1:] = st[1:, cv2.CC_STAT_AREA] >= a.speck * a.up * a.up
ink = keep[lab].astype(np.uint8)
ink = np.pad(ink, 8)
bm = potrace.Bitmap(~ink.astype(bool))
if ink.mean() > 0.5:
    raise SystemExit("ink > 50 %: threshold inverted")
path = bm.trace(turdsize=int(4 * a.up * a.up), alphamax=1.1, opticurve=True, opttolerance=0.3)
H, W = ink.shape
parts = []
for c in path:
    s = c.start_point
    d = [f"M{s.x:.2f},{s.y:.2f}"]
    for seg in c.segments:
        if seg.is_corner:
            d.append(f"L{seg.c.x:.2f},{seg.c.y:.2f}L{seg.end_point.x:.2f},{seg.end_point.y:.2f}")
        else:
            d.append(f"C{seg.c1.x:.2f},{seg.c1.y:.2f} {seg.c2.x:.2f},{seg.c2.y:.2f} {seg.end_point.x:.2f},{seg.end_point.y:.2f}")
    d.append("Z")
    parts.append("".join(d))
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
       f'<path fill="#0c0c0c" fill-rule="evenodd" d="{" ".join(parts)}"/></svg>')
open(a.out + ".svg", "w").write(svg)
scale = a.size / max(W, H)
cairosvg.svg2png(bytestring=svg.encode(), write_to=a.out + "_stencil.png", output_width=int(W * scale), output_height=int(H * scale))
print(a.out, W, H)
