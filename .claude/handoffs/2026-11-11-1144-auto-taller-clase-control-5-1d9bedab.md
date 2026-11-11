---
tema: taller-clase-control-5
fecha: 2026-11-11 11:44
resumen: (auto, fin de sesion) ultimo pedido: no entiendo
---
Handoff automatico de la sesion `1d9bedab-59de-4f0d-b428-2bba934398d3` («Taller clase control 5»), 17 llamadas, contexto final 82.1k. Es mecanico: no interpreta decisiones. Si existe un handoff manual del mismo tema, manda ese.

## Ultimos pedidos del usuario
- hagamos la 3
- el 7
- el 4
- hagmos 2
- como se halla la tangente de ej 1
- no entiendo

## Archivos creados o editados (leer primero los relevantes, por rango)
- (ninguno)

## Ultima respuesta de Claude (recortada)

Vamos más despacio, con una idea a la vez.

## Idea 1: qué es la tangente

Es una **recta que toca la curva en un solo punto**, con la misma inclinación que tiene la curva ahí.

Para escribir cualquier recta basta saber:
- **por dónde pasa**, que es un punto;
- **qué tan inclinada está**, que es la pendiente $m$.

En este ejercicio, el punto ya lo tenemos: $(2,2)$. **Solo falta la pendiente.**

## Idea 2: la pendiente es la derivada

La inclinación de la curva en un punto es **la derivada en ese punto**. Así que el trabajo consiste en calcular $y'$ y reemplazar $x = 2$, $y = 2$.

## Idea 3: cómo derivar esta curva, pieza por pieza

La curva es

$$e^{y^2 - x^2} = xy - 3$$

Derivamos **cada lado por separado**.

**Lado izquierdo:** $e^{y^2 - x^2}$

La derivada de $e^{\text{algo}}$ es $e^{\text{algo}}$ multiplicado por la derivada de ese "algo". Aquí el "algo" es $y^2 - x^2$:

- la derivada de $y^2$ es $2y\cdot y'$ (se pone $y'$ porque $y$ depende de $x$);
- la derivada de $x^2$ es $2x$.

Entonces el lado izquierdo queda

$$e^{y^2 - x^2}\cdot\big(2y\,y' - 2x\big)$$

**Lado derecho:** $xy - 3$

- $xy$ es un producto, así que su derivada es $1\cdot y + x\cdot y'$;
- la derivada de $-3$ es $0$.

Entonces el lado derecho queda

$$y + x\,y'$$

**Juntamos los dos lados:**

$$e^{y^2 - x^2}\big(2y\,y' - 2x\big) = y + x\,y'$$

## Idea 4: reemplazar el punto $(2,2)$

Ponemos $x = 2$ e $y = 2$:

- El exponente queda $y^2 - x^2 = 4 - 4 = 0$, así que $e^0 = 1$.
- El paréntesis queda $2\cdot
