# Auditoria de contexto: 2026-10-03

Proyecto `C:\Espacio de trabajo Metodologia de estudio`, ultimas 10 sesiones. Contexto y salida: tokens reales (API). Tamano de cada pieza: estimado. **Arrastre** = tokens de la pieza × llamadas que la releyeron hasta el fin de la sesion o la siguiente compactacion: es lo que realmente consume cuota.

## Sesiones

| inicio | titulo | llamadas | sobrecarga fija | pico | procesado total | salida | compact. | subagentes |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-10-02 17:55 | Econometría II: elección de tema | 54 | 46.0k | 151.1k (76%) | 5096.9k | 62.6k | 0 | 0 |
| 2026-10-02 15:07 | Econometria II Sesion 2 | 53 | 46.0k | 143.1k (72%) | 5247.8k | 57.5k | 0 | 0 |
| 2026-10-02 17:06 | Control remoto en iPad | 8 | 47.4k | 54.4k (27%) | 414.0k | 2.2k | 0 | 0 |
| 2026-10-01 23:26 | Econometría II | 59 | 45.2k | 150.6k (75%) | 5676.1k | 51.8k | 0 | 0 |
| 2026-10-02 14:15 | Comprimir descarga DEMRE | 22 | 45.7k | 80.0k (40%) | 1449.4k | 12.5k | 0 | 0 |
| 2026-09-27 19:26 | crecimiento Chile | 49 | 51.7k | 133.6k (67%) | 4271.2k | 35.0k | 0 | 0 |
| 2026-09-27 15:59 | Lecturas convergencia y crecimiento Chil | 55 | 52.5k | 73.0k (36%) | 3450.6k | 32.0k | 14 | 991.1k |
| 2026-09-27 17:06 | Evaluaciones Micro 2: Mundaca vs Campos | 50 | 51.3k | 71.8k (36%) | 3136.7k | 15.1k | 6 | 0 |
| 2026-09-27 15:05 | Efectos de nivel, crecimiento y transici | 8 | 52.2k | 64.3k (32%) | 462.1k | 6.0k | 0 | 0 |
| 2026-09-26 16:54 | Macroeconomía II sesión inicial | 54 | 44.0k | 72.1k (36%) | 3298.5k | 51.4k | 13 | 0 |

**Procesado total:** 32503.5k tokens. **61%** es sobrecarga fija (system prompt, herramientas, MCP, skills, CLAUDE.md, memoria) repetida en cada llamada; **23%** es arrastre de lo que entro durante la conversacion; el resto (16%) no se atribuye pieza a pieza (razonamiento interno, recordatorios del sistema, resumenes de compactacion, error de estimacion).

## Arrastre por tipo de pieza

| tipo | arrastre | % |
|---|---:|---:|
| respuesta Claude | 1360.4k | 18% |
| Bash | 1191.8k | 16% |
| Read (completo) | 635.9k | 9% |
| Read | 635.5k | 8% |
| adjunto:file | 591.5k | 8% |
| prompt usuario | 494.2k | 7% |
| escrito:Bash | 338.0k | 5% |
| escrito:Write | 250.6k | 3% |
| adjunto:instructions | 239.7k | 3% |
| adjunto:deferred_tools_delta | 210.6k | 3% |
| imagen | 192.0k | 3% |
| Grep | 178.5k | 2% |
| PowerShell | 176.1k | 2% |
| adjunto:total_tokens_reminder | 169.2k | 2% |
| adjunto:mcp_instructions_delta | 94.6k | 1% |

## Las 20 piezas mas caras

| arrastre | ~tk | releida | tipo | objetivo | sesion |
|---:|---:|---:|---|---|---|
| 139.1k | 5.3k | ×26 | Read | `C:\Users\javie\.claude\projects\C--Espacio-de-trabajo-Metodo` | crecimiento Chile |
| 102.8k | 2.7k | ×38 | escrito:Write | `C:\Espacio de trabajo Metodologia de estudio\trabajo\econome` | Econometria II Sesion 2 |
| 101.8k | 1.9k | ×54 | Read | `C:\Proyecto Metodologia de estudio\metodologia-perry-mazur\1` | Econometría II |
| 80.1k | 1.7k | ×48 | Grep | `write\.csv2?/saveRDS/write_csv/group_by/summarise/summarize/` | Econometria II Sesion 2 |
| 77.3k | 1.9k | ×41 | Read | `\c\Proyecto Metodologia de estudio\metodologia-perry-mazur\1` | crecimiento Chile |
| 70.6k | 1.5k | ×46 | Bash | `find "/c/Proyecto Informe PIB Tendencial" -maxdepth 4 2>/dev` | crecimiento Chile |
| 69.3k | 1.4k | ×51 | Bash | `for d in "C:/Espacio de trabajo Metodologia de estudio" "C:/` | Econometria II Sesion 2 |
| 66.0k | 1.2k | ×54 | Read | `C:\Proyecto Metodologia de estudio\datos\trabajos\econometri` | Econometría II |
| 63.6k | 4.0k | ×16 | prompt usuario | `This session is being continued from a previous conversation` | Evaluaciones Micro 2: Mun |
| 61.7k | 1.5k | ×42 | Bash | `cd "C:/Espacio de trabajo Metodologia de estudio/trabajo/eco` | Econometría II |
| 60.8k | 1.2k | ×51 | Read | `.claude/handoffs/2026-10-02-1454-econometria-ii.md` | Econometría II: elección  |
| 59.4k | 1.5k | ×39 | Bash | `F="C:/Users/javie/.claude/projects/C--Espacio-de-trabajo-Met` | Econometria II Sesion 2 |
| 59.2k | 1.1k | ×55 | Read | `C:\Proyecto Metodologia de estudio\.claude\handoffs\2026-10-` | Econometría II |
| 54.0k | 1.5k | ×36 | imagen | `imagen adjunta` | Econometría II |
| 53.1k | 1.5k | ×35 | Bash | `cd "C:/Espacio de trabajo Metodologia de estudio/trabajo/eco` | Econometría II: elección  |
| 53.0k | 1.1k | ×50 | Read | `C:\Proyecto Metodologia de estudio\datos\trabajos\econometri` | Econometría II: elección  |
| 52.4k | 1.1k | ×47 | Grep | `write[._a-z0-9]*\(/saveRDS/save\.image/is\.na\(/n\(\)/ungrou` | Econometria II Sesion 2 |
| 50.8k | 1.2k | ×41 | Bash | `cd "C:/Proyecto Metodologia de estudio/datos/trabajos/econom` | Econometria II Sesion 2 |
| 49.5k | 1.5k | ×33 | imagen | `imagen adjunta` | Econometría II |
| 48.9k | 2.0k | ×25 | escrito:mcp__visualize__ | `{"title": "conceptest_convergencia_bloque4", "loading_messag` | crecimiento Chile |

## Archivos leidos mas de una vez en la misma sesion

- `trabajo/econometria-ii-demre/informe/informe-etapa-1-grupo.pdf` ×2 en *Econometría II: elección de tema*
- `C:\Proyecto Metodologia de estudio\datos\material\macroeconomia-ii\2026-09-23-clase-2-solow.pdf` ×2 en *Lecturas convergencia y crecimiento Chil*
- `C:\Users\javie\OneDrive\Documentos\Proyecto-ClaudeCode\textos\Macroeconomia_II\T02-03_Solow\Apoyo_Solow-Convergencia_y_Cobre_(Informe_T43)\PDF\1_Convergencia\04_ContrerasPinto_2015_ConvergenciaCondicional.pdf` ×2 en *Lecturas convergencia y crecimiento Chil*
- `C:\Users\javie\AppData\Local\Temp\claude\C--Espacio-de-trabajo-Metodologia-de-estudio\7a6a17e8-74b9-4723-82d9-fe068f0742c1\tasks\bux6aqcvh.output` ×2 en *Evaluaciones Micro 2: Mundaca vs Campos*

## Recomendaciones

1. Sobrecarga fija promedio 47.9k por llamada. Ejecuta `/context` y desactiva los MCP y skills que no uses (cada 10k fijos cuestan 10k × cada llamada).
2. 3 sesiones superaron el 70% de la ventana. Corta con `/handoff` al primer aviso: una sesion nueva arranca en la sobrecarga fija, no en 100k+.
3. 4 relecturas del mismo archivo en una sesion: cita la primera lectura o lee solo el rango que cambio.
4. 6 imagenes adjuntas (~1.5k tk c/u, arrastre 192.0k). Recorta la captura a la zona relevante.
