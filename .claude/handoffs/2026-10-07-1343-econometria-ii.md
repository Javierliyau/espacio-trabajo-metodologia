---
tema: econometria-ii
fecha: 2026-10-07 13:43
resumen: Tres versiones listas (original David limpia, corregida, consenso) de script R + informe LaTeX de la Etapa 1; el grupo debe elegir; consenso recomendada (60.300 × 34).
---
## Objetivo
Etapa 1 del trabajo práctico de Econometría II (prof. Brian Pfeng Ibacache). Entrega jue 8-10 (según correo de Jorge; en clase dijo dom 4-10 → confirmar). Presentación jue 15-10, máx. 10 min. Regla IA: no repetirla.

## Hecho en esta sesión
- `trabajo/revision-05/06-base-david-corregido.R`: script de David + cambios, rutas solo por nombre de archivo (CSV en la misma carpeta). Verificado: 60.300 × 34, Y 40.002/20.298, 0 RBD NA. CSV copiados a `trabajo/revision-05/` para correrlo.
- `trabajo/revision-05/07-base-consenso.R`: rutas absolutas de David, `ANYO_EGRESO==2025` + `SITUACION_EGRESO==1`, conserva `distinct()` en df4 (no cambia filas), sin TASA_MATRICULA. Misma base que 06 (verificado con all.equal).
- Informes LaTeX en `trabajo/econometria-ii-demre/informe/` (los tres compilan sin errores):
  - `informe-etapa-1-david-limpio.tex/.pdf`: original de David (60.544, 30 col.) sin comentarios OJO.
  - `informe-etapa-1-corregido.tex/.pdf`: base del script 06, con TASA_MATRICULA y tabla de dummies.
  - `informe-etapa-1-consenso.tex/.pdf`: base del script 07, sin TASA, con ANYO_EGRESO en la definición de variables.
- Funciones del script comparadas con el catálogo LPE: todas están, salvo las que ya usaba David (read_csv2, joins, reduce, tidyverse).
- Notas estimadas: original 4,5–5,0; corregida/consenso 5,5–6,0; solo ANYO_EGRESO 5,3–5,8 (5,4–5,9 si se explica en el informe).
- Mensajes para David entregados en el chat (explicación de los cambios, respuesta sobre ANYO_EGRESO).

## Decisiones tomadas (no re-litigar)
- Lo innegociable: guardar la base, sacar TIPO_PREF_DUMMY/df3, quitar el 99 del promedio de ingreso, dejar fuera a los sin RBD en las variables del colegio, RINDIO %in% c(1,3).
- Negociable y cedido a David: rutas absolutas, sin TASA_MATRICULA, distinct en df4.
- Egreso: usar los dos filtros juntos (el correo dice "promoción del año alumno regular" = SITUACION_EGRESO 1 en el libro de códigos B).
- Y = primera preferencia vs 2.ª–3.ª, con párrafo de justificación; PTJE_POND y PREFERENCIA no van como X.

## Próximo paso exacto
Que el grupo elija la versión (recomendada: consenso), complete los 4 nombres de la portada (hoy "Nombre 1…4") y entregue .tex/.pdf + script + `base_final_etapa1.csv`.

## Pendientes
- Correo al profesor para confirmar la Y (el mayor riesgo para la nota) y la fecha de entrega.
- Faltan "rural" y "alumnos por curso" (ejemplos del profesor; requieren base Mineduc, fuera del catálogo).
- Guardar en el PROYECTO (`datos/trabajos/econometria-ii/`) la versión final cuando el grupo cierre.
- Presentación del 15-10 (formato sin confirmar); Etapa 2 (dom 18-10) y Etapa 3 (dom 8-11) sin empezar.

## Leer primero (máx. 5 rutas, con rango de líneas o encabezado)
1. `trabajo/revision-05/07-base-consenso.R` — completo (~85 líneas)
2. `trabajo/econometria-ii-demre/informe/informe-etapa-1-consenso.tex` — §3.3–§4 (buscar "Filtros aplicados")
3. `C:\Proyecto Metodologia de estudio\datos\trabajos\econometria-ii\etapa-1-instrucciones-del-profesor.md` — L7-33 (correo)
