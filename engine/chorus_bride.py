"""CHORUS CLIP — The Bride in Thunder (first test, 25 Nov 2026; Alfonso chose ideas 4 + 5).

Story in three lines over real storm footage, then the chorus with the lyrics lighting up word by word.
Story: Þrymskviða (Poetic Edda): the giant Þrymr steals Mjölnir and asks for Freyja as his bride; Thor goes to the
wedding dressed as the bride; the hammer is laid in the bride's lap to hallow the marriage and Thor takes it back.
Song fragment: audio/the-bride-in-thunder.mp3 = full song 0:08-1:23; word times from lyrics/the-bride-in-thunder.json.

Footage (Wikimedia Commons; downloaded 25 Nov 2026 to C:\\Nordic Reign\\stock\\, not in the public repo):
  - "Lightning storm over Colorado, USA" (CC0)
  - "Шторм на Черном море / Storm on the Black Sea" by Евгений (CC BY 3.0)
  - "Lightning strikes in slow motion (240fps) in Muurame, Finland" by MrNousia (CC BY 3.0)
Credit the two CC BY clips in the post text.

Usage: python3 chorus_bride.py <stock dir> <out.mp4> [stills]
"""
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw
import nr
from nr import Card, T, B, GOLD, LIGHT, MIST, W, H, FPS, window, ease

SONG = "the-bride-in-thunder"
FRAG_OFFSET = 8.0          # the repo fragment starts at 0:08 of the full song
T0 = 55.9                  # clip starts here (full-song seconds)
DUR = 23.0
CHORUS = 63.6 - T0         # 7.7 s

# background footage: (file, source start, source dur, speed, crop centre x 0-1, clip start)
SEGS = [
    ("lightning_colorado_CC0.ogg", 14.0, 10.4, 1.35, 0.64, 0.0),
    ("storm_black_sea_CCBY3.webm", 4.0, 8.6, 1.0, 0.16, 7.7 - 0.4),
    ("lightning_muurame_finland_CCBY3_MrNousia.webm", 0.9, 4.7, 1.0, 0.5, 15.45),   # big flash on "Thunder" (17.8 s)
]
BG_END = 20.6
XF = 0.4

def build_bg(stock, out):
    """One 1080x1920 background video from the three clips, crossfaded."""
    ins, parts = [], []
    for i, (f, ss, sd, sp, cx, _) in enumerate(SEGS):
        ins += ["-ss", str(ss), "-t", str(sd), "-i", os.path.join(stock, f)]
        parts.append(
            f"[{i}:v]setpts=PTS/{sp},fps={FPS},scale=-2:{H},"
            f"crop={W}:{H}:'min(max(iw*{cx}-{W}/2,0),iw-{W})':0,setsar=1,format=yuv420p[v{i}]")
    d0 = SEGS[0][2] / SEGS[0][3]
    d1 = SEGS[1][2] / SEGS[1][3]
    o1 = SEGS[1][5]
    o2 = SEGS[2][5] - o1
    fc = ";".join(parts) + (
        f";[v0][v1]xfade=transition=fade:duration={XF}:offset={o1}[a]"
        f";[a][v2]xfade=transition=fade:duration={XF}:offset={SEGS[2][5]}[v]")
    assert d0 >= o1 + XF and d1 >= o2 + XF, (d0, d1)
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error"] + ins + ["-filter_complex", fc, "-map", "[v]",
                    "-an", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", out], check=True)

class BG:
    """Reads the background video frame by frame (frames are asked for in order)."""
    def __init__(self, path):
        self.p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-f", "rawvideo",
                                   "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.i, self.last = -1, None
    def get(self, idx):
        while self.i < idx:
            buf = self.p.stdout.read(W * H * 3)
            if len(buf) < W * H * 3:
                return None if self.last is None else self.last
            self.last = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
            self.i += 1
        return self.last

def grade(a):
    """Half brand grade (shadow blue / candle gold) so the footage sits with the paintings."""
    f = a.astype(np.float32) / 255
    lum = (0.3 * f[..., 0] + 0.59 * f[..., 1] + 0.11 * f[..., 2])[..., None]
    lum = np.clip(lum, 0, 1) ** 1.05
    shadow = np.array([16, 22, 32], np.float32) / 255
    light = np.array([240, 214, 170], np.float32) / 255
    out = (shadow * (1 - lum) + light * lum) * 0.5 + f * 0.5
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)

# darker band in the middle so the text always reads
_y = np.arange(H)[:, None].astype(np.float32)
_band = np.exp(-((_y - 1000) / 430) ** 2) * 120
SHADE = np.zeros((H, W, 4), np.uint8); SHADE[..., 3] = np.repeat(_band, W, axis=1).astype(np.uint8)
SHADE = Image.fromarray(SHADE, "RGBA")

def fit(words, size=66, maxw=960):
    """One line if it fits, else two balanced lines."""
    d = ImageDraw.Draw(Image.new("RGBA", (W, H)))
    wd = lambda ws: nr.line_size(d, T(" ".join(ws), size, LIGHT))[0]
    if wd(words) <= maxw:
        return [T(" ".join(words), size, LIGHT)]
    i = min(range(1, len(words)), key=lambda i: max(wd(words[:i]), wd(words[i:])))
    return [T(" ".join(words[:i]), size, LIGHT), T(" ".join(words[i:]), size, LIGHT)]

def lyric_cards():
    d = json.load(open(f"lyrics/{SONG}.json"))
    rows = []
    for row in d["words"].replace("¶", "").split("\n"):
        ws = [(w.rsplit("@", 1)[0], float(w.rsplit("@", 1)[1]) - T0) for w in row.split() if "@" in w]
        if ws and CHORUS - 0.2 <= ws[0][1] <= DUR:
            rows.append(ws)
    cards = []
    for k, ws in enumerate(rows):
        a = ws[0][1] - 0.35
        b = rows[k + 1][0][1] - 0.15 if k + 1 < len(rows) else 21.4
        words = [w for w, _ in ws if w not in ("—", "-")]
        c = Card(a, b, 1180, fit(words))
        c.reveal = [t for w, t in ws if w not in ("—", "-")]
        cards.append(c)
    return cards

STORY = [
    Card(-1.0, 2.6, 900, [T("A giant stole", 84), T("Thor's hammer.", 84, GOLD), B("His price: Freyja as his bride.", 50, LIGHT)]),
    Card(2.8, 5.2, 930, [T("So Thor put on", 80), T("the bridal veil.", 80, GOLD)]),
    Card(5.4, CHORUS - 0.1, 930, [T("Then they laid the hammer", 70), T("in the bride's lap.", 70, GOLD)]),
]
OUTRO = [
    Card(21.0, DUR, 860, [T("The Bride in Thunder", 66, GOLD), B("Nordic Reign · Before the End Begins", 44, LIGHT),
                          B("Full song: link in bio", 40, MIST)]),
]
LABEL = nr.Label("NORDIC REIGN", "SONG STORY")

def make_frame(bg):
    cards = STORY + lyric_cards() + OUTRO
    def frame(img, t):
        a = bg.get(int(round(t * FPS)))
        vis = window(t, -1.0, BG_END, 0.6)
        if a is not None and vis > 0:
            lay = Image.fromarray(grade(a)).convert("RGBA")
            if vis < 1:
                lay = Image.blend(img, lay, vis)
            img.paste(lay)
            img.alpha_composite(SHADE)
        if t >= 2.0:
            LABEL.draw(img, t - 2.0, DUR - 2.0)
        for c in cards:
            c.draw(img, t)
    return frame

if __name__ == "__main__":
    stock, out = sys.argv[1], sys.argv[2]
    bgv = os.path.splitext(out)[0] + ".bg.mp4"
    if not os.path.exists(bgv):
        build_bg(stock, bgv)
    if len(sys.argv) > 3 and sys.argv[3] == "stills":
        for s in [0.0, 3.5, 6.5, 9.5, 14.0, 17.0, 18.5, 22.0]:
            bg = BG(bgv)
            nr.still(f"stills/chorus_{s}.png", s, make_frame(bg))
    else:
        nr.render(out, DUR, make_frame(BG(bgv)), seed=17, music=f"../audio/{SONG}.mp3", music_start=T0 - FRAG_OFFSET)
