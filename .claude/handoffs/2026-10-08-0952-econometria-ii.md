---
tema: econometria-ii
fecha: 2026-10-08 09:52
resumen: Informe LaTeX de la Etapa 1 alineado con el R y el Excel finales de David; falta confirmar la entrega, guardar la versión final y preparar la presentación del 15-10.
---
## Objetivo
Etapa 1 del trabajo de Econometría II (prof. Brian Pfeng Ibacache). Entrega: hoy, jue 08-10 (informe LaTeX, script R y base final). Presentación: jue 15-10 a las 08:15.

## Hecho en esta sesión
- `trabajo/econometria-ii-demre/informe/informe-etapa-1-final.tex/.pdf` (7 páginas) quedó alineado con `econometria.IIfinal.R` (David, 18:14) y con el Excel final.
- Se verificó contra el Excel: 29 variables en §7; tabla de §8; faltantes de §6; TP_DUMMY 9.110/51.434; 3.108 colegios; 188.538 estudiantes en el archivo D; 31.981 mujeres.
- Cambios respecto de Overleaf (`Trabajo_econometriII-5.pdf`):
  - Se pasa de 30 a 29 variables y se elimina TIPO_PREF_DUMMY.
  - §3.2 menciona el filtro REGULAR.
  - §3.3 tiene los 4 filtros (a–d) en el orden del R.
  - §3.4 ya no repite la fila de 60.544.
  - §5.1 corrige N_ALUMNOS y N_MATRICULADOS, explica el 99 en INGRESO_COLEGIO y explica el colegio fantasma de los 244 sin RBD.
  - §6 agrega una nota sobre los 244.
  - En §7, FECHA_NACIMIENTO aparece como numérica y PTJE_POND queda excluido.
  - §9 tiene una conclusión de 4 oraciones.
- Respaldos: `informe-etapa-1-david-entrega.tex` y `informe-etapa-1-consenso.tex`.

## Decisiones tomadas (no re-litigar)
- El R (`econometria.IIfinal.R`) y el Excel de David se entregan tal cual. Solo se corrigió el LaTeX.
- `econometria.II.R` (16:33) es la versión antigua y no se entrega.
- Los problemas de la base se documentan en el informe sin corregirse:
  - el 99 entra en el promedio de INGRESO_COLEGIO;
  - los 244 sin RBD quedan asignados a un colegio fantasma;
  - falta el filtro SITUACION_EGRESO.
- Nota estimada: 5,4 a 5,8.
- Y = PREF_PRIMERA_DUMMY: 40.173 (66,4 %) frente a 20.371 (13.322 en 2.ª y 7.049 en 3.ª preferencia). La base tiene 60.544 × 29.

## Próximo paso exacto
Preguntarle al usuario si la Etapa 1 ya se subió. Si se subió:
1. copiar el .tex, el .pdf y el R final a `C:/Proyecto Metodologia de estudio/datos/trabajos/econometria-ii/`;
2. marcar la entrega en `datos/agenda/calendario.md` y en `datos/agenda/semanas/2026-10-05.md`;
3. registrarla con `AG anotar`.

## Pendientes
- Etapa 2, según el comentario del evaluador:
  - calcular INGRESO_COLEGIO como mediana del tramo, con el 99 pasado a NA (`median(TRAMO, na.rm=TRUE)`, agrupado por RBD);
  - usar el tramo de ingreso como factor en el logit;
  - se ofreció redactar un mensaje al grupo con estos cambios.
- Arreglar en la Etapa 2 los 244 sin RBD (NA y no colegio fantasma) y agregar el filtro SITUACION_EGRESO.
- Preparar la presentación del 15-10 (slides y reparto con el grupo).

## Leer primero
1. `trabajo/econometria-ii-demre/informe/informe-etapa-1-final.tex`: §5.1 (variables del establecimiento), §6, §7 y §9 «Conclusión» (línea 398)
2. `C:/Proyecto Metodologia de estudio/datos/programas/econometria-ii-protocolo-chat.md`
3. `C:/Proyecto Metodologia de estudio/datos/agenda/semanas/2026-10-05.md`: jue 08-10
4. `C:/Proyecto Metodologia de estudio/datos/agenda/calendario.md`: Econometría II
5. Carpeta Descargas: `econometria.IIfinal.R` (no `econometria.II.R`)
