"""Lyric video (16:9) for "Inside the Lie" by Nordic Reign.

Full song, so the MP4 is NOT committed to the public repo (only this script).
Usage: python3 lyric_inside_the_lie.py <song.wav> <out.mp4> [stills]
Word timings come from Suno's aligned lyrics for the released master.
"""
import sys, subprocess, math
import numpy as np
from PIL import Image, ImageDraw
import nr

nr.W, nr.H = 1920, 1080
W, H = nr.W, nr.H
FPS = 24
DUR = 155.0
GOLD, LIGHT, MIST = nr.GOLD, nr.LIGHT, nr.MIST
T, B = nr.T, nr.B

# --- word timings (start) per sung line, from Suno aligned_lyrics -------------
WORDS = """You@8.69 feel@8.94 it —@9.22 don't@9.44 you@9.72 lie@10.64¶
Something@20.48 crawling@20.90 in@21.47 your@21.67 veins@22.05¶
Whisper@22.96 softly@23.34 through@23.85 your@24.23 brain@24.64¶
Every@25.65 doubt@25.96 you@26.24 try@26.49 to@26.84 hide@27.16¶
I'm@28.17 the@28.30 voice@28.47 you@28.75 keep@29.03 inside@29.67¶
You@40.82 feel@41.06 it —@41.42 don't@41.63 you@41.94 run@42.40¶
Every@43.28 step@43.57 is@44.05 already@44.35 done@44.88¶
Turn@45.80 around,@46.12 there's@46.41 nothing@46.77 there@47.36¶
Still@48.22 you@48.49 feel@48.68 me@49.01 everywhere@49.33¶
Break@50.68 the@50.93 trust,@51.13 twist@51.92 the@52.22 pain@52.47¶
Nothing@53.14 ever@53.71 stays@54.29 the@54.70 same@54.91¶
Love@55.61 and@55.90 hate,@56.18 wrong@56.92 and@57.20 right@57.46¶
I@58.51 decide@58.60 what's@59.12 real@59.66 tonight@60.98¶
You@99.70 feel@99.87 it —@100.18 don't@100.39 you@100.70 lie@101.71¶
You@111.49 were@111.67 mine@111.86 before@112.28 you@112.67 tried@113.01¶
Every@114.05 fear@114.33 you@114.61 try@114.89 to@115.25 fight@115.51¶
I'm@116.55 the@116.67 shadow@116.85 in@117.46 your@117.68 mind@118.33¶
Break@131.51 the@131.76 trust,@131.98 twist@132.77 the@133.06 pain@133.31¶
Nothing@133.96 ever@134.57 stays@135.10 the@135.52 same@135.74¶
Love@136.49 and@136.78 hate,@137.06 wrong@137.75 and@138.05 right@138.29¶
I@139.39 decide@139.47 what's@139.93 real@140.54 tonight@141.84¶
You@150.23 feel@150.39 it —@150.68 don't@150.89 you@151.25 lie@151.71"""
RAW = [[(w.rsplit("@", 1)[0], float(w.rsplit("@", 1)[1])) for w in line.split(" ") if "@" in w]
       for line in WORDS.replace("¶", "").split("\n")]
# first line: the word "fall" starts at 23.83
LINES = []
for i, words in enumerate(RAW):
    starts = [s for _, s in words]
    ends = [min(starts[k + 1] - 0.05, starts[k] + 0.9) if k + 1 < len(starts) else starts[k] + 0.9
            for k in range(len(starts))]
    LINES.append(dict(words=[w for w, _ in words], starts=starts, ends=ends))
for i, L in enumerate(LINES):
    nxt = LINES[i + 1]["starts"][0] if i + 1 < len(LINES) else 999
    L["a"] = L["starts"][0] - 0.7
    L["b"] = min(nxt - 0.35, L["ends"][-1] + 3.0, 151.9)  # clear before the outro card

# --- art --------------------------------------------------------------------
IMG = "../images/"
TREE = nr.Painting(IMG + "bagge_yggdrasil_1847.jpg", 1500, 1080, cx=W / 2, cy=H / 2, focus=(0.5, 0.35),
                   zoom=0.12, feather=0.14)
WAR = nr.Painting(IMG + "froelich_aesir_vanir_war_1895.jpg", 1500, 1080, cx=W / 2, cy=H / 2, focus=(0.5, 0.4),
                  zoom=0.12, feather=0.14)
ODIN = nr.Painting(IMG + "rosen_odin_wanderer_1886.jpg", 1500, 1080, cx=W / 2, cy=H / 2, focus=(0.5, 0.3),
                   zoom=0.12, feather=0.14)
SHADE = Image.new("RGBA", (W, H), (10, 12, 16, 120))

def art(img, t):
    # (painting, start, end) with crossfades; slow push over each block
    blocks = [(WAR, -1, 39.5), (ODIN, 38.5, 62.5), (TREE, 61.5, 99.0), (WAR, 98.0, 130.5), (ODIN, 129.5, 157)]
    for P, a, b in blocks:
        op = nr.window(t, a, b, 1.6)
        if op > 0:
            P.draw(img, t, a, op * 0.85, dur=b - a)
    img.alpha_composite(SHADE)

# --- instrumental (62-99 s): the myth of Episode 9 --------------------------------
def runes(img, t):
    op = nr.window(t, 63.0, 81.0, 1.0)
    if op > 0:
        nr.draw_lines(img, [T("THE WALL OF ASGARD", 44, GOLD)], 300, op)
        nr.draw_lines(img, [B("A builder offered the gods a wall in a single winter.", 50, LIGHT),
                            B("His price: the goddess Freyja, the sun and the moon.", 50, LIGHT),
                            B("On Loki's advice, they let him use his horse.", 50, LIGHT)], 400, op, gap=18)
    op = nr.window(t, 81.5, 98.5, 1.0)
    if op > 0:
        nr.draw_lines(img, [T("THE GODS REMEMBERED", 44, GOLD)], 300, op)
        nr.draw_lines(img, [B("“Then sought the gods their assembly-seats,", 50, LIGHT),
                            B("the holy ones, and council held,", 50, LIGHT),
                            B("to find who with venom the air had filled,", 50, LIGHT),
                            B("or had given Oth's bride to the giants' brood.”", 50, LIGHT),
                            B("Völuspá 25 · trans. H. A. Bellows (1923) · Prose Edda, Gylfaginning 42", 30)], 400, op, gap=16)

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
    nr.Card(-0.8, 7.9, 360, [T("NORDIC REIGN", 40, GOLD), T("INSIDE THE LIE", 104, LIGHT)], gap=26),
    nr.Card(11.5, 19.8, 380, [T("THE NORSE SAGA", 40, GOLD),
                              B("Loki, the god who talks the gods", 50, LIGHT),
                              B("into every bargain they regret.", 50, LIGHT),
                              B("This is his song.", 50, LIGHT)], gap=20),
    nr.Card(30.8, 40.0, 420, [B("Loki: “beautiful and comely to look upon,", 44, LIGHT),
                              B("evil in spirit, very fickle in habit.”", 44, LIGHT),
                              B("Prose Edda, Gylfaginning 33 · trans. A. G. Brodeur (1916)", 30)], gap=16),
    nr.Card(152.2, 156, 330, [T("INSIDE THE LIE", 76, LIGHT), B("Nordic Reign · from the album Before the End Begins", 38),
                              B("Listen on all platforms: link in the description", 40, LIGHT),
                              B("The full story: The Norse Saga, episode 9 · @nordicreignofficial", 36, GOLD)], gap=24),
]

def frame(img, t):
    art(img, t)
    runes(img, t)
    lyric(img, t)
    for c in CARDS:
        c.draw(img, t)
    nr.draw_lines(img, [B("Art: Lorenz Frølich (1895) · O. O. Bagge, Yggdrasil (1847) · Georg von Rosen, Odin the Wanderer (1886)", 22)],
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
        for t in (3, 15, 35, 21, 50, 70, 90, 112, 137, 154):
            img = bg.render(t); frame(img, t)
            img.convert("RGB").save(f"{out}_{int(t):03d}.jpg", quality=85)
    else:
        render(song, out)
