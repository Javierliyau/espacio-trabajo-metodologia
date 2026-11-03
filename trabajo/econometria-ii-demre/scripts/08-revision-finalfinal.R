library(tidyverse)
rm(list = ls())
cat("\014")

df1 <- read_csv2("datos/crudos/1-inscritos-archivo-B/ArchivoB_Adm2026REG.csv")
df2 <- read_csv2("datos/crudos/2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv")
df3 <- read_csv2("datos/crudos/3-postulaciones-archivo-D/ArchivoD_Adm2026REG.csv")
df4 <- read_csv2("datos/crudos/4-matricula/ArchivoMatr_Adm2026.csv")



############## VARIABLES DEL COLEGIO #######################
colegio <- df1 %>%
  group_by(RBD) %>%
  summarise(N_ALUMNOS = n(),
            INGRESO_COLEGIO = mean(INGRESO_PERCAPITA_GRUPO_FA, na.rm = TRUE))
colegio


matricula<- df4 %>%
  filter(VIA==1 & TIPO_MATRICULA==1) %>%
  left_join(df1 %>% select(ID_aux, RBD), by = "ID_aux") %>%
  group_by(RBD) %>%
  summarise(N_MATRICULADOS = n())
matricula

colegio <- colegio %>%
  left_join(matricula, by = "RBD")
colegio$N_MATRICULADOS <- ifelse(is.na(colegio$N_MATRICULADOS), 0, colegio$N_MATRICULADOS)
colegio



############## FILTRAR DATOS #######################
df1 <- df1 %>%
  select(ID_aux,ANYO_EGRESO,FECHA_NACIMIENTO,RBD,RAMA_EDUCACIONAL,GRUPO_DEPENDENCIA,CODIGO_REGION,CODIGO_COMUNA,CODIGO_COMUNA_D,SEXO,PACE,BEA,INGRESO_PERCAPITA_GRUPO_FA,RINDIO_PROCESO_ACTUAL)%>%
  mutate(INGRESO_PERCAPITA_GRUPO_FA = na_if(INGRESO_PERCAPITA_GRUPO_FA, 99))

table(df1$INGRESO_PERCAPITA_GRUPO_FA, useNA = "ifany")

df2 <- df2%>%
  select(ID_aux,PROMEDIO_NOTAS,PTJE_NEM, PTJE_RANKING, CLEC_REG_ACTUAL,MATE1_REG_ACTUAL)
df2

df3 <- df3 %>%
  filter(TIPO_PREF == "REGULAR") %>%
  select(ID_aux, TIPO_PREF) %>%
  distinct(ID_aux, .keep_all = TRUE)
df3

df4 <- df4 %>%
  select(ID_aux, PREFERENCIA,VIA, PTJE_POND,TIPO_MATRICULA) %>%
  distinct(ID_aux, .keep_all = TRUE)
df4
 
lista_dfs <- list(df1, df2, df3,df4)

df_final <- lista_dfs %>% 
  reduce(full_join, by = "ID_aux")%>%
  filter(ANYO_EGRESO==2025)%>%
  filter(VIA==1 & TIPO_MATRICULA==1)%>%
  filter(RINDIO_PROCESO_ACTUAL==1)%>%
  filter(!is.na(PTJE_NEM), PTJE_NEM != 0)
df_final
df_final <- left_join(df_final, colegio, by = "RBD")
df_final

################ CREACION VARIABLES DUMMY ########################

df_final$PREF_PRIMERA_DUMMY <- ifelse(df_final$PREFERENCIA%in% c(1,2,3), 1, 0)
df_final$PREF_PRIMERA_DUMMY

df_final$TP_DUMMY <- ifelse(df_final$RAMA_EDUCACIONAL %in% c("T1","T2","T3","T4","T5"), 1, 0)
df_final$TP_DUMMY

table(df_final$PREFERENCIA)


cat("\n==== REVISION ====\n")
cat("dim df_final:", dim(df_final), "\n")
print(table(df_final$PREFERENCIA, useNA="ifany"))
print(table(df_final$PREF_PRIMERA_DUMMY, useNA="ifany"))
print(summary(df_final$INGRESO_COLEGIO))
print(summary(df_final$N_ALUMNOS)); print(summary(df_final$N_MATRICULADOS))
cat("ingreso alumno NA:", sum(is.na(df_final$INGRESO_PERCAPITA_GRUPO_FA)), "\n")
cat("RBD NA:", sum(is.na(df_final$RBD)), "\n")
print(table(df_final$TP_DUMMY, useNA="ifany"))
cat("ID unicos:", n_distinct(df_final$ID_aux), "\n")
cat("cols:", paste(names(df_final), collapse=","), "\n")
cat("nombres B con SITUACION:", grep("SITUACION|EGRESO", names(read_csv2("datos/crudos/1-inscritos-archivo-B/ArchivoB_Adm2026REG.csv", n_max=1, show_col_types=FALSE)), value=TRUE), "\n")
