# Auditoria de contexto: 2026-11-22

Proyecto `C:\Espacio de trabajo Metodologia de estudio`, ultimas 10 sesiones. Contexto y salida: tokens reales (API). Tamano de cada pieza: estimado. **Arrastre** = tokens de la pieza × llamadas que la releyeron hasta el fin de la sesion o la siguiente compactacion: es lo que realmente consume cuota.

## Sesiones

| inicio | titulo | llamadas | sobrecarga fija | pico | procesado total | salida | compact. | subagentes |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-11-17 12:42 | Calendario tentativo 23 de lunes | 82 | 57.9k | 167.3k (84%) | 8501.4k | 68.3k | 1 | 0 |
| 2026-11-01 16:07 | Análisis modelo motor de predicción | 98 | 56.8k | 172.0k (86%) | 11092.1k | 213.5k | 5 | 6247.8k |
| 2026-11-20 20:18 | Sesión de estudio vie 20: C2 Micro · M4  | 20 | 60.5k | 80.5k (40%) | 1406.7k | 7.3k | 0 | 0 |
| 2026-11-19 23:28 | Sesión de estudio jue 19: μ1 · M4 | 25 | 61.4k | 96.0k (48%) | 1979.8k | 10.3k | 0 | 0 |
| 2026-11-13 15:39 | Método y fuentes del plan paro | 23 | 57.4k | 104.8k (52%) | 1901.5k | 15.1k | 0 | 0 |
| 2026-11-11 12:53 | Plan paro | 55 | 60.2k | 148.7k (74%) | 5537.0k | 43.5k | 0 | 0 |
| 2026-11-11 16:27 | Conversación sobre ocio e hiperfoco | 17 | 60.0k | 98.6k (49%) | 1376.3k | 28.6k | 0 | 766.2k |
| 2026-11-19 22:41 | Sesión de estudio jue 19: μ1 · M4 | 20 | 61.4k | 85.0k (42%) | 1516.2k | 7.8k | 0 | 0 |
| 2026-11-13 22:01 | Historia: primera sesión de paro (vie 13 | 17 | 61.4k | 99.3k (50%) | 1393.8k | 12.0k | 0 | 0 |
| 2026-11-17 12:57 | Método de estudio para PEP | 87 | 59.3k | 166.6k (83%) | 9967.8k | 99.8k | 1 | 0 |

**Procesado total:** 44672.6k tokens. **59%** es sobrecarga fija (system prompt, herramientas, MCP, skills, CLAUDE.md, memoria) repetida en cada llamada; **24%** es arrastre de lo que entro durante la conversacion; el resto (18%) no se atribuye pieza a pieza (razonamiento interno, recordatorios del sistema, resumenes de compactacion, error de estimacion).

## Arrastre por tipo de pieza

| tipo | arrastre | % |
|---|---:|---:|
| Bash | 1613.7k | 15% |
| respuesta Claude | 1129.0k | 11% |
| adjunto:file | 1066.5k | 10% |
| Read (completo) | 1063.5k | 10% |
| prompt usuario | 672.3k | 6% |
| adjunto:hook_success | 631.7k | 6% |
| Read | 629.2k | 6% |
| adjunto:skill_listing | 555.7k | 5% |
| escrito:Write | 454.0k | 4% |
| escrito:Bash | 393.1k | 4% |
| adjunto:deferred_tools_delta | 347.2k | 3% |
| Grep | 284.5k | 3% |
| adjunto:instructions | 215.4k | 2% |
| adjunto:agent_listing_delta | 156.9k | 1% |
| adjunto:remote_session_change | 141.7k | 1% |

## Las 20 piezas mas caras

| arrastre | ~tk | releida | tipo | objetivo | sesion |
|---:|---:|---:|---|---|---|
| 197.3k | 4.8k | ×41 | Read | `.claude/ctx/pdf/2026-11-17-pep1-version-final-2-bloques.md` | Método de estudio para PE |
| 160.2k | 7.3k | ×22 | escrito:Write | `C:/Espacio de trabajo Metodologia de estudio/trabajo/micro/2` | Análisis modelo motor de  |
| 132.1k | 3.9k | ×34 | adjunto:skill_listing | `` | Análisis modelo motor de  |
| 129.7k | 2.4k | ×53 | Read | `C:\Users\javie\.claude\projects\C--Espacio-de-trabajo-Metodo` | Calendario tentativo 23 d |
| 128.3k | 3.9k | ×33 | adjunto:skill_listing | `` | Método de estudio para PE |
| 105.2k | 2.0k | ×52 | Read | `.claude/ctx/pdf/2026-11-09-simulacro-final-pep-1-mundaca.md` | Método de estudio para PE |
| 97.2k | 3.9k | ×25 | adjunto:skill_listing | `` | Calendario tentativo 23 d |
| 96.1k | 1.8k | ×52 | Read | `.claude/ctx/pdf/2026-11-09-matematicos-tal-cual-pep1.md` | Método de estudio para PE |
| 85.5k | 3.9k | ×22 | adjunto:skill_listing | `` | Análisis modelo motor de  |
| 79.9k | 2.3k | ×34 | adjunto:file | `tudio\datos\material\microeconomia-ii\2026-11-01-feedback-co` | Análisis modelo motor de  |
| 78.6k | 2.4k | ×33 | adjunto:file | `C:\Proyecto Metodologia de estudio\datos\agenda\plan-pep-nov` | Método de estudio para PE |
| 72.4k | 3.3k | ×22 | prompt usuario | `This session is being continued from a previous conversation` | Análisis modelo motor de  |
| 69.4k | 2.1k | ×33 | adjunto:file | `de estudio\.claude\ctx\pdf\2026-11-09-simulacro-final-pep-1-` | Método de estudio para PE |
| 68.9k | 2.5k | ×28 | adjunto:hook_success | `` | Plan paro |
| 67.5k | 3.1k | ×22 | adjunto:file | `C:\Proyecto Metodologia de estudio\datos\agenda\calendario.m` | Análisis modelo motor de  |
| 66.1k | 1.5k | ×43 | Read | `trabajo/pdfs-entrada/sesion7-7_11.pdf` | Plan paro |
| 66.1k | 1.5k | ×43 | Read | `trabajo/pdfs-entrada/practica-pep1.pdf` | Plan paro |
| 65.9k | 2.4k | ×27 | adjunto:hook_success | `` | Plan paro |
| 64.8k | 1.4k | ×47 | Bash | `F="C:/Users/javie/.claude/projects/C--Espacio-de-trabajo-Met` | Plan paro |
| 63.9k | 1.3k | ×50 | Bash | `F="C:/Users/javie/.claude/projects/C--Espacio-de-trabajo-Met` | Plan paro |

## Archivos leidos mas de una vez en la misma sesion

- `C:\Proyecto Metodologia de estudio\datos\material\microeconomia-ii\2026-11-09-simulacro-final-pep-1-mundaca.pdf` ×2 en *Sesión de estudio vie 20: C2 Micro · M4 *
- `trabajo/sesion2/sesion2.pdf` ×2 en *Sesión de estudio jue 19: μ1 · M4*
- `trabajo/pdfs-entrada/sesion7-7_11.pdf` ×2 en *Plan paro*
- `trabajo/pdfs-entrada/practica-pep1.pdf` ×2 en *Plan paro*
- `trabajo/sesion2/sesion2.pdf` ×2 en *Sesión de estudio jue 19: μ1 · M4*
- `.claude/ctx/pdf/2026-11-17-pep1-version-final-2-bloques.md` ×2 en *Método de estudio para PEP*

## Recomendaciones

1. Sobrecarga fija promedio 58.9k por llamada. Ejecuta `/context` y desactiva los MCP y skills que no uses (cada 10k fijos cuestan 10k × cada llamada).
2. 1 lecturas completas de archivos > 4.0k tk (arrastre 197.3k). `hook-read` las frena desde ahora.
3. 4 sesiones superaron el 70% de la ventana. Corta con `/handoff` al primer aviso: una sesion nueva arranca en la sobrecarga fija, no en 100k+.
4. 6 relecturas del mismo archivo en una sesion: cita la primera lectura o lee solo el rango que cambio.
5. 7 imagenes adjuntas (~1.5k tk c/u, arrastre 84.0k). Recorta la captura a la zona relevante.
