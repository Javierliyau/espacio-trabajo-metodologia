---
tema: econometria-pep1
fecha: 2026-11-06 07:35
resumen: PEP 1 de Econometría II movida al jue 12-11 08:15; hay un plan de repaso espaciado v2 optimizado (10 sesiones A-J, 307 min, nota esperada 5,25) y falta ejecutarlo desde la sesión A
---
## Objetivo
Llegar a la PEP 1 de Econometría II (jue 12-11, 08:15 asumida, un bloque de ~80 min, el mismo día que Micro) sin olvidar lo estudiado, cubriendo los huecos y con la nota más alta posible por minuto invertido.

## Hecho en esta sesión
- Ajusté la agenda al cambio de fecha (correo de J. Riquelme por el paro): `calendario.md` y el protocolo de Econometría II.
- Creé el plan de repaso espaciado (curva del olvido FSRS-6 + reaprendizaje sucesivo) con método, inventario de 14 temas (T1-T14) y fuentes.
- Creé la hoja de ampliación A1-A5 con pauta: `glm`/RV/McFadden, Youden/utilidad/ROC/KS, cuadrático, PDO y V/F.
- Optimicé las sesiones. Modelo: E[nota] = Σ wᵢ·Rᵢ·qᵢ, con q por Beta-binomial; búsqueda voraz + recocido simulado; validación Monte Carlo con 3.000 escenarios. Resultado: con el mismo tiempo, la nota media pasa de 4,97 a 5,25 y P(≥5) de 46 % a 82 %; con 210 min ya iguala la v1.
- Reescribí las sesiones A-J en la agenda semanal y anoté la bitácora (3 entradas del 6-11).

## Decisiones tomadas (no re-litigar)
- Modelo FSRS-6 con el incremento de S × 0,4: son procedimientos de varios pasos, no tarjetas.
- Metas: R ≥ 0,90 entre sesiones y R ≥ 0,95 el jueves.
- Se usa la v2 optimizada (307 min). La de 240 min queda como alternativa si falta tiempo.
- Cada tema va una vez por sesión (intercalado). Los nuevos (T4, T6) se aprenden en la sesión A. El jueves no entra nada nuevo.
- Las probabilidades de cada tema vienen de la predicción del 31-10. Es una predicción débil: 0 PEP pasadas en el banco y suponía 160 min, no 80.

## Próximo paso exacto
Sesión A, hoy a las 11:00 (55 min): A2 y luego A1 de la hoja de ampliación, con pretest → pauta → criterio. En los últimos 5 min, marcar las fallas del simulacro con `2026-11-04-simulacro-final-pep1-pauta-libro.pdf` y armar la lista de fallas.

## Pendientes
- Sesiones B (16:00, 20 min) y C (22:30, 10 min) de hoy; después D-J según la agenda.
- Después de la sesión A: recalibrar S y q en el §2 del plan con las fallas del simulacro y volver a correr `trabajo/espaciado/opt2.py`.
- Confirmar la hora y la sala de la PEP, y preguntar cuántas preguntas trae el bloque de 80 min. Actualizar los pesos de la predicción.
- Si aparece una PEP o un control pasado de Pfeng en Econometría II: subirlo con `banco-evaluaciones` y reoptimizar.
- La sesión A (11:00) choca con la ayudantía de Macro (09:50-11:10). Puede partir a las 11:10 o pasar a la tarde; si se mueve, reoptimizar.

## Leer primero (máx. 5 rutas, con rango de líneas o encabezado)
1. `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-11-06-plan-repaso-espaciado-pep1.md` §3 (L59-103) y §4 (L104-112)
2. `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-11-06-hoja-ampliacion-pep1.md` (enunciados L7-58; pauta desde L60)
3. `C:/Proyecto Metodologia de estudio/datos/agenda/semanas/2026-11-02.md` L67-88 y `2026-11-09.md` (líneas «sesión F-J»)
4. `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-10-31-prediccion-estructura-pep1.md` §1-§2 (pesos y estructura)
5. `C:/Espacio de trabajo Metodologia de estudio/trabajo/espaciado/opt.py` + `opt2.py` (modelo y optimizador; `opt2.py` agrega las restricciones)
