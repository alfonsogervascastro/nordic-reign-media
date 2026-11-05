"""Nordic Reign narrator voice (Chatterbox TTS on Hugging Face, Space ResembleAI/Chatterbox).

Always the same settings so the narrator sounds identical in every video:
the model's built-in voice (no cloning of any real person), fixed seed and parameters.
Needs HF_TOKEN in the environment (Alfonso's token; never commit it).

    HF_TOKEN=... python3 voice.py ep02          # generates voice/ep02/NN.wav for the lines in SCRIPTS["ep02"]

Pronunciation: write names phonetically in the spoken text when the model mispronounces them
(e.g. "Vay" for Vé). On-screen text keeps the correct spelling.
"""
import os, sys, shutil, time

SETTINGS = dict(exaggeration=0.4, temperature=0.7, seed=42, cfg=0.4)

SCRIPTS = {
    "ep02": [
        "Odin and his brothers, Vili and Vay, killed the giant Ymir.",
        "So much blood poured from him that every frost giant drowned. All but one: Bergelmir.",
        "Then they built the world from his body.",
        "His blood became the sea,",
        "his flesh the earth, his bones the mountains.",
        "His skull became the sky, held up by four dwarves.",
        "His brains, the clouds.",
        "And with his eyebrows, they walled in Midgard.",
        "A home for humans who did not exist yet.",
        "But what holds all the worlds together? Episode three, on Saturday.",
        "This chapter, as a tattoo.",
    ],
}

def tts(text, out):
    from gradio_client import Client
    c = Client("ResembleAI/Chatterbox", token=os.environ["HF_TOKEN"], verbose=False)
    for attempt in range(3):
        try:
            r = c.predict(text, None, SETTINGS["exaggeration"], SETTINGS["temperature"], SETTINGS["seed"],
                          SETTINGS["cfg"], True, api_name="/generate_tts_audio")
            shutil.copy(r, out)
            return out
        except Exception as e:
            print("retry", attempt, str(e)[:120]); time.sleep(10)
    raise RuntimeError("TTS failed: " + text)

if __name__ == "__main__":
    key = sys.argv[1]
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice", key)
    os.makedirs(d, exist_ok=True)
    for i, line in enumerate(SCRIPTS[key]):
        p = os.path.join(d, f"{i:02d}.wav")
        if not os.path.exists(p):
            tts(line, p)
            print("ok", i, line)
