library(tidyverse)
rm(list = ls())
cat("\014")

df1 <- read_csv2("ArchivoB_Adm2026REG.csv")
df2 <- read_csv2("ArchivoC_Adm2026REG.csv")
df4 <- read_csv2("ArchivoMatr_Adm2026.csv")



############## VARIABLES DEL COLEGIO #######################
promo <- df1 %>%
  filter(SITUACION_EGRESO == 1, !is.na(RBD))
promo

colegio <- promo %>%
  mutate(INGRESO_AUX = ifelse(INGRESO_PERCAPITA_GRUPO_FA == 99, NA, INGRESO_PERCAPITA_GRUPO_FA)) %>%
  group_by(RBD) %>%
  summarise(N_ALUMNOS = n(),
            INGRESO_COLEGIO = mean(INGRESO_AUX, na.rm = TRUE))
colegio

matricula<- df4 %>%
  filter(VIA==1 & TIPO_MATRICULA==1) %>%
  left_join(promo %>% select(ID_aux, RBD), by = "ID_aux") %>%
  filter(!is.na(RBD)) %>%
  group_by(RBD) %>%
  summarise(N_MATRICULADOS = n())
matricula

colegio <- colegio %>%
  left_join(matricula, by = "RBD")
colegio$N_MATRICULADOS <- ifelse(is.na(colegio$N_MATRICULADOS), 0, colegio$N_MATRICULADOS)
colegio$TASA_MATRICULA <- colegio$N_MATRICULADOS / colegio$N_ALUMNOS
colegio



############## FILTRAR DATOS #######################
df1 <- df1 %>%
  select(ID_aux,SITUACION_EGRESO,FECHA_NACIMIENTO,RBD,RAMA_EDUCACIONAL,GRUPO_DEPENDENCIA,CODIGO_REGION,CODIGO_COMUNA,CODIGO_COMUNA_D,SEXO,PACE,BEA,INGRESO_PERCAPITA_GRUPO_FA,RINDIO_PROCESO_ACTUAL)
df1

df2 <- df2%>%
  select(ID_aux,PROMEDIO_NOTAS,PTJE_NEM, PTJE_RANKING, CLEC_REG_ACTUAL,MATE1_REG_ACTUAL)
df2

df4 <- df4 %>%
  select(ID_aux, PREFERENCIA,VIA, PTJE_POND,TIPO_MATRICULA)
df4


lista_dfs <- list(df1, df2, df4)

df_final <- lista_dfs %>%
  reduce(full_join, by = "ID_aux")%>%
  filter(SITUACION_EGRESO==1)%>%
  filter(VIA==1 & TIPO_MATRICULA==1)%>%
  filter(RINDIO_PROCESO_ACTUAL %in% c(1,3))%>%
  filter(PREFERENCIA %in% c(1,2,3))%>%
  filter(!is.na(PTJE_NEM), PTJE_NEM != 0)
df_final
df_final <- left_join(df_final, colegio, by = "RBD")
df_final

################ CREACION VARIABLES DUMMY ########################

df_final$PREF_PRIMERA_DUMMY <- ifelse(df_final$PREFERENCIA == 1, 1, 0)
df_final$PREF_PRIMERA_DUMMY

df_final$TP_DUMMY <- ifelse(df_final$RAMA_EDUCACIONAL %in% c("T1","T2","T3","T4","T5"), 1, 0)
df_final$TP_DUMMY

df_final$PACE_DUMMY <- ifelse(is.na(df_final$PACE), 0, 1)
df_final$BEA_DUMMY <- ifelse(is.na(df_final$BEA), 0, 1)
df_final$MUJER <- ifelse(df_final$SEXO == 2, 1, 0)
df_final$INGRESO_NR <- ifelse(df_final$INGRESO_PERCAPITA_GRUPO_FA == 99, 1, 0)
df_final$DEPENDENCIA <- factor(df_final$GRUPO_DEPENDENCIA, levels = 1:4,
                               labels = c("Particular pagado", "Particular subvencionado", "Municipal", "SLEP"))

table(df_final$PREFERENCIA)
summary(df_final)

write_csv2(df_final, "base_final_etapa1.csv")
