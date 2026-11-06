## 3. Las 10 sesiones, optimizadas (≈ 5 h 10 min, el mismo tiempo que la versión 1)

Cada sesión es **recuperación en frío**: primero respondes sin mirar y después corriges. Cada tema aparece **una sola vez por sesión** (intercalado), y si fallas, lo rehaces en esa misma sesión hasta que te salga (criterio).

| Sesión | Cuándo | Min | Temas | Con qué material |
|---|---|---:|---|---|
| **A** | **vie 6, 11:00** | 55 | **T6, T4 nuevos** | Hoja de ampliación **A2** (Youden, utilidad, ROC, KS) y **A1** (`glm`, RV, McFadden): pretest → pauta → criterio. Últimos 5 min: marcar en la pauta del simulacro qué falló (**lista de fallas**), sin rehacerlo |
| **B** | **vie 6, 16:00** | 20 | T7, T14, T1 | 3A con otros números (WOE **×100**) · 6 V/F del núcleo · C2 a) (P̂ de dos perfiles, odds) |
| **C** | **vie 6, 22:30** | 10 | T2, T3 | C1 c) (EP en X = 4) · los 4 problemas del MPL y β/4, de memoria |
| **D** | sáb 7, 13:00 | 25 | T8, T12, T7, T11 | A4 a-b (PDO) · 2 amenazas **con la dirección del sesgo** · WOE e IV de C4 · ATT y tendencias paralelas en voz alta |
| **E** | dom 8, 13:00 | 30 | T2, T8, T3, T7, T5 | A3 (cuadrático) · C5 (scorecard) · MPL ≈ β/4 · un WOE con otros números · C3 (matriz y mover el corte) |
| **F** | lun 9, 12:00 (después de Macro) | 35 | T7, T11, T4, T6, T2 | WOE/IV en frío · Card-Krueger en 3 líneas · A1 con la pauta tapada · A2 a-c tapada · EP de una dummy |
| **G** | mar 10, 13:00 | 45 | T11, T14, T9, T13, T1, T2, T12, T8 | **Mini-simulacro mezclado de 8 ítems**: DiD conceptual · 4 V/F · 2 V/F de scoring · preguntas de la lectura M2 (Econometría I) · un logit P̂/odds · un EP · una amenaza · A4 c) |
| **H** | mié 11, 12:45 | 35 | T6, T10, T8, T4, T3 | A2 d-e (Gini, KS) · DiD 2×2 desde medias (C6) · un PDO con otros números · A1 d) (RV de `edad`) · MPL · y la lista de fallas |
| **I** | mié 11, 22:30 | 15 | T1, T5, T9 | 100(e^β − 1) de un logit · las 4 métricas de una matriz · 3 V/F de scoring. Después, a dormir |
| **J** | **jue 12, 06:45** | 30 | T14, T7, T2, T12, T11 | Calentamiento: «Las 15 frases» · un WOE · un EP · una amenaza con su sesgo · ATT en una frase. Nada nuevo |

### Cómo se optimizó (script `trabajo/espaciado/opt.py` y `opt2.py`)

- **Objetivo:** maximizar la nota esperada E[nota] = nota(π · Σ wᵢ·Rᵢ(jue)·qᵢ / Σ wᵢ). Aquí wᵢ es la probabilidad de que el tema salga (§2), Rᵢ es la recuperabilidad FSRS-6 el jueves a las 08:15, qᵢ la probabilidad de ejecutarlo bien si lo recuerdas y π el factor de presión (0,85-0,97). Escala 1-7 con exigencia del 60 %.
- **Dinámica:** cada repetición tiene éxito con probabilidad R·q. Con éxito, S crece según FSRS-6 (incremento × 0,4, × 1,2 si viene sueño después); con fallo, S baja al 35 %. Además, q sube un 25 % de lo que le falta para 0,95 (corrección con pauta).
- **Estimación de qᵢ:** Beta-binomial con la evidencia de la bitácora. Ejemplos: T1 ≈ 0,80 (P1 27/35), T7 ≈ 0,65 (mismo error dos veces), T4 y T6 ≈ 0,30-0,35 (nunca practicados).
- **Restricciones:** un mínimo de minutos por repetición según el tema, más 18 min la primera vez de un tema nuevo; el cupo de cada franja de la agenda; una vez por tema y sesión; los temas nuevos aprendidos antes del lunes; el jueves solo lo ya repasado dos veces.
- **Algoritmo:** voraz (mayor ganancia por minuto) y después recocido simulado (30.000 pasos, 4 reinicios que coinciden en ±0,02).
- **Validación:** Monte Carlo con 3.000 escenarios que sortean S (log-normal, σ = 0,4), q (Beta), la ganancia (0,25-0,6), el sueño (1,0-1,4), la presión y el éxito o fallo de cada repetición.

**Resultados (Monte Carlo):**

| Plan | Minutos | Nota media | Rango 80 % | P(nota ≥ 5,0) | P(≥ 5,5) |
|---|---:|---:|---|---:|---:|
| Versión 1 (la de esta mañana) | 308 | 4,97 | 4,6-5,3 | 46 % | 2 % |
| **Optimizada (esta tabla)** | **307** | **5,25** | **4,9-5,6** | **82 %** | **18 %** |
| Optimizada con menos tiempo | 240 | 5,06 | 4,7-5,4 | 57 % | 4 % |
| Optimizada con mucho menos | 210 | 4,99 | 4,7-5,3 | 48 % | 2 % |

Con **210 min se iguala la versión 1 (−32 % de tiempo)**, y con el mismo tiempo se ganan **+0,28 puntos**.

**Por qué la versión optimizada es mejor:**
1. La versión 1 cargaba 160 min hoy, cuando todo está fresco y repasar aporta poco. La optimizada mueve tiempo a dom-mié, cuando R ya bajó y cada repaso multiplica más la estabilidad.
2. Usa más temas por sesión y menos minutos por tema: cada tema se recupera **una vez** y se pasa al siguiente.
3. Pone las repeticiones donde peso × (1 − q) es mayor: **T7 (WOE) 5 veces y T2 (efectos parciales) 5 veces**. T10 (DiD numérico) y T5 (matriz), que ya están firmes, van solo 1-2 veces.
4. Los temas nuevos (T4, T6) se aprenden hoy temprano y se repasan 3 veces, a 3 y 5 días.

**Qué más sube la nota:** el techo ya no es la memoria sino **q**, la ejecución. Cada error de la lista de fallas que quede limpio sube el q de ese tema.
