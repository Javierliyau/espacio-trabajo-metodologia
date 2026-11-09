---
tema: retomar-micro-juegos
fecha: 2026-11-09 17:55
resumen: (auto, fin de sesion) ultimo pedido: emepecemos
---
Handoff automatico de la sesion `a812dfac-dedf-4976-8e10-46018838d73e` («Retomar micro-juegos»), 48 llamadas, contexto final 124.8k. Es mecanico: no interpreta decisiones. Si existe un handoff manual del mismo tema, manda ese.

## Ultimos pedidos del usuario
- cual es el paso 2
- habian estrategias estrictamente dominantes?
- como habia que responder la 1
- definicion de estrategia dominada y semidomi9nada
- genial ya termine
- emepecemos

## Archivos creados o editados (leer primero los relevantes, por rango)
- (ninguno)

## Ultima respuesta de Claude (recortada)

Empecemos con la **D2 (juego consecutivo)**, que es la primera parte de μ5a. Después vemos A2 ej. 2 y Daraprim.

## D2: juego consecutivo (10 min, sin mirar)

**A juega primero** y elige Arriba o Abajo. **B ve lo que hizo A** y después elige Izquierda o Derecha. Los pagos, con el de A primero:

| Si A elige… | y B elige… | Pagos (A, B) |
|---|---|---|
| Arriba | Izquierda | (1, 9) |
| Arriba | Derecha | (1, 9) |
| Abajo | Izquierda | (0, 0) |
| Abajo | Derecha | (2, 1) |

**a)** Dibuja el **árbol**. Puedes escribirlo en texto o hacerlo en GoodNotes y mandar una foto.

**b)** Resuelve por **inducción hacia atrás**, con números en cada paso:
- Si A eligió Arriba, ¿qué hace B?
- Si A eligió Abajo, ¿qué hace B?
- Anticipando eso, ¿qué elige A? → **Resultado del juego:** (___, ___)

**c)** Pásalo a **matriz** (forma normal) y encuentra **todos** los EN con mejores respuestas.

**d)** Uno de los EN de c) **no** sale por inducción hacia atrás. ¿Cuál es? ¿Qué amenaza tendría que hacer B para sostenerlo y por qué A **no se la cree**?

**Pista para d):** fíjate en qué gana B si A juega Arriba y qué gana si A juega Abajo. ¿Qué preferiría B que hiciera A?
