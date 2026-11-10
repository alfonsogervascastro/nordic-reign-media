# Nordic Reign · estado y traspaso (10 nov 2026)

Léelo entero antes de trabajar. La fuente de verdad del día a día es `PLAYBOOK.md` del repositorio.

## Dónde está todo
- Repositorio público: https://github.com/alfonsogervascastro/nordic-reign-media (clonar; contiene motor de vídeo, PLAYBOOK, vídeos publicados, métricas). Commits con usuario "Claude <noreply@anthropic.com>".
- `PLAYBOOK.md`: series, plantilla de vídeo (checklist obligatorio), reglas de rigor, voz, imágenes, cómo programar en Metricool, registro de publicaciones, pendientes.
- `engine/`: motor (nr.py, narrate.py = voz Kokoro, scenes.py) y un script por vídeo (v01…v18). `tattoos/`: motor de nudos, designs.py, designs_saga.py, make_pack.py.
- `metrics/`: informes (último: 2026-11-10.md).
- Tarea programada `trig_017Znei3Nj9dwixTMzMs9WhE`: domingos 10:56 (Madrid), sigue el PLAYBOOK. 8 y 15 nov: solo métricas. 22 nov: produce la semana 24–30.
- Metricool: brand id 7741806, zona Europe/Madrid. TikTok exige `tiktokData.title`. Máx. 5 hashtags. Portada con `videoCoverMilliseconds`.

## Cosas que NO están en el repo (a propósito o por tamaño)
- `tattoos/out/` y `tattoos/pack/` (el producto de pago; repo público). Se regeneran: `python3 tattoos/designs.py …`, `designs_saga.py epNN`, `make_pack.py`.
- Modelo de voz Kokoro (`engine/kokoro/`): se descarga de las releases de GitHub `thewh1teagle/kokoro-onnx` (ver PLAYBOOK). Voz fija: `am_michael` («voz 6», elegida por Alfonso).
- Token de Hugging Face: nunca se guarda. Para mejorar diseños con IA, Alfonso pega uno nuevo.

## Estado
- Programado en IG + YouTube + TikTok a las 19:00 hasta el lunes 23 nov (el 10 nov solo IG + TikTok por el límite de Metricool).
- The Norse Saga publicada/programada hasta el Ep. 5 (con voz y cierre de tatuaje). Siguiente: Ep. 6 «Nine Nights» (miér. 25).
- Pack de tatuajes: 23 diseños + PDF de 49 páginas + ZIP de plantillas, generados el 10 nov y copiados a `C:\Nordic Reign\pack\`. Recomendación: Etsy a 12 € (lanzamiento 9 €); ficha, etiquetas y escenarios en `C:\Nordic Reign\pack-tatuajes-venta.md`. Alfonso abre la tienda (Claude no puede crear cuentas) y consulta con gestor el alta/IVA.
- Música: canciones regeneradas con Suno de pago y distribuidas con DistroKid (Spotify, YouTube, Instagram…). En el repo solo fragmentos de 75 s (`audio/`; repo público). Originales, MP3, instrumentales y letras (`letras.md`) en `C:\Nordic Reign\` del ordenador de Alfonso. Suno Pro: quedan pocas descargas hasta el 8 dic.
- Promoción musical (10 nov): Spotify for Artists reclamado (artista `https://open.spotify.com/artist/1l2zYowyNGlt8cwvcjT7vN`). Página con todas las plataformas: `https://distrokid.com/hyperfollow/nordicreign/before-the-end-begins-2` (en enlaces del canal de YouTube; Alfonso la pone en IG desde el móvil; TikTok no permite enlace hasta 1.000 seguidores). Letras de las 9 canciones subidas en DistroKid (plan gratis: Apple, YouTube, Google, Amazon, Deezer, Shazam; Spotify/IG necesitarían Lyric Blaster, 18,99 €/año). Errata de la pista 7 corregida a «Hall of Illusions» (pendiente de aprobación de DistroKid). Content ID / Social Media Pack de DistroKid: no contratado. Cuenta de artista de TikTok: solicitada por Alfonso. Canal oficial de artista de YouTube: falta un vídeo normal (no Short) subido por él → lyric video.

## Métricas (4–9 nov, 6 vídeos)
- TikTok ≈2.040 vistas, YouTube ≈914, Instagram ≈341.
- Lo que mejor funciona: palabras/etimología en TikTok y YouTube (916 y 636); en Instagram, la saga con voz y pintura (Ep. 1: 137 vistas, 6 likes, 3 guardados). Solo texto se hunde en Instagram.
- En Instagram el 55 % se va antes de 3 s → desde el 10 nov el gancho se ve en el fotograma 0.

## Decisiones tomadas
- Publicar en las 3 redes; Alfonso contrata Metricool Starter mensual (20 €/mes + IVA). El gratis solo permite 20 publicaciones/mes y cada red cuenta aparte.
- Voz en la saga y en Hávamál, marcadas como IA en las tres redes.
- Figuras solo en pinturas de dominio público; el código solo dibuja ambiente. Alfonso responde los comentarios.

- 10 nov (tarde): vídeos sin voz del 12–23 nov con canción (`*_m.mp4`); extras programados: carrusel tatuaje Ep. 2 (13 nov 13:00), reel «Pause to find your rune» (15 nov 13:00), carrusel «5 things Vikings never did» (18 nov 13:00). Carruseles añadidos como serie fija en el PLAYBOOK. Lyric video de Nine Days Below hecho (`engine/lyric_nine_days_below.py`; MP4 en `C:\Nordic Reign\videos\` con título y descripción en `youtube-nine-days-below.txt`). Bio y cabecera de Spotify en `C:\Nordic Reign\spotify\`, pendientes de su OK. Recordatorio programado el 9 dic para sacar las 6 instrumentales restantes.

## Pendiente de Alfonso
1. ✔ Metricool Starter activo (10 nov, prueba de 30 días con código; luego 24,20 €/mes con IVA). Página de Facebook «Nordic Reign» creada (id 61596413761887) y conectada; Instagram conectado a Metricool vía Facebook. Competidores añadidos: The Viking Chronicles (144K) y Runar (78K). Audio oficial de IG vía Metricool: las canciones de Nordic Reign NO aparecen en el catálogo de la API (probado 10 nov; «Nordic Reign» devolvió otra canción → nunca buscar por artista sin comprobar `displayArtist`). Se sigue con el audio incrustado.
1b. Subir a YouTube el lyric video de Nine Days Below (archivo y textos en `C:\Nordic Reign\videos\`); después Claude pide el Canal Oficial de Artista en DistroKid.
1c. Aprobar bio y cabecera de Spotify (Claude las sube a Spotify for Artists).
1d. Instagram: enlace HyperFollow en la bio y música del perfil (Nine Days Below), desde el móvil.
2. ✔ Canciones (10 nov): fragmentos de 75 s en `audio/`; instrumentales Ep. 6, 7 y 9; Content ID no contratado (no hace falta lista blanca). Queda: ¿Instagram conectado a una página de Facebook? (para poner su canción oficial en los Reels vía Metricool).
3. ✔ Propuesta de mejoras aprobada el 10 nov («tira con todo»): reel de runas y carruseles hechos; falta el resumen mensual de noticias (1 dic) y lo de «más adelante».
4. Pasar más cuentas de referencia.

## Propuesta (aprobada el 10 nov) (tras analizar runar.hall y thevikingchronicles)
- Reel de prueba «Pause and find your rune» (24 runas pasando rápido, nombre y significado literal; Perthro = «meaning unknown»), publicación extra.
- 2 carruseles por semana en Instagram y TikTok (Myth vs History y el tatuaje del capítulo con su historia).
- Resumen mensual de noticias vikingas, el primero el 1 de dic.
- Más adelante: colaboraciones (a partir de 1–2 mil seguidores), página de enlaces de Metricool en la bio, destacados (Tatuajes, Saga, Música), categoría «Artista», newsletter.
- Cuando Starter esté activo: añadir como competidores en Metricool runar.hall, thevikingchronicles y las que pase Alfonso.
