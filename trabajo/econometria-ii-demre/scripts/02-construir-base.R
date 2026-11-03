rm(list = ls())
graphics.off()
cat("\014")

getwd()

library(dplyr)

# los archivos del DEMRE vienen con ; y coma decimal
matricula <- read.csv2("datos/crudos/4-matricula/ArchivoMatr_Adm2026.csv")
inscritos <- read.csv2("datos/crudos/1-inscritos-archivo-B/ArchivoB_Adm2026REG.csv")
puntajes <- read.csv2("datos/crudos/2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv")
postulaciones <- read.csv2("datos/crudos/3-postulaciones-archivo-D/ArchivoD_Adm2026REG.csv")

# VIA: 1 regular, 2 BEA, 3 PACE, 4 +MC
table(matricula$VIA)
# TIPO_MATRICULA: 1 postulacion regular, 2 repostulacion, el resto son cupos especiales
table(matricula$TIPO_MATRICULA)
table(matricula$PREFERENCIA)
table(inscritos$ANYO_EGRESO)
# SITUACION_EGRESO: 1 es promocion del año alumno regular
table(inscritos$SITUACION_EGRESO)

# los de preferencia 0 no vienen de postulacion regular, se van solos con el filtro
table(matricula$PREFERENCIA, matricula$TIPO_MATRICULA)

# postulaciones trae una fila por preferencia, necesito una por persona
postulantes <- distinct(select(postulaciones, ID_aux))
nrow(postulantes)

inscritos_prom <- filter(inscritos, SITUACION_EGRESO == 1)
nrow(inscritos_prom)

# left_join deja a todos los postulantes, despues saco los que no son promocion del año
base <- left_join(postulantes, inscritos_prom, by = "ID_aux")
base <- filter(base, !is.na(SITUACION_EGRESO))
nrow(base)

# puntajes repite columnas del colegio que ya estan en inscritos, me quedo con las nuevas
puntajes_notas <- select(puntajes, ID_aux, PROMEDIO_NOTAS, PORC_SUP_NOTAS, PTJE_NEM, PTJE_RANKING,
                         CLEC_REG_ACTUAL, MATE1_REG_ACTUAL, MATE2_REG_ACTUAL,
                         HCSOC_REG_ACTUAL, CIEN_REG_ACTUAL)
base <- left_join(base, puntajes_notas, by = "ID_aux")

# los que no se matricularon quedan con NA en las columnas de matricula
base <- left_join(base, matricula, by = "ID_aux")
nrow(base)

table(base$VIA, useNA = "ifany")
table(base$PREFERENCIA, base$TIPO_MATRICULA, useNA = "ifany")

# quedan los no matriculados y los matriculados por via regular y postulacion regular
base <- filter(base, is.na(TIPO_MATRICULA) | (VIA == 1 & TIPO_MATRICULA == 1))
nrow(base)

# Y = 1 si se matriculo en una de sus 3 primeras preferencias
# MATRICULADO sirve para calcular las variables del colegio y despues filtrar
base <- mutate(base,
               Y = ifelse(!is.na(PREFERENCIA) & PREFERENCIA <= 3, 1, 0),
               MATRICULADO = ifelse(is.na(PREFERENCIA), 0, 1))
table(base$Y)
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

# estas columnas ya no separan a nadie despues de los filtros
table(base$ANYO_PROCESO, useNA = "ifany")
table(base$SITUACION_EGRESO, useNA = "ifany")
base <- select(base, -ANYO_PROCESO, -SITUACION_EGRESO, -VIA, -TIPO_MATRICULA, -MATRICULADO)

# los NA de REGIMEN vienen asi del DEMRE
colSums(is.na(base))
summary(base)

write.csv2(base, "datos/procesados/base-etapa-1.csv", row.names = FALSE)
