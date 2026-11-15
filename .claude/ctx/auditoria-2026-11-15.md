# Auditoria de contexto: 2026-11-15

Proyecto `C:\Espacio de trabajo Metodologia de estudio`, ultimas 10 sesiones. Contexto y salida: tokens reales (API). Tamano de cada pieza: estimado. **Arrastre** = tokens de la pieza × llamadas que la releyeron hasta el fin de la sesion o la siguiente compactacion: es lo que realmente consume cuota.

## Sesiones

| inicio | titulo | llamadas | sobrecarga fija | pico | procesado total | salida | compact. | subagentes |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-11-13 22:01 | Historia: primera sesión de paro (vie 13 | 17 | 61.4k | 99.3k (50%) | 1393.8k | 12.0k | 0 | 0 |
| 2026-11-13 21:44 | Plan historia económica PEP | 38 | 59.9k | 134.7k (67%) | 3778.2k | 39.0k | 0 | 0 |
| 2026-11-13 19:02 | Plan paro continuación | 95 | 57.4k | 167.0k (83%) | 10180.0k | 61.0k | 1 | 0 |
| 2026-11-13 20:34 | Plan de paro vie 13: bloque de Macro y t | 25 | 60.7k | 101.7k (51%) | 2058.0k | 17.8k | 0 | 0 |
| 2026-11-13 15:31 | Organizar exposiciones Ingeco26 | 14 | 58.5k | 77.2k (39%) | 961.1k | 7.9k | 0 | 0 |
| 2026-11-13 15:46 | Plan paro continuación | 73 | 57.4k | 153.6k (77%) | 7583.3k | 47.4k | 0 | 0 |
| 2026-11-13 15:39 | Método y fuentes del plan paro | 23 | 57.4k | 104.8k (52%) | 1901.5k | 15.1k | 0 | 0 |
| 2026-11-11 12:53 | Plan paro | 55 | 60.2k | 148.7k (74%) | 5537.0k | 43.5k | 0 | 0 |
| 2026-11-13 13:23 | Plan paro continuación | 51 | 57.4k | 119.7k (60%) | 4569.8k | 34.4k | 0 | 0 |
| 2026-11-01 16:07 | Análisis modelo motor de predicción | 98 | 56.8k | 172.0k (86%) | 11092.1k | 213.5k | 5 | 6247.8k |

**Procesado total:** 49054.9k tokens. **58%** es sobrecarga fija (system prompt, herramientas, MCP, skills, CLAUDE.md, memoria) repetida en cada llamada; **21%** es arrastre de lo que entro durante la conversacion; el resto (21%) no se atribuye pieza a pieza (razonamiento interno, recordatorios del sistema, resumenes de compactacion, error de estimacion).

## Arrastre por tipo de pieza

| tipo | arrastre | % |
|---|---:|---:|
| Bash | 2799.6k | 27% |
| respuesta Claude | 1179.1k | 11% |
| Read | 842.6k | 8% |
| adjunto:file | 664.5k | 6% |
| escrito:Bash | 609.8k | 6% |
| prompt usuario | 514.2k | 5% |
| adjunto:hook_success | 417.4k | 4% |
| imagen | 391.5k | 4% |
| escrito:Write | 385.6k | 4% |
| adjunto:skill_listing | 373.0k | 4% |
| adjunto:deferred_tools_delta | 327.1k | 3% |
| Grep | 283.0k | 3% |
| Read (completo) | 235.8k | 2% |
| adjunto:remote_session_change | 162.5k | 2% |
| adjunto:instructions | 144.6k | 1% |

## Las 20 piezas mas caras

| arrastre | ~tk | releida | tipo | objetivo | sesion |
|---:|---:|---:|---|---|---|
| 160.2k | 7.3k | ×22 | escrito:Write | `C:/Espacio de trabajo Metodologia de estudio/trabajo/micro/2` | Análisis modelo motor de  |
| 132.1k | 3.9k | ×34 | adjunto:skill_listing | `` | Análisis modelo motor de  |
| 109.0k | 1.5k | ×75 | Bash | `cd "C:/Proyecto Metodologia de estudio/datos/agenda" && grep` | Plan paro continuación |
| 96.0k | 1.5k | ×66 | Bash | `cd "C:/Proyecto Metodologia de estudio/datos/agenda" && "C:/` | Plan paro continuación |
| 93.0k | 1.5k | ×64 | Bash | `cd "C:/Proyecto Metodologia de estudio/datos/agenda" && grep` | Plan paro continuación |
| 85.5k | 3.9k | ×22 | adjunto:skill_listing | `` | Análisis modelo motor de  |
| 83.7k | 1.0k | ×81 | Bash | `cd "C:/Espacio de trabajo Metodologia de estudio" && cat ".c` | Plan paro continuación |
| 82.2k | 1.6k | ×53 | Bash | `cd "C:/Proyecto Metodologia de estudio/datos/agenda" && sed ` | Plan paro continuación |
| 81.0k | 1.5k | ×54 | imagen | `imagen adjunta` | Plan paro continuación |
| 80.0k | 1.5k | ×55 | Bash | `cd "C:/Proyecto Metodologia de estudio/datos/agenda" && "C:/` | Plan paro continuación |
| 79.9k | 2.3k | ×34 | adjunto:file | `tudio\datos\material\microeconomia-ii\2026-11-01-feedback-co` | Análisis modelo motor de  |
| 75.0k | 2.3k | ×33 | Read | `C:\Users\javie\.claude\projects\C--Espacio-de-trabajo-Metodo` | Plan historia económica P |
| 72.4k | 3.3k | ×22 | prompt usuario | `This session is being continued from a previous conversation` | Análisis modelo motor de  |
| 72.3k | 1.0k | ×70 | Bash | `cd "C:/Espacio de trabajo Metodologia de estudio" && cat ".c` | Plan paro continuación |
| 70.2k | 1.0k | ×70 | Bash | `cd "C:/Proyecto Metodologia de estudio/datos/agenda" && awk ` | Plan paro continuación |
| 68.9k | 2.5k | ×28 | adjunto:hook_success | `` | Plan paro |
| 68.0k | 3.1k | ×22 | Read | `C:\Proyecto Metodologia de estudio\datos\material\historia-e` | Plan historia económica P |
| 67.5k | 3.1k | ×22 | adjunto:file | `C:\Proyecto Metodologia de estudio\datos\agenda\calendario.m` | Análisis modelo motor de  |
| 66.1k | 1.5k | ×43 | Read | `trabajo/pdfs-entrada/sesion7-7_11.pdf` | Plan paro |
| 66.1k | 1.5k | ×43 | Read | `trabajo/pdfs-entrada/practica-pep1.pdf` | Plan paro |

## Archivos leidos mas de una vez en la misma sesion

- `trabajo/pdfs-entrada/sesion7-7_11.pdf` ×2 en *Plan paro*
- `trabajo/pdfs-entrada/practica-pep1.pdf` ×2 en *Plan paro*

## Recomendaciones

1. Sobrecarga fija promedio 58.2k por llamada. Ejecuta `/context` y desactiva los MCP y skills que no uses (cada 10k fijos cuestan 10k × cada llamada).
2. 4 sesiones superaron el 70% de la ventana. Corta con `/handoff` al primer aviso: una sesion nueva arranca en la sobrecarga fija, no en 100k+.
3. 2 relecturas del mismo archivo en una sesion: cita la primera lectura o lee solo el rango que cambio.
4. 17 imagenes adjuntas (~1.5k tk c/u, arrastre 391.5k). Recorta la captura a la zona relevante.
