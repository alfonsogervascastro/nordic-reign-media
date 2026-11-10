"""Lyric video (16:9) for "Nine Days Below" by Nordic Reign.

Full song, so the MP4 is NOT committed to the public repo (only this script).
Usage: python3 lyric_nine_days_below.py <song.wav> <out.mp4> [stills]
Word timings come from Suno's aligned lyrics for the released master.
"""
import sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw
import nr

nr.W, nr.H = 1920, 1080
W, H = nr.W, nr.H
FPS = 24
DUR = 190.7
GOLD, LIGHT, MIST = nr.GOLD, nr.LIGHT, nr.MIST
T, B = nr.T, nr.B

# --- word timings (start, end) per sung line -------------------------------
RAW = [
    [("Nine", 36.16), ("days", 36.58), ("hanging", 36.95), ("from", 37.67), ("the", 38.02), ("tree", 38.25)],
    [("No", 38.97), ("food,", 39.15), ("no", 39.70), ("drink —", 39.90), ("no", 40.50), ("air", 40.71), ("to", 41.08), ("breathe", 41.38)],
    [("Cold", 48.24), ("wind", 48.60), ("cutting", 48.96), ("through", 49.63), ("my", 50.04), ("skin", 50.22)],
    [("Still", 51.13), ("I", 51.64), ("hold,", 51.79), ("I", 52.60), ("won't", 52.63), ("give", 53.03), ("in", 53.75)],
    [("Spear", 60.06), ("runs", 60.58), ("deep,", 60.95), ("I", 61.56), ("feel", 61.67), ("the", 62.07), ("pain", 62.31)],
    [("Still", 63.14), ("I", 63.64), ("rise", 63.82), ("again,", 64.68), ("again", 66.35)],
    [("I", 78.03), ("chose", 78.12), ("this", 78.59), ("path,", 78.98), ("I", 79.56), ("take", 79.66), ("the", 80.02), ("fall", 80.25)],
    [("No", 81.08), ("god", 81.25), ("forced", 81.51), ("me —", 82.07), ("I", 82.63), ("gave", 82.71), ("it", 83.09), ("all", 83.42)],
    [("Every", 84.34), ("second", 84.88), ("drags", 85.58), ("me", 86.07), ("down", 86.32)],
    [("Still", 86.83), ("I", 87.48), ("refuse", 87.61), ("to", 88.40), ("hit", 88.71), ("the", 89.03), ("ground", 89.33)],
    [("Through", 96.18), ("the", 96.56), ("dark", 96.82), ("I", 97.51), ("start", 97.60), ("to", 98.03), ("see", 98.30)],
    [("Something", 99.21), ("calling", 99.91), ("out", 100.71), ("to", 101.03), ("me", 101.50)],
    [("Now", 102.30), ("I", 102.83), ("know", 102.94), ("what", 103.33), ("I", 103.85), ("must", 103.93), ("take", 104.31)],
    [("Power", 105.40), ("born", 105.83), ("from", 106.29), ("what", 106.62), ("I", 106.97), ("break", 107.06)],
]
# the second chorus (162 s) repeats lines 7-10 sung 84.02 s later
RAW += [[(w, s + 84.02) for w, s in RAW[i]] for i in (6, 7, 8, 9)]

LINES = []
for i, words in enumerate(RAW):
    starts = [s for _, s in words]
    ends = [min(starts[k + 1] - 0.05, starts[k] + 0.9) if k + 1 < len(starts) else starts[k] + 0.9
            for k in range(len(starts))]
    LINES.append(dict(words=[w for w, _ in words], starts=starts, ends=ends))
for i, L in enumerate(LINES):
    nxt = LINES[i + 1]["starts"][0] if i + 1 < len(LINES) else 999
    L["a"] = L["starts"][0] - 0.7
    L["b"] = min(nxt - 0.35, L["ends"][-1] + 3.0)

# --- art --------------------------------------------------------------------
IMG = "../images/"
TREE = nr.Painting(IMG + "bagge_yggdrasil_1847.jpg", 1500, 1080, cx=W / 2, cy=H / 2, focus=(0.5, 0.35),
                   zoom=0.12, feather=0.14)
ODIN = nr.Painting(IMG + "rosen_odin_wanderer_1886.jpg", 1500, 1080, cx=W / 2, cy=H / 2, focus=(0.5, 0.3),
                   zoom=0.12, feather=0.14)
SHADE = Image.new("RGBA", (W, H), (10, 12, 16, 120))

def art(img, t):
    # (painting, start, end) with crossfades; slow push over each block
    blocks = [(TREE, -1, 60.5), (ODIN, 59.5, 108.5), (TREE, 107.5, 161.0), (ODIN, 160.0, 192)]
    for P, a, b in blocks:
        op = nr.window(t, a, b, 1.6)
        if op > 0:
            P.draw(img, t, a, op * 0.85, dur=b - a)
    img.alpha_composite(SHADE)

# --- runes: the 24 of the Elder Futhark carved during the solo ----------------
FUTHARK = ["fehu", "uruz", "thurisaz", "ansuz", "raidho", "kaunan", "gebo", "wunjo",
           "hagalaz", "naudiz", "isa", "jera", "eihwaz", "perthro", "algiz", "sowilo",
           "tiwaz", "berkano", "ehwaz", "mannaz", "laguz", "ingwaz", "othala", "dagaz"]
nr.RUNES.setdefault("algiz", [[(0.5, 0), (0.5, 1)], [(0.5, 0.45), (0.18, 0.05)], [(0.5, 0.45), (0.82, 0.05)]])
R0, RSTEP = 112.0, 1.9      # first rune at 112 s, one every 1.9 s -> last at ~155.7 s
def runes(img, t):
    op = nr.window(t, 109.5, 160.5, 1.0)
    if op <= 0:
        return
    nr.draw_lines(img, [T("HE TOOK UP THE RUNES", 44, GOLD)], 150, op)
    nr.draw_lines(img, [B("“I took up the runes, shrieking I took them, and forthwith back I fell.”", 34, LIGHT),
                        B("Hávamál 139 · trans. H. A. Bellows (1923)", 26)], 900, op, gap=10)
    cw, ch, gx, gy = 110, 150, 160, 70
    x0 = W / 2 - (8 * cw + 7 * gx) / 2 + 0
    for k, r in enumerate(FUTHARK):
        p = (t - (R0 + k * RSTEP)) / 1.2
        if p <= 0:
            continue
        row, col = divmod(k, 8)
        x = W / 2 - (8 * cw + 7 * 70) / 2 + col * (cw + 70)
        y = 290 + row * (ch + gy)
        nr.draw_rune(img, r, x, y, cw * 0.8, ch * 0.8, min(1, p) * op, width=9, glow=0.8 * op)

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
    nr.Card(0.6, 9.5, 360, [T("NORDIC REIGN", 40, GOLD), T("NINE DAYS BELOW", 104, LIGHT)], gap=26),
    nr.Card(10.5, 22.5, 330, [B("“I ween that I hung on the windy tree,", 50, LIGHT),
                              B("hung there for nights full nine;", 50, LIGHT),
                              B("with the spear I was wounded, and offered I was", 50, LIGHT),
                              B("to Othin, myself to myself.”", 50, LIGHT),
                              B("Hávamál 138 · trans. H. A. Bellows (1923)", 30)], gap=16),
    nr.Card(23.5, 34.8, 400, [T("THE NORSE SAGA", 40, GOLD),
                              B("Odin hung nine nights on Yggdrasil to win the runes.", 50, LIGHT),
                              B("This is his song.", 50, LIGHT)], gap=22),
    nr.Card(177.5, 191, 330, [T("NINE DAYS BELOW", 76, LIGHT), B("Nordic Reign · from the album Before the End Begins", 38),
                              B("Listen on all platforms: link in the description", 40, LIGHT),
                              B("The full story: The Norse Saga, episode 6 · @nordicreignofficial", 36, GOLD)], gap=24),
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
        for t in (5, 16, 29, 37.5, 51.5, 65, 98, 125, 158, 163, 182):
            img = bg.render(t); frame(img, t)
            img.convert("RGB").save(f"{out}_{int(t):03d}.jpg", quality=85)
    else:
        render(song, out)
