library(tidyverse)
rm(list = ls())
cat("\014")

df1 <- read_csv2("datos/crudos/1-inscritos-archivo-B/ArchivoB_Adm2026REG.csv")
df2 <- read_csv2("datos/crudos/2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv")
df3 <- read_csv2("datos/crudos/3-postulaciones-archivo-D/ArchivoD_Adm2026REG.csv")
df4 <- read_csv2("datos/crudos/4-matricula/ArchivoMatr_Adm2026.csv")

# El 99 es "prefiero no responder": se pasa a NA apenas se lee df1,
# antes de cualquier group_by(RBD)
df1 <- df1 %>%
  mutate(INGRESO_PERCAPITA_GRUPO_FA = na_if(INGRESO_PERCAPITA_GRUPO_FA, 99))
table(df1$INGRESO_PERCAPITA_GRUPO_FA, useNA = "ifany")



############## VARIABLES DEL COLEGIO #######################
# Se sacan los alumnos sin RBD para que no formen un "colegio" NA;
# al pegar las variables quedan con NA.
# Mediana y no promedio: los tramos de ingreso son ordinales y desiguales.
colegio <- df1 %>%
  filter(!is.na(RBD)) %>%
  group_by(RBD) %>%
  summarise(N_ALUMNOS = n(),
            INGRESO_COLEGIO = median(INGRESO_PERCAPITA_GRUPO_FA, na.rm = TRUE))
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
  select(ID_aux,ANYO_EGRESO,SITUACION_EGRESO,FECHA_NACIMIENTO,RBD,RAMA_EDUCACIONAL,GRUPO_DEPENDENCIA,CODIGO_REGION,CODIGO_COMUNA,CODIGO_COMUNA_D,SEXO,PACE,BEA,INGRESO_PERCAPITA_GRUPO_FA,RINDIO_PROCESO_ACTUAL)
df1

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
  filter(SITUACION_EGRESO==1)%>%          # promocion del año, alumno regular (libro de codigos B)
  filter(VIA==1 & TIPO_MATRICULA==1)%>%
  filter(RINDIO_PROCESO_ACTUAL==1)%>%
  filter(!is.na(PTJE_NEM), PTJE_NEM != 0)
df_final
df_final <- left_join(df_final, colegio, by = "RBD")
df_final

################ CREACION VARIABLES DUMMY ########################

# Y (segun el profesor): 1 si se matriculo en una de sus 3 primeras preferencias,
# 0 si quedo en la 4a o mas abajo
df_final$PREF_TOP3_DUMMY <- ifelse(df_final$PREFERENCIA %in% c(1,2,3), 1, 0)
table(df_final$PREF_TOP3_DUMMY)

# Sin RBD no se conoce la rama: queda NA y no 0
df_final$TP_DUMMY <- ifelse(is.na(df_final$RAMA_EDUCACIONAL), NA,
                            ifelse(df_final$RAMA_EDUCACIONAL %in% c("T1","T2","T3","T4","T5"), 1, 0))
table(df_final$TP_DUMMY, useNA = "ifany")

# PACE y BEA vienen como texto o NA; NA significa "no preseleccionado", no dato faltante
df_final$PACE <- ifelse(is.na(df_final$PACE), 0, 1)
df_final$BEA  <- ifelse(is.na(df_final$BEA), 0, 1)
table(df_final$PACE)
table(df_final$BEA)

table(df_final$PREFERENCIA)
summary(df_final)

cat("\n==== REVISION ====\n")
cat("dim:", dim(df_final), " ID unicos:", n_distinct(df_final$ID_aux), "\n")
print(table(df_final$PREF_TOP3_DUMMY)); print(prop.table(table(df_final$PREF_TOP3_DUMMY)))
print(table(df_final$PREFERENCIA, useNA="ifany"))
print(summary(df_final$INGRESO_COLEGIO)); cat("max N_ALUMNOS:", max(df_final$N_ALUMNOS), " max N_MATR:", max(df_final$N_MATRICULADOS), "\n")
cat("RBD NA:", sum(is.na(df_final$RBD)), " ingreso alumno NA:", sum(is.na(df_final$INGRESO_PERCAPITA_GRUPO_FA)), "\n")
print(table(df_final$TP_DUMMY, useNA="ifany")); cat("PACE1:", sum(df_final$PACE), " BEA1:", sum(df_final$BEA), " colegios:", n_distinct(df_final$RBD), " mujeres:", sum(df_final$SEXO==2), "\n")
x <- df_final; print(colSums(is.na(x))[colSums(is.na(x))>0])
