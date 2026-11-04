# Elementos generados con IA

| Archivo | Uso | Modelo | Fecha |
| --- | --- | --- | --- |
| serpent_head_1.png | Cabeza de Jörmungandr (Ep. 15) | Qwen-Image (Space `mcp-tools/Qwen-Image`, Hugging Face) | 2026-11-04 |
| ravens_0.png | Huginn y Muninn (Ep. 7) | Qwen-Image | 2026-11-04 |

`generate.py` contiene los prompts (estilo: tinta negra plana sobre blanco, arte vikingo). Necesita `HF_TOKEN` en el entorno; el token nunca se guarda en el repositorio.

La IA solo dibuja cabezas o figuras. Los cuerpos entrelazados salen de `knots.py`, para que los cruces sean correctos. Descartados el 4 nov: una prueba de "sleeve" completo (salió con casco de cuernos y entrelazado incorrecto) y una cabeza de lobo con sombreado gris y fondo negro (no sirve como plantilla).

Pendientes de mejorar con IA cuando haya cuota (la gratuita es de unos pocos minutos de GPU al día): `yggdrasil` (Ep. 3), `horn` (Ep. 8), `sleipnir` (Ep. 9) y `wolf_head` (Ep. 11 y 20). Los diseños actuales de esos episodios son geométricos y válidos.
