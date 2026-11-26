"""Second daily video for TikTok + YouTube Shorts (test from 30 Nov 2026): one fact cut from a saga episode.

A 12-20 s stretch of an already rendered voiced episode (captions and new voice/music mix included), with the
hook of hook.py on the first 2 s and "Full episode on the profile" over the last 2 s.

Usage:
  python3 teaser.py <episode.mp4> <out.mp4> <start> <end> <image> x0,y0,x1,y1 "<white>|<gold>" "<episode label>"
"""
import sys, subprocess
import numpy as np
from PIL import Image, ImageDraw
import nr, hook
from nr import W, H, FPS, T, B, GOLD, LIGHT, ease

TAIL = 0.8          # after the last word
END = 2.0           # end card length

def end_card(img, k, label):
    """Dark band + 'Full episode on the profile' (k = 0..1 fade)."""
    if k <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(260):
        a = int(170 * k * (1 - abs(i - 130) / 130))
        d.line([(0, 1250 + i), (W, 1250 + i)], fill=(8, 10, 16, a))
    img.alpha_composite(lay)
    nr.draw_lines(img, [T(label, 50, GOLD), B("Full episode on the profile", 44, LIGHT)], 1290 + 12 * (1 - k), k, gap=12)

def main():
    src, out, a, b, image, box, text, label = sys.argv[1:9]
    a, b = float(a), float(b)
    L = b - a + TAIL
    cut = out + ".cut.mp4"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-ss", str(a), "-t", str(L), "-i", src,
                    "-af", f"afade=t=in:d=0.12,afade=t=out:st={L - TAIL - 0.1}:d={TAIL + 0.1}",
                    "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-c:a", "aac", "-b:a", "160k", cut], check=True)
    d = ImageDraw.Draw(Image.new("RGBA", (W, H)))
    parts = text.split("|")
    lines = hook.fit(parts[0], LIGHT, d) + sum((hook.fit(p, GOLD, d) for p in parts[1:]), [])
    hk = list(hook.frames(hook.full_crop(image, tuple(float(v) for v in box.split(","))), lines, hook.HOOK_DUR))
    rd = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", cut, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                          stdout=subprocess.PIPE)
    tmp = out + ".v.mp4"
    wr = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                           "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    i = 0
    while True:
        buf = rd.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        t = i / FPS
        if i < len(hk):
            img = hk[i].convert("RGBA")
        else:
            img = Image.frombuffer("RGB", (W, H), buf).convert("RGBA")
        end_card(img, ease((t - (L - END)) / 0.5), label)
        wr.stdin.write(img.convert("RGB").tobytes())
        i += 1
    wr.stdin.close(); wr.wait(); rd.wait()
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", tmp, "-i", cut, "-map", "0:v", "-map", "1:a",
                    "-c", "copy", "-shortest", "-movflags", "+faststart", out], check=True)
    import os
    os.remove(cut); os.remove(tmp)
    print(out, round(L, 2))

if __name__ == "__main__":
    main()
