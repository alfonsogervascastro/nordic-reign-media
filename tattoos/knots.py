"""Nordic Reign — Viking knotwork engine.

Draws any set of curves as interlaced bands (alternating over/under at every
crossing), the way Norse knotwork (Borre, Mammen, Urnes) is built: each band is a
double contour with an open centre, and the under-strand is cut where it passes
beneath. Everything is rendered at 3x and downsampled for clean lines.

    from knots import Knot, torus_knot
    k = Knot(size=3000)
    k.add(torus_knot(2, 5, ...), closed=True)
    img = k.render(band=110, line=22)
"""
import math
import numpy as np
from PIL import Image, ImageDraw

SS = 3  # supersampling

# ---------------------------------------------------------------- curves
def torus_knot(p, q, cx, cy, r_mid, r_amp, n=2400, rot=0.0):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = r_mid + r_amp * np.cos(q * t)
    a = p * t + rot
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)

def circle(cx, cy, r, n=1600):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.stack([cx + r * np.cos(t), cy + r * np.sin(t)], 1)

def braid(x0, x1, yc, amp, period, strands=3, n=3000, phase=0.0):
    """Open plait between x0 and x1 (for armbands). Returns a list of curves."""
    xs = np.linspace(x0, x1, n)
    out = []
    for k in range(strands):
        ph = phase + 2 * np.pi * k / strands
        ys = yc + amp * np.sin(2 * np.pi * (xs - x0) / period + ph)
        out.append(np.stack([xs, ys], 1))
    return out

# ---------------------------------------------------------------- geometry
def _seg_intersections(P, Q):
    """All intersections between polyline segments of P and Q (vectorised in chunks).
    Returns list of (i, j, ti, tj, point)."""
    res = []
    a0, a1 = P[:-1], P[1:]
    b0, b1 = Q[:-1], Q[1:]
    da = a1 - a0
    db = b1 - b0
    # bounding-box prefilter on a coarse grid
    for i in range(0, len(a0), 256):
        A0, A1, DA = a0[i:i + 256], a1[i:i + 256], da[i:i + 256]
        ax0 = np.minimum(A0[:, 0], A1[:, 0])[:, None]; ax1 = np.maximum(A0[:, 0], A1[:, 0])[:, None]
        ay0 = np.minimum(A0[:, 1], A1[:, 1])[:, None]; ay1 = np.maximum(A0[:, 1], A1[:, 1])[:, None]
        bx0 = np.minimum(b0[:, 0], b1[:, 0])[None]; bx1 = np.maximum(b0[:, 0], b1[:, 0])[None]
        by0 = np.minimum(b0[:, 1], b1[:, 1])[None]; by1 = np.maximum(b0[:, 1], b1[:, 1])[None]
        cand = (ax0 <= bx1) & (bx0 <= ax1) & (ay0 <= by1) & (by0 <= ay1)
        ii, jj = np.nonzero(cand)
        if not len(ii):
            continue
        pa, ra = A0[ii], DA[ii]
        pb, rb = b0[jj], db[jj]
        den = ra[:, 0] * rb[:, 1] - ra[:, 1] * rb[:, 0]
        ok = np.abs(den) > 1e-9
        w = pb - pa
        t = np.where(ok, (w[:, 0] * rb[:, 1] - w[:, 1] * rb[:, 0]) / np.where(ok, den, 1), -1)
        u = np.where(ok, (w[:, 0] * ra[:, 1] - w[:, 1] * ra[:, 0]) / np.where(ok, den, 1), -1)
        hit = ok & (t >= 0) & (t < 1) & (u >= 0) & (u < 1)
        for k in np.nonzero(hit)[0]:
            res.append((i + ii[k], jj[k], t[k], u[k], pa[k] + t[k] * ra[k]))
    return res

class Knot:
    def __init__(self, size=3000, height=None):
        self.w = size
        self.h = height or size
        self.curves = []  # (points, closed)

    def add(self, pts, closed=True):
        self.curves.append((np.asarray(pts, float), closed))
        return self

    def _crossings(self, min_sep=40):
        """Find crossings and assign over/under alternately along each curve."""
        cr = []  # dict: point, visits=[(curve, param)]
        C = []
        for ci, (P, closed) in enumerate(self.curves):
            C.append(np.vstack([P, P[:1]]) if closed else P)
        for a in range(len(C)):
            for b in range(a, len(C)):
                for i, j, ti, tj, pt in _seg_intersections(C[a], C[b]):
                    if a == b and abs(i - j) <= 2 or (a == b and self.curves[a][1] and abs(i - j) >= len(C[a]) - 3):
                        continue
                    if a == b and j < i:
                        continue  # each self-crossing once
                    cr.append({"pt": pt, "visits": [(a, i + ti), (b, j + tj)], "over": None})
        # merge duplicates (very close points)
        merged = []
        for c in cr:
            if all(np.hypot(*(c["pt"] - m["pt"])) > 2 for m in merged):
                merged.append(c)
        cr = merged
        # alternate along each curve
        for ci in range(len(C)):
            visits = sorted([(par, k, vi) for k, c in enumerate(cr) for vi, (cc, par) in enumerate(c["visits"]) if cc == ci])
            state = None
            for par, k, vi in visits:
                c = cr[k]
                if c["over"] is not None:
                    state = (c["over"] == vi)
                    continue
                state = True if state is None else not state
                c["over"] = vi if state else 1 - vi
        return cr, C

    def render(self, band=100, line=20, gap=None, centre_line=False, piece=2.2):
        """Clean distance-field rendering. band: total width; line: contour width;
        gap: cut into the under-strand at crossings; piece: over-strand length / band."""
        from scipy.spatial import cKDTree
        gap = gap if gap is not None else line * 1.0
        R = band / 2.0
        cr, C = self._crossings()
        Cd = [_resample(P, 0.6) for P in C]
        allpts = np.vstack(Cd)
        yy, xx = np.mgrid[0:self.h, 0:self.w]
        pix = np.stack([xx.ravel() + 0.5, yy.ravel() + 0.5], 1)
        d = cKDTree(allpts).query(pix, distance_upper_bound=R + gap + 4)[0].reshape(self.h, self.w)
        d = np.where(np.isinf(d), 1e6, d)
        cov = lambda dd, r: np.clip(r - dd + 0.5, 0, 1)

        def layers(dd):
            O = cov(dd, R)
            I = O - cov(dd, R - line)
            if centre_line:
                I = np.maximum(I, cov(dd, line * 0.25))
            return O, I

        O, I = layers(d)
        half = int(band * piece)
        for c in cr:
            ci, par = c["visits"][c["over"]]
            P = C[ci]
            # arc-length window around the crossing on the over-strand
            seg = np.hypot(*np.diff(P, axis=0).T)
            cum = np.concatenate([[0], np.cumsum(seg)])
            i = int(par); s0 = cum[i] + (par - i) * (seg[i] if i < len(seg) else 0)
            m = (cum >= s0 - half) & (cum <= s0 + half)
            pc = _resample(P[m], 0.6)
            if len(pc) < 2:
                continue
            x0, y0 = np.floor(pc.min(0) - R - gap - 3).astype(int)
            x1, y1 = np.ceil(pc.max(0) + R + gap + 3).astype(int)
            x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(self.w, x1), min(self.h, y1)
            wy, wx = np.mgrid[y0:y1, x0:x1]
            wp = np.stack([wx.ravel() + 0.5, wy.ravel() + 0.5], 1)
            dp = cKDTree(pc).query(wp)[0].reshape(y1 - y0, x1 - x0)
            # fade the cut out towards the piece ends so it does not leave a hard edge
            cpt = np.asarray(c["pt"])
            dc = np.hypot(wx + 0.5 - cpt[0], wy + 0.5 - cpt[1])
            mcut = cov(dp, R + gap) * cov(dc, band * 1.15)
            Op, Ip = layers(dp)
            O[y0:y1, x0:x1] = O[y0:y1, x0:x1] * (1 - mcut) + Op * mcut
            I[y0:y1, x0:x1] = I[y0:y1, x0:x1] * (1 - mcut) + Ip * mcut
        self.O, self.I = O, I
        rgba = np.zeros((self.h, self.w, 4), np.float32)
        white = (O - I)
        for k in range(3):
            rgba[..., k] = (12 * I + 255 * white) / np.maximum(O, 1e-6)
        rgba[..., 3] = O * 255
        return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8))

def _resample(P, step):
    seg = np.hypot(*np.diff(P, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    n = max(2, int(cum[-1] / step))
    s = np.linspace(0, cum[-1], n)
    return np.stack([np.interp(s, cum, P[:, 0]), np.interp(s, cum, P[:, 1])], 1)

def on_paper(img, bg=(255, 255, 255)):
    out = Image.new("RGB", img.size, bg)
    out.paste(img, (0, 0), img)
    return out

def recolor(img, ink=(224, 164, 74), paper=(14, 17, 22)):
    """Brand preview: gold lines on storm-charcoal."""
    a = np.asarray(img.convert("RGBA"), np.float32)
    lum = (a[..., 0] + a[..., 1] + a[..., 2]) / 765.0
    alpha = a[..., 3] / 255.0
    inkness = (1 - lum) * alpha
    out = np.zeros(a.shape[:2] + (3,), np.float32)
    for k in range(3):
        out[..., k] = paper[k] * (1 - inkness) + ink[k] * inkness
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
