# Respuestas modelo · Comentes PEP 1 Macro II (M1, 17-11)

Plantilla: **veredicto → ecuación o gráfico → mecanismo → ancla (1 línea)**. Hechas en la sesión del 17-11 y corregidas con `2026-11-06-guia-pep-1-PAUTA-no-abrir.md`.

---

## Comente 1 (guía 5) · Verdadero, en valor absoluto

> «El modelo de Solow predice que la tasa de crecimiento del capital por trabajador es mayor mientras más lejos esté la economía de su estado estacionario.»

**Verdadero, en valor absoluto.**

$$\dot k = s\,f(k) - (n+\delta)\,k \quad\Rightarrow\quad \frac{\dot k}{k} = s\,k^{\alpha-1} - (n+\delta)$$

**Mecanismo:**
1. Hay rendimientos decrecientes (α < 1).
2. Por eso el producto medio, k^(α−1), cae cuando k sube.
3. Entonces la inversión **por unidad de capital** (s·y/k) cae con k. La inversión total s·y, en cambio, sube.
4. El requerimiento (n + δ) es constante.

La distancia vertical entre las dos curvas es k̇/k y crece al alejarse de k\*.
**Matiz:** si k > k\*, la tasa es negativa, y más negativa mientras más lejos esté.

**Gráfico:** curva decreciente s·k^(α−1) y recta horizontal n + δ, que se cortan en k\*. Marcar la distancia en k₀ y en un k₀' más a la izquierda (donde la distancia es mayor).

**Ancla:** la URSS creció rápido mientras tenía poco capital y se fue frenando a medida que lo acumulaba (Easterly y Fischer 1995).

---

## Comente 2 (guía 7) · Falso

> «Un aumento permanente de la tasa de ahorro aumenta permanentemente la tasa de crecimiento del producto por trabajador.»

**Falso.** Es un efecto **nivel**, no un efecto **tasa**: la tasa de crecimiento sube solo durante la transición.

$$y^*(t) = A(t)\left(\frac{s}{n+g+\delta}\right)^{\frac{\alpha}{1-\alpha}} \qquad g_y^{\,LP} = g$$

**Mecanismo:**
- Si s sube, la curva s·f(k)/k se desplaza hacia arriba y se abre una brecha con (n + g + δ), así que k crece más rápido.
- Por rendimientos decrecientes, la brecha se cierra en un k\* **nuevo y más alto**.
- Al final, g_y vuelve a g.

**Gráficos:**
- ln y en función de t: un quiebre hacia arriba y después una senda paralela, más alta.
- g_y en función de t: salta sobre g y vuelve gradualmente a g.

**Ancla:** la URSS subió la inversión de ~15 % a ~30 % (Popov 2006) y aun así se frenó. Chile subió el ahorro de ~9 % a ~24 % del PIB y su crecimiento pasó de ~7 % a ~4 % y luego a ~2 %.

---

## Comente 3 (guía 13) · Falso

> «El modelo de Solow predice que los países pobres siempre crecen más rápido que los países ricos.»

**Falso.** Solow predice convergencia **condicional**: cada país crece según la distancia a **su propio** k\*, no según qué tan pobre es.

$$\frac{\dot k}{k} = s\,k^{\alpha-1} - (n+\delta) \qquad k^* = \left(\frac{s}{n+\delta}\right)^{\frac{1}{1-\alpha}}$$

**Mecanismo:**
- Un país pobre con s bajo o n alto tiene un k\* bajo. Si está cerca de él, crece lento.
- Un país rico que está lejos de su k\*, más alto, puede crecer más rápido.
- La convergencia **absoluta** solo vale entre países con los mismos s, n, δ y A.

**Gráfico:** dos curvas, s_R·k^(α−1) (más arriba) y s_P·k^(α−1). k_P está cerca de k\*_P (brecha chica) y k_R lejos de k\*_R (brecha grande).

**Ancla:** en los noventa, Chile creció 4,8 % per cápita y Latinoamérica 1,8 % (PWT), aunque varios países de la región eran más pobres que Chile.

---

## Comente 4 (guía 17) · Verdadero

> «Si ϕ < 1 y el número de investigadores L_A fuera constante, la tasa de crecimiento de la tecnología, Ȧ/A, tendería a cero.»

**Verdadero.**

$$\dot A = \theta\,L_A^{\lambda}\,A^{\phi} \quad\Rightarrow\quad \frac{\dot A}{A} = \theta\,\frac{L_A^{\lambda}}{A^{1-\phi}}$$

**Mecanismo:**
- Como 1 − ϕ > 0, el denominador crece con A. Con L_A fijo, la tasa tiende a 0.
- Vale para todo ϕ < 1: incluye 0 < ϕ < 1 («hombros de gigantes», pero no lo bastante altos) y ϕ < 0 («pesca agotada»).
- Para que haya crecimiento sostenido, L_A tiene que crecer a tasa n:

$$g_A = \frac{\lambda\,n}{1-\phi}$$

**Ancla:** la URSS tenía ~1,5 millones de científicos y gastaba 6,2 % del PNB en I+D (1988), sin un crecimiento sostenido de A.

---

## Comente 5 (guía 18) · Falso

> «En el modelo de Romer con ϕ < 1, un aumento permanente de la fracción de trabajadores dedicados a investigar, s_R, aumenta permanentemente la tasa de crecimiento de largo plazo de la economía.»

**Falso.** Con ϕ < 1, subir s_R es un efecto **nivel** sobre A, no un efecto **tasa** (es la misma lógica que el comente 2, pero con ideas).

$$\frac{\dot A}{A} = \theta\,\frac{(s_R L)^{\lambda}}{A^{1-\phi}} \qquad g_A^{\,LP} = \frac{\lambda\,n}{1-\phi}\ \text{(no depende de } s_R)$$

**Mecanismo:**
- Si s_R sube, el numerador salta y Ȧ/A sube por sobre λn/(1−ϕ).
- A crece más rápido, pero el denominador A^(1−ϕ) también, así que la tasa vuelve a λn/(1−ϕ).
- Queda un A **más alto** para siempre, con la misma tasa.
- Matiz: el nivel de y sube si s_R no es demasiado alto, porque y depende de (1 − s_R): hay menos gente produciendo.

**Gráficos:**
- ln A en función de t: un quiebre hacia arriba y después una senda paralela, más alta.
- g_A en función de t: salta y vuelve a λn/(1−ϕ).

**Ancla:** Corea subió su I+D a ~5 % del PIB, de las más altas del mundo, y aun así su crecimiento potencial ronda el 2 %. La URSS tenía un ejército de científicos sin una aceleración permanente.

---

## Lista de errores (vuelven tapados el jue 19 y el dom 22)

- **E1:** Al subir k, s·y **sube**. Lo que baja es s·y/k (el producto medio).
- **E2:** Si k > k\*, la tasa es negativa: decir «mayor **en valor absoluto**».
- **E3:** Al subir s, la economía va a un k\* **nuevo y más alto**, no al mismo.
- **E4:** En el largo plazo g_y = g, no cero (salvo que A sea constante).
- **E5:** «Siempre» significa «en todos los casos», no «para siempre en el tiempo». La razón del F: cada país va a **su propio** k\*.
- Falta anotar el % de seguridad de cada comente para marcar los **R**.
