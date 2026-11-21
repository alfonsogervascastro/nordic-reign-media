"""Stronger opening for an existing vertical video (decided 21 Nov 2026).

The first HOOK_DUR seconds are replaced by a full-screen close-up of the painting (a face, an eye, a weapon),
already moving on frame 0, with the hook line in large type. Then the original video carries on, with its audio untouched.

Usage:
  python3 hook.py <in.mp4> <out.mp4> <image> <crop x0,y0,x1,y1 in the ORIGINAL image's pixels> "<white line>|<gold line>" [dur]
"""
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageFilter
import nr
from nr import W, H, FPS, T, GOLD, LIGHT

HOOK_DUR = 2.0
PAD = 1.35          # show a bit more than the crop box

def full_crop(path, box):
    """The painting cropped to 9:16 around `box` (given in the original image's pixels), as a large RGB image."""
    src = Image.open(path).convert("RGB")
    orig = os.path.join(os.path.dirname(path), "original", os.path.basename(path))
    r = src.width / Image.open(orig).width if os.path.exists(orig) else 1.0
    x0, y0, x1, y1 = [c * r for c in box]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w, h = (x1 - x0) * PAD, (y1 - y0) * PAD
    if w / h > W / H:
        h = w * H / W
    else:
        w = h * W / H
    # stay inside the image (shrink if needed, keeping 9:16)
    k = min(1.0, src.width / w, src.height / h)
    w, h = w * k, h * k
    cx = min(max(cx, w / 2), src.width - w / 2)
    cy = min(max(cy, h / 2), src.height - h / 2)
    crop = src.crop((int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2)))
    crop = crop.resize((int(W * 1.25), int(H * 1.25)), Image.LANCZOS)
    if "/images/" not in path:                         # a frame of our own video (rune card): keep its colours
        return crop
    return Image.fromarray(grade(np.asarray(crop, np.float32) / 255.0))

def grade(a):
    """Same brand grading as nr.Painting (duotone shadow/candle-light, 28 % original colour)."""
    lum = (0.3 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2])[..., None]
    lum = np.clip((lum - 0.06) / 0.88, 0, 1) ** 1.1
    shadow = np.array([16, 22, 32], np.float32) / 255
    light = np.array([232, 206, 160], np.float32) / 255
    out = (shadow * (1 - lum) + light * lum) * 0.72 + a * 0.28
    return (np.clip(out, 0, 1) * 255).astype(np.uint8)

def fit(text, col, d):
    """Largest size (104 down to 72) that fits 980 px; below that, wrap into two lines."""
    for size in range(104, 71, -4):
        if nr.line_size(d, T(text, size, col))[0] <= 980:
            return [T(text, size, col)]
    words = text.split(); best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        wmax = max(nr.line_size(d, T(a, 88, col))[0], nr.line_size(d, T(b, 88, col))[0])
        if best is None or wmax < best[0]:
            best = (wmax, a, b)
    return [T(best[1], 88, col), T(best[2], 88, col)]

def frames(art, lines, dur):
    big = art
    shade = np.zeros((H, W, 4), np.uint8)
    ys = np.arange(H)[:, None]
    # light artwork (line engravings) needs a darker band behind the text
    top = np.asarray(big.convert("L").resize((W, H)), np.float32)[150:650] / 255
    strong = top.mean() > 0.45
    reach, peak = (0.50, 245) if strong else (0.42, 200)
    a = np.clip(1 - ys / (H * reach), 0, 1) ** (1.0 if strong else 1.4) * peak + np.clip((ys - H * 0.75) / (H * 0.25), 0, 1) * 150
    shade[..., 3] = np.repeat(a, W, axis=1).astype(np.uint8)
    shade = Image.fromarray(shade, "RGBA")
    n = int(round(dur * FPS))
    for i in range(n):
        t = i / FPS
        k = 1 - (1 - t / dur) ** 2                      # fast at first, then settles: movement from frame 0
        z = 1.0 + 0.14 * k
        cw, ch = big.width / (1.25 * z), big.height / (1.25 * z)
        cx = big.width / 2 + 0.02 * big.width * k
        cy = big.height / 2 - 0.015 * big.height * k
        fr = big.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.LANCZOS)
        img = fr.convert("RGBA")
        img.alpha_composite(shade)
        pop = min(1.0, t / 0.12)                         # text is there from frame 0, settles in 0.12 s
        y = 250 - 18 * (1 - pop)
        nr.draw_lines(img, lines, y, 1.0, gap=10)
        yield img.convert("RGB")

def main():
    src, out, image, box, text = sys.argv[1:6]
    dur = float(sys.argv[6]) if len(sys.argv) > 6 else HOOK_DUR
    box = tuple(float(v) for v in box.split(","))
    parts = text.split("|")
    from PIL import ImageDraw
    d = ImageDraw.Draw(Image.new("RGBA", (W, H)))
    lines = fit(parts[0], LIGHT, d) + sum((fit(p, GOLD, d) for p in parts[1:]), [])
    art = full_crop(image, box)
    tmp = out + ".hook.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for fr in frames(art, lines, dur):
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()
    # hook video + rest of the original video, original audio from 0
    fc = (f"[1:v]trim=start={dur},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p[rest];"
          f"[0:v]fps={FPS},format=yuv420p[h];[h][rest]concat=n=2:v=1:a=0[v]")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", tmp, "-i", src, "-filter_complex", fc,
                    "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                    "-c:a", "copy", "-movflags", "+faststart", out], check=True)
    os.remove(tmp)
    print(out)

if __name__ == "__main__":
    main()
