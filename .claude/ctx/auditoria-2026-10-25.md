# Auditoria de contexto: 2026-10-25

Proyecto `C:\Espacio de trabajo Metodologia de estudio`, ultimas 10 sesiones. Contexto y salida: tokens reales (API). Tamano de cada pieza: estimado. **Arrastre** = tokens de la pieza × llamadas que la releyeron hasta el fin de la sesion o la siguiente compactacion: es lo que realmente consume cuota.

## Sesiones

| inicio | titulo | llamadas | sobrecarga fija | pico | procesado total | salida | compact. | subagentes |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-10-24 12:51 | Sociología: 4 fichas por autor para la P | 75 | 60.2k | 167.1k (84%) | 8796.3k | 64.9k | 2 | 0 |
| 2026-10-24 18:41 | Sociología PEP1 | 59 | 59.0k | 155.0k (78%) | 6110.6k | 63.0k | 1 | 1223.7k |
| 2026-10-24 19:15 | Autores y granja de ideas | 35 | 58.7k | 113.5k (57%) | 3025.8k | 38.0k | 0 | 1620.8k |
| 2026-10-24 02:51 | Plan de dia sabado | 74 | 57.0k | 166.8k (83%) | 7945.0k | 60.8k | 1 | 0 |
| 2026-10-24 15:37 | Econometría M2 con la base de la clase 5 | 64 | 60.6k | 163.2k (82%) | 7498.0k | 56.1k | 0 | 457.6k |
| 2026-10-08 12:53 | /retomar econometria-ii. | 285 | 47.8k | 166.8k (83%) | 29482.7k | 227.7k | 3 | 0 |
| 2026-10-24 15:42 | Contenido PEP 1 Econometría | 31 | 58.6k | 111.6k (56%) | 2758.2k | 18.6k | 0 | 0 |
| 2026-10-24 14:49 | Cierre de Macro y Econometría del sáb 24 | 61 | 60.4k | 165.4k (83%) | 7296.6k | 44.2k | 0 | 0 |
| 2026-10-24 15:09 | Consultas econometría: sesgo por variabl | 12 | 58.6k | 79.7k (40%) | 864.8k | 7.8k | 0 | 0 |
| 2026-10-14 15:11 | Fuentes SEIA comunicaciones | 85 | 48.4k | 164.1k (82%) | 9145.1k | 58.1k | 0 | 0 |

**Procesado total:** 82923.0k tokens. **51%** es sobrecarga fija (system prompt, herramientas, MCP, skills, CLAUDE.md, memoria) repetida en cada llamada; **30%** es arrastre de lo que entro durante la conversacion; el resto (19%) no se atribuye pieza a pieza (razonamiento interno, recordatorios del sistema, resumenes de compactacion, error de estimacion).

## Arrastre por tipo de pieza

| tipo | arrastre | % |
|---|---:|---:|
| Bash | 4986.9k | 20% |
| respuesta Claude | 2538.6k | 10% |
| Read | 2404.9k | 10% |
| escrito:Write | 2385.4k | 10% |
| Read (completo) | 2113.5k | 8% |
| escrito:Bash | 1726.8k | 7% |
| prompt usuario | 1539.0k | 6% |
| adjunto:file | 1279.1k | 5% |
| Grep | 832.8k | 3% |
| adjunto:total_tokens_reminder | 601.2k | 2% |
| adjunto:deferred_tools_delta | 588.5k | 2% |
| adjunto:skill_listing | 544.7k | 2% |
| adjunto:hook_success | 473.5k | 2% |
| adjunto:instructions | 419.9k | 2% |
| escrito:Edit | 316.4k | 1% |

## Las 20 piezas mas caras

| arrastre | ~tk | releida | tipo | objetivo | sesion |
|---:|---:|---:|---|---|---|
| 331.9k | 5.7k | ×58 | escrito:Write | `C:\Espacio de trabajo Metodologia de estudio\trabajo\overlea` | /retomar econometria-ii. |
| 271.4k | 3.0k | ×92 | adjunto:file | `etodologia de estudio\trabajo\econometria-ii-demre\informe\_` | /retomar econometria-ii. |
| 270.5k | 4.6k | ×59 | prompt usuario | `deja el codigo listo :  <pasted_content id="e2b6"> \document` | /retomar econometria-ii. |
| 267.6k | 3.2k | ×84 | Grep | `44 mil millones/46.758/Fast Check` | Fuentes SEIA comunicacion |
| 244.5k | 5.6k | ×44 | prompt usuario | `This session is being continued from a previous conversation` | Sociología: 4 fichas por  |
| 239.1k | 3.0k | ×81 | adjunto:file | `etodologia de estudio\trabajo\econometria-ii-demre\informe\_` | /retomar econometria-ii. |
| 222.1k | 2.7k | ×81 | escrito:Write | `C:/Espacio de trabajo Metodologia de estudio/trabajo/econome` | /retomar econometria-ii. |
| 194.3k | 5.7k | ×34 | escrito:Write | `C:/Espacio de trabajo Metodologia de estudio/trabajo/sociolo` | Sociología PEP1 |
| 189.6k | 4.6k | ×41 | Grep | `(?i)macro` | Plan de dia sabado |
| 170.9k | 3.9k | ×44 | adjunto:skill_listing | `` | Sociología: 4 fichas por  |
| 167.2k | 3.8k | ×44 | adjunto:file | `studio\b2de80dd-495a-4177-b925-df934ae40beb\tool-results\bhy` | Sociología: 4 fichas por  |
| 159.7k | 2.0k | ×81 | prompt usuario | `This session is being continued from a previous conversation` | /retomar econometria-ii. |
| 154.0k | 3.6k | ×43 | prompt usuario | `This session is being continued from a previous conversation` | /retomar econometria-ii. |
| 151.3k | 3.6k | ×42 | adjunto:skill_listing | `` | /retomar econometria-ii. |
| 150.2k | 1.6k | ×92 | adjunto:deferred_tools_d | `` | /retomar econometria-ii. |
| 143.8k | 3.3k | ×43 | escrito:Write | `C:/Proyecto Metodologia de estudio/datos/material/sociologia` | Sociología: 4 fichas por  |
| 141.9k | 8.9k | ×16 | Read | `C:\Proyecto Metodologia de estudio\datos\material\sociologia` | Sociología: 4 fichas por  |
| 134.1k | 3.3k | ×41 | escrito:Write | `C:/Proyecto Metodologia de estudio/datos/material/sociologia` | Sociología: 4 fichas por  |
| 132.7k | 1.7k | ×80 | Bash | `cd "C:/Proyecto Metodologia de estudio/datos/material/taller` | Fuentes SEIA comunicacion |
| 132.3k | 1.6k | ×81 | adjunto:deferred_tools_d | `` | /retomar econometria-ii. |

## Archivos leidos mas de una vez en la misma sesion

- `C:\Users\javie\AppData\Local\Temp\hoja.png` ×2 en */retomar econometria-ii.*
- `C:\Users\javie\AppData\Local\Temp\g-1.png` ×2 en */retomar econometria-ii.*
- `trabajo/anexo-p1.png` ×2 en *Fuentes SEIA comunicaciones*

## Recomendaciones

1. Sobrecarga fija promedio 53.9k por llamada. Ejecuta `/context` y desactiva los MCP y skills que no uses (cada 10k fijos cuestan 10k × cada llamada).
2. 7 sesiones superaron el 70% de la ventana. Corta con `/handoff` al primer aviso: una sesion nueva arranca en la sobrecarga fija, no en 100k+.
3. Lo escrito con Write/Edit arrastra 2701.8k (11%): el contenido de cada archivo escrito queda en el chat. Documentos largos: redactarlos en un subagente o cerrar con /handoff justo despues de escribirlos.
4. 3 relecturas del mismo archivo en una sesion: cita la primera lectura o lee solo el rango que cambio.
5. 1 imagenes adjuntas (~1.5k tk c/u, arrastre 30.0k). Recorta la captura a la zona relevante.
