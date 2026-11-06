---
tema: econometria-pep1
fecha: 2026-11-06 07:35
resumen: PEP 1 de Econometría II movida al jue 12-11 08:15-11:10 en DOS bloques; plan de repaso v3 (10 sesiones A-J, 360 min + 58 opcionales, nota esperada 5,12-5,25) y falta ejecutarlo desde la sesión A
---
## Objetivo
Llegar a la PEP 1 de Econometría II (jue 12-11, 08:15-11:10, dos bloques de ~160 min, el mismo día que Micro) sin olvidar lo estudiado, cubriendo los huecos y con la nota más alta posible por minuto invertido.

## Hecho en esta sesión
- Ajusté la agenda al cambio de fecha (correo de J. Riquelme por el paro): `calendario.md` y el protocolo de Econometría II.
- Creé el plan de repaso espaciado (curva del olvido FSRS-6 + reaprendizaje sucesivo) con método, inventario de 14 temas (T1-T14) y fuentes.
- Creé la hoja de ampliación A1-A5 con pauta: `glm`/RV/McFadden, Youden/utilidad/ROC/KS, cuadrático, PDO y V/F.
- Optimicé las sesiones. Modelo: E[nota] = Σ wᵢ·Rᵢ·qᵢ, con q por Beta-binomial; búsqueda voraz + recocido simulado; validación Monte Carlo con 3.000 escenarios. Resultado: con el mismo tiempo, la nota media pasa de 4,97 a 5,25 y P(≥5) de 46 % a 82 %; con 210 min ya iguala la v1.
- La PEP es de dos bloques (dato del estudiante): reoptimicé con los pesos «Dos bloques» y saqué la v3 = v2 + ítems (+T15 probit A6, +T16 primeras diferencias A7). Con dos bloques, la v2 baja a 4,94; la v3 con 360 min da 5,12 y con los opcionales (418 min), 5,25. Actualicé la predicción (nota arriba del §1), la hoja (+A6, A7), el protocolo y la agenda.
- Reescribí las sesiones A-J en la agenda semanal y anoté la bitácora (3 entradas del 6-11).

## Decisiones tomadas (no re-litigar)
- Modelo FSRS-6 con el incremento de S × 0,4: son procedimientos de varios pasos, no tarjetas.
- Metas: R ≥ 0,90 entre sesiones y R ≥ 0,95 el jueves.
- Se usa la v3 (360 min); los «(opcional)» solo si sobra tiempo. Con dos bloques, cada minuto extra rinde más que con uno.
- Cada tema va una vez por sesión (intercalado). Los nuevos (T4, T6) se aprenden en la sesión A. El jueves no entra nada nuevo.
- Las probabilidades de cada tema son la columna «Dos bloques» de la predicción del 31-10 (débil: 0 PEP pasadas en el banco). Primeras diferencias pesa 15 % porque panel no entra.

## Próximo paso exacto
Sesión A, hoy a las 11:00 (60 min; a las 13:45 si hay clases): A2 y luego A1 de la hoja de ampliación (pretest → pauta → criterio), más ATT y tendencias paralelas en 2 frases. En los últimos 5 min, marcar las fallas del simulacro con `2026-11-04-simulacro-final-pep1-pauta-libro.pdf` y armar la lista de fallas.

## Pendientes
- Sesiones B (16:00, 45 min, con A6 probit nuevo) y C (22:30, 14 min) de hoy; después D-J según la agenda.
- Después de la sesión A: recalibrar S y q en el §2 del plan con las fallas del simulacro y volver a correr `trabajo/espaciado/opt4.py (parte de la v2 y agrega ítems)`.
- Confirmar la hora y la sala de la PEP, y confirmar con el profesor que son dos bloques. Actualizar los pesos de la predicción.
- Si aparece una PEP o un control pasado de Pfeng en Econometría II: subirlo con `banco-evaluaciones` y reoptimizar.
- La sesión A choca con la ayudantía de Macro y con Historia si hay clases pese al paro: en ese caso pasa a las 13:45.

## Leer primero (máx. 5 rutas, con rango de líneas o encabezado)
1. `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-11-06-plan-repaso-espaciado-pep1.md` §3 «versión 3» y §4 (por encabezado)
2. `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-11-06-hoja-ampliacion-pep1.md` (enunciados L7-58; pauta desde L60)
3. `C:/Proyecto Metodologia de estudio/datos/agenda/semanas/2026-11-02.md` L67-88 y `2026-11-09.md` (líneas «sesión F-J»)
4. `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-10-31-prediccion-estructura-pep1.md` §1-§2 (pesos y estructura)
5. `C:/Espacio de trabajo Metodologia de estudio/trabajo/espaciado/opt.py`, `opt2.py`, `opt3.py` (pesos de 2 bloques) y `opt4.py` (aumento desde la v2; guarda `v3_360.json`)
