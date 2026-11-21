"""YouTube texts for the 7 lyric videos -> /home/claude/out/youtube-<slug>.txt (same format as the earlier ones)."""
import re

LETRAS = open("/mnt/user-data/uploads/Nordic Reign/letras.md", encoding="utf-8").read()

def lyrics(title):
    sec = LETRAS.split("## " + title)[1].split("\n## ")[0]
    rows = [r.strip() for r in sec.split("\n")[1:]]
    return "\n".join(r for r in rows if r and not r.startswith("*") and not r.startswith("("))

HYPER = "https://distrokid.com/hyperfollow/nordicreign/before-the-end-begins-2"
SPOT = "https://open.spotify.com/artist/1l2zYowyNGlt8cwvcjT7vN"

SONGS = [
    dict(slug="thunder-of-the-gods", title="Thunder of the Gods", sub="Thor and the World Serpent",
         intro="Thor went fishing with the giant Hymir, used the head of an ox as bait and hooked the Midgard Serpent itself. He pulled so hard that his feet broke through the boat. \"Thunder of the Gods\" is Thor's song, from the album Before the End Begins.",
         ep="episode 15", sources="Hymiskviða (Poetic Edda), translation by H. A. Bellows (1923); Prose Edda, Gylfaginning 48, translation by A. G. Brodeur (1916).",
         art="Emil Doepler, Thor and the Midgard Serpent (c. 1905); Mårten Eskil Winge, Tor's Fight with the Giants (1872).",
         tags="#norsemythology #vikingmetal #thor", keys="thunder of the gods, thor, jormungandr, midgard serpent, hymir",
         when="viernes 25 dic (el Ep. 15 sale, si se mantiene el ritmo, el sábado 26)"),
    dict(slug="forge-of-svartalfheim", title="Forge of Svartalfheim", sub="How Mjölnir Was Forged",
         intro="Loki bet his head that two dwarves could not forge anything better than the gods already had. Then he turned into a fly to ruin their work, and Thor's hammer came out with a short handle. \"Forge of Svartalfheim\" tells that story, from the album Before the End Begins.",
         ep="episode 12", sources="Prose Edda, Skáldskaparmál 35, translation by A. G. Brodeur (1916).",
         art="Elmer Boyd Smith, The third gift — an enormous hammer (1902); Arthur Rackham (1901); Mårten Eskil Winge, Tor's Fight with the Giants (1872).",
         tags="#norsemythology #vikingmetal #mjolnir", keys="forge of svartalfheim, mjolnir, dwarves, sindri, brokkr, loki, sif",
         when="martes 15 dic (el Ep. 12 sale, si se mantiene el ritmo, el miércoles 16)"),
    dict(slug="born-in-the-dark", title="Born in the Dark", sub="Loki's Children: Fenrir, Jörmungandr and Hel",
         intro="Loki had three children with the giantess Angrboða: the wolf Fenrir, the World Serpent and Hel. The gods knew they would bring great harm. \"Born in the Dark\" is their song, from the album Before the End Begins.",
         ep="episodes 10 and 11", sources="Prose Edda, Gylfaginning 34, translation by A. G. Brodeur (1916).",
         art="Willy Pogány, The Children of Loki (1920); John Bauer, Tyr and Fenrir (1911); Emil Doepler, Ragnarök (c. 1905).",
         tags="#norsemythology #vikingmetal #fenrir", keys="born in the dark, fenrir, loki, jormungandr, hel, tyr, gleipnir",
         when="martes 8 dic (el Ep. 10 sale el miércoles 9 dic)"),
    dict(slug="hall-of-illusions", title="Hall of Illusions", sub="Thor in the Hall of Útgarða-Loki",
         intro="Thor, Loki and Thjálfi visit the hall of the giant king Útgarða-Loki and lose every contest. Only at the end do they learn the truth: they had been fighting fire, thought, the sea, the World Serpent and old age. \"Hall of Illusions\" tells that story, from the album Before the End Begins.",
         ep="episode 14", sources="Prose Edda, Gylfaginning 44–47, translation by A. G. Brodeur (1916).",
         art="Louis Huard, Giant Skrymir and Thor; Elmer Boyd Smith, I am the giant Skrymir (1902); Lorenz Frølich, Thor and Elli; Arthur Rackham, He raised his hammer with a mighty swing (1901).",
         tags="#norsemythology #vikingmetal #thor", keys="hall of illusions, utgarda-loki, utgard, thor, skrymir, elli, loki",
         when="martes 22 dic (el Ep. 14 sale, si se mantiene el ritmo, el miércoles 23)"),
    dict(slug="the-bride-in-thunder", title="The Bride in Thunder", sub="Thor Dressed as a Bride",
         intro="The giant Thrym stole Thor's hammer and would only give it back for the goddess Freyja. So Thor put on a bridal veil and went himself, with Loki as his bridesmaid. \"The Bride in Thunder\" tells that story, from the album Before the End Begins.",
         ep="episode 13", sources="Þrymskviða (Poetic Edda), translation by H. A. Bellows (1923).",
         art="Elmer Boyd Smith, \"Ah, what a lovely maid it is!\" (1902); Mårten Eskil Winge, Tor's Fight with the Giants (1872).",
         tags="#norsemythology #vikingmetal #thor", keys="the bride in thunder, thrymskvida, thor, thrym, loki, freyja, mjolnir",
         when="viernes 18 dic (el Ep. 13 sale, si se mantiene el ritmo, el sábado 19)"),
    dict(slug="chains-beneath-the-mountain", title="Chains Beneath the Mountain", sub="Loki Bound and Sigyn",
         intro="The gods bound Loki to three stones beneath the earth and hung a serpent over his face. His wife Sigyn holds a bowl to catch the venom; when she empties it, the drops fall and the earth shakes. \"Chains Beneath the Mountain\" is Loki's song, from the album Before the End Begins.",
         ep="episode 18", sources="Prose Edda, Gylfaginning 50, translation by A. G. Brodeur (1916); Lokasenna (Poetic Edda), final prose.",
         art="Mårten Eskil Winge, Loki and Sigyn (1863).",
         tags="#norsemythology #vikingmetal #loki", keys="chains beneath the mountain, loki, sigyn, loki bound, earthquake",
         when="martes 5 ene (el Ep. 18 sale, si se mantiene el ritmo, el miércoles 6)"),
    dict(slug="before-the-end-begins", title="Before the End Begins", sub="Ragnarök (Instrumental)",
         intro="Fimbulwinter, the wolves that swallow the sun and the moon, Fenrir unchained, Odin's last battle and a new world rising from the sea. \"Before the End Begins\" is the instrumental title track of the album: the march to Ragnarök.",
         ep="episodes 19 and 20", sources="Völuspá (Poetic Edda), translation by H. A. Bellows (1923); Prose Edda, Gylfaginning 51–53, translation by A. G. Brodeur (1916).",
         art="Emil Doepler, Ragnarök and Thor and the Midgard Serpent (c. 1905); John Bauer, Tyr and Fenrir (1911); Oluf O. Bagge, Yggdrasil (1847).",
         tags="#norsemythology #vikingmetal #ragnarok", keys="before the end begins, ragnarok, fimbulwinter, fenrir, odin, instrumental",
         when="viernes 8 ene (el Ep. 19 sale, si se mantiene el ritmo, el sábado 9)"),
]

for s in SONGS:
    instr = s["slug"] == "before-the-end-begins"
    kind = "Official Visualizer" if instr else "Official Lyric Video"
    txt = f"""TÍTULO
Nordic Reign - {s['title']} ({kind}) | {s['sub']}

DESCRIPCIÓN
{s['intro']}

Listen on all platforms: {HYPER}
Spotify: {SPOT}

The full story is {s['ep']} of The Norse Saga, the series that retells the Norse myths in order, from the first giant to Ragnarök. Shorts on this channel, Instagram and TikTok: @nordicreignofficial

Sources: {s['sources']}
Art (public domain): {s['art']}
Music made with AI tools.
"""
    if not instr:
        txt += "\nLYRICS\n" + lyrics(s["title"]) .replace("\n\n", "\n") + "\n"
    txt += f"""
{s['tags']}

ETIQUETAS
nordic reign, {s['keys']}, viking metal, norse mythology, {'instrumental, visualizer' if instr else 'lyric video'}, heavy metal

AJUSTES AL SUBIR
- Audiencia: "No, no es contenido para niños"
- Categoría: Música
- Contenido alterado o sintético: "No"
- Lista de reproducción: "Before the End Begins (Lyric Videos)"
- Visibilidad: programado para el {s['when']}
"""
    open(f"/home/claude/out/youtube-{s['slug']}.txt", "w", encoding="utf-8").write(txt)
    print(s["slug"], len(txt))
