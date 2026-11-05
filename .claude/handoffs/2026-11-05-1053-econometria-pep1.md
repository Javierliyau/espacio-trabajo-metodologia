---
tema: econometria-pep1
fecha: 2026-11-05 10:53
resumen: Guía filtrada (5B y SM1-SM12) corregida; faltan los 4 casos de amenazas y el simulacro final de 80 min (hoy en la noche)
---
## Objetivo
PEP 1 de Econometría II (Pfeng), **vie 6-11** (hora asumida 13:45), escrita, un bloque (~80 min), con calculadora, hasta DiD (panel no).

## Hecho en esta sesión
- 5A (SW 13.5, amenazas) explicado: 5 amenazas de SW 13.2, método de 3 preguntas, ITT = β·(pT − pC).
- Simulacro final + pauta: `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-11-04-simulacro-final-pep1(-pauta).(tex|pdf)`. **Sin rendir.**
- Guía filtrada, V/F 5B 1-7: bien, salvo la **justificación del 2** (invirtió las unidades: MPL = pp, logit = log-odds).
- SM1-SM12: 11/12. **Falla SM8**: WOE sin ×100 (marcó 0,693 en vez de 69,3).
- Explicadas desde cero: siglas VP/FP/FN/VN, las 4 métricas (sensibilidad y especificidad por fila, precisión por columna) y el efecto de bajar el corte (sensibilidad ↑, especificidad ↓).
- Todo anotado en la bitácora (4 y 5-11).

## Decisiones tomadas (no re-litigar)
- Convenciones: WOE = ln(%B/%M)·100, buenos arriba; IV sin ×100; en la regresión woeizada el WOE entra sin ×100; y = 1 malo; β woeizados < 0; dummies k − 1; DiD = β3 = ATT.
- Modo pedagógico: concepto → números → respuesta de prueba → trampas.
- Plan acordado para hoy (jue 5-11): **el simulacro final de 80 min reemplaza al simulacro corto del paso 9**.

## Diagnóstico dado al estudiante
Mecánica sólida (logit a mano, DiD, Siddiqi, signos según y = 1). Riesgos: convenciones (×100), precisión de las justificaciones V/F, matriz recién aprendida, ritmo sin medir. Hábito para la prueba: marcar en el enunciado qué es y = 1 y si piden ×100 o pp.

## Próximo paso exacto
Los 4 casos de amenazas en frío (paso 2). El estudiante creyó que ya estaban hechos con el 5A; ya se le aclaró que son otros. Experimento del internet en el dormitorio; responder **amenaza + si sesga y hacia dónde**:
1. Los tratados saben que los observan y estudian más → Hawthorne (efecto experimental), sobreestima.
2. El encargado da internet a las piezas de sus amigos → falla de aleatorización, sesgo de dirección incierta.
3. Los del control, frustrados, se van del estudio → atrición diferencial, sesga.
4. Solo 20 piezas → muestra pequeña (validez interna): imprecisión y grupos desbalanceados.

Corregir, marcar `[x]` el paso 2 en la semana y anotar en la bitácora.

## Pendientes
- **Hoy en la noche, después de Micro (16:40):** simulacro final de 80 min en una sola sentada + corrección con la tabla de registro de la pauta (pasos 7-8). Después, el paso 10 solo con lo fallado + el V/F 5B-2 en frío + releer la hoja de memoria.
- **Vie, en la mañana:** paso 11 (un ejercicio de cada tipo + «Las 15 frases»). Nada nuevo.
- Paso 1 (4B incinerador + f) del 4A): opcional, solo si sobra tiempo.
- Marcar `[x]` en `datos/agenda/semanas/2026-11-02.md` los pasos hechos (la línea SM6-SM12 del jue queda hecha cuando se haga el 5B-2).

## Leer primero
- `C:/Proyecto Metodologia de estudio/datos/agenda/semanas/2026-11-02.md` — líneas 37-70 (pasos 1-11)
- `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-11-04-simulacro-final-pep1-pauta.tex` — «Registro de la corrección» (al final)
- `C:/Proyecto Metodologia de estudio/datos/material/econometria-ii/2026-11-03-guia-filtrada-10-ejercicios-pep1.tex` — líneas 340-370 (pautas 5A, 5B y bloque 6)
