# Nordic Reign · estado y traspaso (16 nov 2026)

Léelo entero antes de trabajar. La fuente de verdad del día a día es `PLAYBOOK.md` del repositorio.

## Dónde está todo
- Repositorio público: https://github.com/alfonsogervascastro/nordic-reign-media (clonar; contiene motor de vídeo, PLAYBOOK, vídeos publicados, métricas). Commits con usuario "Claude <noreply@anthropic.com>".
- `PLAYBOOK.md`: series, plantilla de vídeo (checklist obligatorio), reglas de rigor, voz, imágenes, cómo programar en Metricool, registro de publicaciones, pendientes.
- `engine/`: motor (nr.py, narrate.py = voz Kokoro, scenes.py) y un script por vídeo (v01…v18). `tattoos/`: motor de nudos, designs.py, designs_saga.py, make_pack.py.
- `metrics/`: informes (último: 2026-11-10.md).
- Tarea programada `trig_017Znei3Nj9dwixTMzMs9WhE`: domingos 10:56 (Madrid), sigue el PLAYBOOK. 8 y 15 nov: solo métricas. 22 nov: produce la semana 24–30.
- Metricool: brand id 7741806, zona Europe/Madrid. TikTok exige `tiktokData.title`. Máx. 5 hashtags. Portada propia con `videoThumbnailUrl` (`engine/covers.py`), primer comentario con `firstCommentText`, historia diaria de IG a las 18:30 (ver PLAYBOOK, «Cómo producir y programar», pasos 7–9).

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
- 10 nov (noche), horas: desde el 16 nov, YouTube Shorts a las 16:00 en publicación aparte, Instagram + TikTok a las 18:00; carruseles y extras a las 12:00 entre semana y 10:00 en fin de semana (ya cambiados los del 13, 15, 18 y 21). Línea base 11–15 nov a las 19:00; decidir el 6 dic. Textos de las runas 2 y 3 cambiados a pregunta de opinión. Facebook: Alfonso dice que NO se publica allí. **TikTok: cuenta de artista APROBADA (11 nov, 0:16)** — pestaña de música y etiqueta de artista activas. SmartLink creado (10 nov): **https://t.mtrbio.com/nordicreign** (fondo oscuro, botones dorados: álbum en HyperFollow y Spotify; iconos TikTok, Instagram, YouTube; el botón de YouTube se quitó el 11 nov por estar repetido con el icono). Falta que Alfonso lo ponga en la bio de Instagram y TikTok. Cuando haya tienda de Etsy: añadir botón «Tattoo designs» al SmartLink (Metricool → SmartLinks) y montar Pinterest con los diseños.
- 11 nov: **semana del 24 al 30 producida y programada** (17 publicaciones verificadas: nombre FREYA con IG en aviso al móvil para elegir canción oficial; Ep. 6 Nine Nights y Ep. 7 ojo + cuervos con voz e instrumentales; «rune» = secreto; REAL VIKINGS Birka Bj 581; Hávamál 47 con voz; Ansuz; carruseles Vinland (25) y tatuaje Ep. 6 (27)). Todo programado hasta el **lunes 7 dic** (semana 1–7 dic producida también el 11 nov: INGRID, Ep. 8 hidromiel, Óðinn = furia, berserkers, Ep. 9 muralla, Hávamál 1, Raidho; carruseles grafitis vikingos y tatuaje Ep. 7). Domingos 15 y 22: solo métricas; domingo 29: métricas + carrusel de noticias del 1 dic; domingo 6 dic: semana 8–14 dic. Nuevas pinturas de dominio público (Engels, Stolpe, Winge, Doepler, E. Boyd Smith) y `engine/lyric_video.py` genérico para los 7 lyric videos que faltan: **pendientes de que el ordenador de Alfonso esté enlazado** (hacen falta los WAV y los tiempos de Suno vía Chrome). TikTok: el Prólogo (0 vistas en 6 días) y Fehu (0) no se distribuyeron; motivo desconocido.

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

## 15 nov (tarea del domingo, solo métricas)
- Informe en `metrics/2026-11-15.md`. Seguidores: IG 56, TikTok 2, YouTube 1 (las tres por debajo del escenario pesimista del mes 1; IG cerca). Vistas 8–14 nov: IG 577, TikTok 1.502, YouTube 1.417 (YouTube solo hasta el 12; Metricool va con retraso).
- Mejores: Words «window, sky, egg» (YouTube 625), Saga Ep. 2 (IG 149), Tolkien (IG 123). Peores: carrusel tatuaje Ep. 2 (IG 8, TikTok 1), Fehu en TikTok (2), cuernos en IG (11).
- **Problema:** TikTok da ~250 vistas a cada vídeo y no empuja más (7 de 8 vídeos entre 235 y 275); Fehu y el Prólogo no se distribuyeron. Pedir a Alfonso que mire la retención en la app de TikTok.
- Línea base de horas (11–14 nov a las 19:00): mediana IG 106, TikTok 248; YouTube pendiente de datos. `getBestTimeToPostByNetwork` sin cambios (TikTok 10/12/18 h, YouTube 16 h, IG sin datos).
- Verificado con `getScheduledPosts`: 16–22 nov completo (cada día YouTube 16:00 + IG/TikTok 18:00; carruseles 18 nov 12:00 y 21 nov 10:00; nada en Facebook). Extra «Pause to find your rune» publicado hoy a las 10:00 en las tres redes; Hávamál 76 pendiente a las 19:00.
- Siguiente: 22 nov solo métricas (comparar horas); 29 nov métricas + carrusel de noticias del 1 dic; 6 dic fijar horas y producir 8–14 dic.

## 16 nov (Alfonso vuelve de vacaciones)
- **Revisión de resultados:** vistas totales IG ≈1.060, TikTok ≈3.800 (atascado en ~250 por vídeo), YouTube ≈1.580. Seguidores: IG 56, TikTok 2, YouTube 1. Tasa de salto en IG 53–71 %. Mejor serie: Words from the North (media ≈940). El carrusel fracasó (9 vistas). Prólogo y Fehu: 0–2 vistas en TikTok (Alfonso lo confirma con capturas; no hay aviso de infracción).
- **Competidores nuevos** (IA, misma idea): ancient.chapters (16 seguidores, sigue el mismo orden de la saga con imágenes de IA) y whispers.of.yggdrasil (60, frases motivacionales). Alfonso: «Me parece bien» añadirlos en Metricool → pendiente, necesita Chrome.
- **Herramientas evaluadas:** Lemo Opuscar sí, para piezas especiales (necesita ffmpeg 7; el contenedor tiene 6.1, instalar binario estático). SkillSpector útil; Ponytail menor; FreeLLMAPI y Agent Reach no.
- **Mejoras aprobadas («Ponte a ello pues», puntos 1, 2 y 5) — HECHAS el 16 nov:**
  1. Portadas propias para todos los reels IG + TikTok del 16 nov al 7 dic (`engine/covers.py`, `AAAA-MM/covers/`), subidas con `videoThumbnailUrl`.
  2. Historia diaria de Instagram a las 18:30 del 16 nov al 7 dic (22 historias, imagen `<fecha>_story.jpg` con «NEW TODAY / Watch it on our profile»).
  5. Primer comentario automático en todas las publicaciones IG + TikTok del 16 nov al 7 dic (plantillas en el PLAYBOOK).
- Los demás puntos propuestos quedan para Alfonso o para cuando haya ordenador: fijar 3 publicaciones en IG y TikTok; nueva bio (propuesta: «Norse myths & Viking history, from the original sources. / Real 19th-century art. Our own Viking metal. / The Norse Saga starts here ↓»); SmartLink en las bios; responder comentarios en la primera hora; listas de reproducción de YouTube (The Norse Saga, Runes, Words from the North) y recopilatorio «Episodes 1–5» (necesitan Chrome); posible colaboración con whispers.of.yggdrasil.
- **Lyric videos: HECHOS los 7 (16 nov)** sin Suno: tiempos sacados del audio (separación de voz + reconocimiento, `engine/align/`; ver PLAYBOOK). Están en `C:\Nordic Reign\videos\` con su `youtube-<slug>.txt` (fecha sugerida: el día antes de cada episodio). Los sube Alfonso.
- **Navegador (16 nov):** Chrome no conectado (Alfonso en el móvil) y el navegador de la app de Claude sin sesión en Instagram, Metricool ni YouTube. Competidores ancient.chapters y whispers.of.yggdrasil AÑADIDOS en Metricool (16 nov, 22:20). Bio de Instagram CAMBIADA (16 nov). Fijar publicaciones: no se puede desde la web, lo hace Alfonso en el móvil (Tolkien, nombre en runas, Prólogo). Bio de TikTok CAMBIADA (17 nov): «Norse myths & Viking history from the original sources. Saga starts here ↓» (TikTok no deja enlace hasta 1.000 seguidores). listas de YouTube y comprobar el Canal Oficial de Artista en DistroKid.
- Posible mejora: la separación de voz también saca instrumentales de todas las canciones sin gastar descargas de Suno (calidad algo menor que los stems de Suno); útil para el Ep. 10 (Born in the Dark) que se produce el 6 dic.

## Público por país (16 nov)
- Alfonso: «donde veas que tiene más cabida». Objetivo: angloparlantes (EE. UU., Reino Unido) + Norte de Europa (países nórdicos, Alemania). Noruega sola es demasiado pequeña.
- **Datos reales (TikTok Studio, 17 nov, últimos 7 días, 1.400 espectadores):** Alemania 21,3 %, Reino Unido 10,1 %, Hungría 8,5 %, España 7,6 %, Rumanía 5,8 %, Países Bajos 5,3 %, Polonia 4,5 %, Austria 3,6 %, Noruega 2,8 %, Irlanda 2,8 %. 61 % hombres; 85 % entre 18 y 34. **La hipótesis de «solo España» era falsa**: TikTok ya reparte por toda Europa. El problema es otro: los espectadores son público general (ven a Ibai, McDonald's, Burger King), no gente de mitología, y se van pronto. Estados Unidos no aparece (TikTok separa Europa y EE. UU.). Actividad máxima: 0–1 h.
- Instagram sigue sin dar países (necesita 100 seguidores).
- Palancas propuestas: (1) idioma del vídeo = inglés en YouTube Studio; (2) prueba de TikTok a las 01:00 de Madrid (19:00 Nueva York) a decidir el 6 dic con las horas; (3) promoción pequeña de un reel en Instagram dirigida a EE. UU./Reino Unido/nórdicos (decisión y dinero de Alfonso).

## YouTube (17 nov)
- Creadas 3 listas públicas: «The Norse Saga: All Episodes in Order» (orden: más antiguo primero; Prólogo, Ep. 1–3), «Runes: the Elder Futhark, One by One» (Fehu, Uruz, runa por fecha, nombre en runas) y «Words from the North: Old Norse in Your Language» (semana, Old Norse diario, Tolkien). Ya existían «Nordic Reign» (3 lyric videos) y una privada antigua.
- Metricool no permite elegir lista al programar: los Shorts nuevos hay que añadirlos a mano (YouTube Studio → Contenido → Shorts → marcar → «Añadir a lista»). Hacerlo cada domingo con Chrome.
- Los 7 lyric videos nuevos aún no están subidos (los sube Alfonso). Cuando estén, añadirlos a la lista «Nordic Reign».

- Canal Oficial de Artista de YouTube: **solicitado el 17 nov** vía DistroKid (artista Nordic Reign → canal @nordic-reign). DistroKid confirma «submitted to YouTube»; YouTube avisará por correo (de unos días a 6 semanas). Unirá el canal «Nordic Reign - Topic» (creado solo por la distribución) con @nordic-reign. Es irreversible.

## 17 nov
- **TikToks a cero:** Prólogo (0), Fehu (2), carrusel de tatuaje del 13 nov (1), «Pause the video» del 15 nov (1); el resto ronda 235–275 (y 857–916 los dos primeros). En TikTok Studio web no aparece ningún aviso (las estadísticas solo dicen que se marcharon en el segundo 2). Hay que mirarlo en la app del móvil (vídeo → ··· → Estadísticas): si pone «no apto para el feed Para ti», pedir revisión. Pedido a Alfonso.
- **Recopilatorio YouTube** (16:9, `engine/compilation.py`): «The Norse Saga: Prologue and Episodes 1–5», 3:55 con capítulos, programado en Metricool para el **domingo 22 nov a las 12:00** (solo YouTube, vídeo normal). Archivo: `2026-11/2026-11-22_saga_compilation_prologue-ep05.mp4`. Añadirlo a la lista «The Norse Saga» cuando se publique.
- **Instrumentales HECHAS** de las 6 canciones con voz (separando la voz): `audio/<slug>_inst.mp3` (fragmentos) y `C:\Nordic Reign\mp3\instrumental\` (enteras). El recordatorio del 9 dic queda como opcional (stems oficiales de Suno).
- Alfonso pagará Metricool cuando acabe la prueba (no hace falta comparar opciones).
- **Lyric videos en YouTube (17 nov):** Alfonso subió y programó los 9 que faltaban (16:00): Odin's Sacrifice 27 nov, Inside the Lie 4 dic, Born in the Dark 8 dic, Forge 15 dic, Bride 18 dic, Hall 22 dic, Thunder 25 dic, Chains 5 ene, Before the End Begins (Visualizer) 8 ene. Lista «Nordic Reign». Uso de IA = «Sí» (YouTube ahora pide declararlo cuando la música hecha con IA es lo principal del vídeo). Remezcla de Shorts: solo audio.

## 20 nov
- Týr («This god's name just means god», Words from the North) = mejor reel de IG: 457 vistas en 1 día, 17 me gusta. IG 64 seguidores (+7 en la semana).
- Ep. 4 en IG: 3 espectadores en 2 días (en YouTube 151, en TikTok 228). Estado de la cuenta de IG limpio (sin límites de recomendación). Causa desconocida; por precaución, **evitar cuadros con desnudos en Instagram** (anotado en el PLAYBOOK).
- Publicaciones fijadas por Alfonso. Carruseles: se dejan también en TikTok de momento. Nada más que cambiar hasta revisar la semana del 24 al 30.

## 21 nov
- Reescalados con Real-ESRGAN los 16 cuadros de menos de 1.500 px (originales en images/original/).
- Voz de la cuenta: nunca «we/our/us». Cambiado en todo lo programado hasta el 7 dic (textos, primeros comentarios, 17 historias, 4 carruseles, vídeo de Birka), en las descripciones de YouTube (4 Shorts publicados y 10 vídeos con letra) y en 4 pies de foto de IG. No se puede cambiar: pies de TikTok ya publicados y primeros comentarios ya publicados.
- Comentario de @fakehistoryhunter en el vídeo del baño: respuesta propuesta y regla de rigor nueva (no suavizar fuentes).
- 3D (NR_PARALLAX): DESCARTADO. Alfonso vio el test x3: en Thor se nota poco y en Týr no aporta. El código se queda en el repo sin usar.
- Tarde del 21 nov («tira con todo»): gancho nuevo (`engine/hook.py`) en los 8 vídeos del 22 al 30 nov (todo menos FREYA), sustituido en IG/TikTok y YouTube; 8 reels de prueba de IG con gancho-pregunta a las 21:00 (22–30 nov); vídeo de corrección del baño: descartado por Alfonso (queda en borrador en Metricool, no se publica; él ya respondió el comentario). Reglas nuevas en el PLAYBOOK («Cambios del 21 nov»). Comparar A/B el domingo 29.

## 22 nov (tarea del domingo, solo métricas)
- Informe en `metrics/2026-11-22.md`. Seguidores: IG 66 (+10), TikTok 3, YouTube 5 (+4). Vistas de la cuenta en IG 1.114 (+84 % sobre la semana anterior). Týr = mejor reel de la cuenta (IG 470, salto 45 %, +5 seguidores ese día; YouTube 485).
- Horas (vs. línea base 11–15 nov): TikTok igual (~240, la hora no es el problema); YouTube 16:00 con señal positiva en la saga (Ep. 4 201 vs Ep. 2–3 59–76); Instagram sin conclusión (manda la serie). Base de YouTube completada (mediana 365, inflada por Tolkien y cuernos). `getBestTimeToPostByNetwork` sin cambios. Se decide el 6 dic.
- Portadas / primer comentario / historias: salto medio en IG 65 % → 58 %, pero se explica por los temas (Týr, Ep. 5). El «1 comentario» por reel es casi seguro el nuestro. Visitas al perfil: Metricool ya no las da. Historias: Metricool solo registra la del 16 (5 de alcance); las demás con 0 y **la del 20 nov no aparece** → que Alfonso lo mire en la app.
- Nuevos fallos en TikTok: SIGRID (2 vistas) y las 24 runas (1) tampoco se distribuyeron; los dos carruseles, 10 y 24.
- Verificado 22–30 nov con `getScheduledPosts`: completo y nada en Facebook (detalle en el informe).
- Siguiente: domingo 29 nov, métricas + comparación A/B de ganchos + carrusel de noticias del 1 dic 12:00.
