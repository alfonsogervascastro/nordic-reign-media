# Nordic Reign — playbook de vídeos

Este repositorio aloja los vídeos que se publican en Instagram y YouTube a través de Metricool, y el motor que los genera. Es la fuente de verdad para la tarea semanal.

## Idea central

La cuenta cuenta una historia, no curiosidades sueltas. La columna es **The Norse Saga**: la mitología nórdica en orden, del vacío inicial al Ragnarök, en episodios numerados (miércoles y sábado). El resto de series de la semana gira alrededor del episodio en curso siempre que se pueda. Quien entra en el perfil debe poder seguir la historia y reconocer cada serie de un vistazo.

## Cuentas

- Marca Metricool: `nordicreignofficial`, blogId `7741806`, zona horaria `Europe/Madrid`.
- Redes enlazadas: Instagram (Reel) y YouTube (Short). TikTok todavía no está enlazado.
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
| 2 | Odín, Vili y Vé matan a Ymir y hacen el mundo con su cuerpo | — | |
| 3 | Yggdrasil y los nueve mundos | — | |
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

## Estilo

- Vídeo vertical 1080×1920, 30 fps, 15–32 s, texto en pantalla en inglés, sin voz.
- Paleta: fondo #0E1116, losas #2B3038, texto #D6E2EE, secundario #8E99A6, único acento oro #E0A44A.
- Tipografía: Cinzel (títulos), EB Garamond (texto). Las runas se dibujan con `nr.draw_rune`, nunca con una fuente.
- Etiqueta de serie en y=196; contenido entre y=290 y y=1520. Un mensaje por pantalla, máx. ~8 palabras por línea.
- Gancho en los primeros 2 segundos.

## Imágenes (obligatorio: nada de vídeos solo con texto)

La imagen debe cambiar cada 3–4 segundos y siempre haber movimiento (empuje lento de cámara, capas, partículas). El texto va arriba (y 290–560) o abajo (y 1440–1520) y la ilustración ocupa el centro.

1. **Episodios de la saga: pinturas de dominio público** cuando se puedan descargar. Comprueba al empezar si `upload.wikimedia.org` responde (`curl -s -o /dev/null -w "%{http_code}" https://upload.wikimedia.org/`). Si responde, busca en Wikimedia Commons ilustraciones de los mitos de artistas fallecidos hace más de 70 años: Carl Emil Doepler, Johannes Gehrts, Lorenz Frølich, Mårten Eskil Winge, W. G. Collingwood, Emil Doepler, Ernst Hansen, Arthur Rackham (Ring, 1910–11). Guarda cada imagen en `images/` con su autor y año en `images/CREDITS.md`, aplícales el tratamiento de marca (desaturar ~60 %, tinte azul en sombras y oro en luces, viñeta) y móntalas con zoom/desplazamiento lento. Cita al autor en el texto de la publicación ("Art: Johannes Gehrts, 1901").
2. **Si no se pueden descargar, o para el resto de series: siluetas dibujadas por código** con `scenes.py` y los ejemplos de `v07_saga01.py` (acantilados, resplandores de fuego y hielo, ojos, animales y figuras suavizados con supersampling, Odín como caminante con sombrero y bastón). Dibuja las formas en capas separadas y combínalas con `alpha_composite`: `ImageDraw` sobre RGBA reemplaza píxeles, no los mezcla.
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

- Viernes 13 nov: `2026-11/2026-11-13_myth-vs-history_horns.mp4` ya está programado en Metricool. No crear otro vídeo para ese día.

## Cómo producir y programar

1. `cd engine` y crear un script por vídeo siguiendo los ejemplos (`v07_saga01.py` para episodios, `v06_fehu.py` para runas, `v03_name.py` para nombres, `v05_words.py` para palabras, `v04_horns.py` para mito vs. historia). Siempre con `nr.Label`.
2. `python3 vXX.py stills` → mirar los fotogramas antes del render; luego `python3 vXX.py`.
3. Copiar los `.mp4` a `AAAA-MM/` con el nombre `AAAA-MM-DD_<serie>_<tema>.mp4` y hacer push a `main`.
4. URL pública: `https://raw.githubusercontent.com/alfonsogervascastro/nordic-reign-media/main/AAAA-MM/<archivo>.mp4`.
5. Programar con Metricool `createScheduledPost`: providers instagram + youtube, `instagramData.type = REEL`, `youtubeData.type = short`, `madeForKids = false`, `category = EDUCATION`, título de YouTube terminado en `#shorts` (episodios: "The Norse Saga Ep. n: <título> | #shorts").
6. Comprobar con `getScheduledPosts` y actualizar el registro y la tabla de episodios.

## Registro de publicaciones

| Fecha | Serie | Tema | Archivo |
| --- | --- | --- | --- |
| 2026-11-04 | The Norse Saga · Prólogo | Gleipnir y Fenrir | 2026-11/2026-11-04_saga-prologue_gleipnir.mp4 |
| 2026-11-05 | Words from the North | Días de la semana | 2026-11/2026-11-05_words_days.mp4 |
| 2026-11-06 | Your name in runes | Llamada + ejemplo ASTRID | 2026-11/2026-11-06_name_astrid.mp4 |
| 2026-11-07 | The Norse Saga · Ep. 1 | Ginnungagap → Odín | 2026-11/2026-11-07_saga-ep01_ginnungagap.mp4 |
| 2026-11-08 | Words from the North | window, sky, egg, berserk, they | 2026-11/2026-11-08_words_old-norse.mp4 |
| 2026-11-09 | Rune 1/24 | Fehu | 2026-11/2026-11-09_rune01_fehu.mp4 |
| 2026-11-13 | Myth vs History | Cascos con cuernos | 2026-11/2026-11-13_myth-vs-history_horns.mp4 |
