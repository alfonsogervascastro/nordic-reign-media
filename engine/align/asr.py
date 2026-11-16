import sys, json, subprocess
import numpy as np, soundfile as sf
import sherpa_onnx as so
M = "/home/claude/models/"
out = sys.argv[1]
# --- ASR on 16 kHz mono, in 25 s windows with 5 s overlap ------------------------
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out + "_vocals.wav", "-ac", "1", "-ar", "16000",
                out + "_v16.wav"], check=True)
a, _ = sf.read(out + "_v16.wav", dtype="float32")
P = M + "sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8/"
rec = so.OfflineRecognizer.from_transducer(encoder=P + "encoder.int8.onnx", decoder=P + "decoder.int8.onnx",
                                          joiner=P + "joiner.int8.onnx", tokens=P + "tokens.txt",
                                          model_type="nemo_transducer", num_threads=2)
toks = []
win, hop = 25.0, 20.0
t0 = 0.0
while t0 < len(a) / 16000:
    seg = a[int(t0 * 16000): int((t0 + win) * 16000)]
    st = rec.create_stream(); st.accept_waveform(16000, seg); rec.decode_stream(st)
    r = st.result
    for tok, ts in zip(r.tokens, r.timestamps):
        T = t0 + ts
        # keep tokens in this window's own zone (avoid duplicates from overlap)
        lo = t0 + (2.5 if t0 > 0 else 0); hi = t0 + hop + 2.5
        if lo <= T < hi:
            toks.append([tok, round(T, 2)])
    t0 += hop
json.dump(toks, open(out + "_asr.json", "w"))
words, cur = [], None
for tok, T in toks:
    if tok.startswith(" ") or tok.startswith("▁") or cur is None:
        if cur: words.append(cur)
        cur = [tok.strip(" ▁"), T]
    else:
        cur[0] += tok
if cur: words.append(cur)
json.dump(words, open(out + "_words.json", "w"))
print(" ".join(f"{w}@{t}" for w, t in words))
