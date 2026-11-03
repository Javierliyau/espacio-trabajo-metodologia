---
tema: econometria-pep1
fecha: 2026-11-03 08:37
resumen: PEP 1 Econometría II el jue 5-11 (EF307, un bloque); hoy día completo de estudio; falta diseñar el bloque teórico de comentes y corregir el diagnóstico
---
## Objetivo
PEP 1 de Econometría II (Pfeng): «la nota que más se pueda con la menor cantidad de horas». **Jue 5-11, 08:15, sala EF307, un solo bloque (~80 min)**; pasa al vie 6-11 solo si hay movilizaciones el jueves. Entra hasta DiD; panel no.

## Hecho en esta sesión
- Lectura de la PEP con casos reales (Spector, German Credit, Card y Krueger), 13 pp.: `datos/material/econometria-ii/2026-11-02-lectura-pep1-casos-reales.pdf` (+ `.tex`).
- Calendario actualizado (fecha, sala, un bloque, contingencia viernes). Plan del mar 3-11 y mié 4-11 escrito en `datos/agenda/semanas/2026-11-02.md`.
- Diagnóstico en frío de 6 preguntas entregado en el chat (08:30). Datos y respuestas para corregir:
  1. ẑ = −4,0 + 0,8X + 1,2D, X = 3: P̂₀ = 0,168 (ẑ −1,6); P̂₁ = 0,401 (ẑ −0,4); efecto 23,3 pp; corte 0,5: Ŷ = 0 en ambos.
  2. Efecto marginal de X con D = 0: 0,168·0,832·0,8 = 0,112 → 11,2 pp por unidad.
  3. Odds de D: 100(e^1,2 − 1) = 232 %, ×3,32.
  4. 800 B / 200 M; tramo 120 B / 60 M: %B 0,15, %M 0,30, WOE −0,693, IV tramo 0,104; tasa de malos 33,3 % (fila) vs. %M 30 % (columna).
  5. Tratados 50→58, control 47→51: DiD 4; β₀ 47, β₁ 3, β₂ 4, β₃ 4; ee 1,6 → t 2,5 > 1,96, significativo.
  6. VP 40, FN 10, FP 20, VN 130: sens 80 %, esp 86,7 %, prec 66,7 %, exact 85 %; bajar el corte sube sens y baja esp.

## Decisiones tomadas (no re-litigar)
- Un bloque: fuera RV/McFadden, VIF, stepwise, PDO, probit, PSI, primeras diferencias, STAR, incinerador, Card y Krueger con números.
- Estructura esperada (C): P1 logit + clasificación ~35 pts/28 min; P2 WOE-IV ~30/22; P3 DiD ~25/20; P4 V/F o comentes ~10/7. Orden sugerido: DiD → WOE → logit.
- Cada bloque de hoy practica solo lo que falle en el diagnóstico, sin mirar y con calculadora. Un solo simulacro de 80 min el mié 4-11 11:10.

## Próximo paso exacto
1. Corregir el diagnóstico cuando el estudiante lo mande (foto o texto) y armar el bloque de 09:00 solo con lo fallado.
2. **Pedido pendiente:** «con lo visto en clases también podríamos preparar el bloque teórico y de comentes para que lo diseñes». Diseñar un banco de comentes / V-F justificados (estilo Pfeng, ejemplos casi literales de Wooldridge y Stock-Watson) desde las clases 1-6, con pauta corta (respuesta + frase). Temas: MPL vs. logit, odds vs. probabilidad, EPeP vs. EPP, sens/esp/corte, exactitud vs. base, AUC/Gini/KS, WOE/IV/Siddiqi, %M vs. tasa, monotonía, exclusiones, ventanas, train/test, DiD, ingenuas, tendencias paralelas, ATT vs. ATE, errores agrupados, amenazas internas (5) y externas (3), SLEP. Guardar en `datos/material/econometria-ii/` y usarlo en el simulacro del mié.

## Pendientes
- Simulacro de 80 min para el mié 4-11 (incluye la sección de comentes).
- Hoja de memoria (la escribe el estudiante a mano hoy 15:00).
- Revista 9 de Historia (vie 6-11): estructura el mié en la noche.
- Etapa 2 Econometría: confirmar si se entregó y la fecha de presentación. Macro II: anotar el Control 2 del lun 2-11.
- Al cerrar: `AG anotar` y marcar `[x]` en la semana.

## Leer primero (máx. 5 rutas, con rango de líneas o encabezado)
- `C:/Proyecto Metodologia de estudio/datos/agenda/semanas/2026-11-02.md` § «2026-11-03 · mar» y «2026-11-04 · mié»
- `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-10-31-prediccion-estructura-pep1.md` §3-§5 (líneas 29-92)
- `C:/Proyecto Metodologia de estudio/datos/clases/2026-10-29-econometria-ii-clase-6.md` (amenazas ~60-70; SLEP ~210)
- `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-11-02-lectura-pep1-casos-reales.tex` (base de frases y casos)
- Skill `banco-evaluaciones`: pruebas pasadas de Pfeng / Control 1 Econometría I (molde de V/F, pareo, alternativas)
