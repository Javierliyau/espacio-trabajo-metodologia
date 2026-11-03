# Auditoria de contexto: 2026-10-10

Proyecto `C:\Espacio de trabajo Metodologia de estudio`, ultimas 10 sesiones. Contexto y salida: tokens reales (API). Tamano de cada pieza: estimado. **Arrastre** = tokens de la pieza × llamadas que la releyeron hasta el fin de la sesion o la siguiente compactacion: es lo que realmente consume cuota.

## Sesiones

| inicio | titulo | llamadas | sobrecarga fija | pico | procesado total | salida | compact. | subagentes |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-10-07 15:24 | Registro de trabajo diario | 50 | 45.6k | 120.5k (60%) | 3999.7k | 43.6k | 0 | 0 |
| 2026-10-08 11:33 | Organización de econometría | 30 | 47.5k | 111.6k (56%) | 2380.1k | 21.5k | 0 | 0 |
| 2026-10-09 14:19 | Primeras lecturas de historia económica | 11 | 47.7k | 68.3k (34%) | 632.3k | 6.0k | 0 | 0 |
| 2026-10-08 12:53 | /retomar econometria-ii. | 108 | 47.8k | 156.3k (78%) | 9713.8k | 84.3k | 1 | 0 |
| 2026-10-08 13:42 | Trabajo en econometría | 20 | 47.5k | 104.3k (52%) | 1686.0k | 19.1k | 0 | 0 |
| 2026-10-07 16:50 | Econometria II | 154 | 47.0k | 166.7k (83%) | 17022.4k | 119.4k | 2 | 0 |
| 2026-10-07 12:22 | Econometria II trabajo | 61 | 45.8k | 137.4k (69%) | 5885.9k | 55.9k | 0 | 0 |
| 2026-10-05 13:04 | Textos oficiales Macroeconomía II | 43 | 45.7k | 123.0k (62%) | 3772.9k | 27.7k | 0 | 0 |
| 2026-10-07 12:42 | Proyecto econometría etapa 1 | 49 | 45.6k | 152.8k (76%) | 4968.1k | 57.4k | 0 | 0 |
| 2026-10-07 13:29 | Econometria II | 83 | 45.9k | 155.8k (78%) | 8815.3k | 63.8k | 0 | 0 |

**Procesado total:** 58876.4k tokens. **48%** es sobrecarga fija (system prompt, herramientas, MCP, skills, CLAUDE.md, memoria) repetida en cada llamada; **27%** es arrastre de lo que entro durante la conversacion; el resto (24%) no se atribuye pieza a pieza (razonamiento interno, recordatorios del sistema, resumenes de compactacion, error de estimacion).

## Arrastre por tipo de pieza

| tipo | arrastre | % |
|---|---:|---:|
| Bash | 3885.6k | 24% |
| respuesta Claude | 2290.1k | 14% |
| Read | 1942.6k | 12% |
| escrito:Bash | 1439.7k | 9% |
| adjunto:file | 1131.3k | 7% |
| Read (completo) | 1027.2k | 6% |
| escrito:Write | 940.2k | 6% |
| prompt usuario | 482.7k | 3% |
| adjunto:total_tokens_reminder | 453.1k | 3% |
| WebSearch | 438.2k | 3% |
| adjunto:deferred_tools_delta | 274.2k | 2% |
| adjunto:environment | 207.3k | 1% |
| escrito:Edit | 176.6k | 1% |
| Glob | 167.0k | 1% |
| adjunto:remote_session_change | 166.6k | 1% |

## Las 20 piezas mas caras

| arrastre | ~tk | releida | tipo | objetivo | sesion |
|---:|---:|---:|---|---|---|
| 328.1k | 5.0k | ×66 | Read | `trabajo/econometria-ii-demre/informe/informe-etapa-1-consens` | Econometria II |
| 323.4k | 6.0k | ×54 | Read | `trabajo/econometria-ii-demre/informe/informe-etapa-1-david.t` | Econometria II |
| 237.8k | 5.2k | ×46 | escrito:Write | `C:\Espacio de trabajo Metodologia de estudio\trabajo\econome` | Econometria II |
| 226.6k | 2.9k | ×77 | adjunto:file | `C:\Users\javie\Downloads\Etapa 1 Todas las Universidades.R` | Econometria II |
| 214.6k | 3.9k | ×55 | Read | `.claude/ctx/pdf/trabajo-econometriii.md` | Econometria II |
| 212.9k | 2.8k | ×77 | adjunto:file | `studio\94efd21d-a586-4d5c-a31e-b3b06ce96725\tool-results\bza` | Econometria II |
| 212.0k | 2.8k | ×77 | adjunto:file | `studio\94efd21d-a586-4d5c-a31e-b3b06ce96725\tool-results\btv` | Econometria II |
| 206.1k | 4.4k | ×47 | Read | `trabajo/econometria-ii-demre/informe/informe-etapa-1-david-l` | Econometria II |
| 179.2k | 3.1k | ×57 | Read | `trabajo/econometria-ii-demre/informe/informe-etapa-1-david-e` | Econometria II |
| 169.3k | 5.8k | ×29 | escrito:Write | `C:\Espacio de trabajo Metodologia de estudio\trabajo\econome` | Econometria II trabajo |
| 152.5k | 2.4k | ×63 | Read | `C:\Users\javie\.claude\projects\C--Espacio-de-trabajo-Metodo` | Econometria II |
| 152.1k | 3.9k | ×39 | Read | `.claude/ctx/pdf/trabajo-econometriii.md` | Proyecto econometría etap |
| 151.5k | 4.1k | ×37 | Glob | `*` | Textos oficiales Macroeco |
| 148.2k | 4.2k | ×35 | Read | `C:\Users\javie\.claude\projects\C--Espacio-de-trabajo-Metodo` | Econometria II |
| 141.5k | 3.1k | ×45 | Read | `C:\Proyecto Metodologia de estudio\datos\trabajos\econometri` | Proyecto econometría etap |
| 120.2k | 1.7k | ×72 | Bash | `cd "C:/Espacio de trabajo Metodologia de estudio"; cat -n tr` | Econometria II |
| 119.2k | 1.5k | ×77 | adjunto:deferred_tools_d | `` | Econometria II |
| 118.4k | 1.5k | ×77 | prompt usuario | `This session is being continued from a previous conversation` | Econometria II |
| 117.7k | 2.6k | ×45 | Read | `C:\Users\javie\.claude\projects\C--Espacio-de-trabajo-Metodo` | Proyecto econometría etap |
| 115.1k | 3.0k | ×39 | adjunto:file | `etodologia de estudio\trabajo\econometria-ii-demre\informe\_` | /retomar econometria-ii. |

## Recomendaciones

1. Sobrecarga fija promedio 46.6k por llamada. Ejecuta `/context` y desactiva los MCP y skills que no uses (cada 10k fijos cuestan 10k × cada llamada).
2. 4 sesiones superaron el 70% de la ventana. Corta con `/handoff` al primer aviso: una sesion nueva arranca en la sobrecarga fija, no en 100k+.
3. 2 imagenes adjuntas (~1.5k tk c/u, arrastre 51.0k). Recorta la captura a la zona relevante.
