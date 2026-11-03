---
tema: econometria-ii
fecha: 2026-10-07 13:48
resumen: Versión de consenso con David es la FINAL (script 07 + informe-etapa-1-consenso.tex, 60.300 × 34, explica los 244 excluidos); mensaje a David entregado; faltan nombres, CSV y confirmar la Y.
---
## Objetivo
Etapa 1 del trabajo práctico de Econometría II (prof. Brian Pfeng Ibacache). Entrega jue 8-10 (según correo de Jorge; en clase dijo dom 4-10, por confirmar). Presentación jue 15-10, máx. 10 min. Regla IA: no repetirla.

## Hecho en esta sesión
- **Versión final = consenso:** `trabajo/revision-05/07-base-consenso.R` + `trabajo/econometria-ii-demre/informe/informe-etapa-1-consenso.tex/.pdf` (9 págs., compila sin errores).
- Consenso: rutas absolutas de David, `ANYO_EGRESO==2025` + `SITUACION_EGRESO==1`, `distinct()` en df4 (no cambia filas), sin TASA_MATRICULA. Verificado: 60.300 × 34, Y 40.002 / 20.298, 0 RBD NA; idéntica a la base del script 06.
- Los 244 excluidos por SITUACION_EGRESO: 234 validación de estudios (código 2) + 10 extranjero (código 3), todos sin RBD (171 con Y=1). Ya explicado en el .tex, §3.3 filtro a).
- Otras versiones (respaldo): `06-base-david-corregido.R` + `informe-etapa-1-corregido.tex` (con TASA, rutas por nombre); `informe-etapa-1-david-limpio.tex` (original de David, 60.544, sin OJO).
- Mensaje final para David entregado en el chat (cedido: rutas, tasa, su filtro; defendidos: 99, sin RBD, TIPO_PREF_DUMMY, RINDIO 1-3, guardar base).
- Notas estimadas: original 4,5–5,0; consenso 5,5–6,0.

## Decisiones tomadas (no re-litigar)
- Se entrega la versión de consenso.
- Lo innegociable: guardar la base, sacar TIPO_PREF_DUMMY/df3, 99 fuera del promedio de ingreso, sin RBD fuera de las variables del colegio, RINDIO %in% c(1,3).
- Egreso: los dos filtros juntos ("promoción del año alumno regular" = SITUACION_EGRESO 1 en el libro de códigos B).
- Y = primera preferencia vs 2.ª–3.ª, con justificación; PTJE_POND y PREFERENCIA no van como X.

## Próximo paso exacto
Esperar la respuesta de David al mensaje. Si acepta: que corra el 07 en su computador para generar `base_final_etapa1.csv`, completar los 4 nombres (portada, líneas de `Integrantes`) y entregar .tex/.pdf + script + CSV.

## Pendientes
- Correo al profesor para confirmar la Y y la fecha de entrega.
- Faltan "rural" y "alumnos por curso" (ejemplos del profesor; requieren base Mineduc, fuera del catálogo LPE).
- Guardar en el PROYECTO (`datos/trabajos/econometria-ii/`) la versión final cuando se entregue.
- Presentación del 15-10 (formato sin confirmar); Etapa 2 (dom 18-10) y Etapa 3 (dom 8-11) sin empezar.

## Leer primero (máx. 5 rutas, con rango de líneas o encabezado)
1. `trabajo/revision-05/07-base-consenso.R` — completo (~85 líneas)
2. `trabajo/econometria-ii-demre/informe/informe-etapa-1-consenso.tex` — §3.3 «Filtros aplicados» a §4
3. `C:\Proyecto Metodologia de estudio\datos\trabajos\econometria-ii\etapa-1-instrucciones-del-profesor.md` — L7-33 (correo)
