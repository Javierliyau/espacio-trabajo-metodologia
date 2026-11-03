# Desempeño del motor de predicción

Actualizado 2026-10-29 10:12 · campeón **v1.0** · Platt: no (hace falta ≥ 50 pronósticos prospectivos y pasar la compuerta)

Toda cifra va con su n y su IC 90 %. Brier: menor es mejor (0,25 = decir 50 % siempre). Reglas: `datos/motor-predicciones/fase5-diseno.md` (proyecto de metodología).

## Macroeconomía II — predicciones prospectivas resueltas (n = 1)

| Prueba | Fecha | Motor | Frecuente | Última | Uniforme | Programa | Cuad motor | Media acumulada [IC 90 %] |
|---|---|---|---|---|---|---|---|---|
| Control 1 2026-2 | 2026-10-26 | 0.356 | 0.250 | 0.250 | 0.440 | 0.436 | 0.740 | 0.356 — `██████████████` |

**Veredicto: sin evidencia todavía** (n = 1 < 5 resoluciones prospectivas).

## Microeconomía II — predicciones prospectivas resueltas (n = 1)

| Prueba | Fecha | Motor | Frecuente | Última | Uniforme | Programa | Cuad motor | Media acumulada [IC 90 %] |
|---|---|---|---|---|---|---|---|---|
| Control 1 2026-2 | 2026-10-22 | 0.477 | 0.196 | 0.396 | 0.648 | 0.647 | 0.489 | 0.477 — `███████████████████` |

**Veredicto: sin evidencia todavía** (n = 1 < 5 resoluciones prospectivas).

## Todos los ramos

**Veredicto: sin evidencia todavía** (n = 2 < 5 resoluciones prospectivas).

## Calibración de P(entra) (pronósticos prospectivos)

| Intervalo | n | Pronóstico medio | Observado | Consistencia 5-95 % |
|---|---|---|---|---|
| 0.6-0.8 | 4 | 68 % | 25 % | 25-100 % |
| 0.8-1.0 | 2 | 95 % | 50 % | 50-100 % |

## Walk-forward del campeón (historia sin señales + prospectivas repetidas)

Último ciclo 2026-10-29 10:12 (ingreso de una prueba con prediccion): Brier medio 0.252 en 13 pruebas, cuad medio 0.238 en 10; 2 prospectivas. Es diagnóstico: la historia ya se usó para diseñar el motor.

## Versiones

| Fecha | De | A | Motivo |
|---|---|---|---|
| 2026-10-04 | — | 1.0 | diseno a priori (Fase 2) |

| Retador | Estado | Origen | Último resultado contra el campeón |
|---|---|---|---|
| v1.1 | archivado | estructural (Fase 4: alcance por posicion) | ΔBrier -0.0022 IC90 [-0.0065, +0.0000], cuad 0.2380 vs 0.2380, n = 13 (2026-10-29 10:12, contra v1.0): no pasa — el IC 90 % del Brier no queda entero bajo 0 |
| v1.2 | archivado | deriva en Microeconomía II (formato: 2 preguntas, fuera del rango del profesor (7-9)): vida media a la mitad | ΔBrier +0.0006 IC90 [+0.0000, +0.0018], cuad 0.1781 vs 0.1795, n = 12 (2026-10-22 16:34, contra v1.0): no pasa — el IC 90 % del Brier no queda entero bajo 0 |
| v1.3 | archivado | deriva en Macroeconomía II (profesor nuevo en el ramo (Droller)): vida media a la mitad | ΔBrier +0.0000 IC90 [+0.0000, +0.0000], cuad 0.2380 vs 0.2380, n = 13 (2026-10-29 10:12, contra v1.0): no pasa — el IC 90 % del Brier no queda entero bajo 0 |
