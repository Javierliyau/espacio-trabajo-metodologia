---
tema: requisitos-fase-2-profesor-pfeng
fecha: 2026-10-29 17:42
resumen: (auto, fin de sesion) ultimo pedido: todo se correlaciona al 100%
---
Handoff automatico de la sesion `0371378e-ac53-4c9e-8b28-3d44f08a963e` («Requisitos fase 2 profesor Pfeng»), 384 llamadas, contexto final 61.3k. Es mecanico: no interpreta decisiones. Si existe un handoff manual del mismo tema, manda ese.

## Ultimos pedidos del usuario
- que opinas : / <pasted_content id="09e3"> / [4:14 p. m., 29/10/2026] benja Lizana: Lo que borré o acorté: / 6.1: saqué la frase repetida y la cita «tampoco abusemos». Ahora dice: “Seguimos la regla del curso: si una variable tiene más de 5 % de datos faltantes, no se usa, para no dejar un tramo de f
- como quedarían cambios deja el texto perfecto
- [Image: original 2485x1404, displayed at 2000x1130. Multiply coordinates by 1.24 to map to original image.]
- @"C:\Users\javie\Downloads\Informe_Etapa_2_Econometria (2).pdf" @"C:\Users\javie\Downloads\Informe_Etapa_2_Econometria (3).pdf" @"C:\Users\javie\Downloads\FINAL DEFINITIVO econometria_etapa2_codigo_final_final.R" / esta todo para entregar
- que nota
- todo se correlaciona al 100%

## Archivos creados o editados (leer primero los relevantes, por rango)
- `C:\Proyecto Metodologia de estudio\datos\trabajos\econometria-ii\etapa-2\entrega\informe-etapa-2.tex`
- `C:\Proyecto Metodologia de estudio\datos\trabajos\econometria-ii\etapa-2\entrega\codigo-final-etapa-2.R`
- `trabajo/etapa2-final/correr2.R`
- `trabajo/etapa2-final/verificar-informe.R`
- `C:\Proyecto Metodologia de estudio\datos\trabajos\econometria-ii\etapa-2\entrega\presentacion-etapa-2.tex`

## Ultima respuesta de Claude (recortada)

Sí, el informe, el código y la presentación coinciden al 100 %. Volví a correr el R de David con los datos y comparé cada cifra que citan el informe y la presentación.

**Lo que revisé:**
- **Base y variable respuesta:** N = 168.714, de los cuales Y = 1 son 60.234. También cuadran el desglose por preferencias (39.958 / 13.257 / 7.019, 8.391 en cuarta o más abajo, 100.089 sin matrícula, 55.361 no postulados) y los conteos de TP, Matemática 2, PACE y BEA.
- **Datos faltantes y univariado:** 46.668 faltantes (27,66 %), 61 (0,04 %) y 3 casos. Coinciden los descriptivos, los outliers, las reglas de consistencia y la edad máxima de 71 años.
- **Bivariado:** cuadran las tasas por tramo de todas las variables, la edad retramificada (37,2 / 20,6, 91 % de la base, IV 0,049), la dependencia (28,6 / 36 / 53,1) y los 18 IV.
- **Sección 9:**
  - Las correlaciones de los WOE: 0,96 (NEM con el promedio de notas), 0,95 (ranking con el promedio), 0,72 (dependencia con el ingreso del colegio) y 0,79 (PORC_SUP con el promedio).
  - Los VIF: 45,1 / 27,0 / 22,9 / 16,0 en los cuatro pasos, el empate del paso 3 (2,38 frente a 2,33) y el VIF máximo final de 1,729.

**Dos observaciones (ninguna contradice al informe):**
- N_ALUMNOS tampoco es monótona. Aun así, la frase «salvo la edad» del informe se sostiene, porque habla de las variables que pasan el corte de IV, y N_ALUMNOS tiene IV 0,006.
- La tabla de descriptivos no incluye PORC_SUP_NOTAS, que tiene 0 outliers. Es una omisión, no un error.

**Qu
