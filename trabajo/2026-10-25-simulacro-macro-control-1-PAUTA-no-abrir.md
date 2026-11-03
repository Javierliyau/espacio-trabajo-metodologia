# PAUTA · Simulacro Control 1 Macro II (dom 25-10) · no abrir antes de terminar

Números verificados en Python (24-10). Corregir por hitos: cada hito vale lo indicado; si el número está bien pero falta la frase, se pierde la mitad.

## P1 (30)

- **a) (2)** ŷ = k̂^α = k̂^0,5.
- **b) (3)** k̂ = K/(AL) ⇒ k̂̇/k̂ = K̇/K − Ȧ/A − L̇/L = (sY − δK)/K − g − n. Multiplicando por k̂: **k̂̇ = s·k̂^α − (n + g + δ)·k̂**. Hito: decir que (n + g + δ) es lo que hay que invertir para que k̂ no caiga (depreciación + más trabajadores + cada trabajador más eficiente).
- **c) (6)** n + g + δ = 0,08; s/0,08 = 3. **k̂* = 3^(1/(1−α)) = 3² = 9 · ŷ* = 3 · ĉ* = (1 − s)ŷ* = 0,76·3 = 2,28.** (2 c/u; fórmula general k̂* = (s/(n+g+δ))^(1/(1−α)) antes de reemplazar.)
- **d) (6)** k̂, ŷ: **0 %** · k, y: **g = 2 %** · K, Y: **n + g = 3 %**. Por qué: y = A·ŷ; ŷ constante y A crece a g. (1 por tasa con su justificación.)
- **e) (6)** ŷ₀ = √4 = **2** · inversión s·ŷ₀ = **0,48** · reposición 0,08·4 = **0,32** · **k̂̇₀ = 0,16** (k̂₁ ≈ 4,16). Tasas: k̂ **4 %**; ŷ ≈ α·4 % = **2 %**; y = g + 2 % = **4 %**; Y = n + 4 % = **5 %**. y crece más que g porque k̂₀ < k̂*: la economía está bajo su estado estacionario y acumula capital efectivo (efecto transición).
- **f) (7)** n + g + δ = 0,10; s/0,10 = 2,4 ⇒ **k̂** = 5,76 · ŷ** = 2,4** (k̂ e ŷ **bajan**: con g mayor, el capital por trabajador efectivo se «diluye» más rápido).
  - En el impacto, el **nivel de y no salta** (A y k̂ son continuos).
  - Tasa en el impacto: k̂̇/k̂ = 0,24·9^(−0,5) − 0,10 = 0,08 − 0,10 = **−2 %** ⇒ ŷ crece α·(−2 %) = −1 % ⇒ **y crece 4 % − 1 % = 3 %** (sube de 2 % a 3 % de golpe).
  - Después, la tasa de y sube gradualmente hasta **4 % = g nuevo** en la nueva SBC.
  - (Error típico del 13-10, P3 de la Ay. 2: decir que k̂* sube o que y crece 4 % desde el primer momento.)

## P2 (10)

- **a) (6)** Ejes: k̂ (horizontal), ŷ e inversión por trabajador efectivo (vertical). s·f(k̂) **no se mueve**; la recta (n + g + δ)k̂ **rota hacia arriba** (pendiente 0,08 → 0,10). Corte nuevo a la izquierda: k̂** = 5,76 < k̂* = 9. Flecha: k̂ baja de 9 a 5,76 (movimiento a lo largo de s·f). 2 por rótulos, 2 por qué se desplaza, 2 por la dinámica.
- **b) (4)** ln y contra t: recta con pendiente 2 % hasta t₀; desde t₀ sin salto de nivel, pendiente 3 % que se curva hasta 4 %. La senda nueva de largo plazo tiene **pendiente mayor (4 %) e intercepto más bajo** (ln ŷ** = ln 2,4 < ln 3). Hito: la senda observada converge a la nueva por arriba de esa recta.

## P3 (10) · **Falso**

Con k̂̇/k̂ = s·k̂^(α−1) − (n + g + δ), al subir s la tasa se vuelve positiva **solo durante la transición**; al llegar a k̂* nuevo (más alto) vuelve a 0, e y vuelve a crecer a **g**, que es exógeno. Efecto **nivel** permanente (ŷ* = (s/(n+g+δ))^(α/(1−α)) sube) y efecto **tasa** transitorio. (4 por la ecuación, 3 por nivel vs. tasa, 3 por decir que en SBC γ_y = g.)

## P4 (10) · **Verdadero** (convergencia condicional dentro de Solow)

Mismos parámetros y A₀ ⇒ mismo k̂* y misma senda y(t) = A₀e^(gt)·ŷ*. La tasa γ_k̂ = s·k̂^(α−1) − (n + g + δ) es **decreciente en k̂** (α < 1, rendimientos decrecientes del capital): la que parte con menos k̂ crece más rápido en la transición. Matiz para el 10: si difiriera A₀ o algún parámetro, no habría convergencia al mismo nivel (solo condicional). (4 ecuación, 3 rendimientos decrecientes, 3 matiz.)

## Después de corregir

- Anotar los 3 hitos peores y rehacerlos sin mirar a las 10:05.
- Si P1 f) o P2 b) salen bajo 5/7 y 2/4: repetir la P3 de la Ay. 2 con g de 2 % a 3 %.
- Meta: ≥ 45/60.
