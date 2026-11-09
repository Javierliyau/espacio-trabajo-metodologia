---
tema: simulacro-pep-1-mundaca
fecha: 2026-11-09 17:55
resumen: (auto, fin de sesion) ultimo pedido: ahora en una prueba como se arma la respuesta de la induccion hacia atras ya que yo marco el dibujo nomas ense
---
Handoff automatico de la sesion `2caadb1e-1658-4597-a773-44cabdfdd26b` («Simulacro PEP 1 Mundaca»), 12 llamadas, contexto final 82.8k. Es mecanico: no interpreta decisiones. Si existe un handoff manual del mismo tema, manda ese.

## Ultimos pedidos del usuario
- el pago (0,10) a que correspoonde
- como quedaria en la matrizz
- Como lo ves
- estan bien los equiliobrios de nash?
- como se anotaria en la prueba
- ahora en una prueba como se arma la respuesta de la induccion hacia atras ya que yo marco el dibujo nomas enseñame

## Archivos creados o editados (leer primero los relevantes, por rango)
- (ninguno)

## Ultima respuesta de Claude (recortada)

Marcar el dibujo está bien, pero **solo no basta**: el corrector quiere ver el razonamiento escrito, **nodo por nodo, de atrás hacia adelante**. La estructura siempre es la misma, en 4 pasos.

---

**b)** Resuelvo por inducción hacia atrás, partiendo del último nodo de decisión.

**Paso 1: último nodo (decide I, después de que E entra)**
Si E entra, I compara:
- Acomodar → 4
- Guerra → 1

Como 4 > 1, **I acomoda**. (Marco esa rama en el árbol.)

**Paso 2: nodo anterior (decide E, anticipando lo que hará I)**
E sabe que, si entra, I va a acomodar. Entonces compara:
- Entrar → 3 (porque I acomoda)
- No entrar → 0

Como 3 > 0, **E entra**.

**Paso 3: equilibrio de Nash perfecto en subjuegos (ENPS)**

ENPS = (Entrar, Acomodar)

Resultado: E entra e I acomoda, con pagos (3, 4).

**Paso 4: conexión con la a)**
De los dos equilibrios de Nash de la a), solo (Entrar, Acomodar) es perfecto en subjuegos. (No entrar, Guerra) no sobrevive a la inducción hacia atrás, porque en el subjuego que empieza cuando E entra, Guerra no es óptima para I (1 < 4).

---

**Cómo arma esto la nota**

| Lo que escribes | Por qué suma |
|---|---|
| «Partiendo del último nodo» | Muestra que conoces el método |
| La comparación con números (4 > 1, 3 > 0) | Es la justificación; sin números es solo una afirmación |
| **«E anticipa»** | Es la idea central: el primero decide sabiendo cómo responderá el segundo |
| El ENPS como **par de estrategias** | Es la respuesta pedida |
| La conexión con la a) | Prepara la
