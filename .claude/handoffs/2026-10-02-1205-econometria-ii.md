---
tema: econometria-ii
fecha: 2026-10-02 12:05
resumen: Etapa 1 del trabajo práctico (entrega dom 4-10): base de postulantes construida hasta la Y (108.598 filas) en scripts/02-construir-base.R; faltan variables del colegio, revisión de NA, guardado e informe LaTeX.
---
## Objetivo
Etapa 1 del trabajo práctico grupal de Econometría II (Pfeng): construir la base DEMRE 2026 en un solo data frame e informe en LaTeX. Entrega dom 4-10, presentación jue 8-10 (10 min). Regla del profesor: uso de IA = nota mínima; el usuario fue advertido y pidió igual el script completo.

## Hecho en esta sesión
- Proyecto de trabajo en `C:\Espacio de trabajo Metodologia de estudio\trabajo\econometria-ii-demre\` (Rproj, `LEEME.md`, `datos/originales`, `datos/crudos` con 8 carpetas, `datos/procesados`, `scripts`, `informe`, `presentacion`).
- Los 9 `.rar` del DEMRE extraídos y descritos en `LEEME.md` (filas, llaves, separador `;`, coma decimal).
- `scripts/02-construir-base.R`: completo y verificado con Rscript desde la raíz. Lee B, C, D y matrícula; filtra; une; crea `Y` y `MATRICULADO`. Resultado: 108.598 filas, 39 columnas, una fila por `ID_aux`.
- `scripts/01-leer-datos.R` quedó obsoleto (4 líneas de lectura); se puede borrar si el usuario lo pide.

## Decisiones tomadas (no re-litigar)
- Opción B: la base son postulantes de la promoción del año (`SITUACION_EGRESO == 1`), no solo matriculados. Acordado por el grupo.
- Salen los 6.267 matriculados por vía o tipo no regular. Los 8.403 matriculados en preferencia 4 o más quedan con Y = 0. Los 39.894 no matriculados quedan con Y = 0.
- Y = 1 si se matriculó en preferencia 1 a 3 (60.301 unos, 48.297 ceros). `MATRICULADO` permite pasar a la opción A (68.704 filas) con un filtro.
- Puntajes PAES: solo columnas `REG_ACTUAL`.
- Código R según `C:\Users\javie\OneDrive\Documentos\mi-proyecto-r` (CLAUDE.md, `docs/reglas-restricciones.md`, skills `lenguaje-r-restringido` y `econometria-1`): `<-`, dplyr sin pipe nativo, comentarios cortos sin separadores, solo funciones del catálogo. `merge()` y `unique()` no están permitidas; sí `left_join`, `filter`, `select`, `mutate`, `distinct`, `count`. Si falta una función: detenerse y preguntar.
- Los datos se quedan en `econometria-ii-demre` (no moverlos a OneDrive) salvo que el usuario diga otra cosa: propuesto, sin respuesta.
- Archivos K y L no son vinculables; no se usan.
- Explicaciones cortas: el usuario pidió ir más rápido y documentos simples.

## Próximo paso exacto
Agregar al final de `scripts/02-construir-base.R` las variables del colegio (con `count(base, RBD)` y `left_join`: tamaño = postulantes por RBD; además promedios por colegio si `group_by`/`summarise` están en el catálogo), revisar NA y guardar la base en `datos/procesados/`. Antes, confirmar con el usuario qué variables creadas quiere el grupo.

## Pendientes
- Enviar al profesor la consulta: ¿incluir no matriculados o solo matriculados? (texto propuesto en el chat; no se sabe si se envió).
- RBD enmascarado (libro de códigos B): no comprobado si coincide con el RBD real; define si se puede cruzar con Mineduc para ruralidad y matrícula del colegio.
- Decidir qué hacer con: 168 con 0 en MATE1 (no rindieron), 9.978 NA en `REGIMEN`, 2 NA en PAES.
- Quitar columnas constantes (`VIA`, `TIPO_MATRICULA`, `SITUACION_EGRESO`, `ANYO_PROCESO`).
- Copiar del libro de códigos B los significados de `GRUPO_DEPENDENCIA`, `RAMA_EDUCACIONAL`, `COD_ENS`, `REGIMEN`, `INGRESO_PERCAPITA_GRUPO_FA` para la tabla de variables.
- Informe en LaTeX: fuentes, uniones, tabla de filtros (188.538 → 114.865 → 108.598), definición de Y, tabla de variables, justificación de la opción B con las frases del correo.
- Presentación del 8-10.
- No hay skill de Econometría II en `mi-proyecto-r`; preguntar si vieron funciones nuevas en clase.
- Guardar lo que valga en el PROYECTO (`datos/trabajos/econometria-ii/`) cuando la base esté lista.
- Pendientes anteriores: ver `C:\Proyecto Metodologia de estudio\.claude\handoffs\2026-10-01-2020-econometria-ii.md`, sección «Pendientes».

## Leer primero (máx. 5 rutas, con rango de líneas o encabezado)
1. `trabajo/econometria-ii-demre/scripts/02-construir-base.R` — completo (68 líneas)
2. `trabajo/econometria-ii-demre/LEEME.md` — «Archivos en datos/crudos» y «Dos advertencias»
3. `C:\Proyecto Metodologia de estudio\datos\trabajos\econometria-ii\etapa-1-instrucciones-del-profesor.md` — sección 1 (correo)
4. `C:\Users\javie\OneDrive\Documentos\mi-proyecto-r\docs\reglas-restricciones.md` — completo (35 líneas)
5. `C:\Users\javie\OneDrive\Documentos\mi-proyecto-r\.claude\skills\econometria-1\SKILL.md` — lista de funciones permitidas (líneas 60-90)
