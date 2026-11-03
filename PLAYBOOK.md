# Nordic Reign — playbook de vídeos

Este repositorio aloja los vídeos que se publican en Instagram y YouTube a través de Metricool, y el motor que los genera. Es la fuente de verdad para la tarea semanal.

## Cuentas

- Marca Metricool: `nordicreignofficial`, blogId `7741806`, zona horaria `Europe/Madrid`.
- Redes enlazadas: Instagram (Reel) y YouTube (Short). TikTok todavía no está enlazado.
- Usuario en los vídeos: `@nordicreignofficial`.
- Publicación: un vídeo al día a las 19:00 (Europe/Madrid).

## Estilo

- Vídeo vertical 1080×1920, 30 fps, 15–30 s, texto en pantalla en inglés, sin voz.
- Paleta: fondo #0E1116, losas #2B3038, texto #D6E2EE, secundario #8E99A6, único acento oro #E0A44A.
- Tipografía: Cinzel (títulos), EB Garamond (texto). Las runas se dibujan con `nr.draw_rune`, nunca con una fuente.
- Texto entre y=230 y y=1520 (fuera de la interfaz de las apps). Un mensaje por pantalla, máx. ~8 palabras por línea.
- Gancho en los primeros 2 segundos. Cierre con pregunta o llamada a seguir + `@nordicreignofficial`.
- Audio: el fondo generado por `nr.make_audio` (viento, dron, tambor). Sin música de terceros.

## Reglas de rigor

- Separar siempre lo histórico (fuentes medievales, arqueología) de lo moderno (lecturas del siglo XX). Citar la fuente en el texto de la publicación cuando sea un mito (p. ej. Prose Edda, Gylfaginning; Poetic Edda, Hávamál).
- Vikingos sin cascos con cuernos.
- Elder Futhark ≈ 150–800 d. C.; los vikingos usaban el Younger Futhark. No decir "runas vikingas" del Elder Futhark.
- Algiz y Othala: presentarlas con su contexto histórico. Nunca dibujar Othala con alas, Sowilo doble ni Wolfsangel.
- Hávamál: solo traducciones de dominio público (Bellows, 1923).
- Nada de tatuajes de otras personas.

## Semana tipo (de martes a lunes)

| Día | Formato |
| --- | --- |
| Martes | Tu nombre en runas (nombres de `names.txt`; si está vacío, nombres populares) |
| Miércoles | Rareza de un mito |
| Jueves | Palabras y etimología |
| Viernes | Mito vs. historia |
| Sábado | Los 9 mundos (uno por semana) |
| Domingo | Kenning o verso del Hávamál |
| Lunes | Runa de la semana (en orden del Futhark) |

## Banco de temas (tachar al usar, anotar en el registro)

**Rarezas:** Loki da a luz a Sleipnir · Ratatoskr, la ardilla que lleva insultos por Yggdrasil · las cabras de Thor, comidas y resucitadas · Thor no puede levantar un gato (era Jörmungandr) · el cuerno de Thor y las mareas · Naglfar, el barco de uñas de muertos · el mango corto de Mjölnir (Loki convertido en mosca) · la sangre de Kvasir y el hidromiel de la poesía · Baldr y el muérdago · Thor vestido de novia.

**Palabras:** Bluetooth (Harald Bluetooth y sus iniciales en runas del Younger Futhark) · *husband* (húsbóndi) · *law* (lagu) · *ugly* (uggligr) · *ransack* · *skull*, *skin*, *knife* · *Hel* y *hell* (cuidado: cognados, no préstamo).

**Mito vs. historia:** los vikingos se lavaban (sábado = laugardagur, "día de baño") · no bebían en cráneos (error de traducción de Ole Worm, 1636) · "vikingo" era una actividad, no un pueblo · llegaron a América (L'Anse aux Meadows) · el nombre "Valknut" es moderno · el Vegvísir es de un manuscrito islandés del siglo XIX.

**Los 9 mundos:** Yggdrasil (intro) · Asgard · Midgard · Jötunheim · Vanaheim · Álfheim · Svartálfheim · Niflheim · Múspelheim · Helheim.

**Kennings y Hávamál:** "corcel del mar" = barco · "mar de heridas" = sangre · "hidromiel de Odín" = poesía · "alimentador de cuervos" = guerrero · "cráneo de Ymir" = cielo · Hávamál 76–77 ("Cattle die, kinsmen die…") · Hávamál sobre el huésped.

**Runas (orden):** Fehu ✔ · Uruz · Thurisaz · Ansuz · Raidho · Kaunan · Gebo · Wunjo · Hagalaz · Naudiz · Isa · Jera · Eihwaz · Perthro · Algiz (con contexto) · Sowilo · Tiwaz · Berkano · Ehwaz · Mannaz · Laguz · Ingwaz · Othala (con contexto, sin alas) · Dagaz.

## Cómo producir y programar

1. `cd engine` y crear un script por vídeo siguiendo los ejemplos `v0*_*.py` (clases `Card`, `T`, `B`, `nr.draw_rune`, `nr.render`).
2. `python3 vXX.py stills` → mirar los fotogramas antes del render; luego `python3 vXX.py`.
3. Copiar los `.mp4` a `AAAA-MM/` y hacer push a `main`.
4. URL pública: `https://raw.githubusercontent.com/alfonsogervascastro/nordic-reign-media/main/AAAA-MM/<archivo>.mp4`.
5. Programar con Metricool `createScheduledPost`: providers instagram + youtube, `instagramData.type = REEL`, `youtubeData.type = short`, `madeForKids = false`, `category = EDUCATION`, título de YouTube terminado en `#shorts`.
6. Comprobar con `getScheduledPosts` y anotar en el registro.

## Registro de publicaciones

| Fecha | Formato | Tema | Archivo |
| --- | --- | --- | --- |
| 2026-11-04 | Rareza | Gleipnir y Fenrir | 2026-11/v01_gleipnir.mp4 |
| 2026-11-05 | Palabras | Días de la semana | 2026-11/v02_days.mp4 |
| 2026-11-06 | Nombre en runas | Llamada + ejemplo ASTRID | 2026-11/v03_name.mp4 |
| 2026-11-07 | Mito vs. historia | Cascos con cuernos | 2026-11/v04_horns.mp4 |
| 2026-11-08 | Palabras | window, sky, egg, berserk, they | 2026-11/v05_words.mp4 |
| 2026-11-09 | Runa de la semana | Fehu | 2026-11/v06_fehu.mp4 |
