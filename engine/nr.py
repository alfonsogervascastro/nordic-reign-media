"""Nordic Reign reel engine — shared look, runes, text cards, audio, rendering.

Palette v2 (from the existing cover art): storm charcoal background, steel slabs,
lightning text, mist secondary, rune gold as the single accent.
"""
import math, os, random, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
F_TITLE = os.path.join(HERE, "fonts/Cinzel.ttf")
F_BODY = os.path.join(HERE, "fonts/EBGaramond.ttf")
HANDLE = "@nordicreignofficial"

BG = np.array([14, 17, 22], np.float32)       # carbón tormenta #0E1116
BG2 = np.array([24, 28, 35], np.float32)
STEEL = (43, 48, 56)                            # acero #2B3038
LIGHT = (214, 226, 238)                         # relámpago #D6E2EE
MIST = (142, 153, 166)                          # niebla #8E99A6
GOLD = (224, 164, 74)                           # oro rúnico #E0A44A

SAFE_TOP, SAFE_BOTTOM = 230, 1520               # keep text clear of app UI

_font_cache = {}
def font(kind, size):
    key = (kind, size)
    if key not in _font_cache:
        path = F_TITLE if kind == "title" else F_BODY
        f = ImageFont.truetype(path, size)
        try:
            f.set_variation_by_axes([700 if kind == "title" else 500])
        except Exception:
            pass
        _font_cache[key] = f
    return _font_cache[key]

def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def window(t, a, b, fade=0.4):
    if t < a or t > b:
        return 0.0
    return ease((t - a) / fade) * ease((b - t) / fade)

# ---------------- background ----------------
class Background:
    def __init__(self, seed=3):
        rng = np.random.default_rng(seed)
        g = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
        self.base = (BG * (1 - g) + BG2 * g).repeat(W, axis=1)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        v = 1 - 0.5 * (((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.47) / (H * 0.7)) ** 2)
        self.vign = np.clip(v, 0.4, 1)[..., None]
        small = rng.random((48, 27)).astype(np.float32)
        fog = Image.fromarray((small * 255).astype(np.uint8)).resize((W, H * 2), Image.BICUBIC)
        self.fog = np.asarray(fog.filter(ImageFilter.GaussianBlur(44)), np.float32) / 255.0
        random.seed(seed)
        self.embers = [dict(x=random.uniform(0, W), y=random.uniform(0, H), v=random.uniform(35, 110),
                            r=random.uniform(1.5, 3.8), ph=random.uniform(0, 6.28)) for _ in range(60)]

    def render(self, t):
        off = int((t * 16) % H)
        f = self.fog[H - off: 2 * H - off] if off else self.fog[H:2 * H]
        rgb = (self.base + f[..., None] * np.array([30, 34, 42], np.float32) * 1.3) * self.vign
        img = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for e in self.embers:
            y = (e["y"] - e["v"] * t) % H
            x = e["x"] + 16 * math.sin(t * 0.8 + e["ph"])
            a = max(0, int(130 + 90 * math.sin(t * 3 + e["ph"])))
            r = e["r"]
            d.ellipse([x - r, y - r, x + r, y + r], fill=(240, 160, 80, a))
        img.alpha_composite(layer)
        return img

# ---------------- text ----------------
def _segments(line):
    """A line is (text, kind, size, color) or a list of such segments."""
    return line if isinstance(line, list) else [line]

def line_size(d, line):
    w = h = 0
    for text, kind, size, col in _segments(line):
        bb = d.textbbox((0, 0), text, font=font(kind, size))
        w += bb[2] - bb[0]
        h = max(h, size)
    return w, h

def draw_lines(img, lines, y, op, rise=0.0, gap=20):
    if op <= 0:
        return y
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cy = y + rise
    for line in lines:
        lw, lh = line_size(d, line)
        x = (W - lw) / 2
        for text, kind, size, col in _segments(line):
            f = font(kind, size)
            d.text((x + 2, cy + 3), text, font=f, fill=(0, 0, 0, int(170 * op)))
            d.text((x, cy), text, font=f, fill=tuple(col) + (int(255 * op),))
            bb = d.textbbox((0, 0), text, font=f)
            x += bb[2] - bb[0]
        cy += lh + gap
    img.alpha_composite(layer)
    return cy

class Card:
    def __init__(self, a, b, y, lines, gap=20):
        self.a, self.b, self.y, self.lines, self.gap = a, b, y, lines, gap
    def draw(self, img, t):
        op = window(t, self.a, self.b)
        if op > 0:
            rise = (1 - ease((t - self.a) / 0.55)) * 22
            draw_lines(img, self.lines, self.y, op, rise, self.gap)

class Label:
    """Fixed series label at the top: e.g. Label("THE NORSE SAGA", "EP. 1")."""
    def __init__(self, series, part="", y=196):
        self.series, self.part, self.y = series, part, y
    def draw(self, img, t, dur):
        op = window(t, 0.15, dur, 0.5)
        if op <= 0:
            return
        line = [("title", self.series, GOLD)]
        if self.part:
            line.append(("title", "  ·  " + self.part, LIGHT))
        segs = [(txt, kind, 34, col) for kind, txt, col in line]
        y2 = draw_lines(img, [segs], self.y, op)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        d.line([(W / 2 - 40, self.y + 58), (W / 2 + 40, self.y + 58)], fill=GOLD + (int(170 * op),), width=2)
        img.alpha_composite(lay)

class Painting:
    """A public-domain painting graded to the brand palette, with feathered edges
    and a slow Ken Burns push. Use: P = Painting(path, 960, 1100); P.draw(img, t, t0, op)."""
    def __init__(self, path, w, h, cx=W / 2, cy=980, focus=(0.5, 0.4), zoom=0.10, feather=0.16, crop=None):
        src = Image.open(path).convert("RGB")
        if crop:
            src = src.crop(crop)
        sw, sh = src.size
        tw, th = int(w * (1 + zoom)), int(h * (1 + zoom))
        s = max(tw / sw, th / sh)
        src = src.resize((int(sw * s) + 1, int(sh * s) + 1), Image.LANCZOS)
        fx = int((src.width - tw) * focus[0]); fy = int((src.height - th) * focus[1])
        src = src.crop((fx, fy, fx + tw, fy + th))
        a = np.asarray(src, np.float32) / 255.0
        lum = (0.3 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2])[..., None]
        lum = np.clip((lum - 0.06) / 0.88, 0, 1) ** 1.1
        shadow = np.array([16, 22, 32], np.float32) / 255
        light = np.array([232, 206, 160], np.float32) / 255
        duo = shadow * (1 - lum) + light * lum
        graded = duo * 0.72 + a * 0.28
        yy, xx = np.mgrid[0:th, 0:tw].astype(np.float32)
        ex = np.minimum(xx, tw - 1 - xx) / (tw * feather)
        ey = np.minimum(yy, th - 1 - yy) / (th * feather)
        mask = np.clip(np.minimum(ex, ey), 0, 1) ** 1.5
        rgba = np.dstack([graded * 255, mask * 255])
        self.img = Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8))
        self.w, self.h, self.cx, self.cy, self.zoom = w, h, cx, cy, zoom
    def draw(self, img, t, t0, op, dur=4.5):
        if op <= 0:
            return
        k = ease((t - t0) / dur)
        z = 1 + self.zoom * (1 - k)          # starts wide, pushes in
        cw, ch = int(self.img.width / z), int(self.img.height / z)
        x0 = (self.img.width - cw) // 2; y0 = (self.img.height - ch) // 2
        frame = self.img.crop((x0, y0, x0 + cw, y0 + ch)).resize((self.w, self.h), Image.BILINEAR)
        if op < 1:
            a = np.asarray(frame, np.float32).copy(); a[..., 3] *= op
            frame = Image.fromarray(a.astype(np.uint8))
        img.alpha_composite(frame, (int(self.cx - self.w / 2), int(self.cy - self.h / 2)))

class TattooEnd:
    """Closing card for saga episodes: the episode's knotwork tattoo in gold, ~3 s.
    Use: END = TattooEnd("../tattoos/out/ep02_ymir/ep02_ymir_gold.png", t0=DUR - 3.2)
         in frame(): END.draw(img, t)   (draw it last, it dims everything behind it)"""
    def __init__(self, gold_png, t0, size=820, cy=880):
        im = Image.open(gold_png).convert("RGB")
        a = np.asarray(im, np.float32)
        bg = np.array([14, 17, 22], np.float32)
        alpha = np.clip(np.abs(a - bg).max(axis=2) / 60.0, 0, 1)   # charcoal background -> transparent
        rgba = np.dstack([a, alpha * 255]).astype(np.uint8)
        self.img = Image.fromarray(rgba)
        self.img.thumbnail((size, size), Image.LANCZOS)
        self.t0, self.cy = t0, cy
    def draw(self, img, t):
        if t < self.t0:
            return
        k = ease((t - self.t0) / 0.6)
        img.alpha_composite(Image.new("RGBA", img.size, (14, 17, 22, int(215 * k))))
        z = 0.92 + 0.08 * ease((t - self.t0) / 2.5)
        im = self.img.resize((int(self.img.width * z), int(self.img.height * z)), Image.LANCZOS)
        if k < 1:
            arr = np.asarray(im, np.float32).copy(); arr[..., 3] *= k
            im = Image.fromarray(arr.astype(np.uint8))
        img.alpha_composite(im, (int(W / 2 - im.width / 2), int(self.cy - im.height / 2)))
        draw_lines(img, [T("THIS CHAPTER, AS A TATTOO", 40, GOLD)], 300, k)
        draw_lines(img, [B("Save it for your next tattoo", 46, LIGHT), B(HANDLE, 38)], 1360, k)

# shorthand line builders
def T(text, size=64, col=LIGHT): return (text, "title", size, col)
def B(text, size=50, col=MIST): return (text, "body", size, col)

# ---------------- runes ----------------
RUNES = {
    "fehu": [[(0.3, 0), (0.3, 1)], [(0.3, 0.35), (0.75, 0.05)], [(0.3, 0.6), (0.75, 0.3)]],
    "uruz": [[(0.25, 1), (0.25, 0), (0.75, 0.3), (0.75, 1)]],
    "thurisaz": [[(0.3, 0), (0.3, 1)], [(0.3, 0.25), (0.72, 0.5), (0.3, 0.75)]],
    "ansuz": [[(0.3, 0), (0.3, 1)], [(0.3, 0.05), (0.75, 0.35)], [(0.3, 0.35), (0.75, 0.65)]],
    "raidho": [[(0.28, 1), (0.28, 0), (0.72, 0.25), (0.28, 0.5), (0.72, 1)]],
    "kaunan": [[(0.68, 0.15), (0.3, 0.45), (0.68, 0.75)]],
    "gebo": [[(0.15, 0.1), (0.85, 0.9)], [(0.85, 0.1), (0.15, 0.9)]],
    "wunjo": [[(0.3, 1), (0.3, 0), (0.72, 0.25), (0.3, 0.5)]],
    "hagalaz": [[(0.25, 0), (0.25, 1)], [(0.75, 0), (0.75, 1)], [(0.25, 0.35), (0.75, 0.65)]],
    "naudiz": [[(0.5, 0), (0.5, 1)], [(0.25, 0.35), (0.75, 0.65)]],
    "isa": [[(0.5, 0), (0.5, 1)]],
    "jera": [[(0.45, 0.15), (0.2, 0.4), (0.45, 0.65)], [(0.55, 0.35), (0.8, 0.6), (0.55, 0.85)]],
    "perthro": [[(0.8, 0), (0.55, 0.2), (0.3, 0), (0.3, 1), (0.55, 0.8), (0.8, 1)]],
    "eihwaz": [[(0.5, 0), (0.5, 1)], [(0.5, 0), (0.75, 0.15)], [(0.5, 1), (0.25, 0.85)]],
    "sowilo": [[(0.7, 0), (0.3, 0.42), (0.7, 0.58), (0.3, 1)]],
    "tiwaz": [[(0.5, 0), (0.5, 1)], [(0.18, 0.3), (0.5, 0), (0.82, 0.3)]],
    "berkano": [[(0.3, 0), (0.3, 1)], [(0.3, 0), (0.72, 0.25), (0.3, 0.5), (0.72, 0.75), (0.3, 1)]],
    "ehwaz": [[(0.2, 1), (0.2, 0), (0.5, 0.3), (0.8, 0), (0.8, 1)]],
    "mannaz": [[(0.2, 1), (0.2, 0), (0.8, 0.5)], [(0.8, 1), (0.8, 0), (0.2, 0.5)]],
    "laguz": [[(0.35, 1), (0.35, 0), (0.75, 0.3)]],
    "ingwaz": [[(0.5, 0.2), (0.8, 0.5), (0.5, 0.8), (0.2, 0.5), (0.5, 0.2)]],
    "othala": [[(0.2, 1), (0.75, 0.45), (0.5, 0.2), (0.25, 0.45), (0.8, 1)]],
    "dagaz": [[(0.15, 0), (0.15, 1), (0.85, 0), (0.85, 1), (0.15, 0)]],
}
LETTER = {"a": "ansuz", "b": "berkano", "c": "kaunan", "d": "dagaz", "e": "ehwaz", "f": "fehu",
          "g": "gebo", "h": "hagalaz", "i": "isa", "j": "jera", "k": "kaunan", "l": "laguz",
          "m": "mannaz", "n": "naudiz", "o": "othala", "p": "perthro", "q": "kaunan", "r": "raidho",
          "s": "sowilo", "t": "tiwaz", "u": "uruz", "v": "wunjo", "w": "wunjo", "y": "jera", "z": "sowilo"}

def transliterate(name):
    name = name.lower()
    out, i = [], 0
    while i < len(name):
        two = name[i:i + 2]
        if two == "th":
            out.append(("TH", "thurisaz")); i += 2; continue
        if two == "ng":
            out.append(("NG", "ingwaz")); i += 2; continue
        c = name[i]
        if c == "x":
            out += [("X", "kaunan"), ("", "sowilo")]
        elif c in LETTER:
            out.append((c.upper(), LETTER[c]))
        i += 1
    return out

def _poly_len(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))

def draw_rune(img, rune, x, y, w, h, progress, width=None, glow=1.0, col=GOLD):
    """Draw rune strokes into box (x, y, w, h); progress 0..1 carves strokes in order."""
    if progress <= 0:
        return
    width = width or max(6, int(w * 0.1))
    pad = width * 3
    region = Image.new("RGBA", (int(w + 2 * pad), int(h + 2 * pad)), (0, 0, 0, 0))
    d = ImageDraw.Draw(region)
    strokes = [[(pad + px * w, pad + py * h) for px, py in s] for s in RUNES[rune]]
    total = sum(_poly_len(s) for s in strokes)
    remaining = progress * total
    r = width / 2
    for s in strokes:
        for i in range(len(s) - 1):
            if remaining <= 0:
                break
            a, b = s[i], s[i + 1]
            seg = math.dist(a, b)
            k = min(1.0, remaining / seg) if seg else 1.0
            e = (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
            d.line([a, e], fill=col + (255,), width=width)
            d.ellipse([a[0] - r, a[1] - r, a[0] + r, a[1] + r], fill=col + (255,))
            d.ellipse([e[0] - r, e[1] - r, e[0] + r, e[1] + r], fill=col + (255,))
            remaining -= seg
    if glow > 0:
        g = region.filter(ImageFilter.GaussianBlur(max(8, width)))
        ga = np.asarray(g, np.float32).copy()
        ga[..., 3] *= 1.5 * glow
        img.alpha_composite(Image.fromarray(np.clip(ga, 0, 255).astype(np.uint8)), (int(x - pad), int(y - pad)))
    core = np.asarray(region, np.float32).copy()
    core[..., :3] = core[..., :3] * 0.6 + np.array([255, 228, 185], np.float32) * 0.4
    img.alpha_composite(Image.fromarray(np.clip(core, 0, 255).astype(np.uint8)), (int(x - pad), int(y - pad)))

def draw_slab(img, x, y, w, h, op):
    if op <= 0:
        return
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(min(w, h) * 0.12),
                        fill=STEEL + (int(235 * op),), outline=(70, 77, 88, int(255 * op)), width=3)
    img.alpha_composite(layer)

def draw_rule(img, y, op, length=180):
    if op <= 0:
        return
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.line([(W / 2 - length / 2, y), (W / 2 + length / 2, y)], fill=GOLD + (int(200 * op),), width=3)
    img.alpha_composite(layer)

# ---------------- audio ----------------
def make_audio(path, dur, bpm=60, seed=1, drum_from=1.0):
    """Calm cinematic bed: warm low pad (Dm - Bb - F - C), soft frame drum, faint low wind.
    No hiss, no pure-sine hum."""
    from scipy.signal import butter, lfilter
    sr = 44100
    n = int(dur * sr)
    rng = np.random.default_rng(seed)
    t = np.arange(n) / sr

    def lowpass(x, hz, order=2):
        b, a = butter(order, hz / (sr / 2), "low")
        return lfilter(b, a, x)

    # pad: each chord voice = 3 slightly detuned soft saw-ish tones (few harmonics), low-passed
    chords = [(73.42, 110.0, 146.83, 174.61),   # Dm
              (58.27, 116.54, 146.83, 174.61),  # Bb
              (87.31, 130.81, 174.61, 220.0),   # F
              (65.41, 130.81, 164.81, 196.0)]   # C
    seg = 7.5
    pad = np.zeros(n, np.float64)
    for ci in range(int(dur // seg) + 2):
        notes = chords[ci % len(chords)]
        s0 = ci * seg - 1.5
        i0, i1 = max(0, int(s0 * sr)), min(n, int((s0 + seg + 3.0) * sr))
        if i0 >= i1:
            continue
        tt = t[i0:i1] - s0
        env = np.clip(tt / 2.5, 0, 1) * np.clip((seg + 3.0 - tt) / 2.5, 0, 1)
        v = np.zeros(i1 - i0)
        for k, f0 in enumerate(notes):
            amp = [0.5, 0.32, 0.22, 0.14][k]
            for det in (-0.25, 0.0, 0.25):
                ph = rng.uniform(0, 6.28)
                for h, ha in ((1, 1.0), (2, 0.35), (3, 0.15)):
                    v += amp * ha * np.sin(2 * np.pi * (f0 + det) * h * tt + ph)
        pad[i0:i1] += v * env
    pad = lowpass(pad, 900)
    pad /= (np.abs(pad).max() + 1e-6)

    # wind: low-passed noise, slow swells, very quiet
    wind = lowpass(rng.standard_normal(n), 400, 2)
    wind /= (np.abs(wind).max() + 1e-6)
    wind *= 0.5 + 0.5 * np.sin(2 * np.pi * 0.06 * t + 1.0)

    # soft frame drum on beats 1 and 3, no click
    drum = np.zeros(n)
    beat = 60.0 / bpm
    hl = int(1.2 * sr)
    ht = np.arange(hl) / sr
    freq = 52 + 18 * np.exp(-ht * 12)
    hit = np.sin(2 * np.pi * np.cumsum(freq) / sr) * np.exp(-ht * 4.0) * (1 - np.exp(-ht * 300))
    tb, k = drum_from, 0
    while tb < dur - 1.0:
        amp = (1.0, 0.0, 0.6, 0.0)[k % 4]
        if amp:
            i = int(tb * sr); e = min(n, i + hl)
            drum[i:e] += hit[: e - i] * amp
        tb += beat; k += 1

    mix = 0.55 * pad + 0.08 * wind + 0.45 * drum
    fade = np.ones(n)
    fi, fo = int(1.2 * sr), int(1.8 * sr)
    fade[:fi] = np.linspace(0, 1, fi)
    fade[-fo:] = np.linspace(1, 0, fo)
    mix = mix * fade
    mix = mix / (np.abs(mix).max() + 1e-6) * 0.8
    stereo = np.stack([mix, np.roll(mix, 300)], axis=1)
    pcm = (stereo * 32767).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())

# ---------------- render ----------------
def render(out, dur, draw_frame, seed=3, bpm=66, music=None, music_start=0.0):
    """draw_frame(img, t) draws on top of the background. Writes out (mp4) atomically.
    music: optional path to a licensed Nordic Reign track (e.g. ../audio/nine-days-below.mp3);
    a dur-long excerpt from music_start (seconds) is used instead of the generated soundscape."""
    bg = Background(seed)
    n = int(round(dur * FPS))
    base = os.path.splitext(out)[0]
    tmp_v = base + ".video.tmp.mp4"
    wav = base + ".wav"
    if music:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(music_start), "-t", str(dur), "-i", music,
                        "-af", f"afade=t=in:d=0.8,afade=t=out:st={dur - 1.5}:d=1.5", "-ar", "44100", "-ac", "2",
                        wav], check=True)
    else:
        make_audio(wav, dur, bpm=bpm, seed=seed)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "19", "-pix_fmt", "yuv420p", tmp_v], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        img = bg.render(t)
        draw_frame(img, t)
        k = ease((dur - t) / 0.4)  # no fade-in: the first frame must already show the hook
        if k < 1:
            img = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), img, k)
        p.stdin.write(img.convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError("video encode failed")
    tmp = base + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp_v, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", tmp],
                   check=True)
    os.replace(tmp, out)
    os.remove(tmp_v)

def still(path, t, draw_frame, seed=3):
    img = Background(seed).render(t)
    draw_frame(img, t)
    img.convert("RGB").save(path)
