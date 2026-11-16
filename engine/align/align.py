"""Match recognized words (with times) to the known lyric lines and write the `words` string for lyric_video.py.
Usage: python3 align.py <prefix> "<song title in letras.md>"  -> prints the table and writes <prefix>_words.txt
Greedy: at each recognized word, try every lyric line; take the best match; repeated choruses come out naturally."""
import sys, json, re, difflib

LETRAS = "/mnt/user-data/uploads/Nordic Reign/letras.md"
prefix, title = sys.argv[1], sys.argv[2]

def norm(w):
    return re.sub(r"[^a-z']", "", w.lower().replace("’", "'"))

def lyric_lines():
    txt = open(LETRAS, encoding="utf-8").read()
    sec = txt.split("## " + title)[1].split("\n## ")[0]
    out = []
    for row in sec.split("\n")[1:]:
        row = row.strip()
        if not row or row.startswith("*") or row.startswith("("):
            continue
        # long rows with two sung lines separated by a comma in the middle are kept as one display line
        out.append(row)
    return out

def wsim(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()

def match(line_words, asr, i):
    """Align line words to asr[i:i+n+3]; returns (score, {line_idx: asr_idx}, last_asr_idx)."""
    n = len(line_words)
    win = [w for w in asr[i:i + n + 3] if w[1] <= asr[i][1] + 7.0]
    # DP over (line pos, asr pos) maximizing summed similarity, monotone, skips allowed
    best = [[0.0] * (len(win) + 1) for _ in range(n + 1)]
    back = [[None] * (len(win) + 1) for _ in range(n + 1)]
    for a in range(n + 1):
        for b in range(len(win) + 1):
            if a == 0 and b == 0:
                continue
            cands = []
            if a > 0:
                cands.append((best[a - 1][b], (a - 1, b, False)))
            if b > 0:
                cands.append((best[a][b - 1] - (0.15 if a > 0 else 0.6), (a, b - 1, False)))
            if a > 0 and b > 0:
                s = wsim(line_words[a - 1], win[b - 1][0])
                if s >= 0.5:
                    cands.append((best[a - 1][b - 1] + s, (a - 1, b - 1, True)))
            best[a][b], back[a][b] = max(cands, key=lambda c: c[0])
    b = max(range(len(win) + 1), key=lambda k: best[n][k])
    score = best[n][b] / n
    pairs, a = {}, n
    while a > 0 or b > 0:
        pa, pb, m = back[a][b]
        if m:
            pairs[pa] = i + pb
        a, b = pa, pb
    last = max(pairs.values()) if pairs else i
    return score, pairs, last

asr = [(w, t) for w, t in json.load(open(prefix + "_words.json"))]
lines = lyric_lines()
LW = [l.replace(" — ", " ").replace(" - ", " ").replace("…", " ").split() for l in lines]
DISP = [l.split() for l in lines]
out, i = [], 0
while i < len(asr):
    res = [(match(lw, asr, i), k) for k, lw in enumerate(LW)]
    res = [r for r in res if r[0][1] and min(r[0][1].values()) <= i + 1]
    if not res:
        i += 1
        continue
    (score, pairs, last), k = max(res, key=lambda r: r[0][0])
    if score < 0.4:
        i += 1
        continue
    words = DISP[k]
    # display words vs. match words: same count unless dashes; map by index on the dash-free list
    times = [asr[pairs[j]][1] if j in pairs else None for j in range(len(LW[k]))]
    # interpolate gaps
    known = [j for j, t in enumerate(times) if t is not None]
    for j in range(len(times)):
        if times[j] is None:
            lo = max([q for q in known if q < j], default=None)
            hi = min([q for q in known if q > j], default=None)
            if lo is not None and hi is not None:
                times[j] = times[lo] + (times[hi] - times[lo]) * (j - lo) / (hi - lo)
            elif lo is not None:
                times[j] = times[lo] + 0.3 * (j - lo)
            else:
                times[j] = times[hi] - 0.3 * (hi - j)
    # attach dash/ellipsis tokens of the display line to the previous word
    disp, ti = [], 0
    for w in words:
        if w in ("—", "-", "…"):
            disp.append((w, disp[-1][1]))
            continue
        disp.append((w, round(times[ti], 2)))
        ti += 1
    out.append((score, disp))
    i = last + 1

rows = []
for score, disp in out:
    print(f"{disp[0][1]:7.2f}  {score:.2f}  " + " ".join(w for w, _ in disp))
    rows.append(" ".join(f"{w}@{t}" for w, t in disp) + "¶")
open(prefix + "_words.txt", "w").write("\n".join(rows))
