"""Build engine/lyrics/<slug>.json from <prefix>_words.txt plus manual fixes.
Usage: python3 make_cfg.py <spec.py>   (spec defines PREFIX, SLUG, TITLE, DUR, END_CLEAR, CREDIT, ART, CARDS, FIX, ADD, DROP)
FIX:  {approx_start: "Word@t Word@t ..."}  replaces the aligned line that starts within 0.6 s of approx_start
ADD:  ["Word@t ...", ...]                    extra lines (missed by recognition)
DROP: [approx_start, ...]                    aligned lines to remove"""
import sys, json, runpy

S = runpy.run_path(sys.argv[1])
rows = []
if S.get("PREFIX"):
    for row in open(f"/home/claude/align/{S['PREFIX']}_words.txt").read().split("\n"):
        row = row.strip().rstrip("¶")
        if not row:
            continue
        t0 = float(row.split(" ")[0].rsplit("@", 1)[1])
        if any(abs(t0 - d) < 0.6 for d in S.get("DROP", [])):
            continue
        for k, v in S.get("FIX", {}).items():
            if abs(t0 - k) < 0.6:
                row = v
        rows.append(row)
rows += S.get("ADD", [])
# long rows (two sung phrases) -> two display lines, split at the comma/ellipsis nearest the middle
split = []
for r in rows:
    ws = r.split(" ")
    names = [w.rsplit("@", 1)[0] for w in ws]
    if len(ws) > 9:
        cuts = [k + 1 for k, n in enumerate(names[:-1]) if n.endswith(",") or n.endswith("…")]
        c = min(cuts, key=lambda k: abs(k - len(ws) / 2)) if cuts else len(ws) // 2
        split += [" ".join(ws[:c]), " ".join(ws[c:])]
        continue
    split.append(r)
rows = split
rows.sort(key=lambda r: float(r.split(" ")[0].rsplit("@", 1)[1]))
cfg = dict(title=S["TITLE"], dur=S["DUR"], end_clear=S["END_CLEAR"], credit=S["CREDIT"],
           words="\n".join(r + "¶" for r in rows), art=S["ART"], cards=S["CARDS"])
out = f"/home/claude/nordic-reign-media/engine/lyrics/{S['SLUG']}.json"
json.dump(cfg, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in rows:
    print(f"{float(r.split(' ')[0].rsplit('@', 1)[1]):7.2f}  " + " ".join(w.rsplit("@", 1)[0] for w in r.split(" ")))
print("->", out)
