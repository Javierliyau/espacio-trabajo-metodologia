---
tema: econometria-ii
fecha: 2026-10-02 14:54
resumen: Etapa 1 del trabajo práctico (entrega dom 4-10): base final guardada (68.704 matriculados, 42 columnas) e informe LaTeX en borrador de 5 páginas; faltan nombres, revisión del grupo, correo al profesor y la presentación del jue 8-10.
---
## Objetivo
Etapa 1 del trabajo práctico grupal de Econometría II (Pfeng): base DEMRE 2026 en un solo data frame e informe en LaTeX. Entrega dom 4-10, presentación jue 8-10 (10 min). Regla del profesor: uso de IA = nota mínima; el usuario fue advertido y decidió seguir (no repetirlo).

## Hecho en esta sesión
- `trabajo/econometria-ii-demre/scripts/02-construir-base.R` (109 líneas): completo y verificado con Rscript. Agrega variables del colegio, variables del estudiante, filtro de matriculados, revisión de NA y guardado.
- `datos/procesados/base-etapa-1.csv`: 68.704 filas, 42 columnas, guardada con `write.csv2()` y releída sin problemas.
- `informe/informe-etapa-1.tex` y PDF (5 páginas, compila sin errores; no revisado visualmente): fuentes, pasos, tabla de filtros, Y, variables creadas, faltantes, tabla de definiciones.
- `LEEME.md`: sección «Base final» agregada.
- Borrador de correo al profesor y análisis de decisiones: quedaron solo en el chat anterior (ver Pendientes).

## Decisiones tomadas (no re-litigar)
- La base final es **solo de matriculados** (cambia la opción B del handoff anterior). Y = 1 si preferencia 1 a 3 (60.301), Y = 0 si preferencia 4 o más (8.403). 88 % de unos.
- Las variables del colegio se calculan con los 108.598 postulantes de la promoción, antes del filtro de matriculados.
- Variables creadas: `TAMANO_COLEGIO`, `PROM_NEM_COLEGIO`, `PROM_CLEC_COLEGIO`, `PROM_MATE1_COLEGIO`, `PORC_MATRICULADOS_COLEGIO`, `EDAD`, `ESTUDIA_OTRA_COMUNA`, `COLEGIO_TP`.
- Solo datos del DEMRE: el usuario descartó el cruce con el Mineduc.
- Guardado con `write.csv2()`. `group_by`, `summarise`, `rename`, `count`, `colSums` están en el catálogo (LPE clase 4 y 7).
- Código R según `C:\Users\javie\OneDrive\Documentos\mi-proyecto-r` (reglas del handoff 2026-10-02-1205, sección «Decisiones»). Si falta una función: preguntar.
- Explicaciones cortas y en palabras simples; el usuario lo pidió varias veces.

## Próximo paso exacto
Preguntar al usuario qué consulta tiene. Si no trae una, proponer la presentación del jue 8-10 (10 min) a partir del informe, preguntando antes si va en LaTeX (beamer) u otro formato.

## Pendientes
- Informe: poner los nombres del grupo (autor dice «INTEGRANTES DEL GRUPO») y revisión del grupo.
- Decidir faltantes: 6.183 NA en `REGIMEN` y 18.410 con código 99 en `INGRESO_PERCAPITA_GRUPO_FA`. Recomendado: categoría «sin dato». No aplicado.
- Correo al profesor: confirmar que la base es solo de matriculados con los de preferencia 4 o más como Y = 0, y si se adjunta base y código. No se sabe si se envió.
- `EDAD`: 136 matriculados de más de 25 años (educación de adultos); sin tocar.
- 1 estudiante sin puntajes PAES regulares; sin tocar.
- `ANYO_EGRESO` es constante (2025) y sigue en la base.
- RBD: parece ser el real (8485 y 8487 calzan con Instituto Nacional y Liceo 1), no comprobado contra el Mineduc.
- `scripts/01-leer-datos.R` está obsoleto; borrar solo si el usuario lo pide.
- No hay skill de Econometría II en `mi-proyecto-r`; preguntar si vieron funciones nuevas.
- Guardar en el PROYECTO (`datos/trabajos/econometria-ii/`) script, informe y descripción de la base cuando el grupo cierre la etapa.
- Etapa 2 (análisis descriptivo, entrega 18-10) y etapa 3 (logit, entrega 8-11): sin empezar.

## Leer primero (máx. 5 rutas, con rango de líneas o encabezado)
1. `trabajo/econometria-ii-demre/scripts/02-construir-base.R` — líneas 56-109
2. `trabajo/econometria-ii-demre/LEEME.md` — «Base final (2-10-2026)»
3. `trabajo/econometria-ii-demre/informe/informe-etapa-1.tex` — secciones «Variable de respuesta» y «Variables creadas» (líneas 78-123)
4. `C:\Proyecto Metodologia de estudio\datos\trabajos\econometria-ii\instrucciones-trabajo-practico.md` — completo (88 líneas)
