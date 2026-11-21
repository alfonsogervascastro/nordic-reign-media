"""4x upscaling of low-resolution paintings with Real-ESRGAN (ncnn, CPU), tile by tile.
Models: realesrgan-ncnn-vulkan release zip (github.com/xinntao/Real-ESRGAN/releases) unpacked in /home/claude/models/esrgan/models.
Usage: python3 upscale.py <in.jpg> <out.jpg> [x4plus|x4plus-anime] [max_side]
x4plus for paintings; x4plus-anime keeps engravings and line art crisper."""
import sys
import numpy as np
import ncnn
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "x4plus"
max_side = int(sys.argv[4]) if len(sys.argv) > 4 else 2400
M = "/home/claude/models/esrgan/models/realesrgan-" + model

net = ncnn.Net()
net.opt.use_vulkan_compute = False
net.opt.num_threads = 2
net.load_param(M + ".param")
net.load_model(M + ".bin")

img = np.asarray(Image.open(src).convert("RGB"), np.float32) / 255.0
h, w, _ = img.shape
T, P, S = 160, 12, 4
out = np.zeros((h * S, w * S, 3), np.float32)
for y in range(0, h, T):
    for x in range(0, w, T):
        y0, x0 = max(y - P, 0), max(x - P, 0)
        y1, x1 = min(y + T + P, h), min(x + T + P, w)
        tile = np.ascontiguousarray(img[y0:y1, x0:x1].transpose(2, 0, 1))
        ex = net.create_extractor()
        ex.input("data", ncnn.Mat(tile))
        _, o = ex.extract("output")
        o = np.array(o).transpose(1, 2, 0)
        oy, ox = (y - y0) * S, (x - x0) * S
        th, tw = min(T, h - y) * S, min(T, w - x) * S
        out[y * S:y * S + th, x * S:x * S + tw] = o[oy:oy + th, ox:ox + tw]
res = Image.fromarray((np.clip(out, 0, 1) * 255).round().astype(np.uint8))
if max(res.size) > max_side:
    k = max_side / max(res.size)
    res = res.resize((round(res.width * k), round(res.height * k)), Image.LANCZOS)
res.save(dst, quality=92)
print(src, (w, h), "->", res.size)
