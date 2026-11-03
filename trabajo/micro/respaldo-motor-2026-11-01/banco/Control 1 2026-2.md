# Postmortem · Control 1 2026-2 · Microeconomía II

- **Registro evaluado:** `20261010-220946-control-1` (emitido 2026-10-10T22:09:46, modelo v1.0). Fecha real de la prueba: 2026-10-22.
- **Alcance predicho:** U1, U2, U4. Puntos reales fuera de él: 0 %.
- Se evalúa la predicción tal como quedó congelada; las líneas base usan las mismas pruebas que ella.

| Modelo | Brier (P entra) | Cuad (reparto) | Top-1 |
|---|---|---|---|
| **motor** | 0.477 | 0.489 | 100 % |
| frecuente | 0.196 | 0.566 | 0 % |
| ultima_prueba | 0.396 | 0.885 | 0 % |
| uniforme | 0.648 | 0.667 | 33 % |
| programa | 0.647 | 0.667 | 33 % |

_Una sola prueba no dice si el motor sirve: eso lo dice el tablero con n ≥ 5._

## Por unidad

| Unidad | P(entra) | Reparto predicho | Reparto real |
|---|---|---|---|
| U1 Monopolio | 97 % | 44 % | 100 % |
| U2 Prácticas monopólicas | 75 % | 20 % | 0 % |
| U4 Competencia imperfecta | 93 % | 36 % | 0 % |

## Señales (acierto direccional: la señal movió la unidad hacia su reparto real)

- clase: 2 de 3 unidades

## Sorpresas

- Unidades con puntos y P(entra) < 30 % o fuera del alcance: ninguna
- Temas sin unidad del programa: ninguno

## Causas probables (reglas fijas, sin LLM)

- Ninguna regla se activó.

## Deriva

- ⚠ formato: 2 preguntas, fuera del rango del profesor (7-9)
- El próximo `motor ciclo` prueba un retador con la vida media a la mitad para este ramo.

## Dominio

- sin cambios (la ficha no trae el puntaje obtenido por pregunta)
