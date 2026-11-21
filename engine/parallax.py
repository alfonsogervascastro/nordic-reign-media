"""2.5D parallax for paintings (DepthFlow-style), as a drop-in replacement for nr.Painting.
A depth map (Depth Anything ViT-S, ONNX from github.com/fabio-sim/Depth-Anything-ONNX releases) splits the painting into
planes: near figures grow and drift more than the background, so the still painting reads as a slow camera move.
Turn it on for any script with NR_PARALLAX=1 (nr.py swaps Painting for ParallaxPainting); NR_PARALLAX=0.5 halves the effect."""
import os
import numpy as np
import cv2
import onnxruntime as ort
import nr

MODEL = "/home/claude/models/depth/depth_anything_vits14.onnx"
_sess = None
_cache = {}

def depth_map(rgb):
    """Relative depth in 0..1 (1 = nearest), same size as rgb (uint8 HxWx3)."""
    global _sess
    key = (rgb.shape, int(rgb[::37, ::41].sum()))
    if key in _cache:
        return _cache[key]
    if _sess is None:
        so = ort.SessionOptions(); so.intra_op_num_threads = 2
        _sess = ort.InferenceSession(MODEL, so)
    h, w = rgb.shape[:2]
    s = 518 / max(h, w)
    nh, nw = max(14, round(h * s / 14) * 14), max(14, round(w * s / 14) * 14)
    x = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_CUBIC).astype(np.float32) / 255
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    d = _sess.run(None, {"image": x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0, 0]
    d = cv2.resize(d, (w, h), interpolation=cv2.INTER_CUBIC)
    lo, hi = np.percentile(d, 2), np.percentile(d, 98)
    d = np.clip((d - lo) / max(hi - lo, 1e-6), 0, 1)
    d = cv2.GaussianBlur(d, (0, 0), max(h, w) / 120)        # soft edges -> less tearing
    _cache[key] = d.astype(np.float32)
    return _cache[key]

class ParallaxPainting(nr.Painting):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.rgba = np.asarray(self.img).astype(np.float32)
        self.depth = depth_map(self.rgba[..., :3].astype(np.uint8))
        h, w = self.depth.shape
        self.yy, self.xx = np.mgrid[0:h, 0:w].astype(np.float32)
        self.amp = float(os.environ.get("NR_PARALLAX", "1") or 1)

    def draw(self, img, t, t0, op, dur=4.5):
        if op <= 0:
            return
        k = nr.ease((t - t0) / dur)
        h, w = self.depth.shape
        cx, cy = w / 2, h / 2
        d = self.depth
        # base push-in (same as the 2D version) + extra zoom for near planes + slow sideways drift by depth
        z = 1 + self.zoom * k + self.amp * 0.045 * k * d
        drift = self.amp * 0.016 * w * (k - 0.5) * d
        lift = self.amp * 0.010 * h * (k - 0.5) * d
        mx = (cx + (self.xx - cx) / z - drift).astype(np.float32)
        my = (cy + (self.yy - cy) / z + lift).astype(np.float32)
        # keep the frame inside the painting (scale the whole thing by the base zoom headroom)
        s = 1 / (1 + self.zoom)
        mx = cx + (mx - cx) * s
        my = cy + (my - cy) * s
        out = cv2.remap(self.rgba, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        out[..., 3] = np.asarray(self.img)[..., 3]            # keep the feathered edge fixed to the frame
        frame = cv2.resize(out, (self.w, self.h), interpolation=cv2.INTER_AREA)
        if op < 1:
            frame[..., 3] *= op
        from PIL import Image
        img.alpha_composite(Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)),
                            (int(self.cx - self.w / 2), int(self.cy - self.h / 2)))
