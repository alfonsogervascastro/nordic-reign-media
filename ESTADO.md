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

## Revisión del 10 nov (noche)
- La tarea del domingo 8 FALLÓ por límite de uso de la cuenta (el informe de métricas se hizo a mano). Prompt de la tarea `trig_017Znei3Nj9dwixTMzMs9WhE` actualizado el 10 nov: lee ESTADO + PLAYBOOK, respeta los domingos «solo métricas», produce vídeo diario + 2 carruseles + reel de audio oficial + noticias mensuales, y verifica «un vídeo a las 19:00 más extras a las 13:00».
- Comprobaciones de respaldo programadas en esta conversación: 15 nov 13:30 (métricas) y 22 nov 14:00 (producción 24–30 nov). Recordatorios: 13 nov 19:30 (Canal Oficial de Artista) y 9 dic (instrumentales).
- Clon limpio probado: carousel.py, designs.py y v19 funcionan siguiendo el PLAYBOOK. Textos de tatuaje para carruseles de los Ep. 2–7 listos; carruseles Ep. 6 y 7 ya generados.
- Lyric video de Odin's Sacrifice: `engine/lyric_odins_sacrifice.py`; MP4 y textos en `C:\Nordic Reign\videos\` para que Alfonso lo suba (programado el 27 nov, antes del Ep. 7).

## 10 nov (cierre)
- Competidores en Metricool. Instagram: The Viking Chronicles, Runar, Viking History, Viking Spirits, SAGASTAD, Wardruna, Amon Amarth. YouTube (máx. 10): Jackson Crawford, Arith Härger, Nordic Mythology Podcast, North Mythology. Metricool no permite competidores de TikTok.
- Lyric videos listos en `C:\Nordic Reign\videos\` (MP4 + textos para YouTube): Odin's Sacrifice (programar para el 27 nov) e Inside the Lie (para el 4 dic). Scripts: `engine/lyric_*.py`; los tiempos por palabra salen de Suno (`aligned_lyrics`, con la sesión de Alfonso en Chrome).
- Fotos de la ficha de Etsy (10, 3000×2250, con marca de agua) en `C:\Nordic Reign\pack\etsy\`; script `tattoos/etsy_images.py`.
- Orden oficial del álbum anotado en el PLAYBOOK («Música»); `letras.md` reordenado según el álbum.

## Métricas (4–9 nov, 6 vídeos)
- TikTok ≈2.040 vistas, YouTube ≈914, Instagram ≈341.
- Lo que mejor funciona: palabras/etimología en TikTok y YouTube (916 y 636); en Instagram, la saga con voz y pintura (Ep. 1: 137 vistas, 6 likes, 3 guardados). Solo texto se hunde en Instagram.
- En Instagram el 55 % se va antes de 3 s → desde el 10 nov el gancho se ve en el fotograma 0.

## Decisiones tomadas
- Publicar en las 3 redes; Alfonso contrata Metricool Starter mensual (20 €/mes + IVA). El gratis solo permite 20 publicaciones/mes y cada red cuenta aparte.
- Voz en la saga y en Hávamál, marcadas como IA en las tres redes.
- Figuras solo en pinturas de dominio público; el código solo dibuja ambiente. Alfonso responde los comentarios.

- 10 nov (tarde): vídeos sin voz del 12–23 nov con canción (`*_m.mp4`); extras programados: carrusel tatuaje Ep. 2 (13 nov 13:00), reel «Pause to find your rune» (15 nov 13:00), carrusel «5 things Vikings never did» (18 nov 13:00). Carruseles añadidos como serie fija en el PLAYBOOK. Lyric video de Nine Days Below hecho (`engine/lyric_nine_days_below.py`; MP4 en `C:\Nordic Reign\videos\` con título y descripción en `youtube-nine-days-below.txt`). Bio y cabecera de Spotify en `C:\Nordic Reign\spotify\`, pendientes de su OK. Recordatorio programado el 9 dic para sacar las 6 instrumentales restantes.
- 10 nov (noche), tras analizar competidores: (1) viernes alternos **REAL VIKINGS** (persona o tumba real con su fuente; primera el viernes 27 nov) y **MYTH vs HISTORY** (vuelve el 4 dic), con banco de temas en el PLAYBOOK; (2) carrusel «Were Vikings tattooed?» (Ibn Fadlan 922, «posible, no probado», cierra con los diseños de la saga) programado el **sábado 21 nov 13:00** en IG + TikTok (`python3 carousel.py tattooed`); (3) regla del PLAYBOOK: vídeos, textos y última diapositiva terminan con pregunta de opinión o identidad, no de examen.

## Pendiente de Alfonso
1. ✔ Metricool Starter activo (10 nov, prueba de 30 días con código; luego 24,20 €/mes con IVA). Página de Facebook «Nordic Reign» creada (id 61596413761887) y conectada; Instagram conectado a Metricool vía Facebook. Competidores añadidos: The Viking Chronicles (144K) y Runar (78K). Audio oficial de IG vía Metricool: las canciones de Nordic Reign NO aparecen en el catálogo de la API (probado 10 nov; «Nordic Reign» devolvió otra canción → nunca buscar por artista sin comprobar `displayArtist`). Se sigue con el audio incrustado.
1b. ✔ Lyric video de Nine Days Below subido por Alfonso: https://youtu.be/MYLzjeOEj0k. El formulario del Canal Oficial de Artista en DistroKid aún no aparecía el 10 nov (falta que DistroKid detecte el lanzamiento en YouTube); recordatorio programado el 13 nov 19:30 para volver a intentarlo.
1c. ✔ Spotify for Artists (10 nov): bio, cabecera (tarda hasta 72 h) y enlaces a Instagram, Facebook y TikTok publicados.
1d. ✔ Instagram: enlace HyperFollow en la bio y Nine Days Below como música del perfil (hecho por Alfonso). Sus canciones salen en la app con la cuenta de Empresa.
1e. Pendiente (cuando Alfonso quiera): tienda de Etsy y gestor; TikTok artist account (en revisión).
2. ✔ Canciones (10 nov): fragmentos de 75 s en `audio/`; instrumentales Ep. 6, 7 y 9; Content ID no contratado (no hace falta lista blanca). Queda: ¿Instagram conectado a una página de Facebook? (para poner su canción oficial en los Reels vía Metricool).
3. ✔ Propuesta de mejoras aprobada el 10 nov («tira con todo»): reel de runas y carruseles hechos; falta el resumen mensual de noticias (1 dic) y lo de «más adelante».
4. Pasar más cuentas de referencia.

## Propuesta (aprobada el 10 nov) (tras analizar runar.hall y thevikingchronicles)
- Reel de prueba «Pause and find your rune» (24 runas pasando rápido, nombre y significado literal; Perthro = «meaning unknown»), publicación extra.
- 2 carruseles por semana en Instagram y TikTok (Myth vs History y el tatuaje del capítulo con su historia).
- Resumen mensual de noticias vikingas, el primero el 1 de dic.
- Más adelante: colaboraciones (a partir de 1–2 mil seguidores), página de enlaces de Metricool en la bio, destacados (Tatuajes, Saga, Música), categoría «Artista», newsletter.
- Cuando Starter esté activo: añadir como competidores en Metricool runar.hall, thevikingchronicles y las que pase Alfonso.
