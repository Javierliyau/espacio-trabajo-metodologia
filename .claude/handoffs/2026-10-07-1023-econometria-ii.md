---
tema: econometria-ii
fecha: 2026-10-07 10:23
resumen: Revisión del script de David (05-base-david.R) e informe PDF del grupo; script corregido solo con funciones del catálogo LPE, verificado (60.300 × 34); lista de cambios obligatorios/opcionales entregada.
---
## Objetivo
Etapa 1 del trabajo práctico de Econometría II (Pfeng). Entrega **jue 8-10** (informe LaTeX + script R + base final; según correo de Jorge Riquelme, segunda mano). Presentación jue 15-10. Regla IA: el usuario ya fue advertido, no repetirlo.

## Hecho en esta sesión
- Revisado `C:\Users\javie\Downloads\05-base-david.R` y `C:\Users\javie\Downloads\Trabajo_econometriII.pdf` (texto extraído en `.claude/ctx/pdf/trabajo-econometriii.md`). Corrido con datos reales: reproduce 60.544 filas, Y 40.173/20.371.
- Errores confirmados: ANYO_EGRESO deja 244 de validación/extranjero (sin RBD); left_join une RBD NA → "colegio" de 3.169 alumnos; INGRESO_COLEGIO promedia el 99 (máx. 94); TIPO_PREF_DUMMY aleatoria (25 % con >1 tipo); RINDIO==1 = "solo regular" (3 = ambas); no guarda la base; rutas absolutas; portada con marcadores.
- Script corregido `trabajo/revision-05/05-base-final.R` (estilo de David, rutas `datos/…`), verificado vía `prueba.R`: N por paso 317.700 → 218.066 → 68.704 → 68.703 → 60.300; 34 col.; Y 40.002 / 20.298 (pref 2 = 13.270, pref 3 = 7.028); 0 RBD NA.
- Valores nuevos para el informe: N_ALUMNOS 3/85/106,1/586; INGRESO_COLEGIO 1,0/4,8/5,2/10,0 (27 NA); N_MATRICULADOS 1/33/41,8/218; TASA_MATRICULA 0,01/0,40/0,41/0,96; PACE 5.162; BEA 6.739; MUJER 31.845 (52,8 %); INGRESO_NR 16.175; TP 9.110; dependencia 11.587/32.273/11.482/4.958; 3.108 colegios.
- Notas estimadas: como está 4,5–5,0; con obligatorios 5,0–5,5; con todo 5,5–6,0.

## Decisiones tomadas (no re-litigar)
- **Solo funciones del catálogo LPE** (`C:\Users\javie\OneDrive\Documentos\mi-proyecto-r\.claude\skills\lenguaje-r-restringido\reference\`); si no hay función, no se hace el cambio. Se conservan las que ya usaba David (tidyverse, read_csv2, full_join, left_join, reduce).
- `write_csv2` se acepta: `readr` habilitado en LPE clase 3 para leer/escribir.
- Eliminados por no estar en catálogo: EDAD (str_sub), inner_join (→ left_join + filter), Parte C Mineduc (rural, alumnos por curso).
- Y del grupo se mantiene (pref 1 vs 2–3) con párrafo de justificación; PTJE_POND no va como X.
- Obligatorios: guardar base, SITUACION_EGRESO==1, ingreso 99 + RBD NA en colegio, sacar TIPO_PREF_DUMMY/df3, rutas relativas, actualizar números del informe, definición RINDIO, portada, párrafo Y + nota PTJE_POND. Resto opcional.

## Próximo paso exacto
Esperar que el grupo aplique los cambios en su script e informe `.tex`; si el usuario pasa el `.tex`, comparar cada número con la base (60.300 × 34) antes de entregar.

## Pendientes
- Presentación del 15-10 (formato sin confirmar: Beamer u otro).
- Confirmar con el profesor la definición de la Y (riesgo principal del criterio d).
- Guardar en el PROYECTO (`datos/trabajos/econometria-ii/`) script, informe y descripción cuando el grupo cierre.
- Etapa 2 (descriptivo, dom 18-10) y 3 (logit, dom 8-11): sin empezar.

## Leer primero (máx. 5 rutas, con rango de líneas o encabezado)
1. `trabajo/revision-05/05-base-final.R` — completo (~95 líneas)
2. `C:\Users\javie\Downloads\05-base-david.R` — completo (79 líneas, original)
3. `.claude/ctx/pdf/trabajo-econometriii.md` — L57-413 (informe del grupo, §3–§8)
4. `C:\Proyecto Metodologia de estudio\datos\trabajos\econometria-ii\etapa-1-instrucciones-del-profesor.md` — §1 Correo
5. `C:\Users\javie\OneDrive\Documentos\mi-proyecto-r\.claude\skills\lenguaje-r-restringido\SKILL.md` — «Referencia por clase» (L350+)
