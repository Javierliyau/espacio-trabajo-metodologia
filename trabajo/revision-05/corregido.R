library(tidyverse)
setwd("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos")
df1 <- read_csv2("1-inscritos-archivo-B/ArchivoB_Adm2026REG.csv")
df2 <- read_csv2("2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv")
df4 <- read_csv2("4-matricula/ArchivoMatr_Adm2026.csv")

############## VARIABLES DEL COLEGIO #######################
promo <- df1 %>%
  filter(SITUACION_EGRESO == 1, !is.na(RBD))

matricula <- df4 %>%
  filter(VIA == 1 & TIPO_MATRICULA == 1) %>%
  inner_join(promo %>% select(ID_aux, RBD), by = "ID_aux") %>%
  group_by(RBD) %>%
  summarise(N_MATRICULADOS = n())

colegio <- promo %>%
  mutate(INGRESO_AUX = ifelse(INGRESO_PERCAPITA_GRUPO_FA == 99, NA, INGRESO_PERCAPITA_GRUPO_FA)) %>%
  group_by(RBD) %>%
  summarise(N_ALUMNOS = n(),
            INGRESO_COLEGIO = mean(INGRESO_AUX, na.rm = TRUE)) %>%
  left_join(matricula, by = "RBD") %>%
  mutate(N_MATRICULADOS = ifelse(is.na(N_MATRICULADOS), 0, N_MATRICULADOS),
         TASA_MATRICULA = N_MATRICULADOS / N_ALUMNOS)

############## FILTRAR DATOS #######################
df1 <- df1 %>% select(ID_aux,SITUACION_EGRESO,FECHA_NACIMIENTO,RBD,RAMA_EDUCACIONAL,GRUPO_DEPENDENCIA,CODIGO_REGION,CODIGO_COMUNA,CODIGO_COMUNA_D,SEXO,PACE,BEA,INGRESO_PERCAPITA_GRUPO_FA,RINDIO_PROCESO_ACTUAL)
df2 <- df2 %>% select(ID_aux,PROMEDIO_NOTAS,PTJE_NEM,PTJE_RANKING,CLEC_REG_ACTUAL,MATE1_REG_ACTUAL)
df4 <- df4 %>% select(ID_aux,PREFERENCIA,VIA,PTJE_POND,TIPO_MATRICULA)

base <- list(df1, df2, df4) %>% reduce(full_join, by = "ID_aux")
n0 <- nrow(base)
p1 <- base %>% filter(SITUACION_EGRESO == 1)
p2 <- p1 %>% filter(VIA == 1 & TIPO_MATRICULA == 1)
p3 <- p2 %>% filter(RINDIO_PROCESO_ACTUAL %in% c(1, 3))
p4 <- p3 %>% filter(PREFERENCIA %in% c(1, 2, 3))
p5 <- p4 %>% filter(!is.na(PTJE_NEM), PTJE_NEM != 0)
cat("PASOS:", n0, nrow(p1), nrow(p2), nrow(p3), nrow(p4), nrow(p5), "\n")
df_final <- left_join(p5, colegio, by = "RBD")

################ VARIABLES CREADAS ########################
df_final <- df_final %>%
  mutate(PREF_PRIMERA_DUMMY = ifelse(PREFERENCIA == 1, 1, 0),
         TP_DUMMY = ifelse(RAMA_EDUCACIONAL %in% c("T1","T2","T3","T4","T5"), 1, 0),
         PACE_DUMMY = ifelse(is.na(PACE), 0, 1),
         BEA_DUMMY = ifelse(is.na(BEA), 0, 1),
         MUJER = ifelse(SEXO == 2, 1, 0),
         INGRESO_NR = ifelse(INGRESO_PERCAPITA_GRUPO_FA == 99, 1, 0),
         EDAD = 2025 - as.numeric(str_sub(FECHA_NACIMIENTO, -4)),
         DEPENDENCIA = factor(GRUPO_DEPENDENCIA, levels = 1:4,
                              labels = c("Particular pagado","Particular subvencionado","Municipal","SLEP")))

cat("dim:", dim(df_final), "ids:", n_distinct(df_final$ID_aux), "RBD NA:", sum(is.na(df_final$RBD)), "colegios:", n_distinct(df_final$RBD), "\n")
print(table(df_final$PREF_PRIMERA_DUMMY)); print(table(df_final$PREFERENCIA))
print(summary(df_final %>% select(N_ALUMNOS, INGRESO_COLEGIO, N_MATRICULADOS, TASA_MATRICULA, EDAD)))
cat("PACE1:", sum(df_final$PACE_DUMMY), "BEA1:", sum(df_final$BEA_DUMMY), "MUJER:", sum(df_final$MUJER), "INGRESO_NR:", sum(df_final$INGRESO_NR), "TP:", sum(df_final$TP_DUMMY), "\n")
print(table(df_final$DEPENDENCIA, useNA = "ifany"))
print(table(df_final$EDAD, useNA = "ifany"))
cat("NA por col:\n"); print(colSums(is.na(df_final))[colSums(is.na(df_final)) > 0])
