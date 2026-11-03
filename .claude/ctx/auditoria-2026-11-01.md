# Auditoria de contexto: 2026-11-01

Proyecto `C:\Espacio de trabajo Metodologia de estudio`, ultimas 10 sesiones. Contexto y salida: tokens reales (API). Tamano de cada pieza: estimado. **Arrastre** = tokens de la pieza × llamadas que la releyeron hasta el fin de la sesion o la siguiente compactacion: es lo que realmente consume cuota.

## Sesiones

| inicio | titulo | llamadas | sobrecarga fija | pico | procesado total | salida | compact. | subagentes |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-10-31 23:29 | Econometría II Clase 6 - Apuntes | 96 | 58.6k | 164.9k (82%) | 11999.7k | 136.1k | 2 | 0 |
| 2026-11-01 00:31 | Política económica | 4 | 56.8k | 70.4k (35%) | 264.2k | 3.1k | 0 | 0 |
| 2026-11-01 00:02 | Caso real control 2 macro | 27 | 56.8k | 154.4k (77%) | 3158.6k | 74.7k | 1 | 622.0k |
| 2026-10-27 16:35 | Requisitos fase 2 profesor Pfeng | 386 | 56.2k | 167.1k (84%) | 44256.9k | 324.5k | 7 | 0 |
| 2026-10-29 13:02 | Control y clase teórica 2/11 | 72 | 56.6k | 164.5k (82%) | 8309.1k | 69.1k | 1 | 145.1k |
| 2026-10-28 23:35 | Nota para archivo R | 142 | 66.5k | 165.1k (83%) | 16541.1k | 93.8k | 2 | 0 |
| 2026-10-28 19:32 | Econometría M3 | 13 | 57.4k | 97.7k (49%) | 941.2k | 6.3k | 0 | 0 |
| 2026-10-26 17:54 | Econometría sesión de hoy | 92 | 56.2k | 166.9k (83%) | 9327.0k | 81.6k | 1 | 0 |
| 2026-10-28 19:22 | Organizar semana y hoy | 29 | 56.7k | 93.9k (47%) | 2308.8k | 17.6k | 0 | 0 |
| 2026-10-28 14:27 | Simulacro prueba1 anotaciones | 50 | 57.9k | 134.0k (67%) | 4772.0k | 39.7k | 0 | 0 |

**Procesado total:** 101878.7k tokens. **52%** es sobrecarga fija (system prompt, herramientas, MCP, skills, CLAUDE.md, memoria) repetida en cada llamada; **31%** es arrastre de lo que entro durante la conversacion; el resto (17%) no se atribuye pieza a pieza (razonamiento interno, recordatorios del sistema, resumenes de compactacion, error de estimacion).

## Arrastre por tipo de pieza

| tipo | arrastre | % |
|---|---:|---:|
| Bash | 4550.5k | 15% |
| adjunto:file | 3579.0k | 12% |
| Read (completo) | 2866.1k | 9% |
| Read | 2396.2k | 8% |
| respuesta Claude | 2291.8k | 7% |
| adjunto:skill_listing | 2245.5k | 7% |
| escrito:Write | 1811.7k | 6% |
| prompt usuario | 1473.8k | 5% |
| escrito:Bash | 1308.6k | 4% |
| adjunto:deferred_tools_delta | 1053.4k | 3% |
| adjunto:hook_success | 958.6k | 3% |
| adjunto:instructions | 870.5k | 3% |
| Grep | 686.1k | 2% |
| adjunto:invoked_skills | 468.8k | 2% |
| adjunto:agent_listing_delta | 431.2k | 1% |

## Las 20 piezas mas caras

| arrastre | ~tk | releida | tipo | objetivo | sesion |
|---:|---:|---:|---|---|---|
| 335.1k | 7.1k | ×47 | escrito:Write | `C:/Proyecto Metodologia de estudio/datos/trabajos/econometri` | Requisitos fase 2 profeso |
| 307.0k | 18.1k | ×17 | mcp__visualize__read_me | `{"modules": ["diagram"], "platform": "desktop"}` | Econometría sesión de hoy |
| 260.3k | 3.9k | ×67 | adjunto:skill_listing | `` | Requisitos fase 2 profeso |
| 251.6k | 5.5k | ×46 | adjunto:file | `C:\Users\javie\Downloads\GermanCredit_Scorecard.R` | Requisitos fase 2 profeso |
| 247.1k | 7.5k | ×33 | adjunto:file | `C:\Users\javie\Downloads\David_Etapa2_FINAL_AUDITADO_RStudio` | Nota para archivo R |
| 244.8k | 3.9k | ×63 | adjunto:skill_listing | `` | Requisitos fase 2 profeso |
| 242.1k | 6.2k | ×39 | adjunto:file | `C:\Users\javie\Downloads\David_Econometria_Etapa2_Corregido_` | Requisitos fase 2 profeso |
| 232.7k | 8.0k | ×29 | adjunto:file | `sers\javie\Downloads\David_Econometria_II_Etapa_2_VERSION_7_` | Nota para archivo R |
| 221.4k | 3.9k | ×57 | adjunto:skill_listing | `` | Nota para archivo R |
| 220.1k | 3.9k | ×56 | Read | `C:\Users\javie\Downloads\DAVID econometria_etapa2_codigo_fin` | Nota para archivo R |
| 219.8k | 4.1k | ×53 | adjunto:invoked_skills | `` | Econometría II Clase 6 -  |
| 210.6k | 4.7k | ×45 | escrito:Write | `C:/Proyecto Metodologia de estudio/datos/trabajos/econometri` | Requisitos fase 2 profeso |
| 209.8k | 3.9k | ×54 | adjunto:skill_listing | `` | Requisitos fase 2 profeso |
| 205.9k | 3.9k | ×53 | adjunto:skill_listing | `` | Econometría II Clase 6 -  |
| 193.0k | 3.9k | ×49 | escrito:Write | `C:\Proyecto Metodologia de estudio\datos\trabajos\econometri` | Nota para archivo R |
| 191.8k | 3.6k | ×54 | escrito:Write | `C:/Proyecto Metodologia de estudio/datos/trabajos/econometri` | Requisitos fase 2 profeso |
| 190.4k | 3.9k | ×49 | adjunto:skill_listing | `` | Requisitos fase 2 profeso |
| 183.1k | 3.9k | ×47 | prompt usuario | `Base directory for this skill: C:\Users\javie\.claude\skills` | Control y clase teórica 2 |
| 182.6k | 3.9k | ×47 | adjunto:skill_listing | `` | Requisitos fase 2 profeso |
| 176.9k | 8.0k | ×22 | adjunto:file | `ers\javie\Downloads\David_Econometria_II_Etapa_2_CORREGIDA_L` | Nota para archivo R |

## Archivos leidos mas de una vez en la misma sesion

- `C:\Proyecto Metodologia de estudio\datos\clases\2026-10-29-econometria-ii-clase-6.md` ×2 en *Econometría II Clase 6 - Apuntes*
- `C:\Proyecto Metodologia de estudio\datos\material\macroeconomia-ii\2026-10-29-prediccion-control-2.md` ×2 en *Caso real control 2 macro*
- `trabajo/jv5-traduccion.txt` ×2 en *Caso real control 2 macro*
- `C:\Users\javie\Downloads\PPT Econometria_II___Etapa_1__presentacion_.pdf` ×5 en *Requisitos fase 2 profesor Pfeng*

## Recomendaciones

1. Sobrecarga fija promedio 58.2k por llamada. Ejecuta `/context` y desactiva los MCP y skills que no uses (cada 10k fijos cuestan 10k × cada llamada).
2. 3 lecturas completas de archivos > 4.0k tk (arrastre 212.6k). `hook-read` las frena desde ahora.
3. 6 sesiones superaron el 70% de la ventana. Corta con `/handoff` al primer aviso: una sesion nueva arranca en la sobrecarga fija, no en 100k+.
4. 4 relecturas del mismo archivo en una sesion: cita la primera lectura o lee solo el rango que cambio.
5. 1 imagenes adjuntas (~1.5k tk c/u, arrastre 46.5k). Recorta la captura a la zona relevante.
