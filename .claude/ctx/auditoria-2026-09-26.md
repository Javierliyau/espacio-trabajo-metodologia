# Auditoria de contexto: 2026-09-26

Proyecto `C:\Espacio de trabajo Metodologia de estudio`, ultimas 2 sesiones. Contexto y salida: tokens reales (API). Tamano de cada pieza: estimado. **Arrastre** = tokens de la pieza × llamadas que la releyeron hasta el fin de la sesion o la siguiente compactacion: es lo que realmente consume cuota.

## Sesiones

| inicio | titulo | llamadas | sobrecarga fija | pico | procesado total | salida | compact. | subagentes |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-09-26 14:00 | Transcripción clase Política Económica | 14 | 43.2k | 66.2k (44%) | 750.7k | 10.1k | 0 | 0 |
| 2026-09-24 23:22 | Esqueleto informe política monetaria | 80 | 57.7k | 116.4k (78%) | 7001.6k | 120.7k | 3 | 4107.9k |

**Procesado total:** 7752.3k tokens. **67%** es sobrecarga fija (system prompt, herramientas, MCP, skills, CLAUDE.md, memoria) repetida en cada llamada; **24%** es arrastre de lo que entro durante la conversacion; el resto (9%) no se atribuye pieza a pieza (razonamiento interno, recordatorios del sistema, resumenes de compactacion, error de estimacion).

## Arrastre por tipo de pieza

| tipo | arrastre | % |
|---|---:|---:|
| adjunto:file | 222.4k | 12% |
| Bash | 210.0k | 11% |
| prompt usuario | 203.9k | 11% |
| respuesta Claude | 203.1k | 11% |
| escrito:Write | 140.1k | 8% |
| Read (completo) | 136.5k | 7% |
| adjunto:instructions | 96.6k | 5% |
| adjunto:deferred_tools_delta | 84.6k | 5% |
| adjunto:skill_listing | 55.0k | 3% |
| escrito:Bash | 54.9k | 3% |
| Read | 51.2k | 3% |
| adjunto:mcp_instructions_delta | 50.4k | 3% |
| adjunto:agent_listing_delta | 40.3k | 2% |
| imagen | 34.5k | 2% |
| Agent | 32.3k | 2% |

## Las 20 piezas mas caras

| arrastre | ~tk | releida | tipo | objetivo | sesion |
|---:|---:|---:|---|---|---|
| 103.2k | 4.7k | ×22 | Read | `C:\Proyecto Metodologia de estudio\datos\informe-pe\00-ESPAC` | Esqueleto informe polític |
| 80.1k | 3.3k | ×24 | prompt usuario | `This session is being continued from a previous conversation` | Esqueleto informe polític |
| 73.0k | 4.1k | ×18 | prompt usuario | `This session is being continued from a previous conversation` | Esqueleto informe polític |
| 61.8k | 2.6k | ×24 | adjunto:file | `ologia de estudio\datos\programas\macroeconomia-ii-programa-` | Esqueleto informe polític |
| 55.3k | 3.1k | ×18 | escrito:Write | `C:\Proyecto Metodologia de estudio\datos\informe-pe\diseno-i` | Esqueleto informe polític |
| 55.0k | 5.0k | ×11 | adjunto:skill_listing | `` | Esqueleto informe polític |
| 49.8k | 3.1k | ×16 | Bash | `cd "/c/Proyecto Metodologia de estudio/datos/informe-pe"; se` | Esqueleto informe polític |
| 46.9k | 2.0k | ×24 | adjunto:file | `C:\Proyecto Metodologia de estudio\datos\informe-pe\quiz-esq` | Esqueleto informe polític |
| 45.4k | 3.8k | ×12 | prompt usuario | `This session is being continued from a previous conversation` | Esqueleto informe polític |
| 44.2k | 1.8k | ×24 | escrito:Write | `C:\Proyecto Metodologia de estudio\datos\informe-pe\quiz-esq` | Esqueleto informe polític |
| 43.6k | 2.7k | ×16 | Bash | `cd "/c/Proyecto Metodologia de estudio/datos/informe-pe"; se` | Esqueleto informe polític |
| 42.9k | 1.8k | ×24 | adjunto:instructions | `` | Esqueleto informe polític |
| 35.2k | 2.0k | ×18 | adjunto:file | `C:\Proyecto Metodologia de estudio\datos\informe-pe\quiz-esq` | Esqueleto informe polític |
| 34.5k | 1.5k | ×23 | imagen | `imagen adjunta` | Esqueleto informe polític |
| 33.5k | 1.4k | ×24 | adjunto:deferred_tools_d | `` | Esqueleto informe polític |
| 32.2k | 1.8k | ×18 | adjunto:instructions | `` | Esqueleto informe polític |
| 31.4k | 1.7k | ×18 | Agent | `Research Víctor Salas profile` | Esqueleto informe polític |
| 31.0k | 2.1k | ×15 | respuesta Claude | `Te lo resumo todo acá en el chat, sin que tengas que abrir a` | Esqueleto informe polític |
| 25.9k | 1.4k | ×18 | adjunto:file | `o de trabajo Metodologia de estudio\trabajo\optimizacion-inf` | Esqueleto informe polític |
| 25.1k | 1.4k | ×18 | adjunto:deferred_tools_d | `` | Esqueleto informe polític |

## Archivos leidos mas de una vez en la misma sesion

- `C:\Proyecto Metodologia de estudio\datos\informe-pe\00-ESPACIO-TEMA-43.md` ×2 en *Esqueleto informe política monetaria*
- `C:\Proyecto Metodologia de estudio\datos\informe-pe\00-ESPACIO-TEMA-43.md [L112+2]` ×2 en *Esqueleto informe política monetaria*
- `C:\Proyecto Metodologia de estudio\datos\informe-pe\diseno-informe-tendencial.md` ×2 en *Esqueleto informe política monetaria*

## Recomendaciones

1. Sobrecarga fija promedio 55.5k por llamada. Ejecuta `/context` y desactiva los MCP y skills que no uses (cada 10k fijos cuestan 10k × cada llamada).
2. 2 lecturas completas de archivos > 4.0k tk (arrastre 126.2k). `hook-read` las frena desde ahora.
3. 2 salidas de terminal > 2.5k tk (arrastre 93.3k). Filtra con `| head`, `grep`, `--stat`, o pide solo conteos.
4. 1 sesiones superaron el 70% de la ventana. Corta con `/handoff` al primer aviso: una sesion nueva arranca en la sobrecarga fija, no en 100k+.
5. 3 relecturas del mismo archivo en una sesion: cita la primera lectura o lee solo el rango que cambio.
6. 1 imagenes adjuntas (~1.5k tk c/u, arrastre 34.5k). Recorta la captura a la zona relevante.
