"""SHORT: the second daily video for TikTok + YouTube Shorts (rebuilt 27 Nov 2026).

The first version cut 13-20 s out of the saga episodes (teaser.py). Alfonso rejected it: the image did not show what the
voice was saying (the eagle over the roots), and there was text on screen that the voice never finished reading.
So each short is now written and built on its own, with three rules:
  1. Every word on screen is spoken, and every spoken sentence is on screen (word-by-word captions).
  2. Every line has its own image, chosen to show what that line says.
  3. It ends on complete sentences, then "Full episode on the profile." (spoken too).
Credits (art, source) go in the post text, not on screen.

Scenes: (display, say, image, box, mode)
  display  text on screen; "|" splits it, the part after "|" is gold
  say      what the narrator says (phonetic spelling of Old Norse names), or None = display
  image    file name in images/ (no extension)
  box      x0, y0, x1, y1 in the pixels of images/<image>.jpg
  mode     "full" = fills the screen (box widened to 9:16); "fit" = the box framed over a blurred copy of itself
The first scene is the hook: full screen, big type, already moving on frame 0, and spoken.

Usage: python3 short.py <name> <out.mp4> [stills]
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import nr, narrate, hook
from nr import Card, T, B, GOLD, LIGHT, W, H, FPS, ease, window

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "images")
XF = 0.35                      # crossfade between shots
FW, FH, FCY = 1000, 1160, 1190  # framed image box
TEXT_Y = 300
END = ("Full episode on the profile.", None)

SHORTS = {
    # 30 Nov — Ep. 3 (Gylfaginning 16)
    "squirrel": dict(label="EP. 3", seed=23, bpm=60, music=None, scenes=[
        ("A squirrel carries insults|up the world tree.", None, "bagge_yggdrasil_1847", (850, 1300, 1250, 2050), "full"),
        ("At the top of Yggdrasil|sits an eagle.", "At the top of Igdrasil sits an eagle.", "bagge_yggdrasil_1847", (550, 0, 1550, 600), "fit"),
        ("At the roots,|a dragon gnaws.", None, "bagge_yggdrasil_1847", (650, 1880, 1500, 2350), "fit"),
        ("Between them runs a squirrel,|Ratatoskr,", "Between them runs a squirrel, Rata-tosker,", "bagge_yggdrasil_1847", (850, 1250, 1250, 2000), "full"),
        ("carrying their insults|up and down the trunk.", None, "bagge_yggdrasil_1847", (100, 0, 2050, 2400), "fit"),
    ], end=("bagge_yggdrasil_1847", (100, 0, 2050, 2400))),
    # 1 Dec — Ep. 7 (Gylfaginning 15; Völuspá 28)
    "eye": dict(label="EP. 7", seed=73, bpm=60, music=("../audio/odins-sacrifice.mp3", 0.0), scenes=[
        ("Odin gave an eye|for one drink.", None, "engels_odin_mimir_well_1903", (350, 1000, 950, 1750), "full"),
        ("Under one root of the world tree|lies Mímir's well.", "Under one root of the world tree lies Meemir's well.", "bagge_yggdrasil_1847", (650, 1880, 1500, 2350), "fit"),
        ("Wisdom itself|is hidden in its water.", None, "engels_odin_mimir_well_1903", (30, 1180, 760, 1620), "fit"),
        ("Its keeper, Mímir,|asked a price.", "Its keeper, Meemir, asked a price.", "engels_odin_mimir_well_1903", (150, 0, 700, 600), "fit"),
        ("Odin paid with his eye,|and drank.", None, "engels_odin_mimir_well_1903", (250, 1000, 1100, 1750), "fit"),
        ("The eye is still down there,|in the well.", None, "rosen_odin_wanderer_1886", (300, 450, 1300, 1350), "fit"),
    ], end=("engels_odin_mimir_well_1903", (250, 1000, 1100, 1750))),
    # 2 Dec — Ep. 6 (Hávamál 138-139)
    "hanged": dict(label="EP. 6", seed=61, bpm=60, music=("../audio/nine-days-below.mp3", 2.0), scenes=[
        ("Odin hanged himself.|On purpose.", None, "rosen_odin_wanderer_1886", (250, 450, 1350, 1500), "full"),
        ("Nine nights|on a windy tree,", None, "bagge_yggdrasil_1847", (550, 0, 1550, 600), "fit"),
        ("wounded with a spear,|given to Odin, himself to himself.", None, "rosen_odin_wanderer_1886", (0, 0, 1100, 1500), "fit"),
        ("No bread.|No drink.", None, "bagge_yggdrasil_1847", (850, 1300, 1250, 2000), "full"),
        ("He looked down,|and took up the runes, screaming.", None, "rosen_odin_wanderer_1886", (300, 450, 1300, 1350), "fit", "runes"),
        ("Then he fell.", None, "bagge_yggdrasil_1847", (100, 0, 2050, 2400), "fit"),
    ], end=("rosen_odin_wanderer_1886", (0, 0, 1637, 2400))),
    # 3 Dec — Ep. 7 (Gylfaginning 38; Grímnismál 20)
    "ravens": dict(label="EP. 7", seed=74, bpm=60, music=("../audio/odins-sacrifice.mp3", 40.0), scenes=[
        ("Odin's two spies|are ravens.", None, "froelich_odin_ravens_1895", (60, 0, 560, 890), "full"),
        ("Two ravens sit|on his shoulders.", None, "froelich_odin_ravens_1895", (420, 60, 1150, 620), "fit"),
        ("Huginn, “Thought”,|and Muninn, “Memory”.", "Hugin, thought. And Munin, memory.", "froelich_odin_ravens_1895", (100, 90, 700, 420), "fit"),
        ("At dawn he sends them|over the whole world.", None, "froelich_odin_ravens_1895", (0, 0, 1328, 1152), "fit"),
        ("By breakfast they are back,|telling him all they saw and heard.", None, "froelich_odin_ravens_1895", (300, 40, 1150, 700), "fit"),
        ("Odin fears for Thought,|but he fears more for Memory.", None, "rosen_odin_wanderer_1886", (300, 450, 1300, 1350), "fit"),
    ], end=("froelich_odin_ravens_1895", (0, 0, 1328, 1152))),
    # 4 Dec — Prologue (Gylfaginning 34)
    "gleipnir": dict(label="PROLOGUE", seed=11, bpm=66, music=None, scenes=[
        ("This chain is made of|six impossible things.", None, "bauer_tyr_fenrir_1911", (1150, 850, 1950, 2150), "full"),
        ("The gods bound the wolf Fenrir|with a ribbon called Gleipnir.", "The gods bound the wolf Fenrir with a ribbon called Gleipneer.", "bauer_tyr_fenrir_1911", (0, 1250, 2058, 2200), "fit"),
        ("Dwarves made it from|the sound of a cat's footsteps,", None, "bauer_tyr_fenrir_1911", (50, 1650, 1000, 2150), "fit"),
        ("a woman's beard,|the roots of a mountain,", None, "bauer_tyr_fenrir_1911", (300, 1300, 1300, 2000), "fit"),
        ("the sinews of a bear, the breath of a fish|and the spit of a bird.", None, "bauer_tyr_fenrir_1911", (780, 520, 1260, 920), "fit"),
        ("Týr put his hand in the wolf's mouth|as a pledge. He lost it.", "Teer put his hand in the wolf's mouth as a pledge. He lost it.", "bauer_tyr_fenrir_1911", (1250, 1350, 1800, 1850), "fit"),
    ], end=("bauer_tyr_fenrir_1911", (0, 1100, 2058, 2250))),
    # 5 Dec — Ep. 5 (Ynglinga saga 4)
    "mimir": dict(label="EP. 5", seed=43, bpm=60, music=None, scenes=[
        ("Odin kept a head|that still talks.", None, "rosen_odin_wanderer_1886", (250, 450, 1350, 1500), "full"),
        ("After the war, the gods sent wise Mímir|to the Vanir as a hostage.", "After the war, the gods sent wise Meemir to the Vahnir as a hostage.", "engels_odin_mimir_well_1903", (100, 0, 800, 760), "fit"),
        ("The Vanir felt cheated.|They cut off his head and sent it back.", "The Vahnir felt cheated. They cut off his head and sent it back.", "engels_odin_mimir_well_1903", (150, 40, 650, 560), "fit"),
        ("Odin smeared it with herbs|so it would not rot,", None, "rosen_odin_wanderer_1886", (0, 300, 700, 1300), "fit"),
        ("and sang spells over it|until it could speak.", None, "rosen_odin_wanderer_1886", (300, 450, 1300, 1350), "fit"),
        ("From then on, it told him|many secrets.", None, "engels_odin_mimir_well_1903", (100, 0, 1700, 1500), "fit"),
    ], end=("rosen_odin_wanderer_1886", (0, 0, 1637, 2400))),
    # 6 Dec — Ep. 9 (Gylfaginning 42)
    "sleipnir": dict(label="EP. 9", seed=97, bpm=60, music=("../audio/inside-the-lie.mp3", 0.0), scenes=[
        ("Odin's horse has eight legs.|Its mother was Loki.", None, "froelich_odin_ravens_1895", (150, 80, 750, 1146), "full"),
        ("A giant offered to build|a wall around Asgard.", "A giant offered to build a wall around Ahsgard.", "bagge_yggdrasil_1847", (150, 650, 2000, 1300), "fit"),
        ("His price: the goddess Freyja,|the sun and the moon.", "His price: the goddess Fraya, the sun and the moon.", "bagge_yggdrasil_1847", (600, 250, 1450, 750), "fit"),
        ("His stallion hauled the stones.|He was nearly done.", None, "froelich_odin_ravens_1895", (100, 150, 800, 800), "fit"),
        ("So Loki turned into a mare|and lured the stallion away.", None, "froelich_odin_ravens_1895", (230, 170, 620, 500), "fit"),
        ("The giant lost his bet,|and Thor killed him.", None, "winge_thor_giants_1872", (250, 0, 1050, 1000), "fit"),
        ("Later, Loki gave birth to a foal|with eight legs: Sleipnir.", "Later, Loki gave birth to a foal with eight legs: Slayp-neer.", "froelich_odin_ravens_1895", (50, 450, 1100, 1050), "fit"),
    ], end=("froelich_odin_ravens_1895", (0, 0, 1328, 1152))),
}

# ---------------- pictures ----------------
_cache = {}
def _src(name):
    if name not in _cache:
        _cache[name] = Image.open(os.path.join(IMG, name + ".jpg")).convert("RGB")
    return _cache[name]

def _grade(im):
    return Image.fromarray(hook.grade(np.asarray(im, np.float32) / 255.0))

def _cover(im, w, h):
    """Scale and centre-crop im to exactly w x h."""
    s = max(w / im.width, h / im.height)
    im = im.resize((max(w, int(im.width * s + 0.5)), max(h, int(im.height * s + 0.5))), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

def _box916(src, box):
    """Widen/heighten box to 9:16 around its centre, staying inside the picture."""
    x0, y0, x1, y1 = box
    cx, cy, w, h = (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
    if w / h > W / H:
        h = w * H / W
    else:
        w = h * W / H
    k = min(1.0, src.width / w, src.height / h)
    w, h = w * k, h * k
    cx = min(max(cx, w / 2), src.width - w / 2)
    cy = min(max(cy, h / 2), src.height - h / 2)
    return (int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2))

Z = 1.07   # slow push-in over each shot

class Shot:
    def __init__(self, image, box, mode):
        src = _src(image)
        self.mode = mode
        if mode == "full":
            self.big = _grade(_cover(src.crop(_box916(src, box)), int(W * Z), int(H * Z)))
        else:
            crop = src.crop(box)
            bg = _cover(crop, int(W * Z), int(H * Z)).filter(ImageFilter.GaussianBlur(40))
            bg = Image.eval(_grade(bg), lambda v: int(v * 0.42))
            s = min(FW / crop.width, FH / crop.height)
            fw, fh = int(crop.width * s), int(crop.height * s)
            fg = _grade(crop.resize((int(fw * Z), int(fh * Z)), Image.LANCZOS))
            yy, xx = np.mgrid[0:fg.height, 0:fg.width].astype(np.float32)
            e = np.minimum(np.minimum(xx, fg.width - 1 - xx) / (fg.width * 0.07),
                           np.minimum(yy, fg.height - 1 - yy) / (fg.height * 0.07))
            mask = Image.fromarray((np.clip(e, 0, 1) ** 1.5 * 255).astype(np.uint8))
            self.bg, self.fg, self.mask, self.fsize = bg, fg, mask, (fw, fh)

    def frame(self, k):
        """k = 0..1 progress through the shot."""
        z = 1 + (Z - 1) * k                                                       # pushes in
        if self.mode == "full":
            cw, ch = self.big.width / (Z / z), self.big.height / (Z / z)
            x, y = (self.big.width - cw) / 2, (self.big.height - ch) / 2
            return self.big.crop((int(x), int(y), int(x + cw), int(y + ch))).resize((W, H), Image.BILINEAR).convert("RGBA")
        bw, bh = self.bg.width / (Z / z), self.bg.height / (Z / z)
        x, y = (self.bg.width - bw) / 2, (self.bg.height - bh) / 2
        img = self.bg.crop((int(x), int(y), int(x + bw), int(y + bh))).resize((W, H), Image.BILINEAR).convert("RGBA")
        fw, fh = self.fsize
        cw, ch = self.fg.width / (Z / z), self.fg.height / (Z / z)
        x, y = (self.fg.width - cw) / 2, (self.fg.height - ch) / 2
        box = (int(x), int(y), int(x + cw), int(y + ch))
        fg = self.fg.crop(box).resize((fw, fh), Image.BILINEAR).convert("RGBA")
        fg.putalpha(self.mask.resize((fw, fh), Image.BILINEAR))
        img.alpha_composite(fg, (int(W / 2 - fw / 2), int(FCY - fh / 2)))
        return img

# dark band behind the text at the top
_ys = np.arange(H)[:, None].astype(np.float32)
def _band(peak, flat, fade):
    """Dark band behind the text: full strength down to y=flat, then fading out by y=fade."""
    a = np.zeros((H, W, 4), np.uint8)
    k = np.clip((fade - _ys) / (fade - flat), 0, 1) ** 1.3
    a[..., 3] = np.repeat(k * peak, W, axis=1).astype(np.uint8)
    return Image.fromarray(a, "RGBA")
BAND = _band(215, 380, 760)
HOOK_BAND = _band(235, 580, 980)   # line engravings are light: the hook needs a solid dark top

def runes_overlay(img, k):
    """The runes he took up: five staves carved one after another along the bottom of the picture."""
    names = ["fehu", "uruz", "thurisaz", "ansuz", "raidho"]
    for i, r in enumerate(names):
        nr.draw_rune(img, r, 150 + i * 165, 1560, 120, 190, (k * 1.6 - i * 0.12) * 1.4)

def wrap(text, col):
    """One line if it fits at 70-58 px; otherwise two balanced lines at 64 px."""
    d = ImageDraw.Draw(Image.new("RGBA", (W, H)))
    wd = lambda t, sz: nr.line_size(d, B(t, sz, col))[0]
    for size in (70, 66, 62, 58):
        if wd(text, size) <= 980:
            return [B(text, size, col)]
    ws = text.split()
    i = min(range(1, len(ws)), key=lambda i: max(wd(" ".join(ws[:i]), 64), wd(" ".join(ws[i:]), 64)))
    return [B(" ".join(ws[:i]), 64, col), B(" ".join(ws[i:]), 64, col)]

def lines_for(display):
    parts = display.split("|")
    return wrap(parts[0], LIGHT) + sum((wrap(p, GOLD) for p in parts[1:]), [])

def hook_lines(display):
    d = ImageDraw.Draw(Image.new("RGBA", (W, H)))
    parts = display.split("|")
    return hook.fit(parts[0], LIGHT, d) + sum((hook.fit(p, GOLD, d) for p in parts[1:]), [])

def build(name):
    cfg = SHORTS[name]
    scenes = [dict(display=s[0], say=s[1] or s[0].replace("|", " "), image=s[2], box=s[3], mode=s[4],
                   extra=s[5] if len(s) > 5 else None) for s in cfg["scenes"]]
    end_img, end_box = cfg["end"]
    scenes.append(dict(display=END[0], say=END[0], image=end_img, box=end_box, mode="fit", extra=None))
    # timeline = the narration itself (lead/tail kept short: a short has no room for pauses)
    lead, tail = 0.15, 0.30
    t, segs = 0.0, []
    for s in scenes:
        n = len(narrate.speak(s["say"])) / narrate.SR
        s["a"], s["b"] = t, t + lead + n + tail
        segs.append((s["a"], s["b"], s["say"]))
        t = s["b"]
    dur = t + 0.6
    for s in scenes:
        s["shot"] = Shot(s["image"], s["box"], s["mode"])
    cards = []
    for s in scenes[1:]:
        c = Card(s["a"] + 0.02, s["b"] + 0.25, TEXT_Y, lines_for(s["display"]), gap=12)
        if s is scenes[-1]:
            c = Card(s["a"] + 0.02, dur, TEXT_Y, [T("Full episode", 76, LIGHT), T("on the profile.", 76, GOLD)], gap=10)
        cards.append(c)
    hk = hook_lines(scenes[0]["display"])
    label = nr.Label("THE NORSE SAGA", cfg["label"])
    h_end = scenes[0]["b"]

    def frame(img, t):
        i = max(j for j, s in enumerate(scenes) if s["a"] <= t or j == 0)
        s = scenes[i]
        span = (s["b"] - s["a"]) if i < len(scenes) - 1 else (dur - s["a"])
        cur = s["shot"].frame(min(1.0, (t - s["a"]) / (span + XF)))
        if i > 0 and t < s["a"] + XF:
            p = scenes[i - 1]
            prev = p["shot"].frame(1.0)
            cur = Image.blend(prev, cur, ease((t - s["a"]) / XF))
        img.paste(cur)
        if i == 0:
            img.alpha_composite(HOOK_BAND)
            nr.draw_lines(img, hk, 250 - 18 * (1 - min(1.0, t / 0.12)), 1.0, gap=10)
        else:
            k = ease((t - s["a"]) / XF) if i == 1 else 1.0
            img.alpha_composite(Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 0)), BAND, k) if k < 1 else BAND)
            label.draw(img, t - h_end, dur - h_end)
            if s["extra"] == "runes":
                runes_overlay(img, (t - s["a"]) / (s["b"] - s["a"]))
        for c in cards:
            c.draw(img, t)
    return cfg, segs, dur, frame, cards

def render(name, out):
    cfg, segs, dur, frame, cards = build(name)
    new_dur, warp, track = narrate.plan(segs, dur, lead=0.15, tail=0.30)
    narrate.attach_captions(cards)
    silent = os.path.splitext(out)[0] + ".music.mp4"
    music, start = cfg["music"] or (None, 0.0)
    nr.render(silent, new_dur, lambda img, t: frame(img, warp(t)), seed=cfg["seed"], bpm=cfg["bpm"],
              music=music, music_start=start)
    narrate.mix_voice(silent, track, out)
    os.remove(silent)
    return new_dur

if __name__ == "__main__":
    name, out = sys.argv[1], sys.argv[2]
    if len(sys.argv) > 3 and sys.argv[3] == "stills":
        cfg, segs, dur, frame, cards = build(name)
        os.makedirs(out, exist_ok=True)
        for k, (a, b, _) in enumerate(segs):
            nr.still(os.path.join(out, f"{name}_{k}.png"), (a + b) / 2, frame, seed=cfg["seed"])
        print(round(dur, 2))
    else:
        print(out, round(render(name, out), 2))
