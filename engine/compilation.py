"""YouTube compilation (16:9) of several vertical episodes: each episode centred over a blurred, darkened copy of itself,
with a side panel naming the episode, and a 4 s title card at the start.
Usage: python3 compilation.py <out.mp4> "<title>" "<subtitle>" "<label 1>|<file 1>" "<label 2>|<file 2>" ...
Prints the YouTube chapter list (timestamps) at the end."""
import sys, os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
F_T, F_B = os.path.join(HERE, "fonts/Cinzel.ttf"), os.path.join(HERE, "fonts/EBGaramond.ttf")
GOLD, LIGHT, MIST = (214, 175, 96), (232, 228, 218), (150, 156, 166)
out, title, subtitle = sys.argv[1], sys.argv[2], sys.argv[3]
items = [a.split("|", 1) for a in sys.argv[4:]]
tmp = tempfile.mkdtemp()

def text_center(d, xc, y, s, font, fill):
    w = d.textlength(s, font=font)
    d.text((xc - w / 2, y), s, font=font, fill=fill)

def panel(label, path):
    """Transparent 1920x1080 overlay: episode name in the two side panels."""
    im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    big, small = ImageFont.truetype(F_T, 46), ImageFont.truetype(F_B, 34)
    top, name = label.split(":", 1) if ":" in label else (label, "")
    text_center(d, 330, 470, top.strip().upper(), big, GOLD)
    text_center(d, 330, 540, name.strip(), small, LIGHT)
    text_center(d, 1590, 470, "THE NORSE SAGA", big, GOLD)
    text_center(d, 1590, 540, "@nordicreignofficial", small, MIST)
    im.save(path)

def title_card(path):
    im = Image.new("RGB", (1920, 1080), (12, 14, 18))
    d = ImageDraw.Draw(im)
    text_center(d, 960, 380, "NORDIC REIGN", ImageFont.truetype(F_T, 44), GOLD)
    text_center(d, 960, 450, title, ImageFont.truetype(F_T, 96), LIGHT)
    text_center(d, 960, 590, subtitle, ImageFont.truetype(F_B, 48), MIST)
    im.save(path)

segs = []
title_card(f"{tmp}/title.png")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", "4", "-i", f"{tmp}/title.png",
                "-f", "lavfi", "-t", "4", "-i", "anullsrc=r=44100:cl=stereo",
                "-vf", "fps=30,format=yuv420p,fade=in:0:15,fade=out:st=3.5:d=0.5", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "23", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{tmp}/s0.mp4"], check=True)
segs.append(f"{tmp}/s0.mp4")
chapters, t = [], 4.0
for k, (label, f) in enumerate(items, 1):
    panel(label, f"{tmp}/p{k}.png")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                               capture_output=True, text=True).stdout)
    fc = ("[0:v]split[a][b];[a]scale=1920:-2,crop=1920:1080,gblur=sigma=40,eq=brightness=-0.35[bg];"
          "[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0[v];[v][1:v]overlay=0:0,fps=30,format=yuv420p[vo]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f, "-i", f"{tmp}/p{k}.png", "-filter_complex", fc,
                    "-map", "[vo]", "-map", "0:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", f"{tmp}/s{k}.mp4"], check=True)
    segs.append(f"{tmp}/s{k}.mp4")
    chapters.append((t, label))
    t += dur
open(f"{tmp}/list.txt", "w").write("".join(f"file '{s}'\n" for s in segs))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt", "-c", "copy",
                "-movflags", "+faststart", out], check=True)
print("0:00 Intro")
for t0, label in chapters:
    print(f"{int(t0 // 60)}:{int(t0 % 60):02d} {label}")
