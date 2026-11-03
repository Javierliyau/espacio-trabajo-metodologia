# PAUTA · M2 con la salida PAES · 24-10 (no abrir: es para el tutor)

Fuente: `trabajo/econometria-ii-estudio/salidas-paes-estudio.txt` (base 168.714 / 60.234; MCO con n = 168.711).

## Hito 1 · ficha
1. $F = \dfrac{(R^2_{nr} - R^2_r)/q}{(1 - R^2_{nr})/(n - k - 1)} \sim F_{q,\,n-k-1}$; para restricciones **conjuntas** (q ≥ 2), p. ej. todas las dummies de una categórica.
2. Infla $\text{Var}(\hat\beta_j)$ y el ee (t bajos, β inestables, signos raros); **no sesga** ni viola Gauss-Markov (salvo colinealidad perfecta). $\text{VIF}_j = 1/(1 - R^2_j)$. Libro: > 10; Pfeng (scoring): > 2.
3. Viola homocedasticidad, $\text{Var}(u \mid X) = \sigma^2$. $\hat\beta$ sigue **insesgado y consistente**, pero deja de ser MELI y los ee usuales están mal → t, F y p no sirven.
4. $H_0$: homocedasticidad. Auxiliar: $\hat u^2$ sobre las X. $LM = nR^2_{\hat u^2} \sim \chi^2_k$ (o F).
5. Cambian los ee (y por eso t, p, IC); **no** cambian los $\hat\beta$ ni el $R^2$.

## Hito 2
**a)** MCO: minimiza $\sum \hat u_i^2$. «En promedio, un punto más de promedio de notas (p. ej., de 5,5 a 6,5) se asocia con 137,5 puntos más en M1, manteniendo constantes el tipo de enseñanza y la dependencia.» «En promedio, los egresados de colegios particulares pagados obtienen 153,3 puntos más en Matemática 1 que los de colegios públicos con el mismo promedio de notas y el mismo tipo de enseñanza (TP o HC).» Asociación, no efecto causal (selección e ingreso del hogar en $u$).

**b)** $H_0: \beta_P = \beta_S = 0$; $H_1$: al menos una ≠ 0. $q = 2$, gl = 168.706.
$F = \dfrac{(0{,}4063 - 0{,}3139)/2}{(1 - 0{,}4063)/168.706} = \dfrac{0{,}0462}{3{,}519\times10^{-6}} \approx 13.128$ (R da 13.118 con los R² sin redondear). $13.128 > 3{,}00$ → se rechaza $H_0$: la dependencia es **conjuntamente** significativa; las dos dummies entran juntas o no entran.

**c)** $R^2_j = 1 - 1/3.869 = 0{,}99974$: el resto de las X explica el 99,97 % de la varianza de PROM (NEM es una transformación del promedio). $\sqrt{3.869} \approx 62{,}2$: el ee de PROM se multiplica ≈ 62 veces por la colinealidad; en la salida pasó de 0,583 a 35,15 (× 60,3), casi lo mismo. Se sobreestima la **varianza y el ee** de los β̂ (no el β, que sigue insesgado). Los β̂ se vuelven inestables: 1.770 puntos por nota y NEM con signo negativo (más NEM, menos puntaje: contradice que mejores notas van con más puntaje); el modelo no puede separar el efecto de dos variables que se mueven juntas. Se deja una sola (PROM) porque las otras no aportan información nueva y el VIF pasa con creces el umbral (2 de Pfeng, 10 del libro). Ojo: con n = 168.711 los t siguen enormes; la multicolinealidad hace daño sobre todo en la interpretación.

**d)** $H_0$: homocedasticidad, $\text{Var}(u \mid X) = \sigma^2$. $5.396{,}5 > 9{,}49$ → se rechaza: hay heterocedasticidad. $R^2_{aux} = 5.396{,}5/168.711 \approx 0{,}032$ (pequeño, pero con este n basta para rechazar).

**d, V/F)** **Falso** en dos partes. (i) Lo primero es verdadero: con heterocedasticidad se usan ee robustos. (ii) Los $\hat\beta$ **no cambian** (153,3 sigue igual), solo los ee; y la heterocedasticidad **no genera sesgo**: el sesgo viene de $E(u \mid X) \neq 0$ (variable omitida), y los robustos no lo corrigen. $t_{rob} = 153{,}3/1{,}034 \approx 148{,}3$ (antes 160,8): baja, pero sigue siendo significativo. El ee de TP **baja** (0,691 → 0,621): los robustos no siempre suben.

**e) E8** = ítem 3 del E7 de abajo (selección muestral: quedaban fuera los ~55.700 que rindieron y no postularon, 168.714 − ~113.000 de la clase 5. La tasa de I = 1 subía del 35,7 % a cerca del 56 %, si los 60.234 estaban dentro: 60.234/108.251. Los β quedaban atenuados).

## Hito 3 · E7 (ítems 1, 2 y 4; el 3 ya es la e)
1. PROM (+): más notas, más preparación y habilidad. TP (−): menos horas de formación general (matemática) y selección. Pagado (+) y Subv (+), respecto del público: ingreso del hogar, preuniversitario, recursos del colegio; Pagado > Subv. Todos asociaciones, no causales.
2. *Ex post*: se conoce **después** de I (o es parte de su resultado): el ponderado se calcula al postular y el N de matriculados es consecuencia de la matrícula. No está disponible cuando se predice y provoca endogeneidad o fuga de información (*leakage*): el modelo «acierta» con datos del futuro.
3. Sesgo de **selección muestral**: quedarse con los que postularon o se matricularon es condicionar en un resultado relacionado con Y. Los que no postularon (puntaje más bajo) desaparecen; la muestra se trunca y los β quedan sesgados (por lo general, atenuados) y la tasa de I = 1 se infla. Por eso la base correcta conserva a los 168.714 que rindieron, y los que no postularon cuentan como I = 0.
4. En el MPL $\text{Var}(u \mid X) = p(X)[1 - p(X)]$: es heterocedástico **por construcción**. Se usan errores robustos (HC1) siempre; MCG factible, si $0 < \hat p < 1$. O se pasa a logit o probit.

## Puntaje sugerido (por hito, sobre 5)
Hito 2: a) 1 · b) 1 · c) 1,2 · d) 0,8 · e) 1. Hito 3: 0,5 por ítem (sobre 2).
