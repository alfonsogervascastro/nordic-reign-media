"""EXPERIMENT (27 Nov 2026, not used yet): code-drawn animals came out stiff; kept for Borre borders and as a base.

Viking-age ornament built from the rules of the real styles (27 Nov 2026).

Why: the old designs (knots.py torus knots) are generic mathematical knots and read as Celtic / new-age.
Rules used here (Jonas Lau Markussen, Gelmir compendium; Gräslund's runestone styles):
  Borre (c. 850-950): ring-chain = circles and lozenges side by side, each outlined by a closed ribbon that
      interlaces with its neighbours; tight interlace, almost no background; even ribbons, circular curves.
  Jelling / Mammen (c. 900-1000): ribbon animal in profile, round or almond eye, curled lip lappet, neck
      tendril, spiral at the hip, pellets at the joints; even outline, S-shapes and pretzel knots.
  Urnes (c. 1050-1125): great beast + thinner snakes, only two ribbon widths; figure-of-eight loops, circular
      curves in opposite directions; open interlace with background showing; no central symmetry; head reduced
      to an elongated terminal with almond eye and lip lappets; tightly scrolled terminals.
Every crossing alternates over / under along each strand (as in all Norse interlace).
"""
import math
import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import cKDTree
from knots import Knot, chaikin

INK = 12

def smooth(pts, iters=5, closed=False):
    return chaikin(np.asarray(pts, float), iters, closed=closed)

def resample_r(P, r, step):
    seg = np.hypot(*np.diff(P, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    n = max(2, int(cum[-1] / step))
    s = np.linspace(0, cum[-1], n)
    return (np.stack([np.interp(s, cum, P[:, 0]), np.interp(s, cum, P[:, 1])], 1), np.interp(s, cum, r))

class Ribbons:
    """Interlaced ribbons with a width that can change along each strand; extra drawings on top."""
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.strands = []
        self.overlays = []

    def add(self, P, r, closed=False):
        P = np.asarray(P, float)
        r = np.broadcast_to(np.asarray(r, float), (len(P),)).copy()
        self.strands.append((P, closed, r))
        return P

    def render(self, line=18, gap=None, groove=False, piece=2.0):
        gap = line * 1.1 if gap is None else gap
        k = Knot(self.w, self.h)
        for P, closed, _ in self.strands:
            k.add(P, closed)
        cr, C = k._crossings()
        R = [np.concatenate([r, r[:1]]) if closed else r for (P, closed, r) in self.strands]
        pts, rr = zip(*[resample_r(Cc, Rc, 0.6) for Cc, Rc in zip(C, R)])
        allp, allr = np.vstack(pts), np.concatenate(rr)
        rmax = allr.max()
        yy, xx = np.mgrid[0:self.h, 0:self.w]
        pix = np.stack([xx.ravel() + 0.5, yy.ravel() + 0.5], 1)
        d, idx = cKDTree(allp).query(pix, distance_upper_bound=rmax + gap + 4)
        ok = np.isfinite(d)
        rpix = np.zeros_like(d); rpix[ok] = allr[idx[ok]]
        d = np.where(ok, d, 1e6).reshape(self.h, self.w); rpix = rpix.reshape(self.h, self.w)
        cov = lambda dd, r: np.clip(r - dd + 0.5, 0, 1)

        def layers(dd, rp):
            O = cov(dd, rp)
            lw = np.minimum(line, rp * 0.42)
            I = O - cov(dd, rp - lw)
            if groove:
                I = np.maximum(I, cov(dd, lw * 0.30) * (rp > line * 2.6))
            return O, I

        O, I = layers(d, rpix)
        for c in cr:
            ci, par = c["visits"][c["over"]]
            P, Rc = C[ci], R[ci]
            seg = np.hypot(*np.diff(P, axis=0).T)
            cum = np.concatenate([[0], np.cumsum(seg)])
            i = int(par); s0 = cum[i] + (par - i) * (seg[i] if i < len(seg) else 0)
            rloc = float(np.interp(s0, cum, Rc))
            half = 2 * rloc * piece + gap
            m = (cum >= s0 - half) & (cum <= s0 + half)
            if m.sum() < 2:
                continue
            pc, rc = resample_r(P[m], Rc[m], 0.6)
            x0, y0 = np.floor(pc.min(0) - rc.max() - gap - 3).astype(int)
            x1, y1 = np.ceil(pc.max(0) + rc.max() + gap + 3).astype(int)
            x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(self.w, x1), min(self.h, y1)
            if x1 <= x0 or y1 <= y0:
                continue
            wy, wx = np.mgrid[y0:y1, x0:x1]
            wp = np.stack([wx.ravel() + 0.5, wy.ravel() + 0.5], 1)
            dp, ip = cKDTree(pc).query(wp)
            dp = dp.reshape(y1 - y0, x1 - x0); rp = rc[ip].reshape(y1 - y0, x1 - x0)
            cpt = np.asarray(c["pt"])
            dc = np.hypot(wx + 0.5 - cpt[0], wy + 0.5 - cpt[1])
            # the other strand's width decides how far the cut has to reach
            ci2, par2 = c["visits"][1 - c["over"]]
            seg2 = np.hypot(*np.diff(C[ci2], axis=0).T); cum2 = np.concatenate([[0], np.cumsum(seg2)])
            i2 = int(par2); r2 = float(np.interp(cum2[min(i2, len(cum2) - 1)], cum2, R[ci2]))
            mcut = cov(dp, rp + gap) * cov(dc, max(rloc, r2) * 2.6 + gap)
            Op, Ip = layers(dp, rp)
            O[y0:y1, x0:x1] = O[y0:y1, x0:x1] * (1 - mcut) + Op * mcut
            I[y0:y1, x0:x1] = I[y0:y1, x0:x1] * (1 - mcut) + Ip * mcut
        rgba = np.zeros((self.h, self.w, 4), np.float32)
        white = O - I
        for k_ in range(3):
            rgba[..., k_] = (INK * I + 255 * white) / np.maximum(O, 1e-6)
        rgba[..., 3] = O * 255
        img = Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8))
        for f in self.overlays:
            img = f(img, line)
        return img

# ---------------------------------------------------------------- shapes
def rot(pts, ang, at=(0, 0), s=1.0):
    c, si = math.cos(ang), math.sin(ang)
    p = np.asarray(pts, float) * s
    return np.stack([at[0] + c * p[:, 0] - si * p[:, 1], at[1] + si * p[:, 0] + c * p[:, 1]], 1)

def circle(cx, cy, r, n=900):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.stack([cx + r * np.cos(t), cy + r * np.sin(t)], 1)

def lozenge(cx, cy, rx, ry, round_=2):
    p = np.array([(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)])
    return smooth(np.repeat(p, 1, 0), round_, closed=True)

def spiral(cx, cy, r0, turns, ang0=0.0, cw=True, n=400):
    t = np.linspace(0, turns * 2 * np.pi, n)
    r = r0 * (1 - t / (turns * 2 * np.pi)) ** 0.9 + r0 * 0.06
    a = ang0 + (t if cw else -t)
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)

# ---------------------------------------------------------------- overlays
def draw_poly(img, pts, line, fill=(255, 255, 255, 255), outline=True, SS=2):
    big = img.resize((img.width * SS, img.height * SS), Image.LANCZOS)
    d = ImageDraw.Draw(big)
    p = [tuple(q) for q in np.asarray(pts) * SS]
    if fill is not None:
        d.polygon(p, fill=fill)
    if outline:
        d.line(p + [p[0]], fill=(INK, INK, INK, 255), width=int(line * SS), joint="curve")
    return big.resize(img.size, Image.LANCZOS)

def draw_line(img, pts, width, SS=2):
    big = img.resize((img.width * SS, img.height * SS), Image.LANCZOS)
    d = ImageDraw.Draw(big)
    p = [tuple(q) for q in np.asarray(pts) * SS]
    d.line(p, fill=(INK, INK, INK, 255), width=int(width * SS), joint="curve")
    r = width * SS / 2
    for q in (p[0], p[-1]):
        d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=(INK, INK, INK, 255))
    return big.resize(img.size, Image.LANCZOS)

# Urnes head: profile, elongated, almond eye, upper and lower lip lappets. Points along +x from the neck (origin),
# unit = half the beast's ribbon width.
URNES_HEAD = [(0, -1.0), (1.4, -1.25), (2.8, -1.1), (4.2, -0.7), (5.6, -0.45), (6.6, -0.5),
              (7.4, -0.2), (6.8, 0.15), (5.4, 0.25), (4.0, 0.55), (2.6, 0.95), (1.2, 1.1), (0, 1.0)]
URNES_EYE = [(2.0, -0.2), (2.9, -0.62), (3.9, -0.42), (2.9, 0.02)]

def urnes_head(img, line, at, ang, s, upper_lappet, lower_lappet, tendril):
    head = rot(smooth(URNES_HEAD, 3, closed=True), ang, at, s)
    img = draw_poly(img, head, line)
    img = draw_poly(img, rot(smooth(URNES_EYE, 3, closed=True), ang, at, s), line, fill=(INK, INK, INK, 255), outline=False)
    for curve in (upper_lappet, lower_lappet, tendril):
        if curve is not None:
            img = draw_line(img, rot(curve, ang, at, s), line * 1.5)
    return img

# ---------------------------------------------------------------- motifs
def borre_ring_chain(w, units=4):
    """Borre ring-chain: circles and lozenges side by side, each a closed ribbon interlaced with its neighbours."""
    n = 2 * units + 1
    h = int(w * 0.92 / ((n - 1) * 0.64 + 0.9))
    rb = Ribbons(w, h)
    cy = h / 2
    R = h * 0.36                    # circle radius
    D = h * 0.44                    # lozenge half-diagonal
    s = (R + D) * 0.80              # centre spacing circle -> lozenge (overlap)
    total = (n - 1) * s
    x0 = (w - total) / 2
    band = h * 0.045
    for k in range(n):
        x = x0 + k * s
        if k % 2 == 0:
            rb.add(circle(x, cy, R), band, closed=True)
        else:
            rb.add(lozenge(x, cy, D, D), band, closed=True)
    return rb

def figure8(cx, cy, a, b, ang=0.0, t0=0.0, t1=2 * np.pi, n=1600):
    """Figure-of-eight (lemniscate of Gerono) with lobes along the rotated x axis."""
    t = np.linspace(t0, t1, n)
    pts = np.stack([a * np.sin(t), b * np.sin(t) * np.cos(t)], 1)
    return rot(pts, ang, (cx, cy))

def urnes_beast(size=3000):
    """Great beast in a figure-of-eight with a thin snake through it (two ribbon widths, open interlace)."""
    S = size / 1000
    rb = Ribbons(size, size)
    W1, W2 = 30 * S, 11 * S         # beast, snake half-widths
    # beast: neck at upper left, body runs down into a big figure-of-eight, tail ends in a tight scroll
    ctrl = np.array([(330, 260), (300, 360), (330, 470), (430, 560), (560, 600), (690, 640), (760, 740),
                     (720, 840), (600, 860), (520, 790), (530, 680), (600, 560), (690, 440), (720, 320),
                     (660, 210), (540, 170), (430, 220), (410, 320), (470, 380)]) * S
    P = smooth(ctrl, 5)
    tt = np.linspace(0, 1, len(P))
    r = W1 * (1 - 0.55 * np.clip((tt - 0.55) / 0.45, 0, 1))
    rb.add(P, r)
    tail = P[-1]; vt = P[-1] - P[-8]; at = math.atan2(vt[1], vt[0])
    sc = spiral(0, 0, 34 * S, 1.6, ang0=math.pi, cw=False)
    sc = rot(sc - sc[0], at + math.pi / 2, tail)
    rb.overlays.append(lambda img, line: draw_line(img, sc, W1 * 0.5 + 0 * line))
    # foreleg from the chest, hip spiral marks the joint, leg ends in a scrolled foot
    hip = P[int(len(P) * 0.16)]
    leg = smooth(np.array([hip, hip + (-120 * S, 40 * S), hip + (-170 * S, 140 * S), hip + (-120 * S, 220 * S)]), 4)
    rb.add(leg, W2 * 1.2)
    # snake: thin, threads through both loops, head at lower left biting toward the beast's neck
    ctrl2 = np.array([(180, 760), (300, 700), (450, 690), (600, 720), (780, 690), (850, 560), (760, 450),
                      (600, 420), (470, 470), (420, 600), (470, 740), (560, 860), (700, 900), (830, 860)]) * S
    Q = smooth(ctrl2, 5)
    rq = np.full(len(Q), W2); rq[-120:] = np.linspace(W2, W2 * 0.45, 120)
    rb.add(Q, rq)
    sq = Q[-1]; vq = Q[-1] - Q[-8]
    sc2 = rot(spiral(0, 0, 22 * S, 1.6, cw=True) - spiral(0, 0, 22 * S, 1.6, cw=True)[0], math.atan2(vq[1], vq[0]) - math.pi / 2, sq)
    rb.overlays.append(lambda img, line: draw_line(img, sc2, W2 * 0.7))
    # heads on top
    v = P[0] - P[10]; ang = math.atan2(v[1], v[0])
    up = smooth([(5.6, -0.45), (6.2, -1.6), (5.4, -2.6), (4.4, -2.4), (4.8, -1.9)], 3)
    lo = smooth([(5.0, 0.35), (5.4, 1.5), (4.6, 2.2), (3.8, 1.8)], 3)
    nt = smooth([(0.6, -1.1), (-0.6, -2.4), (-2.2, -2.6), (-2.8, -1.6), (-2.1, -1.2)], 3)
    rb.overlays.append(lambda img, line: urnes_head(img, line, P[0], ang, W1, up, lo, nt))
    vq0 = Q[0] - Q[10]; angq = math.atan2(vq0[1], vq0[0])
    rb.overlays.append(lambda img, line: urnes_head(img, line * 0.7, Q[0], angq, W2, None, None, None))
    return rb

if __name__ == "__main__":
    import sys, os
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    which = sys.argv[2:] or ["borre", "urnes"]
    if "borre" in which:
        borre_ring_chain(3000, 3).render(line=14, groove=True).save(os.path.join(out, "borre.png"))
    if "urnes" in which:
        urnes_beast(2000).render(line=11).save(os.path.join(out, "urnes.png"))
