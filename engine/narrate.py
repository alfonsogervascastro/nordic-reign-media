"""Nordic Reign narrator: adds a consistent voice-over to any video script.

Voice: Kokoro-82M (Apache-2.0, runs locally on CPU, no token, no quota), always the same voice and speed.
Model files (download once, ~350 MB, from GitHub releases):
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
into engine/kokoro/ (git-ignored).  pip install kokoro-onnx

How it works: the script keeps its original timeline; each narrated segment (t0, t1, text) is stretched
if the spoken line needs more time, and the whole video is time-warped to match. Music is lowered under the voice.

    import narrate, v08_saga02 as ep
    narrate.render_voiced("out/v08v.mp4", ep.DUR, ep.frame, SEGMENTS, seed=19, bpm=60)

Write hard names phonetically in the spoken text (Ymir → "Eemeer", Vé → "Vay"); on-screen text keeps the real spelling.
"""
import os, subprocess
import numpy as np
import scipy.io.wavfile as wavfile
import nr

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE = os.environ.get("NR_VOICE", "bm_george")
SPEED = 0.95
LANG = "en-gb"
SR = 24000
_k = None

def speak(text, voice=None):
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        d = os.path.join(HERE, "kokoro")
        _k = Kokoro(os.path.join(d, "kokoro-v1.0.onnx"), os.path.join(d, "voices-v1.0.bin"))
    s, sr = _k.create(text, voice=voice or VOICE, speed=SPEED, lang=LANG)
    assert sr == SR
    return np.asarray(s, np.float32)

def plan(segments, dur, lead=0.35, tail=0.45, voice=None):
    """segments: [(t0, t1, text)] on the original timeline, in order, non-overlapping.
    Returns (new_dur, warp(t_new)->t_orig, voice_track)."""
    clips = [speak(txt, voice) for _, _, txt in segments]
    knots_o, knots_n = [0.0], [0.0]
    starts = []
    shift = 0.0
    for (t0, t1, _), c in zip(segments, clips):
        n0 = t0 + shift
        knots_o.append(t0); knots_n.append(n0)
        need = lead + len(c) / SR + tail
        L = max(t1 - t0, need)
        starts.append(n0 + lead)
        shift += L - (t1 - t0)
        knots_o.append(t1); knots_n.append(t1 + shift)
    knots_o.append(dur); knots_n.append(dur + shift)
    new_dur = dur + shift
    track = np.zeros(int((new_dur + 1) * SR), np.float32)
    for s, c in zip(starts, clips):
        i = int(s * SR)
        track[i:i + len(c)] += c[: len(track) - i]
    ko, kn = np.array(knots_o), np.array(knots_n)
    warp = lambda t: float(np.interp(t, kn, ko))
    return new_dur, warp, track[: int(new_dur * SR)]

def render_voiced(out, dur, frame, segments, seed=3, bpm=60, music=None, music_start=0.0, voice=None, music_gain=0.45):
    new_dur, warp, track = plan(segments, dur, voice=voice)
    base = os.path.splitext(out)[0]
    silent = base + ".music.mp4"
    nr.render(silent, new_dur, lambda img, t: frame(img, warp(t)), seed=seed, bpm=bpm, music=music, music_start=music_start)
    vw = base + ".voice.wav"
    peak = np.abs(track).max() or 1.0
    wavfile.write(vw, SR, (track / peak * 0.9 * 32767).astype(np.int16))
    # music ducked under the voice (sidechain), voice slightly warmed with a short room reverb
    fc = (f"[1:a]aresample=44100,aformat=channel_layouts=stereo,aecho=0.8:0.5:40:0.12,volume=1.0,asplit=2[v][vk];"
          f"[0:a]volume={music_gain}[m];"
          f"[m][vk]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=400[md];"
          f"[md][v]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", vw, "-filter_complex", fc,
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", out], check=True)
    os.remove(silent); os.remove(vw)
    return new_dur
