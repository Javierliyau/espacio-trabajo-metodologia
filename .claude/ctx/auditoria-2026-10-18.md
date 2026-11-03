# Auditoria de contexto: 2026-10-18

Proyecto `C:\Espacio de trabajo Metodologia de estudio`, ultimas 10 sesiones. Contexto y salida: tokens reales (API). Tamano de cada pieza: estimado. **Arrastre** = tokens de la pieza × llamadas que la releyeron hasta el fin de la sesion o la siguiente compactacion: es lo que realmente consume cuota.

## Sesiones

| inicio | titulo | llamadas | sobrecarga fija | pico | procesado total | salida | compact. | subagentes |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-10-16 13:35 | Gráfico de crecimiento poblacional USA | 19 | 55.7k | 105.1k (53%) | 1601.7k | 19.3k | 0 | 0 |
| 2026-10-15 21:33 | Econometría M1 | 53 | 57.5k | 112.4k (56%) | 4597.2k | 27.8k | 0 | 0 |
| 2026-10-15 21:14 | Plan óptimo de estudio en econometría | 53 | 57.0k | 145.1k (73%) | 5932.9k | 36.2k | 0 | 0 |
| 2026-10-08 12:53 | /retomar econometria-ii. | 285 | 47.8k | 166.8k (83%) | 29482.7k | 227.7k | 3 | 0 |
| 2026-10-15 20:09 | Tiempo de estudio | 61 | 56.4k | 154.7k (77%) | 6586.1k | 49.7k | 0 | 0 |
| 2026-10-13 18:12 | Continuacion control micro 2 | 84 | 48.1k | 155.8k (78%) | 8379.3k | 52.6k | 0 | 0 |
| 2026-10-14 18:26 | Clases telemáticas 15-17 octubre | 107 | 59.6k | 165.8k (83%) | 11722.8k | 82.7k | 1 | 0 |
| 2026-10-14 16:38 | Costos marginales monopolios naturales C | 16 | 58.2k | 88.2k (44%) | 1213.5k | 14.5k | 0 | 307.1k |
| 2026-10-14 15:11 | Fuentes SEIA comunicaciones | 85 | 48.4k | 164.1k (82%) | 9145.1k | 58.1k | 0 | 0 |
| 2026-10-14 13:47 | Organizar el día de hoy | 66 | 48.2k | 147.2k (74%) | 6543.0k | 45.7k | 0 | 2603.5k |

**Procesado total:** 85204.2k tokens. **50%** es sobrecarga fija (system prompt, herramientas, MCP, skills, CLAUDE.md, memoria) repetida en cada llamada; **29%** es arrastre de lo que entro durante la conversacion; el resto (20%) no se atribuye pieza a pieza (razonamiento interno, recordatorios del sistema, resumenes de compactacion, error de estimacion).

## Arrastre por tipo de pieza

| tipo | arrastre | % |
|---|---:|---:|
| Bash | 7365.0k | 30% |
| respuesta Claude | 3116.5k | 13% |
| escrito:Bash | 2357.0k | 9% |
| Read (completo) | 2268.3k | 9% |
| adjunto:file | 1339.3k | 5% |
| escrito:Write | 1223.9k | 5% |
| prompt usuario | 1025.3k | 4% |
| Read | 949.6k | 4% |
| adjunto:total_tokens_reminder | 700.9k | 3% |
| adjunto:deferred_tools_delta | 554.6k | 2% |
| adjunto:hook_success | 406.3k | 2% |
| adjunto:instructions | 363.0k | 1% |
| Grep | 353.7k | 1% |
| adjunto:environment | 285.8k | 1% |
| adjunto:skill_listing | 245.5k | 1% |

## Las 20 piezas mas caras

| arrastre | ~tk | releida | tipo | objetivo | sesion |
|---:|---:|---:|---|---|---|
| 348.4k | 7.0k | ×50 | Read | `C:\Users\javie\.claude\projects\C--Espacio-de-trabajo-Metodo` | Plan óptimo de estudio en |
| 331.9k | 5.7k | ×58 | escrito:Write | `C:\Espacio de trabajo Metodologia de estudio\trabajo\overlea` | /retomar econometria-ii. |
| 271.4k | 3.0k | ×92 | adjunto:file | `etodologia de estudio\trabajo\econometria-ii-demre\informe\_` | /retomar econometria-ii. |
| 270.5k | 4.6k | ×59 | prompt usuario | `deja el codigo listo :  <pasted_content id="e2b6"> \document` | /retomar econometria-ii. |
| 267.6k | 3.2k | ×84 | Grep | `44 mil millones/46.758/Fast Check` | Fuentes SEIA comunicacion |
| 239.1k | 3.0k | ×81 | adjunto:file | `etodologia de estudio\trabajo\econometria-ii-demre\informe\_` | /retomar econometria-ii. |
| 222.1k | 2.7k | ×81 | escrito:Write | `C:/Espacio de trabajo Metodologia de estudio/trabajo/econome` | /retomar econometria-ii. |
| 219.3k | 7.1k | ×31 | Read | `C:\Users\javie\.claude\projects\C--Espacio-de-trabajo-Metodo` | Organizar el día de hoy |
| 170.2k | 9.5k | ×18 | mcp__visualize__read_me | `{"modules": ["chart"], "platform": "desktop"}` | Gráfico de crecimiento po |
| 159.7k | 2.0k | ×81 | prompt usuario | `This session is being continued from a previous conversation` | /retomar econometria-ii. |
| 154.7k | 4.0k | ×39 | Read | `C:\Proyecto Metodologia de estudio\metodologia-perry-mazur\0` | Clases telemáticas 15-17  |
| 154.0k | 3.6k | ×43 | prompt usuario | `This session is being continued from a previous conversation` | /retomar econometria-ii. |
| 151.3k | 3.6k | ×42 | adjunto:skill_listing | `` | /retomar econometria-ii. |
| 150.2k | 1.6k | ×92 | adjunto:deferred_tools_d | `` | /retomar econometria-ii. |
| 132.7k | 1.7k | ×80 | Bash | `cd "C:/Proyecto Metodologia de estudio/datos/material/taller` | Fuentes SEIA comunicacion |
| 132.3k | 1.6k | ×81 | adjunto:deferred_tools_d | `` | /retomar econometria-ii. |
| 129.4k | 1.4k | ×92 | adjunto:instructions | `` | /retomar econometria-ii. |
| 128.6k | 1.4k | ×92 | prompt usuario | `This session is being continued from a previous conversation` | /retomar econometria-ii. |
| 127.1k | 1.6k | ×79 | Bash | `cd "C:/Proyecto Metodologia de estudio/datos/material/taller` | Fuentes SEIA comunicacion |
| 125.5k | 2.4k | ×52 | adjunto:queued_command | `` | Organizar el día de hoy |

## Archivos leidos mas de una vez en la misma sesion

- `C:\Users\javie\AppData\Local\Temp\hoja.png` ×2 en */retomar econometria-ii.*
- `C:\Users\javie\AppData\Local\Temp\g-1.png` ×2 en */retomar econometria-ii.*
- `trabajo/micro/sesion5-14-10.pdf` ×2 en *Continuacion control micro 2*
- `trabajo/anexo-p1.png` ×2 en *Fuentes SEIA comunicaciones*
- `C:\Users\javie\.claude\projects\C--Espacio-de-trabajo-Metodologia-de-estudio\1a06e269-11f3-4d57-ab33-c1a4270b3d77\tool-results\bgcygq5ws.txt` ×2 en *Organizar el día de hoy*

## Recomendaciones

1. Sobrecarga fija promedio 51.7k por llamada. Ejecuta `/context` y desactiva los MCP y skills que no uses (cada 10k fijos cuestan 10k × cada llamada).
2. 1 lecturas completas de archivos > 4.0k tk (arrastre 219.3k). `hook-read` las frena desde ahora.
3. 7 sesiones superaron el 70% de la ventana. Corta con `/handoff` al primer aviso: una sesion nueva arranca en la sobrecarga fija, no en 100k+.
4. 5 relecturas del mismo archivo en una sesion: cita la primera lectura o lee solo el rango que cambio.
5. 4 imagenes adjuntas (~1.5k tk c/u, arrastre 201.0k). Recorta la captura a la zona relevante.
