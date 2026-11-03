---
tema: econometria-pep1-cuarto-chat
fecha: 2026-11-03 17:53
resumen: (auto, fin de sesion) ultimo pedido: [Image: source: C:\Users\javie\AppData\Local\Temp\claude\C--Espacio-de-trabajo-Metodologia-de-estudio\5a23d799
---
Handoff automatico de la sesion `5a23d799-3876-4f60-9400-64286dd80963` («Econometría PEP1 cuarto chat»), 45 llamadas, contexto final 100.4k. Es mecanico: no interpreta decisiones. Si existe un handoff manual del mismo tema, manda ese.

## Ultimos pedidos del usuario
- @"C:\Users\javie\Downloads\3A-woe-iv.pdf"
- explicame la b del sidiquio
- qu etendriamos que hacer ahora
- que hacemos ahora
- que hay que hacer en la a
- [Image: source: C:\Users\javie\AppData\Local\Temp\claude\C--Espacio-de-trabajo-Metodologia-de-estudio\5a23d799-3876-4f60-9400-64286dd80963\images\1.png]

## Archivos creados o editados (leer primero los relevantes, por rango)
- `trabajo/p3a-woe-practica/3A-woe-iv.tex`
- `trabajo/p3a-woe-practica/3B-scorecard.tex`

## Ultima respuesta de Claude (recortada)

La a) pide un **efecto parcial discreto**: comparar dos perfiles que solo difieren en `study`. No se usa la derivada, sino que **se calculan dos probabilidades y se restan**.

**Pasos:**

1. **Índice z del perfil de 5 h**, reemplazando todo en la parte lineal:
   z₅ = −1,17 + 0,24·(3,0) + 0,00058·(1.200) + 0,073·(5)

2. **Índice z del perfil de 10 h**: igual, pero con study = 10.
   Atajo: z₁₀ = z₅ + 0,073·5, porque solo cambia study.

3. **Pasar cada z por la logística:**
   P̂ = Λ(z) = 1 / (1 + e^(−z))

4. **Restar:** ΔP̂ = P̂(10 h) − P̂(5 h).

5. **Interpretar en pp:** «Manteniendo hsGPA = 3,0 y SAT = 1.200, estudiar 10 h en vez de 5 h aumenta la probabilidad estimada de graduarse en ___ **puntos porcentuales**».

**Trampas (las de tu P1):**
- La respuesta va en **pp**, no en %.
- **No** sirve hacer 0,073 × 5: eso es el cambio en el **índice z** (log-odds), no en la probabilidad. Hay que pasar por Λ.
- Ojo con el SAT: es **1.200** (mil doscientos). En el libro aparece como «1,200» con coma de miles.

**Para que verifiques:** z₅ ≈ 0,611. Calcula tú los dos P̂ y la diferencia, y me dices qué te dio.
