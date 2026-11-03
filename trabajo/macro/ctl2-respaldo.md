# Predicción del Control 2 de Macroeconomía II (lun 2-11-2026, 09:50, al comienzo de la clase)

**Temario (correo de Droller, 27-10):** Jones y Vollrath (JV, 3.ª ed.), **cap. 5.1 completo, 5.2.1 y 5.2.2**. Es todo el modelo de Romer:

| Sección JV | Contenido | Dónde lo tienes |
|---|---|---|
| 5.1 (5.1.1-5.1.3) | Mecánica de las ideas: $\dot A = \theta L_A^\lambda A^\phi$, $g = \frac{\lambda}{1-\phi}n$, efecto tasa vs. efecto nivel, alza de $s_R$ | [clase 6](../../clases/2026-10-16-macroeconomia-ii-clase-6.md), [clase 7](../../clases/2026-10-19-macroeconomia-ii-clase-7.md), [láminas Romer](2026-10-19-clase-6-7-ideas-romer.md) §3-6 |
| 5.2.1 | Sector de bienes finales: $Y = L_Y^{1-\alpha}\int_0^A x_j^\alpha dj$, CPO (5.12) y (5.13) | [clase 8](../../clases/2026-10-21-macroeconomia-ii-clase-8.md); [láminas «El modelo de Romer»](2026-10-21-ideas-ii-romer.md) lám. 3-4 |
| 5.2.2 | Sector de bienes intermedios: monopolista, $p = r/\alpha$, $\pi = \alpha(1-\alpha)Y/A$, $x = K/A$, vuelta a $Y = K^\alpha(AL_Y)^{1-\alpha}$ | [láminas «El modelo de Romer»](2026-10-21-ideas-ii-romer.md) lám. 5-9 (la clase 8 sólo lo anticipó) |

**No entra:** 5.2.3 (sector de investigación, $P_A = \pi/r$), 5.2.4 (resolver el modelo, $r = \alpha^2 Y/K$), Schumpeter (5.3-5.4), I+D óptima (5.5). El cap. 4 (economía de las ideas) no está en el temario, pero 5.1 lo da por sabido.

**Motor (`banco-evaluaciones predecir`, pre-registro `20261029-100429-control-2.json`, v1.0):** alcance U6, P(entra) 100 %, fuerza «débil: sin historia». Con una sola unidad el motor no reparte nada: **todo lo de abajo es juicio sobre evidencia citada, no probabilidad calibrada.**

---

## 1. Formato: lo que fue el Control 1 (26-10, reconstruido de memoria el 29-10)

| # | Pregunta del Control 1 | De dónde salió | ¿Estaba predicha? |
|---|---|---|---|
| Ej. 1 | Demuestre $\dot k/k$, grafique y comente por qué fuera del EE crece y en el EE la tasa es cero | **Ayudantía 1, ej. 4**, casi textual; gráfico de clase | sí (`Control 1 - lectura cualitativa.md`: «Demostración, Ayud. 1 ej. 4») |
| Analice | ¿Qué es el sendero de crecimiento balanceado? | **Ayudantía 2, P2**, textual | sí («definición de la senda balanceada») |
| Comente 1 | Terremoto destruye la mitad del capital | Shock clásico de Solow; gráfico de Hiroshima y Nagasaki (clase 2: la variable vuelve a su tendencia) | sí (mini control del 25-10, P2) |
| Comente 2 | Dos países iguales en $g$, $n$, $\delta$; uno crece más; ¿y si cambia la tasa de inversión? | Dinámica de transición / convergencia condicional (clase 4, 07-10) | en parte (V/F «subir $s$ da crecimiento solo en el corto plazo») |
| Comente 3 | Cae $n$: corto y largo plazo | Estática comparativa de Solow (clase 3; JV 2.1.3) | sí (V/F 4 de la lectura cualitativa) |

**Lo que eso dice del Control 2:**
- **No hubo numérico.** El molde es: 1 desarrollo (demostrar + graficar + comentar), 1 «analice» de definición y 3 comentes de shocks (corto vs. largo plazo, nivel vs. tasa). El supuesto anterior (numérico encadenado de Principios) **se descarta**.
- **2 de 5 preguntas salieron casi textuales de las ayudantías.** La **ayudantía del vie 30-10** es la fuente más probable del Control 2: lo que salga ahí va primero.
- Los comentes son **shocks a una economía en su senda**, y la respuesta se juzga por distinguir el efecto en la tasa del efecto en el nivel.
- El Control 2 va al comienzo de la clase, igual que el 1: el mismo largo es lo más probable.

## 2. Molde probable del Control 2 (mismo esqueleto, materia de Romer)

| Lugar | Candidato principal | Alternativa |
|---|---|---|
| Desarrollo | Demuestre $g_A = \frac{\lambda}{1-\phi}n$, grafique $\dot A/A$ vs. $L/A$ y comente por qué $s_R$ no cambia $g$ de largo plazo (preg. 1-2) | Maximización: CPO de bienes finales → $p = r/\alpha$ → $\pi = \alpha(1-\alpha)Y/A$ (preg. 3-5) |
| Analice | ¿Por qué el crecimiento de $A$ exige competencia imperfecta? / ¿Qué es el markup y de dónde sale? | ¿Qué representa $A$ en Romer II (variedades) y por qué $Y = K^\alpha(AL_Y)^{1-\alpha}$ sigue valiendo? (preg. 11) |
| Comente (shock 1) | Sube $s_R$: ¿crece más rápido para siempre? (preg. 6) | Sube $\theta$ (preg. 12) |
| Comente (shock 2, **espejo del terremoto**) | Se pierde la mitad de $A$ (o de los investigadores): con $\lambda=1,\ \phi=0$, $\dot A/A = \theta s_RL/A$ salta, $g_A$ sube transitoriamente y $A$ vuelve **a la misma senda** | Romer original ($\phi = 1$) y los datos (preg. 7) |
| Comente (shock 3, **espejo de «cae $n$»**) | Cae $n$ **en Romer**: $g = \frac{\lambda}{1-\phi}n$ **baja para siempre**. Trampa: en Solow una caída de $n$ sube el **nivel** y no toca la tasa; en Romer baja la **tasa** | Dos países iguales salvo $L$ o $s_R$: misma tasa de largo plazo, distinto nivel (efecto escala) |

Reparto aproximado: 5.1 ~60 % (desarrollo + 2 comentes), 5.2.1-5.2.2 ~40 % (un desarrollo o un analice, más la distribución del ingreso de las láminas 10-12). Si la ayudantía del viernes es de 5.2, sube el peso de 5.2.

## 3. Las 12 preguntas más probables (con respuesta)

| # | Pregunta | Prob. | Forma |
|---|---|---|---|
| 1 | Derivar $g_A = \frac{\lambda}{1-\phi}n$ desde $\dot A = \theta L_A^\lambda A^\phi$ | alta | desarrollo |
| 2 | Alza permanente de $s_R$: qué pasa con $g_A$ y con el nivel de $A$ en el tiempo (gráfico) | alta | gráfico + explicación |
| 3 | CPO de la empresa de bienes finales: $w$ y $p_j$ | alta | desarrollo / numérico |
| 4 | Precio del monopolista: $p = r/\alpha$ (markup $1/\alpha$) | alta | desarrollo |
| 5 | Beneficio $\pi = \alpha(1-\alpha)Y/A$ y $x = K/A$ | media-alta | numérico |
| 6 | V/F: «si $s_R$ sube, la economía crece más rápido para siempre» | media-alta | V/F |
| 7 | Romer original ($\phi = 1$) y por qué los datos lo descartan | media-alta | V/F o comente |
| 8 | $y^*(t)$ con $s_R$: signos de $s_R$, $L$ y $n$ | media | comente |
| 9 | $s_R$ que maximiza $y$ en la SCB ($=\tfrac12$; JV ej. 2) | media | numérico |
| 10 | Con datos: estimar $\lambda/(1-\phi)$ y el $g$ de largo plazo (JV ej. 3) | media | numérico |
| 11 | Mostrar que con simetría se vuelve a $Y = K^\alpha(AL_Y)^{1-\alpha}$ | media | desarrollo |
| 12 | Alza de $\theta$ (JV ej. 1): mismo patrón que $s_R$ | media-baja | V/F |

### Pauta resumida

**1. Derivación de $g$.** $\frac{\dot A}{A} = \theta\frac{L_A^\lambda}{A^{1-\phi}}$. En la SCB $\dot A/A$ es constante → su log también → la derivada del log respecto de $t$ es 0: $0 = \lambda\frac{\dot L_A}{L_A} - (1-\phi)\frac{\dot A}{A}$. En la SCB $L_A = s_R L$ con $s_R$ constante → $\dot L_A/L_A = n$ (si fuera mayor, a la larga todos investigan). Por lo tanto $g_A = \frac{\lambda}{1-\phi}n$. Requiere $\phi < 1$.
- Lectura: $g$ depende solo de parámetros de la tecnología de ideas y de $n$; **no** de $s_R$, $s$ ni $\theta$. Con $\lambda = 1,\ \phi = 0$: $g_A = n$.
- Por qué baja $g_A$ con $L_A$ fijo: con $\phi < 1$ el denominador $A^{1-\phi}$ crece; cada idea nueva es una fracción más chica de un stock mayor (ej. de clase: $\theta = 0{,}01$, $L_A = 100$: $A = 100 \to 1\%$, $A = 200 \to 0{,}5\%$).

**2. Alza de $s_R$** ($\lambda=1,\ \phi=0$: $\frac{\dot A}{A} = \theta s_R\frac{L}{A}$). Gráfico: eje vertical $\dot A/A$, horizontal $L/A$; recta desde el origen con pendiente $\theta s_R$ y horizontal en $n$. Sube $s_R$ → la recta se empina → en el $L/A$ inicial $g_A$ salta sobre $n$ → $A$ crece más rápido que $L$ → $L/A$ baja → $g_A$ vuelve a $n$. Resultado: **efecto tasa transitorio, efecto nivel permanente** ($\ln A$ se desplaza hacia arriba con la misma pendiente). Igual que un alza de $s$ en Solow. Nuevo nivel en la SCB: $A = \frac{\theta s_R L}{g}$ (general: $A^{1-\phi} = \frac{\theta s_R^\lambda L^\lambda}{g}$).

**3. Bienes finales (5.12-5.13).** $\max_{L_Y,x_j} L_Y^{1-\alpha}\int_0^A x_j^\alpha dj - wL_Y - \int_0^A p_jx_jdj$ (precio de $Y$ = 1).
- $w = (1-\alpha)\frac{Y}{L_Y}$ (PMgL = salario).
- $p_j = \alpha L_Y^{1-\alpha}x_j^{\alpha-1}$ (PMg del bien de capital $j$ = su precio de arriendo): es la **demanda inversa** que enfrenta el monopolista $j$.
- Con $A$ dado la función tiene **rendimientos constantes** en $L_Y$ y los $x_j$ → competencia perfecta en este sector.

**4. Monopolista intermedio (5.2.2).** Compra la patente (costo fijo) y transforma 1 unidad de capital bruto en 1 de bien de capital a costo $r$. $\max_x\ p(x)x - rx$ → $p'(x)x + p - r = 0$ → $p = \frac{r}{1 + p'x/p}$. De (5.13), $\frac{p'(x)x}{p} = \alpha - 1$ → $p = \frac{r}{\alpha}$. Markup $\frac1\alpha > 1$ sobre el costo marginal. Elasticidad precio de la demanda $= \frac{1}{\alpha-1}$, en valor absoluto $\frac{1}{1-\alpha}$. Todos cobran lo mismo → simetría $x_j = x$.

**5. Beneficio y $x$.** $\pi = (p - r)x = \frac{1-\alpha}{\alpha}rx$. Con $r = \alpha p = \alpha^2L_Y^{1-\alpha}x^{\alpha-1}$: $\pi = \alpha(1-\alpha)L_Y^{1-\alpha}x^\alpha$, y como $Y = AL_Y^{1-\alpha}x^\alpha$: $\pi = \alpha(1-\alpha)\frac{Y}{A}$ (5.14). Mercado de capital: $\int_0^A x_jdj = K$ → $x = K/A$ (5.15).
- Reparto del producto: $wL_Y = (1-\alpha)Y$; pagos a los bienes de capital $Apx = \alpha Y$, que se dividen en capital bruto $rK = \alpha^2Y$ y beneficios $A\pi = \alpha(1-\alpha)Y$. Suma: $Y$. **Droller lo pone en sus láminas 10-12**, justo después del monopolista y antes del sector de investigación, y cierra con «los tres pagos» contra Solow ($rK + wL = Y$, nada para los innovadores): súbelo a probabilidad media-alta.

**6. V/F de $s_R$.** **Falso** con $\phi < 1$: eleva $g_A$ sólo en la transición; en el largo plazo $g = \frac{\lambda}{1-\phi}n$. Lo permanente es el nivel. (Verdadero sólo en el Romer original, $\phi = 1$.)

**7. Romer original ($\lambda = 1,\ \phi = 1$).** $\frac{\dot A}{A} = \theta L_A$: la tasa depende del **número** de investigadores (efecto escala sobre la tasa). Como $L_A$ creció muchísimo en el siglo XX (patentes y científicos de EE. UU. y el G-5), el crecimiento debió acelerarse; el PIB per cápita de EE. UU. creció a una tasa estable (lám. 9) → $\phi = 1$ es rechazado por los datos → $\phi < 1$ (Jones 1995). Ojo con la confusión de clase: $\theta L_A$ es el **cambio** $\dot A$ si $\phi = 0$ y la **tasa** $\dot A/A$ si $\phi = 1$.

**8. $y^*$ con $s_R$** (JV 5.11, $\lambda=1,\ \phi=0$): $y^*(t) = \left(\frac{s_K}{n+g+d}\right)^{\frac{\alpha}{1-\alpha}}(1-s_R)\,\frac{\theta s_R}{g}\,L(t)$.
- $s_R$: **ambiguo** (más ideas, pero menos gente produciendo: factor $1-s_R$).
- $L$: **+** (efecto escala sobre el nivel: más gente, más ideas, y las ideas no se diluyen).
- $n$: **−** (con $g = n$, sube el denominador de $\theta s_R/g$ y también diluye el capital, como en Solow).
- De dónde sale: $\hat A = A(1-s_R)$ crece a $g$, así que es Solow con $\hat A$: $\tilde y^* = (1-s_R)\left(\frac{s}{\delta+n+g}\right)^{\alpha/(1-\alpha)}$ y $y = A\tilde y^*$ (clase 8).

**9. $s_R$ óptimo para el nivel (JV ej. 2).** En $y^*$ sólo depende de $s_R$ el producto $s_R(1-s_R)$ → derivando, $1 - 2s_R = 0$ → $s_R = \tfrac12$. Se puede investigar «demasiado»: pasado ese punto, la caída de trabajadores en $Y$ pesa más que las ideas extra.

**10. Estimar con datos (JV ej. 3).** $n = 1\%$, investigadores crecen 3 %, $\dot A/A = 2\%$.
- (a) $2\% = \frac{\lambda}{1-\phi}\cdot 3\%$ → $\frac{\lambda}{1-\phi} = \tfrac23$.
- (b) Largo plazo: $g = \tfrac23\cdot 1\% \approx 0{,}67\%$.
- (c) Difiere del 2 % observado porque los investigadores no pueden crecer más rápido que la población para siempre ($s_R \le 1$): el 2 % histórico es en parte transición (alza de $s_R$, educación).
- (d) Que más países hagan I+D sube el número de investigadores del mundo por un tiempo (nivel y transición), pero el largo plazo sigue atado a $n$.

**11. Recuperar Solow.** Simetría $x_j = x$: $Y = AL_Y^{1-\alpha}x^\alpha$; con $x = K/A$: $Y = AL_Y^{1-\alpha}A^{-\alpha}K^\alpha = K^\alpha(AL_Y)^{1-\alpha}$ (5.16). Intuición (ej. de la clase 8, $\alpha = \tfrac12$, $K = 100$, $L_Y = 1$): $A = 1,\ x = 100 \to Y = 10$; $A = 4,\ x = 25 \to Y = 20$. Mismo capital en más variedades produce más, porque cada variedad tiene rendimientos decrecientes.

**12. Alza de $\theta$.** Igual que $s_R$: la recta $\theta s_R L/A$ se empina → $g_A$ sube transitoriamente → vuelve a $n$ con un nivel de $A$ más alto.

## 4. Numérico de práctica (para fijar las fórmulas; el Control 1 no tuvo numérico)

**Parte I (5.2).** $\alpha = 0{,}5$, $K = 1000$, $A = 10$, $L_Y = 100$.
a) $x = K/A = 100$. b) $Y = K^\alpha(AL_Y)^{1-\alpha} = \sqrt{1000}\sqrt{1000} = 1000$. c) $w = (1-\alpha)Y/L_Y = 5$. d) $p = \alpha L_Y^{0,5}x^{-0,5} = 0{,}5\cdot10\cdot0{,}1 = 0{,}5$. e) $r = \alpha p = 0{,}25$. f) $\pi = \alpha(1-\alpha)Y/A = 25$; control: $(p-r)x = 0{,}25\cdot100 = 25$ ✓. g) Reparto: $wL_Y = 500$, $rK = 250$, $A\pi = 250$; suma 1000 ✓.

**Parte II (5.1).** $\lambda = 1,\ \phi = 0,\ \theta = 0{,}01,\ L = 1000,\ n = 1\%,\ s_R = 0{,}05$.
a) $g$ de largo plazo $= n = 1\%$. b) $A$ en la SCB $= \theta s_RL/g = 0{,}01\cdot0{,}05\cdot1000/0{,}01 = 50$. c) $s_R$ sube a $0{,}10$: en el impacto $g_A = 0{,}01\cdot0{,}10\cdot1000/50 = 2\%$. d) En el largo plazo $g_A$ vuelve a 1 % y la nueva senda de $A$ es el doble de la antigua ($\theta s_R'L/g = 100$ con el mismo $L$). e) $y^*$ cambia en $\frac{0{,}10\cdot0{,}90}{0{,}05\cdot0{,}95} \approx 1{,}89$ veces respecto de la senda antigua (sigue bajo $s_R = \tfrac12$, así que subirlo aumenta $y$).

## 5. Qué estudiar primero (con lo que queda: vie 30, sáb 31, dom 1)

1. **Vie (pasada 1, 5.1):** derivar $g$ de memoria (preg. 1) y dibujar el gráfico de $s_R$ con sus dos trayectorias (preg. 2). Después V/F 6, 7 y 12.
2. **Sáb (pasada 2, 5.2.1-5.2.2):** preg. 3-5 y 11 de memoria; después la Parte I del numérico sin mirar.
3. **Dom (repaso espaciado):** preg. 8-10 y la Parte II; lo que haya salido en la ayudantía del vie, primero.

Fuentes: correo de Droller (27-10); JV 3.ª ed., secciones 5.1-5.2.2 y ejercicios del cap. 5 (`.claude/ctx/pdf/introductiontoeconomicgrowth3rd…md`, líneas 5161-5976 y 7016-7050); láminas y apuntes de las clases 6-8; pre-registro del motor (`OneDrive/BancoEvaluaciones/Macroeconomía II/Predicciones/20261029-100429-control-2.json`).
