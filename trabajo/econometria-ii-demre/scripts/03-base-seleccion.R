rm(list = ls())
graphics.off()
cat("\014")

getwd()

library(dplyr)

# los archivos del DEMRE vienen con ; y coma decimal
inscritos <- read.csv2("datos/crudos/1-inscritos-archivo-B/ArchivoB_Adm2026REG.csv")
puntajes <- read.csv2("datos/crudos/2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv")
postulaciones <- read.csv2("datos/crudos/3-postulaciones-archivo-D/ArchivoD_Adm2026REG.csv")
matricula <- read.csv2("datos/crudos/4-matricula/ArchivoMatr_Adm2026.csv")

# lo que elegimos de cada archivo, mas lo que se necesita para filtrar y crear variables
# RBD, SITUACION_EGRESO, RAMA_EDUCACIONAL, fecha, año y comunas son de apoyo
inscritos <- select(inscritos, ID_aux, RBD, SITUACION_EGRESO, CODIGO_REGION, SEXO,
                    INGRESO_PERCAPITA_GRUPO_FA, GRUPO_DEPENDENCIA, REGIMEN,
                    RAMA_EDUCACIONAL, FECHA_NACIMIENTO, ANYO_EGRESO,
                    CODIGO_COMUNA, CODIGO_COMUNA_D)

puntajes <- select(puntajes, ID_aux, PROMEDIO_NOTAS, PORC_SUP_NOTAS, PTJE_NEM, PTJE_RANKING,
                   CLEC_REG_ACTUAL, MATE1_REG_ACTUAL)

postulaciones <- select(postulaciones, ID_aux, COD_CARRERA_PREF, ORDEN_PREF, TIPO_PREF, PTJE_PREF)

# PREFERENCIA es para la Y, TIPO_MATRICULA para el filtro, CODIGO para unir con postulaciones
matricula <- select(matricula, ID_aux, CODIGO, VIA, TIPO_MATRICULA, PREFERENCIA, PTJE_POND)

# SITUACION_EGRESO: 1 es promocion del año alumno regular
table(inscritos$SITUACION_EGRESO)
inscritos <- filter(inscritos, SITUACION_EGRESO == 1)
nrow(inscritos)

# TIPO_PREF: la misma carrera se repite si ademas postula por BEA, PACE o GENERO
table(postulaciones$TIPO_PREF)
postulaciones <- filter(postulaciones, TIPO_PREF == "REGULAR")

# postulaciones trae una fila por preferencia, necesito una por persona
n_postulaciones <- count(postulaciones, ID_aux)
n_postulaciones <- rename(n_postulaciones, N_POSTULACIONES = n)
summary(n_postulaciones$N_POSTULACIONES)

# left_join deja a todos los postulantes, despues saco los que no son promocion del año
base <- left_join(n_postulaciones, inscritos, by = "ID_aux")
base <- filter(base, !is.na(SITUACION_EGRESO))
nrow(base)

base <- left_join(base, puntajes, by = "ID_aux")

# los que no se matricularon quedan con NA en las columnas de matricula
base <- left_join(base, matricula, by = "ID_aux")
nrow(base)

# VIA: 1 regular. TIPO_MATRICULA: 1 postulacion regular
table(base$VIA, base$TIPO_MATRICULA, useNA = "ifany")
base <- filter(base, is.na(TIPO_MATRICULA) | (VIA == 1 & TIPO_MATRICULA == 1))
nrow(base)

# Y = 1 si se matriculo en una de sus 3 primeras preferencias
# MATRICULADO sirve para calcular las variables del colegio y despues filtrar
base <- mutate(base,
               Y = ifelse(!is.na(PREFERENCIA) & PREFERENCIA <= 3, 1, 0),
               MATRICULADO = ifelse(is.na(PREFERENCIA), 0, 1))
table(base$MATRICULADO, base$Y)

# reviso que haya una fila por estudiante
nrow(distinct(select(base, ID_aux)))

# tamaño del colegio: postulantes de la promocion que salieron del mismo RBD
tamano <- count(base, RBD)
tamano <- rename(tamano, TAMANO_COLEGIO = n)
summary(tamano$TAMANO_COLEGIO)

# un 0 en puntaje es que no rindio o no tiene notas, lo saco del promedio del colegio
colegios <- summarise(group_by(base, RBD),
                      PROM_NEM_COLEGIO = mean(PTJE_NEM[PTJE_NEM > 0], na.rm = TRUE),
                      PROM_CLEC_COLEGIO = mean(CLEC_REG_ACTUAL[CLEC_REG_ACTUAL > 0], na.rm = TRUE),
                      PROM_MATE1_COLEGIO = mean(MATE1_REG_ACTUAL[MATE1_REG_ACTUAL > 0], na.rm = TRUE),
                      PORC_MATRICULADOS_COLEGIO = mean(MATRICULADO) * 100)
summary(colegios)

base <- left_join(base, tamano, by = "RBD")
base <- left_join(base, colegios, by = "RBD")
nrow(base)

# FECHA_NACIMIENTO viene como mes y año pegados, el resto de dividir por 10000 es el año
# EDAD es la que cumple el año que egreso
base <- mutate(base,
               EDAD = ANYO_EGRESO - FECHA_NACIMIENTO %% 10000,
               ESTUDIA_OTRA_COMUNA = ifelse(CODIGO_COMUNA != CODIGO_COMUNA_D, 1, 0),
               COLEGIO_TP = ifelse(RAMA_EDUCACIONAL == "H1" | RAMA_EDUCACIONAL == "H2" |
                                     RAMA_EDUCACIONAL == "H3" | RAMA_EDUCACIONAL == "H4", 0, 1))
summary(base$EDAD)
table(base$ESTUDIA_OTRA_COMUNA, useNA = "ifany")
table(base$RAMA_EDUCACIONAL, base$COLEGIO_TP, useNA = "ifany")

# la base final es solo de matriculados, los demas sirvieron para las variables del colegio
base <- filter(base, MATRICULADO == 1)
nrow(base)
table(base$Y)

# de postulaciones traigo la fila de la carrera donde se matriculo
postulaciones <- rename(postulaciones, CODIGO = COD_CARRERA_PREF)
base <- left_join(base, postulaciones, by = c("ID_aux", "CODIGO"))
nrow(base)

# ORDEN_PREF tiene que ser igual a PREFERENCIA y PTJE_PREF igual a PTJE_POND
table(base$ORDEN_PREF == base$PREFERENCIA, useNA = "ifany")
table(base$PTJE_PREF == base$PTJE_POND, useNA = "ifany")
table(base$TIPO_PREF, useNA = "ifany")
table(base$VIA, useNA = "ifany")

# saco las columnas de apoyo que ya no separan a nadie o ya se usaron
base <- select(base, -SITUACION_EGRESO, -TIPO_MATRICULA, -MATRICULADO, -CODIGO,
               -RAMA_EDUCACIONAL, -FECHA_NACIMIENTO, -ANYO_EGRESO,
               -CODIGO_COMUNA, -CODIGO_COMUNA_D)

# los NA de REGIMEN vienen asi del DEMRE
colSums(is.na(base))
summary(base)

write.csv2(base, "datos/procesados/base-etapa-1-seleccion.csv", row.names = FALSE)
