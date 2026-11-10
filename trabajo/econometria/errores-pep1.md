# Lista de errores · PEP 1 Econometría II

Formato: ítem · qué escribí · **frase correcta** · marcas. Se pregunta tapado al inicio de cada sesión (`plan-paro.md` §3); con 2 aciertos seguidos sale de la lista. Llenada el 10-11 con lo que consta en la bitácora.

| # | Ítem | Qué escribí | Frase correcta | Marcas |
|---|---|---|---|---|
| 1 | WOE (3A y SM8) | Sin ×100: 0,693 | WOE = ln(% buenos / % malos) × 100 = 69,3 | |
| 2 | IV, escala de Siddiqi | IV 0,163 = «alto» | < 0,02 no predictivo · 0,02-0,1 débil · **0,1-0,3 medio** · > 0,3 fuerte. 0,163 es medio | |
| 3 | Tramos del WOE | < 10 por ≥ 10, < 5 por ≥ 5 | Copiar el signo del tramo tal como viene en la tabla antes de calcular | |
| 4 | IV después de fusionar | Faltó el IV total (0,154) y el porqué | Al fusionar tramos se pierde información, así que el IV baja o queda igual (0,163 → 0,154); nunca sube | |
| 5 | Logit, interpretación (P1 a) | «%» | Un cambio de probabilidad se dice en **puntos porcentuales** | |
| 6 | Efecto parcial (P1 b) | 0,041 en vez de 0,0441; el porqué, al revés | EP = β · p(1 − p): depende del perfil, y es mayor mientras más cerca esté p de 0,5. Rehacer la cuenta con 4 decimales | |
| 7 | Sensibilidad | «De los predichos» | Sensibilidad = VP / (VP + FN): de los positivos **reales**. «De los predichos positivos» es la precisión | |
| 8 | Mover el corte (d4) | Faltó el costo | Si un FN cuesta más que un FP, se **baja** el corte: sube la sensibilidad a costa de más FP | |
| 9 | Amenazas (4 casos) | Amenaza bien, sin dirección del sesgo | Cada amenaza cierra con «sobrestima» o «subestima» el efecto y por qué | |
| 10 | Atrición | Justificada por el tamaño de la muestra | Es problema cuando **no es aleatoria** (salen distintos de tratados y de controles), no por dejar menos datos | |
| 11 | Muestra pequeña | La llamé sesgo | Es **imprecisión** (más varianza, intervalos anchos), no sesgo | |
| 12 | V/F MPL vs logit (5B-2) | Faltó cerrar | Los coeficientes no se comparan (pp contra log-odds); se comparan los **efectos marginales** (regla rápida: β_logit/4 ≈ β_MPL) | |
