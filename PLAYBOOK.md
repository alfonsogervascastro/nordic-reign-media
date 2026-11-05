# Nordic Reign — playbook de vídeos

Este repositorio aloja los vídeos que se publican en Instagram y YouTube a través de Metricool, y el motor que los genera. Es la fuente de verdad para la tarea semanal.

## Idea central

La cuenta cuenta una historia, no curiosidades sueltas. La columna es **The Norse Saga**: la mitología nórdica en orden, del vacío inicial al Ragnarök, en episodios numerados (miércoles y sábado). El resto de series de la semana gira alrededor del episodio en curso siempre que se pueda. Quien entra en el perfil debe poder seguir la historia y reconocer cada serie de un vistazo.

## Cuentas

- Marca Metricool: `nordicreignofficial`, blogId `7741806`, zona horaria `Europe/Madrid`.
- Redes enlazadas: Instagram (Reel), YouTube (Short) y TikTok (cuenta "Nordic Reign", enlazada el 4 nov). Cada vídeo se publica en las tres.
- Usuario en los vídeos: `@nordicreignofficial`.
- Publicación: un vídeo al día a las 19:00 (Europe/Madrid).

## Series y semana tipo (de martes a lunes)

| Día | Serie (etiqueta `nr.Label`) | Contenido |
| --- | --- | --- |
| Martes | `YOUR NAME IN RUNES` | Nombres de `names.txt` (si está vacío, 5–6 nombres populares variados) |
| Miércoles | `THE NORSE SAGA` · `EP. n` | Siguiente episodio de la lista |
| Jueves | `WORDS FROM THE NORTH` | Palabras/etimología, a ser posible del episodio de la semana |
| Viernes | `MYTH vs HISTORY` | Qué dicen las fuentes o la arqueología, a ser posible sobre el episodio |
| Sábado | `THE NORSE SAGA` · `EP. n` | Siguiente episodio |
| Domingo | `HÁVAMÁL` | Una estrofa del Hávamál (Bellows, 1923) o un kenning |
| Lunes | `RUNE` · `n / 24` | Siguiente runa del Futhark |

Cada vídeo lleva su etiqueta de serie arriba durante todo el vídeo. Cada episodio de la saga termina con "Episode n+1: <día>  ·  @nordicreignofficial", y su texto de publicación dice "The Norse Saga, episode n. Start from the prologue on our profile."

## Episodios de The Norse Saga

Fuente principal: Snorri Sturluson, Prose Edda (Gylfaginning, Skáldskaparmál) y Poetic Edda (Völuspá, Hávamál, Þrymskviða, Lokasenna, Baldrs draumar). Cuando un episodio tiene canción, usarla como banda sonora si existe en `audio/` (ver Música).

| Ep. | Tema | Canción | Estado |
| --- | --- | --- | --- |
| Prólogo | Gleipnir: la cadena imposible y Fenrir | Born in the Dark | ✔ 2026-11-04 |
| 1 | Ginnungagap, Ymir, Auðumbla, Búri → Odín | — | ✔ 2026-11-07 |
| 2 | Odín, Vili y Vé matan a Ymir y hacen el mundo con su cuerpo | — | ✔ 2026-11-11 |
| 3 | Yggdrasil y los nueve mundos | — | ✔ 2026-11-14 |
| 4 | Ask y Embla, los primeros humanos | — | |
| 5 | La guerra entre Æsir y Vanir | — | |
| 6 | Odín, nueve noches colgado de Yggdrasil: el origen de las runas | Nine Days Below | |
| 7 | Odín entrega su ojo en el pozo de Mímir | Odin's Sacrifice | |
| 8 | Kvasir y el hidromiel de la poesía | — | |
| 9 | La muralla de Asgard y el nacimiento de Sleipnir | Inside the Lie | |
| 10 | Los hijos de Loki: Fenrir, Hel, Jörmungandr | Born in the Dark | |
| 11 | La atadura de Fenrir y la mano de Týr (enlaza con el prólogo) | Born in the Dark | |
| 12 | El pelo de Sif y la forja de Mjölnir | Forge of Svartalfheim | |
| 13 | Thor vestido de novia | The Bride in Thunder | |
| 14 | Las ilusiones de Útgarða-Loki | Hall of Illusions | |
| 15 | Thor pesca a Jörmungandr | Thunder of the Gods | |
| 16 | Las manzanas de Iðunn | — | |
| 17 | Los sueños y la muerte de Baldr | — | |
| 18 | Loki atado bajo la montaña, Sigyn | Chains Beneath the Mountain | |
| 19 | Fimbulvetr y las señales del fin | Before the End Begins | |
| 20 | Ragnarök I: los gigantes marchan, Odín cae ante Fenrir | Before the End Begins | |
| 21 | Ragnarök II: Thor y Jörmungandr, Surtr quema el mundo | — | |
| 22 | El mundo renace | — | |

## Música

Las 10 canciones actuales se hicieron con el plan gratuito de Suno: **no usarlas** hasta que existan versiones remezcladas con plan de pago en `audio/` (nombre de archivo en minúsculas con guiones, p. ej. `audio/nine-days-below.mp3`). Si existe, pasarla a `nr.render(..., music="../audio/<archivo>.mp3", music_start=<segundo>)` y añadir al texto de publicación "Soundtrack: <canción> by Nordic Reign". Si no existe, usar el fondo generado.

## Tatuajes (pack de diseños)

Cada episodio de la saga tiene su diseño de tatuaje en **nudo vikingo** que cuenta la historia del episodio con un símbolo. Se generan con `tattoos/designs.py` (motor de entrelazado en `tattoos/knots.py`: cualquier curva se dibuja como banda con cruces alternos por encima/por debajo). Cada diseño produce: plantilla negra transparente de 3000 px, versión sobre blanco, vista previa oro sobre carbón y una tarjeta 1080×1350 con la historia.

| Episodio | Diseño | Símbolo | Estado |
| --- | --- | --- | --- |
| Prólogo | Gleipnir | Brazalete trenzado con Tiwaz | ✔ |
| 1 | Ginnungagap | Roseta alrededor del vacío, Isa y Kenaz | ✔ |
| 2 | Ymir's World | Nudo de cuatro lazos | ✔ |
| 3 | Yggdrasil | Tronco trenzado con tres copas y tres raíces | ✔ (mejorable con IA) |
| 4 | Ask & Embla | Dos troncos entrelazados | ✔ |
| 5 | The First War | Dos anillos unidos atravesados por Gungnir | ✔ |
| 6 | Nine Nights | Nudo de nueve lazos con Ansuz | ✔ |
| 7 | Thought & Memory | Huginn y Muninn (IA) sobre un nudo | ✔ |
| 8 | The Mead of Poetry | Cuerno con bandas entrelazadas | ✔ (mejorable con IA) |
| 9 | Sleipnir | Nudo de ocho lazos con Ehwaz | ✔ (mejorable con IA) |
| 10 | Born in the Dark | Trébol de tres lazos | ✔ |
| 11 | The Binding of Fenrir | Gleipnir cerrado en anillo con Tiwaz | ✔ (mejorable con IA) |
| 12 | Mjölnir | Silueta de colgante con nudo | ✔ |
| 13 | The Bride in Thunder | Mjölnir entre dos anillos | ✔ |
| 14 | Hall of Illusions | Nudo (3,5) | ✔ |
| 15 | Jörmungandr | Cuerpo trenzado + cabeza de dragón (IA) | ✔ |
| 16 | Iðunn's Apples | Cinco anillos entrelazados | ✔ |
| 17 | Baldr | Anillo de luz atravesado por el dardo | ✔ |
| 18 | Chains Beneath the Mountain | Arco de eslabones y gota de veneno | ✔ |
| 19 | Fimbulvetr | Nudo de seis lazos con Hagalaz | ✔ |
| 20 | Ragnarök | El anillo del lobo atrapa al sol (Sowilo) | ✔ (mejorable con IA) |
| 21 | Nine Steps | Mjölnir dentro de la serpiente | ✔ |
| 22 | The World Rises Again | Sol con Dagaz sobre mar trenzado | ✔ |

Todos los diseños de la saga están hechos (`tattoos/designs.py`, `tattoos/designs_saga.py`, resultado en `tattoos/out/`). La tarea semanal **no crea diseños nuevos**: usa el del episodio que toque. Solo si se añade un episodio que no esté en la tabla, crea uno geométrico siguiendo los ejemplos.

**Diseños con figura (cabezas de animales, cuervos, lobos):** la IA solo dibuja la cabeza o la figura y el motor hace el cuerpo entrelazado (ejemplo: `jormungandr()` y `tattoos/ai/README.md`). La generación con IA necesita el token de Hugging Face de Alfonso, que no se guarda en el repositorio, así que esos diseños se preparan por adelantado en sesiones con Alfonso; la tarea semanal solo los usa si ya existen. Si un episodio necesita figura y no hay diseño preparado, la tarea hace un diseño geométrico.

Para cada episodio nuevo: crea su diseño en `designs.py` antes de producir el vídeo (función con la curva, runas si aplican, título, capítulo y 4 líneas de historia en inglés). Reglas: geometría limpia, sin figuras humanas ni animales dibujados por código, nada de Othala alada, Sowilo doble ni Wolfsangel. **El vídeo del episodio termina con 3 s del diseño**: el dibujo en oro aparece sobre el fondo con el texto "This chapter, as a tattoo" y "Save it for your next tattoo". Guarda los archivos del diseño en `tattoos/out/<slug>/`.

**Cómo poner el cierre del tatuaje en el vídeo:** `END = nr.TattooEnd("../tattoos/out/<slug>/<slug>_gold.png", t0=DUR - 3.2)` y, al final de `frame()`, `END.draw(img, t)` (lo último, porque oscurece todo lo de detrás). Alarga `DUR` unos 3 s y termina las demás tarjetas antes de `t0`. Ejemplos: `v08_saga02.py`, `v10_saga03.py`.

**`tattoos/out/` y `tattoos/pack/` no están en el repositorio a propósito** (el repo es público y los diseños son el producto de pago). En una sesión nueva, antes de renderizar un episodio, genera su diseño: `cd tattoos && python3 designs_saga.py ep04` (episodios 3–22 salvo el 15) o `python3 designs.py ymir` (prólogo `gleipnir`, 1 `ginnungagap`, 2 `ymir`, 15 `jormungandr`). Nunca subas al repo los PNG de los diseños ni el PDF del pack.

**Pack de venta:** `python3 tattoos/make_pack.py` genera `tattoos/pack/NordicReign_NorseSaga_TattooPack.pdf` (portada, licencia de uso personal, índice y dos páginas por diseño: historia y plantilla) y `NordicReign_NorseSaga_Stencils.zip` (plantillas de 3000 px con fondo transparente). Si se mejora un diseño con IA, vuelve a generar el pack.

## Métricas semanales (cada domingo, antes de producir)

1. Con Metricool (`getAnalyticsAvailableMetrics` y `getAnalyticsDataByMetrics`, blogId 7741806) lee los últimos 7 días de Instagram, TikTok y YouTube: seguidores, visualizaciones por vídeo, guardados, compartidos, comentarios y, si existen, retención o tasa de salto.
2. Compáralo con los escenarios (mes contado desde el 2 nov 2026):

| Red | Escenario | Mes 1 | Mes 3 | Mes 6 | Mes 12 |
| --- | --- | --- | --- | --- | --- |
| Instagram (seguidores) | Pesimista / Más probable / Optimista | 100 / 300 / 1.500 | 300 / 1.200 / 6.000 | 600 / 3.000 / 15.000 | 1.200 / 6.000 / 40.000 |
| TikTok (seguidores) | Pesimista / Más probable / Optimista | 50 / 300 / 2.000 | 200 / 1.500 / 10.000 | 500 / 4.000 / 25.000 | 1.000 / 8.000 / 60.000 |
| YouTube (suscriptores) | Pesimista / Más probable / Optimista | 10 / 50 / 300 | 40 / 200 / 2.000 | 100 / 600 / 8.000 | 250 / 1.500 / 25.000 |
| Mediana de visualizaciones por vídeo (IG / TikTok / YT), mes 3 | Más probable | 400 / 550 / 90 | | | |

3. Escribe `metrics/AAAA-MM-DD.md` con una tabla por red, el escenario en el que está cada una y el vídeo y la serie que mejor y peor han funcionado.
4. Ajusta la semana: si una serie lleva 3 semanas por debajo de la mitad de la mediana de la cuenta, sustitúyela esa semana por la serie que mejor funcione (nunca la saga). Anótalo en el informe.
5. Incluye un resumen de 3 líneas en el mensaje final.

## Estilo

- Vídeo vertical 1080×1920, 30 fps, 15–32 s, texto en pantalla en inglés, sin voz.
- Paleta: fondo #0E1116, losas #2B3038, texto #D6E2EE, secundario #8E99A6, único acento oro #E0A44A.
- Tipografía: Cinzel (títulos), EB Garamond (texto). Las runas se dibujan con `nr.draw_rune`, nunca con una fuente.
- Etiqueta de serie en y=196; contenido entre y=290 y y=1520. Un mensaje por pantalla, máx. ~8 palabras por línea.
- Gancho en los primeros 2 segundos.

## Voz en off (decidido 5 nov: voz 6)

Narrador con **Kokoro-82M** (licencia Apache-2.0, uso comercial permitido), en local con CPU: sin token ni cuota, así que la tarea del domingo también puede usarlo. Siempre la misma voz: **`am_michael` (la «voz 6», elegida por Alfonso)**, fijada en `narrate.VOICE` y la misma velocidad para que suene igual en todos los vídeos. Es una voz sintética de la librería, no la imitación de nadie.
- Instalación en una sesión nueva: `pip install --break-system-packages kokoro-onnx` y descargar `kokoro-v1.0.onnx` y `voices-v1.0.bin` de las releases de GitHub `thewh1teagle/kokoro-onnx` (`model-files-v1.0`) en `engine/kokoro/`. El CDN de Hugging Face está bloqueado; GitHub releases funciona.
- Uso: ver `engine/narrate.py` y el ejemplo `v08v_saga02_voice.py` (segmentos `(t0, t1, texto)` sobre la línea de tiempo original; el vídeo se estira donde la frase lo necesita, la música baja bajo la voz y el audio se normaliza a −14 LUFS).
- Los nombres difíciles se escriben como suenan en el texto hablado (Ymir → "Eemeer", Vé → "Vay", Bergelmir → "Bergelmeer").
- **Dónde va la voz:** en todos los episodios de The Norse Saga (desde el Ep. 1) y en Hávamál (el texto en nórdico antiguo va sin voz: segmento con texto vacío `""`). El resto de series, sin voz salvo que Alfonso diga lo contrario. Para cada episodio: haz primero el script normal (`vNN_sagaXX.py`), luego su versión con voz (`vNNv_sagaXX_voice.py`, mismos segmentos que las tarjetas) y programa **solo la versión con voz** (`..._voz.mp4`).
- Con voz, marca en Metricool `instagramData.isAiGenerated = true`, `youtubeData.isAiGeneratedContent = true` y `tiktokData.isAigc = true` (la voz es sintética).
- El vídeo se alarga (Ep. 2: 34 → 44 s; Ep. 3: 38 → 57 s). Escribe frases cortas: menos de 60 s por episodio.
- `engine/voice.py` (Chatterbox en Hugging Face) queda como alternativa: suena más natural pero gasta la cuota gratuita de ZeroGPU (≈8 frases al día) y necesita el token, así que no sirve para la tarea automática.

## Estructura de un vídeo (checklist obligatorio, 5 nov)

Qué premian las plataformas: Instagram ordena los Reels por tiempo visto/finalización, «me gusta» por alcance y **envíos por DM por alcance** (la señal más fuerte para llegar a quien no te sigue). YouTube Shorts mira cuántos eligen verlo frente a cuántos deslizan y cuánto del vídeo se ve. En las dos, lo que decide es el primer segundo y que la recompensa llegue pronto.

Plantilla (30–45 s; nunca más de 60 s con voz):
1. **0–1 s · Gancho.** Imagen fuerte y una frase de ≤7 palabras **visibles desde el fotograma 0** (`Card(-0.8, ...)` y el cuadro con `window(t, -1.0, ...)`). La frase es una afirmación sorprendente o una pregunta, nunca un resumen. Bien: "Our world is made from a dead giant", "Tolkien didn't invent his dwarves' names". Mal: "Odin and his brothers killed Ymir" (es contexto, no gancho). La voz empieza en t≈0,35 s.
2. **1–4 s · Por qué importa.** Una línea de contexto.
3. **Cuerpo · 3–5 pasos de 3–5 s.** Cada paso cambia la imagen o añade algo que se mueve. Nunca más de 4 s con la misma imagen quieta. Máximo ~12 palabras en pantalla a la vez.
4. **A mitad · Segundo gancho.** Un giro ("All but one…", "But the poems disagree…") para frenar la caída del medio.
5. **Final · Recompensa + llamada.** La recompensa nunca después del 80 % del vídeo. Termina con una pregunta concreta para comentar (elegir entre opciones o escribir un nombre) o un motivo para enviarlo ("Send this to…"). En la saga, enlace al siguiente episodio y 3 s del tatuaje (motivo para guardar).
6. **Texto de la publicación:** primera línea = el gancho; máximo 5 hashtags; una frase para enviar o guardar cuando tenga sentido.

Antes de programar, revisa: ¿el fotograma 0 tiene imagen + gancho? ¿hay algún tramo >4 s sin cambio visual? ¿dura menos de 45 s (60 s con voz)? ¿la pregunta final se contesta con una palabra?

Cómo medir (desde 10–14 vídeos publicados, no antes): % que elige verlo (YouTube), visionado medio en % y envíos + guardados por alcance (Instagram). Las visualizaciones solas no dicen nada.

## Imágenes (obligatorio: nada de vídeos solo con texto)

La imagen debe cambiar cada 3–4 segundos y siempre haber movimiento (empuje lento de cámara, capas, partículas). El texto va arriba (y 290–560) o abajo (y 1440–1520) y la ilustración ocupa el centro.

1. **Episodios de la saga: pinturas de dominio público** (al menos una por episodio, en la escena clave). Artistas fallecidos hace más de 70 años: Carl Emil Doepler, Johannes Gehrts, Lorenz Frølich, Mårten Eskil Winge, W. G. Collingwood, Georg von Rosen, John Bauer, Nicolai Abildgaard, Arthur Rackham (Ring, 1910–11).
    - Cómo descargarlas: la API de Commons suele responder 429. Busca el nombre exacto del archivo con WebSearch ("commons.wikimedia.org File <obra> <autor>") y descárgalo directamente de `upload.wikimedia.org` construyendo la ruta con el MD5 del nombre (`h = md5(nombre)`; `https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{nombre}`), con User-Agent `NordicReignVideoBot/1.0 (https://github.com/alfonsogervascastro/nordic-reign-media)`. Si da 429, prueba la miniatura estándar `.../thumb/{h[0]}/{h[:2]}/{nombre}/960px-{nombre}`, espera 30–60 s entre intentos y no insistas más de 3 veces: si no hay forma, usa siluetas.
    - Guarda la imagen en `images/` (nombre `autor_obra_año.jpg`) y añádela a `images/CREDITS.md`. Mira la imagen antes de usarla.
    - Móntala con `nr.Painting(path, w, h, cy=..., focus=..., crop=...)`: aplica el tratamiento de marca (duotono azul/oro), bordes difuminados y empuje lento. Ejemplos en `v07_saga01.py` (Odín de Rosen) y `v01_gleipnir.py` (Týr y Fenrir de Bauer).
    - Cita la obra en pantalla (B 30 px, y≈1530: "Art: <autor>, <obra>, <año>") y en el texto de la publicación.
    - Ya en `images/`: Rosen (Odín caminante), Bauer (Týr y Fenrir), Abildgaard (Ymir y Auðumbla), Frølich (Ymir asesinado, 1895; usada en Ep. 2), Bagge (Yggdrasil, 1847; usada en Ep. 3 entera y en tres detalles), uro de Hamilton Smith (1827; Uruz). Truco que funcionó el 4 nov: cuando la miniatura da 429 por "robot policy", el **original** (sin `/thumb/`) a veces sí baja; espera 8–10 s entre peticiones. Fallaron: `The_Ash_Yggdrasil_by_Friedrich_Wilhelm_Heine.jpg` y el manuscrito Codex Regius.
2. **Ilustración por código: solo atmósfera, nunca figuras.** Alfonso ve poco logrados los personajes y animales dibujados por código y el salto de estilo con las pinturas. Por eso el código solo dibuja lo que queda bien: cielo, niebla, resplandores de fuego y hielo, acantilados y montañas en silueta, Yggdrasil, ojos brillando en la oscuridad, cadenas, runas talladas y partículas (`scenes.py`, `v07_saga01.py`). **Personas, dioses y animales solo aparecen en pinturas.** Si una escena necesita una figura y no hay pintura, se resuelve con atmósfera y texto. Dibuja las formas en capas separadas y combínalas con `alpha_composite`: `ImageDraw` sobre RGBA reemplaza píxeles, no los mezcla.
3. No usar imágenes generadas con IA salvo que Alfonso las suba a `images/ai/`; en ese caso marcar `isAiGenerated` / `isAiGeneratedContent` en Metricool.
4. Nunca fotos de personas reales ni de tatuajes ajenos.

## Reglas de rigor

- Separar siempre lo histórico (fuentes medievales, arqueología) de lo moderno (lecturas del siglo XX). Citar la fuente en pantalla o en el texto de la publicación.
- Vikingos sin cascos con cuernos.
- Elder Futhark ≈ 150–800 d. C.; los vikingos usaban el Younger Futhark. No decir "runas vikingas" del Elder Futhark.
- Algiz y Othala: presentarlas con su contexto histórico. Nunca dibujar Othala con alas, Sowilo doble ni Wolfsangel.
- Hávamál: solo la traducción de dominio público de Bellows (1923).
- Nada de tatuajes de otras personas.

## Banco de temas para las series satélite

**Words from the North:** Midgard → Middle-earth · Bluetooth (Harald Bluetooth, iniciales en Younger Futhark) · *husband* (húsbóndi) · *law* (lagu) · *ugly* (uggligr) · *ransack* · *skull*, *skin*, *knife* · *Hel* y *hell* (cognados, no préstamo).

**Myth vs History:** cascos con cuernos (✔ programado 13 nov) · los vikingos se lavaban (laugardagur, "día de baño") · no bebían en cráneos (error de Ole Worm, 1636) · "vikingo" era una actividad, no un pueblo · L'Anse aux Meadows · el nombre "Valknut" es moderno · el Vegvísir es del siglo XIX.

**Hávamál/kennings:** estrofas 76–77 ("Cattle die, kinsmen die…") · el huésped · la moderación al beber · "corcel del mar" = barco · "mar de heridas" = sangre · "hidromiel de Odín" = poesía · "cráneo de Ymir" = cielo.

**Runas (orden):** Fehu ✔ · Uruz · Thurisaz · Ansuz · Raidho · Kaunan · Gebo · Wunjo · Hagalaz · Naudiz · Isa · Jera · Eihwaz · Perthro · Algiz (con contexto) · Sowilo · Tiwaz · Berkano · Ehwaz · Mannaz · Laguz · Ingwaz · Othala (con contexto, sin alas) · Dagaz.

## Pendientes

- **Antes de producir, mira `getScheduledPosts` de martes a lunes y produce solo los días que falten.** No dupliques días ya programados.
- Semana del 10 al 16 nov: **ya programado** del miércoles 11 al lunes 16 (Ep. 2, Tolkien, cascos, Ep. 3, Hávamál 76, Uruz). **Solo falta el martes 10 (Your name in runes)**, con nombres de `names.txt` o de comentarios; si no hay ninguno, usa un nombre nórdico popular (p. ej. ERIK o FREYA).
- Semana del 17 al 23 nov: Ep. 4 (Ask y Embla, miércoles 18) y Ep. 5 (Æsir y Vanir, sábado 21); runa 3/24 Thurisaz el lunes 23 (el vídeo de Uruz ya lo anuncia).

## Cómo producir y programar

1. `cd engine` y crear un script por vídeo siguiendo los ejemplos (`v07_saga01.py` para episodios, `v06_fehu.py` para runas, `v03_name.py` para nombres, `v05_words.py` para palabras, `v04_horns.py` para mito vs. historia). Siempre con `nr.Label`.
2. `python3 vXX.py stills` → mirar los fotogramas antes del render; luego `python3 vXX.py`.
3. Copiar los `.mp4` a `AAAA-MM/` con el nombre `AAAA-MM-DD_<serie>_<tema>.mp4` y hacer push a `main`.
4. URL pública: `https://raw.githubusercontent.com/alfonsogervascastro/nordic-reign-media/main/AAAA-MM/<archivo>.mp4`.
5. Programar con Metricool `createScheduledPost`: providers instagram + youtube + tiktok, `instagramData.type = REEL`, `youtubeData.type = short`, `madeForKids = false`, `category = EDUCATION`, título de YouTube terminado en `#shorts` (episodios: "The Norse Saga Ep. n: <título> | #shorts"), y `tiktokData` con `title` (obligatorio; el mismo título sin `#shorts`), `privacyOption = PUBLIC_TO_EVERYONE`, `isAigc = false`.
6. **Máximo 5 hashtags** por publicación (límite de Instagram desde finales de 2025). Portada: `videoCoverMilliseconds` en un fotograma con título + imagen (≈2500 en sagas, Hávamál y palabras; en runas, cuando la runa ya está dibujada).
7. Comprobar con `getScheduledPosts` y actualizar el registro y la tabla de episodios.

## Registro de publicaciones

| Fecha | Serie | Tema | Archivo |
| --- | --- | --- | --- |
| 2026-11-04 | The Norse Saga · Prólogo | Gleipnir y Fenrir | 2026-11/2026-11-04_saga-prologue_gleipnir_a2.mp4 |
| 2026-11-05 | Words from the North | Días de la semana | 2026-11/2026-11-05_words_days_a2.mp4 |
| 2026-11-06 | Your name in runes | Llamada + ejemplo ASTRID | 2026-11/2026-11-06_name_astrid_a2.mp4 |
| 2026-11-07 | The Norse Saga · Ep. 1 | Ginnungagap → Odín | 2026-11/2026-11-07_saga-ep01_ginnungagap_voz.mp4 (con voz) |
| 2026-11-08 | Words from the North | window, sky, egg, berserk, they | 2026-11/2026-11-08_words_old-norse_a2.mp4 |
| 2026-11-09 | Rune 1/24 | Fehu | 2026-11/2026-11-09_rune01_fehu_a2.mp4 |
| 2026-11-11 | The Norse Saga · Ep. 2 | El mundo hecho de Ymir (+ tatuaje, con voz) | 2026-11/2026-11-11_saga_ep02_ymir_voz2.mp4 |
| 2026-11-12 | Words from the North | Los enanos de Tolkien vienen de la Völuspá; Midgard | 2026-11/2026-11-12_words_tolkien-dwarves.mp4 |
| 2026-11-13 | Myth vs History | Cascos con cuernos | 2026-11/2026-11-13_myth-vs-history_horns_a2.mp4 |
| 2026-11-14 | The Norse Saga · Ep. 3 | Yggdrasil (+ tatuaje, con voz) | 2026-11/2026-11-14_saga_ep03_yggdrasil_voz2.mp4 |
| 2026-11-15 | Hávamál | Estrofa 76 ("Deyr fé", con voz) | 2026-11/2026-11-15_havamal_76_voz.mp4 |
| 2026-11-16 | Rune 2/24 | Uruz | 2026-11/2026-11-16_rune02_uruz.mp4 |
