"""Generate AI motifs with Qwen-Image on Hugging Face (needs HF_TOKEN in the environment).

    HF_TOKEN=... python3 generate.py name1 name2 ...
Each motif is saved as ai/<name>_<n>.png. Prompts live in PROMPTS below.
"""
import os, sys, shutil
from gradio_client import Client

STYLE = ("Flat solid black ink on pure white background, clean vector tattoo flash, bold even outlines, "
         "no grey, no gradients, no texture, isolated, centered, Viking Age art style as carved on runestones "
         "and the Urnes stave church")
NEG = ("text, letters, watermark, signature, color, grey shading, gradient, photo, realistic, 3d, blurry, "
       "low resolution, frame, border, background scenery")

PROMPTS = {
    "sleeve_test": ("Dense Viking Mammen style blackwork tattoo panel: Odin with his spear and two ravens, "
                    "surrounded by interlaced gripping-beast knotwork, Norse ornament filling the whole square. "
                    "Black and white tattoo flash, bold lines."),
    "ravens": ("Two ravens, Huginn and Muninn, facing each other in mirrored symmetry, wings raised, "
               "stylized Viking art with spiral joints and almond eyes, " + STYLE),
    "wolf_head": ("Fierce wolf head in side profile facing left, jaws open showing fangs, stylized Viking "
                  "Urnes art with spiral jaw joint, almond eye and long curling lip lappet, neck ends in a clean "
                  "ribbon, " + STYLE),
    "sleipnir": ("Sleipnir, Odin's eight-legged horse, in side view galloping to the left, stylized like the "
                 "Gotland picture stones, eight legs clearly visible, " + STYLE),
    "yggdrasil": ("Yggdrasil the world tree, symmetric, wide crown of branches and deep roots forming a circle, "
                  "branches and roots curl into spirals, " + STYLE),
    "horn": ("A Viking drinking horn lying diagonally, decorated with a band of interlace, metal rim and tip "
             "ending in a small dragon head, " + STYLE),
}

def main(names, n=1):
    c = Client("mcp-tools/Qwen-Image", token=os.environ["HF_TOKEN"], verbose=False)
    here = os.path.dirname(os.path.abspath(__file__))
    for name in names:
        for i in range(n):
            try:
                img, _ = c.predict(PROMPTS[name], 0, True, "1:1", NEG, 4.5, 16, api_name="/generate_image")
                out = os.path.join(here, f"{name}_{i}.png")
                shutil.copy(img, out)
                print("ok", name, i, flush=True)
            except Exception as e:
                print("FAIL", name, i, str(e)[:160], flush=True)
                if "limit" in str(e).lower() or "quota" in str(e).lower():
                    return

if __name__ == "__main__":
    args = sys.argv[1:]
    n = 1
    if args and args[0].startswith("-n"):
        n = int(args[0][2:]); args = args[1:]
    main(args or list(PROMPTS), n)
