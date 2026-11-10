"""Lyric video (16:9) for "Odin's Sacrifice" by Nordic Reign.

Full song, so the MP4 is NOT committed to the public repo (only this script).
Usage: python3 lyric_odins_sacrifice.py <song.wav> <out.mp4> [stills]
Word timings come from Suno's aligned lyrics for the released master.
"""
import sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw
import nr

nr.W, nr.H = 1920, 1080
W, H = nr.W, nr.H
FPS = 24
DUR = 197.36
GOLD, LIGHT, MIST = nr.GOLD, nr.LIGHT, nr.MIST
T, B = nr.T, nr.B

# --- word timings (start) per sung line, from Suno aligned_lyrics -------------
WORDS = """I@19.81 gave@20.16 my@20.55 sight —@20.81 no@21.96 fear,@22.22 no@23.21 fall¶
Blood@36.37 on@36.63 stone,@36.84 I@37.59 hear@37.67 the@37.98 call@38.29¶
Wisdom@38.96 comes@39.52 when@39.97 gods@40.32 must@40.67 fall@40.99¶
One@41.59 eye@41.86 gone@42.14 but@42.63 now@42.90 I@43.22 see@43.43¶
The@43.93 truth@44.13 was@44.67 never@44.95 meant@45.54 to@46.17 be@46.43 free@47.17¶
I@56.45 gave@56.54 my@56.92 sight —@57.21 no@58.28 fear,@58.53 no@59.54 fall@60.03¶
Through@61.64 the@62.08 dark@62.52 I@63.57 conquer@63.74 all@65.23¶
No@67.01 more@67.25 doubt,@67.50 no@69.09 more@69.43 disguise@70.15¶
Power@72.18 lives@72.79 where@73.69 sacrifice@74.07 lies@75.94¶
Ravens@88.33 fly@88.92 across@89.50 the@89.88 sky@90.24¶
They@90.79 bring@90.95 the@91.23 fate@91.45 I@92.15 can't@92.16 deny@92.82¶
Through@93.41 the@93.75 pain@94.03 I@94.67 claim@94.73 my@95.06 throne@95.23¶
A@96.06 god@96.17 is@96.53 never@96.79 truly@97.54 alone@99.02¶
I@108.39 gave@108.46 my@108.79 sight —@109.05 no@110.21 fear,@110.45 no@111.45 fall@111.94¶
Through@113.61 the@114.00 dark@114.44 I@115.49 conquer@115.66 all@117.28¶
No@118.94 more@119.19 doubt,@119.60 no@121.02 more@121.36 disguise@122.12¶
Power@124.07 lives@124.77 where@125.62 sacrifice@125.99 lies@127.72¶
I@149.93 gave@150.02 my@150.39 sight —@150.67 no@151.75 fear,@151.99 no@153.05 fall@153.54¶
Through@155.16 the@155.53 dark@155.97 I@157.07 conquer@157.25 all@158.79¶
No@160.46 more@160.70 doubt,@161.09 no@162.56 more@162.90 disguise@163.77¶
Power@165.69 lives@166.29 where@167.19 sacrifice@167.65 lies@169.02¶
I@170.71 gave@170.78 my@171.14 sight —@171.46 no@172.52 fear,@172.81 no@173.78 fall@174.29¶
Through@175.91 the@176.32 dark@176.76 I@177.81 conquer@177.99 all@179.52¶
No@181.25 more@181.49 doubt,@181.92 no@183.33 more@183.67 disguise@184.44¶
Power@186.42 lives@187.08 where@187.92 sacrifice@188.32 lies@189.83"""
RAW = [[(w.rsplit("@", 1)[0], float(w.rsplit("@", 1)[1])) for w in line.split(" ") if "@" in w]
       for line in WORDS.replace("¶", "").split("\n")]
# first line: the word "fall" starts at 23.83
RAW[0].append(("fall", 23.83)) if RAW[0][-1][0] != "fall" else None
LINES = []
for i, words in enumerate(RAW):
    starts = [s for _, s in words]
    ends = [min(starts[k + 1] - 0.05, starts[k] + 0.9) if k + 1 < len(starts) else starts[k] + 0.9
            for k in range(len(starts))]
    LINES.append(dict(words=[w for w, _ in words], starts=starts, ends=ends))
for i, L in enumerate(LINES):
    nxt = LINES[i + 1]["starts"][0] if i + 1 < len(LINES) else 999
    L["a"] = L["starts"][0] - 0.7
    L["b"] = min(nxt - 0.35, L["ends"][-1] + 3.0, 190.6)  # clear before the outro card (191 s)

# --- art --------------------------------------------------------------------
IMG = "../images/"
TREE = nr.Painting(IMG + "bagge_yggdrasil_1847.jpg", 1500, 1080, cx=W / 2, cy=H / 2, focus=(0.5, 0.35),
                   zoom=0.12, feather=0.14)
ODIN = nr.Painting(IMG + "rosen_odin_wanderer_1886.jpg", 1500, 1080, cx=W / 2, cy=H / 2, focus=(0.5, 0.3),
                   zoom=0.12, feather=0.14)
SHADE = Image.new("RGBA", (W, H), (10, 12, 16, 120))

def art(img, t):
    # (painting, start, end) with crossfades; slow push over each block
    blocks = [(ODIN, -1, 34.5), (TREE, 33.5, 55.5), (ODIN, 54.5, 87.5), (TREE, 86.5, 128.5), (TREE, 127.5, 149.0), (ODIN, 148.0, 199)]
    for P, a, b in blocks:
        op = nr.window(t, a, b, 1.6)
        if op > 0:
            P.draw(img, t, a, op * 0.85, dur=b - a)
    img.alpha_composite(SHADE)

# --- solo (129-149 s): the source, Völuspá 28 ------------------------------------
def runes(img, t):
    op = nr.window(t, 129.5, 148.5, 1.0)
    if op <= 0:
        return
    nr.draw_lines(img, [T("MÍMIR'S WELL", 44, GOLD)], 300, op)
    nr.draw_lines(img, [B("“I know where Othin's eye is hidden,", 52, LIGHT),
                        B("deep in the wide-famed well of Mimir;", 52, LIGHT),
                        B("mead from the pledge of Othin each morn", 52, LIGHT),
                        B("does Mimir drink: would you know yet more?”", 52, LIGHT),
                        B("Völuspá 28 · trans. H. A. Bellows (1923)", 30)], 400, op, gap=16)

# --- lyrics: karaoke line with gold fill as each word is sung -----------------
def lyric(img, t):
    for i, L in enumerate(LINES):
        op = nr.window(t, L["a"], L["b"], 0.35)
        if op <= 0:
            continue
        rise = (1 - nr.ease((t - L["a"]) / 0.5)) * 18
        segs = []
        for w, s, e in zip(L["words"], L["starts"], L["ends"]):
            k = nr.ease((t - s) / max(0.15, e - s))
            col = tuple(int(LIGHT[c] * (1 - k) + GOLD[c] * k) for c in range(3))
            segs.append((w + " ", "title", 66, col))
        nr.draw_lines(img, [segs], 470 + rise, op)
        # next line, dimmed, as a preview
        if i + 1 < len(LINES) and LINES[i + 1]["a"] - L["b"] < 1.0:
            nxt = " ".join(LINES[i + 1]["words"])
            nr.draw_lines(img, [B(nxt, 40, MIST)], 590 + rise, op * 0.55)

# --- intro / outro cards -------------------------------------------------------
CARDS = [
    nr.Card(0.6, 9.0, 360, [T("NORDIC REIGN", 40, GOLD), T("ODIN'S SACRIFICE", 104, LIGHT)], gap=26),
    nr.Card(9.8, 18.8, 380, [T("THE NORSE SAGA", 40, GOLD),
                             B("Odin gave one eye for a single drink", 50, LIGHT),
                             B("from Mímir's well of wisdom.", 50, LIGHT),
                             B("This is his song.", 50, LIGHT)], gap=20),
    nr.Card(24.8, 35.0, 400, [B("His ravens, Huginn and Muninn, “thought” and “memory”,", 44, LIGHT),
                              B("fly over the world each day and bring him the news.", 44, LIGHT),
                              B("Grímnismál 20; Prose Edda, Gylfaginning 38", 30)], gap=16),
    nr.Card(191.0, 198, 330, [T("ODIN'S SACRIFICE", 76, LIGHT), B("Nordic Reign · from the album Before the End Begins", 38),
                              B("Listen on all platforms: link in the description", 40, LIGHT),
                              B("The full story: The Norse Saga, episode 7 · @nordicreignofficial", 36, GOLD)], gap=24),
]

def frame(img, t):
    art(img, t)
    runes(img, t)
    lyric(img, t)
    for c in CARDS:
        c.draw(img, t)
    nr.draw_lines(img, [B("Art: O. O. Bagge, Yggdrasil (1847) · Georg von Rosen, Odin the Wanderer (1886)", 22)],
                  1040, 0.75)

def render(song, out):
    bg = nr.Background(5)
    n = int(round(DUR * FPS))
    tmp_v = out + ".v.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                          "-pix_fmt", "yuv420p", tmp_v], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        img = bg.render(t)
        frame(img, t)
        k = min(nr.ease(t / 0.8), nr.ease((DUR - t) / 1.2))
        if k < 1:
            img = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), img, k)
        p.stdin.write(img.convert("RGB").tobytes())
        if i % 480 == 0:
            print(f"{t:.0f}s", flush=True)
    p.stdin.close(); p.wait()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp_v, "-i", song, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True)

if __name__ == "__main__":
    song, out = sys.argv[1], sys.argv[2]
    if len(sys.argv) > 3 and sys.argv[3] == "stills":
        bg = nr.Background(5)
        for t in (5, 14, 30, 22, 40, 58, 92, 135, 175, 194):
            img = bg.render(t); frame(img, t)
            img.convert("RGB").save(f"{out}_{int(t):03d}.jpg", quality=85)
    else:
        render(song, out)
