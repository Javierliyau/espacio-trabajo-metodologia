## 3. Las 10 sesiones · versión 3: PEP de dos bloques (≈ 6 h)

Cada sesión es **recuperación en frío**: primero respondes sin mirar y después corriges. Cada tema aparece **una vez por sesión** (intercalado); si fallas, lo rehaces ahí mismo hasta que te salga (criterio). Lo que está en **negrita con «+»** se agregó porque la prueba es de dos bloques; lo que dice **(opcional)**, solo si sobra tiempo.

| Sesión | Cuándo | Min | Temas | Con qué material |
|---|---|---:|---|---|
| **A** | **vie 6, 11:00** (si hay clases por el paro, pasa a las 13:45) | 60 | T6, T4 nuevos **+ T11** | Hoja de ampliación **A2** (Youden, utilidad, ROC, KS) y **A1** (`glm`, RV, McFadden): pretest → pauta → criterio · **+ ATT y tendencias paralelas en 2 frases** · últimos 5 min: marcar las fallas del simulacro con su pauta (**lista de fallas**). (Opcional: 4 V/F del núcleo) |
| **B** | **vie 6, 16:00** | 45 | T7, T14, T1 **+ T15 nuevo** | 3A con otros números (WOE **×100**) · 6 V/F del núcleo · C2 a) (P̂ de dos perfiles, odds) · **+ A6 (probit a mano): pretest → pauta → criterio**. (Opcional, +45 min: A7 primeras diferencias · una amenaza · A2 d-e · MPL) |
| **C** | **vie 6, 22:30** | 14 | T2, T3 **+ T11** | C1 c) (EP en X = 4) · los 4 problemas del MPL y β/4 · **+ Card-Krueger en 3 líneas** |
| **D** | sáb 7, 13:00 | 35 | T8, T12, T7, T11 **+ T4** | A4 a-b (PDO) · 2 amenazas **con la dirección del sesgo** · WOE e IV de C4 · ATT y tendencias paralelas en voz alta · **+ A1 b-d con la pauta tapada**. (Opcional: 2 V/F de scoring) |
| **E** | dom 8, 13:00 | 38 | T2, T8, T3, T7, T5 **+ T12** | A3 (cuadrático) · C5 (scorecard) · MPL ≈ β/4 · un WOE con otros números · C3 (matriz y mover el corte) · **+ una amenaza (STAR o ECA) con su sesgo** |
| **F** | lun 9, 12:00 (después de Macro) | 36 | T7, T11, T4, T6, T2 | WOE/IV en frío · Card-Krueger · A1 tapada · A2 a-c tapada · EP de una dummy. (Opcional: A7 tapada) |
| **G** | mar 10, 13:00 | 53 | T11, T14, T9, T13, T1, T2, T12, T8 **+ T15** | **Mini-simulacro mezclado de 9 ítems**: DiD conceptual · 4 V/F · 2 V/F de scoring · preguntas M2 (Econometría I) · logit P̂/odds · un EP · una amenaza · A4 c) · **+ A6 tapada**. (Opcional: A7 en 3 líneas) |
| **H** | mié 11, 12:45 | 37 | T6, T10, T8, T4, T3 | A2 d-e (Gini, KS) · DiD 2×2 desde medias (C6) · un PDO con otros números · A1 d) · MPL · lista de fallas |
| **I** | mié 11, 22:30 | 15 | T1, T5, T9 | 100(e^β − 1) de un logit · las 4 métricas de una matriz · 3 V/F de scoring. Después, a dormir |
| **J** | **jue 12, 06:45** | 30 | T14, T7, T2, T12, T11 | Calentamiento: «Las 15 frases» · un WOE · un EP · una amenaza con su sesgo · ATT en una frase. Nada nuevo |

### Cómo se optimizó (scripts `opt.py` a `opt4.py` en `trabajo/espaciado/`)

- **Objetivo:** maximizar E[nota] = nota(π · Σ wᵢ·Rᵢ(jue)·qᵢ / Σ wᵢ). Los pesos wᵢ son los de la columna «Dos bloques» de la predicción (§2). Rᵢ es la recuperabilidad FSRS-6 al momento de la PEP, qᵢ la probabilidad de ejecutarlo bien si lo recuerdas (Beta-binomial con la bitácora) y π la presión (0,85-0,97). Escala 1-7 con exigencia del 60 %.
- **Dinámica:** cada repetición tiene éxito con probabilidad R·q. Con éxito, S crece según FSRS-6 (incremento × 0,4; × 1,2 si viene sueño); con fallo, S baja al 35 %; q sube un 25 % de lo que le falta para 0,95.
- **Restricciones:** minutos por ejercicio (más 18 la primera vez de un tema nuevo), el cupo de cada franja, una vez por tema y sesión, los temas nuevos antes del lunes y el jueves solo lo ya repasado.
- **Búsqueda:** voraz + recocido simulado con 4 reinicios. Después, aumento voraz desde la versión 2: dio mejor resultado que reoptimizar desde cero, porque el paisaje es plano.
- **Validación:** Monte Carlo con 3.000 escenarios (S log-normal, q Beta, ganancia, sueño, presión y el éxito o fallo de cada repetición).

**Resultados con la PEP de dos bloques (Monte Carlo):**

| Plan | Minutos | Nota media | Rango 80 % | P(≥ 5,0) | P(≥ 5,5) |
|---|---:|---:|---|---:|---:|
| Versión 2 tal cual | 307 | 4,94 | 4,6-5,3 | 42 % | 0 % |
| Reoptimizado desde cero, mismo tiempo | 307 | 4,96 | 4,6-5,3 | 44 % | 1 % |
| **Versión 3 (esta tabla, sin opcionales)** | **360** | **5,12** | **4,8-5,4** | **65 %** | **5 %** |
| Versión 3 con todos los opcionales | 418 | 5,25 | 4,9-5,6 | 81 % | 19 % |

**Lectura:**
1. **La versión 2 ya estaba cerca del óptimo** también para dos bloques: reoptimizar con el mismo tiempo gana solo 0,02. Por eso se conservó su estructura y solo se agregaron ítems.
2. **Con dos bloques la nota esperada baja si no se agrega nada (5,25 → 4,94).** La prueba cubre más temas, y pesan más los débiles: salida de `glm`, ROC/KS, amenazas, probit y PDO.
3. **Ahora cada minuto extra vale más:** +53 min dan +0,18 puntos, y +111 min dan +0,31. Antes, con un bloque, el tiempo extra casi no sumaba.
4. Lo que más rinde de lo agregado: **probit (A6) nuevo**, **ATT y tendencias paralelas** (pesan 75 % y aún están débiles) y una vuelta más a `glm` y a las amenazas.
