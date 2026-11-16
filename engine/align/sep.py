"""Vocals with UVR MDX-Net (sherpa-onnx). Each 10 s chunk runs in its own process: the library keeps memory between calls.
Usage: python3 sep.py <song.wav> <out_prefix>  -> <out_prefix>_vocals.wav"""
import sys, subprocess, os
import numpy as np, soundfile as sf

M = "/home/claude/models/"
if sys.argv[1] == "--chunk":
    import sherpa_onnx as so
    src, i0, n, dst = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    x, sr = sf.read(src, dtype="float32", always_2d=True, start=i0, frames=n)
    cfg = so.OfflineSourceSeparationConfig(model=so.OfflineSourceSeparationModelConfig(
        uvr=so.OfflineSourceSeparationUvrModelConfig(model=M + "UVR_MDXNET_Main.onnx"), num_threads=2))
    res = so.OfflineSourceSeparation(cfg).process(sample_rate=sr, samples=np.ascontiguousarray(x.T))
    np.save(dst, np.array(res.stems[0].data, dtype=np.float32))  # stem 0 = vocals
    sys.exit(0)

song, out = sys.argv[1], sys.argv[2]
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", song, "-ac", "2", "-ar", "44100", out + "_44k.wav"], check=True)
info = sf.info(out + "_44k.wav")
sr, total = info.samplerate, info.frames
CH = 10 * sr
parts = []
for i in range(0, total, CH):
    dst = f"{out}_chunk.npy"
    subprocess.run([sys.executable, __file__, "--chunk", out + "_44k.wav", str(i), str(CH), dst], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    parts.append(np.load(dst))
voc = np.concatenate(parts, axis=1)
sf.write(out + "_vocals.wav", voc.T, sr)
os.remove(dst)
