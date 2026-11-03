# Econometría II: trabajo práctico, etapa 1 (base DEMRE 2026)

Carpeta de trabajo del grupo. La organización es una propuesta, no una instrucción del profesor.

Fuente de todos los datos: portal de bases de datos del DEMRE, proceso de admisión 2026 (https://demre.cl/portales/portal-bases-datos). Bajados el 1 de octubre de 2026.

## Carpetas

| Carpeta | Qué va |
|---|---|
| `datos/originales/` | Los 9 `.rar` tal como se bajaron. No se tocan. |
| `datos/crudos/` | Los archivos extraídos, una carpeta por archivo, cada uno con su libro de códigos. No se editan. |
| `datos/procesados/` | La base final que construya el grupo. |
| `scripts/` | El código R del grupo. |
| `informe/` | El informe en LaTeX. |
| `presentacion/` | La presentación del 8 de octubre. |

Abrir `econometria-ii-demre.Rproj` en RStudio para que las rutas sean relativas a esta carpeta (por ejemplo `datos/crudos/4-matricula/ArchivoMatr_Adm2026.csv`).

## Archivos en `datos/crudos/`

Todos los CSV usan `;` como separador y coma decimal. Todos están en UTF-8, salvo la oferta académica, que está en Latin-1.

| Carpeta | Archivo | Filas | Una fila es | Llave | Variables principales |
|---|---|---|---|---|---|
| `1-inscritos-archivo-B` | `ArchivoB_Adm2026REG.csv` | 317.700 | un inscrito | `ID_aux` (única) | RBD, dependencia, rama, año de egreso, situación de egreso, región y comuna, sexo, ingreso per cápita, BEA, PACE |
| `2-rinden-paes-archivo-C` | `ArchivoC_Adm2026REG.csv` | 317.700 | un inscrito | `ID_aux` (única) | promedio de notas, NEM, ranking, puntajes PAES (regular e invierno, proceso actual y anterior) |
| `3-postulaciones-archivo-D` | `ArchivoD_Adm2026REG.csv` | 1.686.689 | una preferencia de un postulante | `ID_aux` + `ORDEN_PREF` | carrera, estado de la preferencia, tipo, puntaje ponderado. Hay 188.538 postulantes |
| `4-matricula` | `ArchivoMatr_Adm2026.csv` | 128.345 | un matriculado | `ID_aux` (única) | universidad, carrera, vía, preferencia, puntaje ponderado, tipo de matrícula |
| `5-cuestionario-archivos-K-L` | `ArchivoK_ADM2026.csv`, `ArchivoL_ADM2026.csv` | 119.827 y 111.758 | un matriculado | `ID` propio | cuestionario de caracterización |
| `6-oferta-academica` | `OfertaAcadémica_Admisión2026.csv` | 2.150 | una carrera | `CODIGO_CARRERA` | universidad, ponderaciones, vacantes, puntajes mínimos |
| `7-estadisticas-seleccion` | `ADM2026_INDICADORES_POR_CARRERA_...csv` | 2.150 | una carrera | `CODIGO_CARRERA` | área, vacantes, seleccionados, distribución de puntajes |
| `8-percentiles` | dos archivos | 101 | un percentil | `Percentil` | puntaje de cada prueba por percentil (regular e invierno) |

## Dos advertencias que salen de los libros de códigos

1. **Los archivos K y L no se pueden unir con nada.** El documento explicativo del DEMRE dice que no son vinculables entre sí ni con las otras bases del portal. No sirven para el data frame único.
2. **El RBD viene enmascarado.** El libro de códigos del archivo B lo describe como «RBD enmascarado del establecimiento de egreso». Antes de planear un cruce con datos del Mineduc por RBD, comprobar si el código coincide con el RBD real.

## Cómo se conectan los archivos

- B, C, D y matrícula se unen por `ID_aux`.
- La carrera (`CODIGO` en matrícula, `COD_CARRERA_PREF` en D) se une con la oferta académica y con las estadísticas por `CODIGO_CARRERA`.

## Base final (2-10-2026)

- `scripts/02-construir-base.R` parte de `datos/crudos/` y guarda `datos/procesados/base-etapa-1.csv` con `write.csv2()`.
- 68.704 filas (una por estudiante matriculado) y 42 columnas. `Y` = 1 en 60.301 (preferencia 1 a 3) y 0 en 8.403 (preferencia 4 o posterior).
- Las variables del colegio se calculan con los 108.598 postulantes de la promoción, antes de dejar solo a los matriculados.
- Informe: `informe/informe-etapa-1.tex` y su PDF (5 páginas).
