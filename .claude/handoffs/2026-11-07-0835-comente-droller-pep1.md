---
tema: comente-droller-pep1
fecha: 2026-11-07 08:35
resumen: Pauta oficial del Control 1 de Macro II al banco y al motor; anatomía del comente V/F de Droller y plan para la PEP 1 (lun 9-11)
---
## Objetivo
Responder los comentes V/F de la PEP 1 de Macro II (Droller, lun 9-11, 09:50) calcados al formato de la pauta, y mantener al día el banco y el motor de predicción.

## Hecho en esta sesión
- `Downloads/Pauta_control1.pdf` (pauta oficial del Control 1) ingresado al banco. Ficha `macroeconomia-ii/2026-2-control-1-droller` limpia: 5 preguntas oficiales de 12 pts, sin la versión de memoria. Respaldo de la ficha fusionada en `trabajo/control1-ficha-fusionada.bak.json`.
- Motor: `preparar` ok. `motor corregir` del Control 1: Brier 0,356 → 0,189 (mejor que las líneas base, 0,250). `ciclo` sin retador. Nueva predicción de la PEP 1: registro `20261107-083539-pep-1.json` (v1.1, U1-U6). El motor pone U1 25 % y U2 14 %, contra la lectura cualitativa (Solow ~45 %). Con 2 pruebas en el banco, manda la predicción cualitativa.
- Predicción PEP 1 §7 «Ajuste v3»: S4 0,80, F6 0,60, S3 0,65.
- Creado: anatomía del comente, con la plantilla C0-C6, la rúbrica deducida de 12 pts, la comparación de una respuesta de ~5/12 con una de 12/12 y la estrategia.
- `calendario.md`: Control 1 registrado en el banco. Bitácora anotada.

## Decisiones tomadas (no re-litigar)
- La plantilla tiene 7 casillas en orden fijo: veredicto, concesión, ecuación, gráfico, mecanismo, CP/LP y cierre.
- Pregunta de tasas → gráfico $s\,y/k$ contra $n+\delta$. Pregunta de niveles → $sf(k)$ contra $(n+\delta)k$.
- El reparto de los 12 pts es una deducción: se recalibra cuando llegue el Control 1 corregido (después de la PEP).

## Próximo paso exacto
**Pedido nuevo (7-11, 08:40):** armar hoy una «prueba-banco» exhaustiva con pauta 12/12 en formato C0-C6. Comentes: los de la guía con p alta, más extras que cubran cada candidato con p ≥ 0,3 (§3 de la predicción). Matemáticos: los moldes S1-S6 y R1-R4. Hoy se practica en recuperación (tapar la pauta, escribir, corregir por hitos); no se relee. **No se debe repetir ningún ítem del simulacro del dom 8** (`2026-11-08-simulacro-pep-1-PAUTA-no-abrir.md`): revisarlo antes para evitar solapes, y si hay cruce, cambiar el ítem de la prueba-banco. Mañana: corrección y luego el simulacro final cronometrado (M4).
Después:
El estudiante escribe en frío P3, P4 y P5 del Control 1 (5 min c/u) al final de M2 y manda la foto. Se corrige hito por hito con la §3 de la anatomía y cada hito perdido se anota en `trabajo/macro/errores-pep1.md`.

## Pendientes
- Dom 8: 4 comentes de la guía en formato completo antes de M4 (los fallados en M1, o si no 2, 5, 13 y 16). Corregir el simulacro con la rúbrica.
- Cuando entreguen el Control 1: anotar `obtenido` por pregunta en la ficha y correr `motor corregir`, para que se sume el dominio.
- Bloom: «Claude 0/11» (falta la codificación ciega; opcional).
- Cuota diaria de Gemini agotada el 7-11.

## Leer primero (máx. 5 rutas, con rango de líneas o encabezado)
- `C:/Proyecto Metodologia de estudio/datos/material/macroeconomia-ii/2026-11-07-anatomia-comente-droller.md` (§2 y §3)
- `C:/Proyecto Metodologia de estudio/datos/material/macroeconomia-ii/2026-11-06-prediccion-final-pep-1.md` (§4.2 sesiones y §7)
- Ficha del banco: `banco.py ver 2026-2-control-1-droller --pregunta 3` (y 4, 5)
- `C:/Users/javie/OneDrive/BancoEvaluaciones/Macroeconomía II/Postmortem/Control 1 2026-2.md`
