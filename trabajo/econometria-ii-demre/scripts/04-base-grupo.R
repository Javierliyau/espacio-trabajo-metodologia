############## TRABAJO PRACTICO ECONOMETRIA II - ETAPA 1 #######################
# Base de datos de matriculados, proceso de admision 2026
# Fuente: DEMRE, https://demre.cl/portales/portal-bases-datos
# Integrantes:

library(tidyverse)
rm(list = ls())
cat("\014")

# abrir econometria-ii-demre.Rproj para que las rutas funcionen en cualquier computador
df1 <- read_csv2("datos/crudos/1-inscritos-archivo-B/ArchivoB_Adm2026REG.csv")
df2 <- read_csv2("datos/crudos/2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv")
df3 <- read_csv2("datos/crudos/3-postulaciones-archivo-D/ArchivoD_Adm2026REG.csv")
df4 <- read_csv2("datos/crudos/4-matricula/ArchivoMatr_Adm2026.csv")



############## SELECCIONAR COLUMNAS #######################

# df1: datos del estudiante y de su colegio
# RBD es el codigo del colegio y SITUACION_EGRESO es para el filtro
# RAMA_EDUCACIONAL, FECHA_NACIMIENTO, ANYO_EGRESO y las comunas son para crear variables
df1 <- df1 %>%
  select(ID_aux, RBD, SITUACION_EGRESO, CODIGO_REGION, SEXO, INGRESO_PERCAPITA_GRUPO_FA,
         GRUPO_DEPENDENCIA, REGIMEN, RAMA_EDUCACIONAL, FECHA_NACIMIENTO, ANYO_EGRESO,
         CODIGO_COMUNA, CODIGO_COMUNA_D)
df1

# df2: notas de enseñanza media y puntajes PAES
df2 <- df2 %>%
  select(ID_aux, PROMEDIO_NOTAS, PORC_SUP_NOTAS, PTJE_NEM, PTJE_RANKING,
         CLEC_REG_ACTUAL, MATE1_REG_ACTUAL)
df2

# df3: carreras a las que postulo cada estudiante
df3 <- df3 %>%
  select(ID_aux, ORDEN_PREF, TIPO_PREF, PTJE_PREF)
df3

# df4: matricula. PREFERENCIA es para la Y, VIA y TIPO_MATRICULA son para el filtro
df4 <- df4 %>%
  select(ID_aux, VIA, TIPO_MATRICULA, PREFERENCIA, PTJE_POND)
df4



############## FILTRAR DATOS #######################

# SITUACION_EGRESO 1 es promocion del año, alumno regular
table(df1$SITUACION_EGRESO)
df1 <- df1 %>%
  filter(SITUACION_EGRESO == 1)

# la misma carrera aparece repetida si ademas se postula por BEA, PACE o GENERO
table(df3$TIPO_PREF)
df3 <- df3 %>%
  filter(TIPO_PREF == "REGULAR")

# df3 trae una fila por carrera postulada, lo dejo en una fila por estudiante
df3 <- df3 %>%
  count(ID_aux) %>%
  rename(N_POSTULACIONES = n)
df3



############## UNIR LOS ARCHIVOS #######################

# parto de los postulantes (df3) para que quede una fila por estudiante
lista_dfs <- list(df3, df1, df2, df4)

df_final <- lista_dfs %>%
  reduce(left_join, by = "ID_aux")
nrow(df_final)

# los que no son promocion del año quedaron con NA en las columnas de df1
df_final <- df_final %>%
  filter(!is.na(SITUACION_EGRESO))
nrow(df_final)

# VIA 1 es regular y TIPO_MATRICULA 1 es postulacion regular
# los no matriculados (NA) se quedan por ahora para calcular las variables del colegio
table(df_final$VIA, df_final$TIPO_MATRICULA, useNA = "ifany")
df_final <- df_final %>%
  filter(is.na(TIPO_MATRICULA) | (VIA == 1 & TIPO_MATRICULA == 1))
nrow(df_final)

# reviso que haya una fila por estudiante
n_distinct(df_final$ID_aux)



################ VARIABLE DE RESPUESTA ########################

# Y = 1 si se matriculo en una de sus 3 primeras preferencias
# Y = 0 si se matriculo en la cuarta preferencia o en una posterior
df_final$Y <- ifelse(!is.na(df_final$PREFERENCIA) & df_final$PREFERENCIA <= 3, 1, 0)
df_final$MATRICULADO <- ifelse(is.na(df_final$PREFERENCIA), 0, 1)
table(df_final$MATRICULADO, df_final$Y)



################ VARIABLES DEL COLEGIO ########################

# se calculan con todos los postulantes de la promocion que salieron del mismo colegio
# un 0 en puntaje es que no rindio o no tiene notas, no entra en el promedio
colegios <- df_final %>%
  group_by(RBD) %>%
  summarise(TAMANO_COLEGIO = n(),
            PROM_NEM_COLEGIO = mean(PTJE_NEM[PTJE_NEM > 0], na.rm = TRUE),
            PROM_CLEC_COLEGIO = mean(CLEC_REG_ACTUAL[CLEC_REG_ACTUAL > 0], na.rm = TRUE),
            PROM_MATE1_COLEGIO = mean(MATE1_REG_ACTUAL[MATE1_REG_ACTUAL > 0], na.rm = TRUE),
            PORC_MATRICULADOS_COLEGIO = mean(MATRICULADO) * 100)
summary(colegios)

df_final <- df_final %>%
  left_join(colegios, by = "RBD")
nrow(df_final)



################ CREACION DE VARIABLES DUMMY ########################

# 1 si el colegio es tecnico profesional (T1 a T5), 0 si es humanista cientifico (H1 a H4)
df_final$COLEGIO_TP <- ifelse(df_final$RAMA_EDUCACIONAL %in% c("H1", "H2", "H3", "H4"), 0, 1)
table(df_final$RAMA_EDUCACIONAL, df_final$COLEGIO_TP, useNA = "ifany")

# 1 si la comuna del colegio es distinta de la comuna donde vive
df_final$ESTUDIA_OTRA_COMUNA <- ifelse(df_final$CODIGO_COMUNA != df_final$CODIGO_COMUNA_D, 1, 0)
table(df_final$ESTUDIA_OTRA_COMUNA, useNA = "ifany")

# FECHA_NACIMIENTO viene como texto con mes y año pegados, el resto de dividir por 10000 es el año
# EDAD es la que cumple el año que egreso
df_final$EDAD <- df_final$ANYO_EGRESO - as.numeric(df_final$FECHA_NACIMIENTO) %% 10000
summary(df_final$EDAD)



################ BASE FINAL ########################

# la base final es solo de matriculados
df_final <- df_final %>%
  filter(MATRICULADO == 1)
nrow(df_final)

df_final <- df_final %>%
  drop_na(PROMEDIO_NOTAS, PTJE_NEM, PTJE_RANKING, CLEC_REG_ACTUAL, MATE1_REG_ACTUAL, PTJE_POND)

df_final <- df_final %>%
  filter(PTJE_NEM != 0)
nrow(df_final)

# REGIMEN viene sin dato para algunos colegios, los dejo como categoria 0
table(df_final$REGIMEN, useNA = "ifany")
df_final$REGIMEN <- ifelse(is.na(df_final$REGIMEN), 0, df_final$REGIMEN)
table(df_final$REGIMEN, useNA = "ifany")

# en INGRESO_PERCAPITA_GRUPO_FA el 99 es prefiero no responder, se deja como categoria
table(df_final$INGRESO_PERCAPITA_GRUPO_FA, useNA = "ifany")

# dejo solo las columnas de la base, ordenadas: llaves, respuesta, estudiante, notas, colegio
df_final <- df_final %>%
  select(ID_aux, RBD, Y, PREFERENCIA, PTJE_POND, N_POSTULACIONES,
         SEXO, EDAD, INGRESO_PERCAPITA_GRUPO_FA, ESTUDIA_OTRA_COMUNA,
         PROMEDIO_NOTAS, PORC_SUP_NOTAS, PTJE_NEM, PTJE_RANKING,
         CLEC_REG_ACTUAL, MATE1_REG_ACTUAL,
         CODIGO_REGION, GRUPO_DEPENDENCIA, REGIMEN, COLEGIO_TP,
         TAMANO_COLEGIO, PROM_NEM_COLEGIO, PROM_CLEC_COLEGIO, PROM_MATE1_COLEGIO,
         PORC_MATRICULADOS_COLEGIO)

# revision final: una fila por estudiante, sin faltantes
nrow(df_final)
n_distinct(df_final$ID_aux)
table(df_final$Y)
colSums(is.na(df_final))
summary(df_final)
df_final

write_csv2(df_final, "datos/procesados/base-etapa-1-grupo.csv")
