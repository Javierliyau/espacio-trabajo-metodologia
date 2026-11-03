library(tidyverse)
rm(list = ls())
cat("\014")

df1 <- read_csv2("/Users/david/Downloads/econometria-ii-demre/datos/crudos/base de datos/ArchivoB_Adm2026REG.csv")
df2 <- read_csv2("/Users/david/Downloads/econometria-ii-demre/datos/crudos/base de datos/ArchivoC_Adm2026REG.csv")
df3 <- read_csv2("/Users/david/Downloads/econometria-ii-demre/datos/crudos/base de datos/ArchivoD_Adm2026REG.csv")
df4 <- read_csv2("/Users/david/Downloads/econometria-ii-demre/datos/crudos/base de datos/ArchivoMatr_Adm2026.csv")



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
  select(ID_aux,ANYO_EGRESO,FECHA_NACIMIENTO,RBD,RAMA_EDUCACIONAL,GRUPO_DEPENDENCIA,CODIGO_REGION,CODIGO_COMUNA,CODIGO_COMUNA_D,SEXO,PACE,BEA,INGRESO_PERCAPITA_GRUPO_FA,RINDIO_PROCESO_ACTUAL)
df1

df2 <- df2%>%
  select(ID_aux,PROMEDIO_NOTAS,PTJE_NEM, PTJE_RANKING, CLEC_REG_ACTUAL,MATE1_REG_ACTUAL)
df2

df3 <- df3 %>%
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
  filter(PREFERENCIA %in% c(1,2,3))%>%
  filter(!is.na(PTJE_NEM), PTJE_NEM != 0)
df_final
df_final <- left_join(df_final, colegio, by = "RBD")
df_final

################ CREACION VARIABLES DUMMY ########################

df_final$PREF_PRIMERA_DUMMY <- ifelse(df_final$PREFERENCIA == 1, 1, 0)
df_final$PREF_PRIMERA_DUMMY

df_final$TIPO_PREF_DUMMY<-ifelse(df_final$TIPO_PREF =="REGULAR",1,0)
df_final$TIPO_PREF_DUMMY

df_final$TP_DUMMY <- ifelse(df_final$RAMA_EDUCACIONAL %in% c("T1","T2","T3","T4","T5"), 1, 0)
df_final$TP_DUMMY

table(df_final$PREFERENCIA)
summary(df_final)
