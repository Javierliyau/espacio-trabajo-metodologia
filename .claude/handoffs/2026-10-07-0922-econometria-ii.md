---
tema: econometria-ii
fecha: 2026-10-07 09:22
resumen: Etapa 1: script 04-base-grupo.R (68.703 matriculados, 25 col.) e informe-etapa-1-grupo.pdf listos; el grupo escribió un 3er código a mano (pref 1 vs 2-3) que se revisó; falta decidir la Y con el grupo y la presentación del jue 8-10.
---
## Objetivo
Etapa 1 del trabajo práctico de Econometría II (Pfeng): base DEMRE 2026 en un data frame + informe LaTeX. Presentación jue 8-10 (10 min). Regla IA = nota mínima: el usuario ya fue advertido, no repetirlo.

## Hecho en esta sesión
- `trabajo/econometria-ii-demre/scripts/03-base-seleccion.R`: versión dplyr sin pipe con la selección del grupo (29 col., incluye columnas redundantes). Superada por la 04.
- `scripts/04-base-grupo.R`: estructura del código del grupo (tidyverse, df1-df4, reduce, secciones ####), corregido y verificado con Rscript. Guarda `datos/procesados/base-etapa-1-grupo.csv`: 68.703 filas, 25 col., 0 NA; Y = 60.300 unos / 8.403 ceros. Coincide con la base 02 en todas las variables comunes.
- `informe/informe-etapa-1-grupo.tex` y `.pdf` (5 págs., compila; revisada a la vista solo la pág. 4). El informe viejo `informe-etapa-1.*` no se tocó.
- Se revisaron 2 códigos a mano del grupo (David). El 2.º (pegado el 7-10, no guardado en archivo) se corrió en /tmp: 60.544 filas, una por estudiante; Y = PREF_PRIMERA_DUMMY (pref 1 = 40.173, pref 2-3 = 20.371).

## Decisiones tomadas (no re-litigar)
- Base 04: solo matriculados vía 1 y tipo 1, SITUACION_EGRESO == 1; Y = pref 1-3 vs 4+; variables del colegio con los 108.598 postulantes de la promoción.
- REGIMEN NA -> categoría 0; ingreso 99 se deja como categoría.
- Sacadas por redundantes: VIA, TIPO_PREF, ORDEN_PREF, PTJE_PREF (constantes o copias, verificado).
- Explicaciones cortas y simples.

## Próximo paso exacto
El grupo debe elegir la definición de la Y. Hay 3 lecturas del correo: (a) matriculados, Y = pref 1-3 vs 4+ (script 04 e informe); (b) postulantes, Y = matriculado en pref 1-3 vs no matriculado, descartando pref 4+; (c) la del 2.º código del grupo: solo pref 1-3, Y = pref 1 vs 2-3. Recomendar confirmar con el profesor. Luego ajustar script e informe a la elegida y hacer la presentación (preguntar formato: beamer u otro).

## Pendientes
- Problemas del 2.º código del grupo: ANYO_EGRESO == 2025 deja entrar 300 de situación 2-4 (usar SITUACION_EGRESO == 1); INGRESO_COLEGIO promedia el código 99 (máx. 99, mediana 27: sin sentido); N_ALUMNOS y N_MATRICULADOS cuentan todos los inscritos del RBD, no solo la promoción, y N_MATRICULADOS es conteo (mejor %); df3 con distinct toma un TIPO_PREF arbitrario (30 % no REGULAR), TIPO_PREF_DUMMY no sirve; RINDIO_PROCESO_ACTUAL == 1 solo saca 2 (inofensivo); rutas absolutas de David.
- Nombres del grupo en informe (línea 11 del .tex) y en el script (`# Integrantes:`).
- PORC_SUP_NOTAS: valores 10-100, definición sin confirmar.
- Correo al profesor (Y y adjuntos): no se sabe si se envió.
- `write.csv2` y join con dos llaves (script 03) no están en el catálogo de mi-proyecto-r; la 04 usa tidyverse (reduce, drop_na, n()) sin verificar catálogo.
- Guardar en el PROYECTO (`datos/trabajos/econometria-ii/`) script, informe y descripción cuando el grupo cierre.
- Etapa 2 (descriptivo, 18-10) y 3 (logit, 8-11): sin empezar.

## Leer primero (máx. 5 rutas, con rango de líneas o encabezado)
1. `trabajo/econometria-ii-demre/scripts/04-base-grupo.R` — secciones «FILTRAR DATOS» a «VARIABLE DE RESPUESTA»
2. `trabajo/econometria-ii-demre/informe/informe-etapa-1-grupo.tex` — «Construcción de la base» y «Variable de respuesta»
3. `C:\Proyecto Metodologia de estudio\datos\trabajos\econometria-ii\instrucciones-trabajo-practico.md` — «Etapa 1» (líneas 18-56)
