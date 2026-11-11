"""Generic 16:9 lyric video for Nordic Reign songs, driven by a JSON config in engine/lyrics/<slug>.json.

Full song in the MP4, so the MP4 is NOT committed to the public repo (only scripts and configs).
Usage:  python3 lyric_video.py lyrics/<slug>.json <song.wav|mp3> <out.mp4> [stills]

Config keys:
  title, dur, end_clear (last second lyrics may show), credit (art line at the bottom),
  words: "Word@start Word@start ...¶\\n..." one sung line per row (Suno aligned_lyrics, released master);
         empty for an instrumental (then only cards and art),
  art:   [[image file in ../images, start, end, focus_x, focus_y], ...]  (crossfaded, slow push),
  cards: [[a, b, y, [["T"|"B", text, size, "gold"|"light"|"mist"], ...]], ...]
The first card should be the title card and the last one the outro (album + link + episode).
"""
import sys, json, subprocess
from PIL import Image
import nr

nr.W, nr.H = 1920, 1080
W, H = nr.W, nr.H
FPS = 24
COL = {"gold": nr.GOLD, "light": nr.LIGHT, "mist": nr.MIST}

def load(path):
    cfg = json.load(open(path, encoding="utf-8"))
    lines = []
    raw = [[(w.rsplit("@", 1)[0], float(w.rsplit("@", 1)[1])) for w in row.split(" ") if "@" in w]
           for row in cfg.get("words", "").replace("¶", "").split("\n") if row.strip()]
    for words in raw:
        starts = [s for _, s in words]
        ends = [min(starts[k + 1] - 0.05, starts[k] + 0.9) if k + 1 < len(starts) else starts[k] + 0.9
                for k in range(len(starts))]
        lines.append(dict(words=[w for w, _ in words], starts=starts, ends=ends))
    for i, L in enumerate(lines):
        nxt = lines[i + 1]["starts"][0] if i + 1 < len(lines) else 1e9
        L["a"] = L["starts"][0] - 0.7
        L["b"] = min(nxt - 0.35, L["ends"][-1] + 3.0, cfg.get("end_clear", cfg["dur"]))
    art = [(nr.Painting("../images/" + f, 1500, 1080, cx=W / 2, cy=H / 2, focus=(fx, fy), zoom=0.12, feather=0.14), a, b)
           for f, a, b, fx, fy in cfg["art"]]
    cards = [nr.Card(a, b, y, [((nr.T if k == "T" else nr.B)(txt, size, COL[c])) for k, txt, size, c in ls], gap=20)
             for a, b, y, ls in cfg["cards"]]
    return cfg, lines, art, cards

SHADE = Image.new("RGBA", (W, H), (10, 12, 16, 120))

def make_frame(cfg, lines, art, cards):
    def frame(img, t):
        for P, a, b in art:
            op = nr.window(t, a, b, 1.6)
            if op > 0:
                P.draw(img, t, a, op * 0.85, dur=b - a)
        img.alpha_composite(SHADE)
        for i, L in enumerate(lines):
            op = nr.window(t, L["a"], L["b"], 0.35)
            if op <= 0:
                continue
            rise = (1 - nr.ease((t - L["a"]) / 0.5)) * 18
            segs = []
            for w, s, e in zip(L["words"], L["starts"], L["ends"]):
                k = nr.ease((t - s) / max(0.15, e - s))
                col = tuple(int(nr.LIGHT[c] * (1 - k) + nr.GOLD[c] * k) for c in range(3))
                segs.append((w + " ", "title", 66, col))
            nr.draw_lines(img, [segs], 470 + rise, op)
            if i + 1 < len(lines) and lines[i + 1]["a"] - L["b"] < 1.0:
                nr.draw_lines(img, [nr.B(" ".join(lines[i + 1]["words"]), 40, nr.MIST)], 590 + rise, op * 0.55)
        for c in cards:
            c.draw(img, t)
        nr.draw_lines(img, [nr.B(cfg["credit"], 22)], 1040, 0.75)
    return frame

def render(cfg, frame, song, out):
    dur = cfg["dur"]
    bg = nr.Background(5)
    tmp_v = out + ".v.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                          "-pix_fmt", "yuv420p", tmp_v], stdin=subprocess.PIPE)
    for i in range(int(round(dur * FPS))):
        t = i / FPS
        img = bg.render(t)
        frame(img, t)
        k = min(nr.ease(t / 0.8), nr.ease((dur - t) / 1.2))
        if k < 1:
            img = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), img, k)
        p.stdin.write(img.convert("RGB").tobytes())
        if i % 480 == 0:
            print(f"{t:.0f}s", flush=True)
    p.stdin.close(); p.wait()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp_v, "-i", song, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True)
    subprocess.run(["rm", "-f", tmp_v])

if __name__ == "__main__":
    cfg, lines, art, cards = load(sys.argv[1])
    frame = make_frame(cfg, lines, art, cards)
    song, out = sys.argv[2], sys.argv[3]
    if len(sys.argv) > 4 and sys.argv[4] == "stills":
        bg = nr.Background(5)
        marks = sorted({c[0] + 2 for c in cfg["cards"]} | {L["starts"][0] + 1 for L in lines[::3]})
        for t in marks:
            img = bg.render(t); frame(img, t)
            img.convert("RGB").save(f"{out}_{int(t):03d}.jpg", quality=85)
    else:
        render(cfg, frame, song, out)
