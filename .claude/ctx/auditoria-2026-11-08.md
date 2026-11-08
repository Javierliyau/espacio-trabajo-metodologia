# Auditoria de contexto: 2026-11-08

Proyecto `C:\Espacio de trabajo Metodologia de estudio`, ultimas 10 sesiones. Contexto y salida: tokens reales (API). Tamano de cada pieza: estimado. **Arrastre** = tokens de la pieza × llamadas que la releyeron hasta el fin de la sesion o la siguiente compactacion: es lo que realmente consume cuota.

## Sesiones

| inicio | titulo | llamadas | sobrecarga fija | pico | procesado total | salida | compact. | subagentes |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-11-07 13:23 | Retomar comente-droller-pep1 | 85 | 0 | 166.6k (83%) | 9557.7k | 76.8k | 2 | 0 |
| 2026-11-07 20:47 | Primera sesión Micro | 42 | 59.3k | 144.5k (72%) | 4344.4k | 31.1k | 0 | 0 |
| 2026-11-07 18:31 | Como es este | 8 | 59.9k | 72.1k (36%) | 529.1k | 9.0k | 0 | 0 |
| 2026-11-07 15:29 | Retomar entrenamiento comentes | 58 | 59.0k | 143.8k (72%) | 5747.9k | 55.5k | 0 | 0 |
| 2026-11-07 12:59 | Retomar entrenamiento comentes | 49 | 59.0k | 129.1k (65%) | 4474.7k | 43.5k | 0 | 0 |
| 2026-11-07 14:08 | Ajustar calendario según viernes | 21 | 58.6k | 116.4k (58%) | 1949.1k | 25.3k | 0 | 0 |
| 2026-11-07 11:39 | Retomar comente-droller-pep1 | 72 | 58.9k | 135.3k (68%) | 7179.4k | 93.1k | 1 | 0 |
| 2026-11-07 11:48 | Responder comentarios V/F de Droller | 45 | 58.6k | 149.8k (75%) | 4885.5k | 54.4k | 0 | 0 |
| 2026-11-07 11:17 | Motor de predicción análisis | 56 | 59.6k | 155.5k (78%) | 6255.7k | 39.1k | 0 | 0 |
| 2026-11-07 11:14 | Macro continuación | 4 | 58.5k | 64.3k (32%) | 247.1k | 1.6k | 0 | 0 |

**Procesado total:** 45170.6k tokens. **46%** es sobrecarga fija (system prompt, herramientas, MCP, skills, CLAUDE.md, memoria) repetida en cada llamada; **24%** es arrastre de lo que entro durante la conversacion; el resto (29%) no se atribuye pieza a pieza (razonamiento interno, recordatorios del sistema, resumenes de compactacion, error de estimacion).

## Arrastre por tipo de pieza

| tipo | arrastre | % |
|---|---:|---:|
| Bash | 2244.8k | 21% |
| Read (completo) | 1664.3k | 15% |
| escrito:Write | 1374.7k | 13% |
| respuesta Claude | 1036.9k | 9% |
| escrito:Bash | 687.3k | 6% |
| Read | 637.0k | 6% |
| prompt usuario | 494.8k | 5% |
| adjunto:skill_listing | 458.4k | 4% |
| mcp:read_me | 307.0k | 3% |
| adjunto:file | 281.9k | 3% |
| adjunto:deferred_tools_delta | 253.7k | 2% |
| imagen | 219.0k | 2% |
| adjunto:hook_success | 177.9k | 2% |
| adjunto:agent_listing_delta | 154.7k | 1% |
| adjunto:instructions | 102.4k | 1% |

## Las 20 piezas mas caras

| arrastre | ~tk | releida | tipo | objetivo | sesion |
|---:|---:|---:|---|---|---|
| 608.5k | 12.2k | ×50 | escrito:Write | `C:\Proyecto Metodologia de estudio\datos\material\macroecono` | Retomar comente-droller-p |
| 413.7k | 12.2k | ×34 | escrito:Write | `C:\Proyecto Metodologia de estudio\datos\material\macroecono` | Retomar comente-droller-p |
| 307.0k | 18.1k | ×17 | mcp__visualize__read_me | `{"modules": ["diagram"], "platform": "desktop"}` | Primera sesión Micro |
| 241.0k | 4.4k | ×55 | prompt usuario | `Base directory for this skill: C:\Users\javie\.claude\skills` | Motor de predicción análi |
| 194.2k | 3.9k | ×50 | adjunto:skill_listing | `` | Retomar comente-droller-p |
| 166.1k | 6.6k | ×25 | escrito:Write | `C:/Proyecto Metodologia de estudio/datos/material/macroecono` | Responder comentarios V/F |
| 132.1k | 3.9k | ×34 | adjunto:skill_listing | `` | Retomar comente-droller-p |
| 132.1k | 3.9k | ×34 | adjunto:skill_listing | `` | Retomar comente-droller-p |
| 125.6k | 3.7k | ×34 | prompt usuario | `This session is being continued from a previous conversation` | Retomar comente-droller-p |
| 124.2k | 3.0k | ×41 | Read | `C:\Proyecto Metodologia de estudio\datos\material\macroecono` | Responder comentarios V/F |
| 115.5k | 2.3k | ×50 | adjunto:file | `studio\f1ad7075-9c00-4998-a957-cc357e4f4c04\tool-results\b7a` | Retomar comente-droller-p |
| 86.6k | 2.7k | ×32 | Read | `C:\Users\javie\.claude\projects\C--Espacio-de-trabajo-Metodo` | Responder comentarios V/F |
| 84.9k | 1.7k | ×50 | adjunto:deferred_tools_d | `` | Retomar comente-droller-p |
| 78.5k | 2.3k | ×34 | adjunto:file | `studio\f1ad7075-9c00-4998-a957-cc357e4f4c04\tool-results\b7a` | Retomar comente-droller-p |
| 75.4k | 1.5k | ×50 | adjunto:hook_success | `` | Retomar comente-droller-p |
| 74.5k | 1.4k | ×54 | Read | `.claude/ctx/pdf/pauta-control1.md` | Motor de predicción análi |
| 71.2k | 1.6k | ×44 | Bash | `cd "C:/Proyecto Metodologia de estudio" && ls datos/programa` | Responder comentarios V/F |
| 70.2k | 2.1k | ×34 | prompt usuario | `This session is being continued from a previous conversation` | Retomar comente-droller-p |
| 69.6k | 1.3k | ×52 | Read | `C:\Proyecto Metodologia de estudio\datos\material\macroecono` | Retomar entrenamiento com |
| 67.0k | 2.0k | ×34 | Read | `C:\Proyecto Metodologia de estudio\datos\material\macroecono` | Motor de predicción análi |

## Archivos leidos mas de una vez en la misma sesion

- `trabajo/macro/pb/p-02.png` ×2 en *Retomar comente-droller-pep1*
- `trabajo/macro/pb/p-03.png` ×3 en *Retomar comente-droller-pep1*
- `trabajo/macro/pb/p-04.png` ×2 en *Retomar comente-droller-pep1*
- `trabajo/macro/pb/e-4.png` ×2 en *Retomar comente-droller-pep1*
- `C:\Proyecto Metodologia de estudio\datos\material\microeconomia-ii\2026-11-07-grafico-competencia-monopolistica-lp.png` ×2 en *Primera sesión Micro*
- `trabajo/macro/pb/p-02.png` ×2 en *Retomar comente-droller-pep1*
- `trabajo/macro/pb/p-03.png` ×3 en *Retomar comente-droller-pep1*
- `trabajo/macro/pb/p-04.png` ×2 en *Retomar comente-droller-pep1*
- `trabajo/macro/pb/e-4.png` ×2 en *Retomar comente-droller-pep1*

## Recomendaciones

1. Sobrecarga fija promedio 47.6k por llamada. Ejecuta `/context` y desactiva los MCP y skills que no uses (cada 10k fijos cuestan 10k × cada llamada).
2. 5 sesiones superaron el 70% de la ventana. Corta con `/handoff` al primer aviso: una sesion nueva arranca en la sobrecarga fija, no en 100k+.
3. Lo escrito con Write/Edit arrastra 1430.8k (13%): el contenido de cada archivo escrito queda en el chat. Documentos largos: redactarlos en un subagente o cerrar con /handoff justo despues de escribirlos.
4. 9 relecturas del mismo archivo en una sesion: cita la primera lectura o lee solo el rango que cambio.
5. 12 imagenes adjuntas (~1.5k tk c/u, arrastre 219.0k). Recorta la captura a la zona relevante.
