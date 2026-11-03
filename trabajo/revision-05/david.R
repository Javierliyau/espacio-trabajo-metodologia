library(tidyverse)

cat("\014")

df1 <- read_csv2("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/1-inscritos-archivo-B/ArchivoB_Adm2026REG.csv")
df2 <- read_csv2("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv")
df3 <- read_csv2("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/3-postulaciones-archivo-D/ArchivoD_Adm2026REG.csv")
df4 <- read_csv2("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/4-matricula/ArchivoMatr_Adm2026.csv")



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
cat("\n===== CHEQUEOS =====\n")
d1 <- read_csv2(sub("x","x","C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/1-inscritos-archivo-B/ArchivoB_Adm2026REG.csv"), show_col_types=FALSE)
d4 <- read_csv2("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/4-matricula/ArchivoMatr_Adm2026.csv", show_col_types=FALSE)
d3 <- read_csv2("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/3-postulaciones-archivo-D/ArchivoD_Adm2026REG.csv", show_col_types=FALSE)
cat("dim final:", dim(df_final), " ids unicos:", n_distinct(df_final$ID_aux), "\n")
cat("filas matricula:", nrow(d4), " ids unicos matricula:", n_distinct(d4$ID_aux), "\n")
cat("tabla Y:\n"); print(table(df_final$PREF_PRIMERA_DUMMY))
cat("RBD NA en final:", sum(is.na(df_final$RBD)), "\n")
print(df_final %>% filter(is.na(RBD)) %>% distinct(N_ALUMNOS, INGRESO_COLEGIO, N_MATRICULADOS))
cat("Top N_ALUMNOS colegio:\n"); print(colegio %>% arrange(desc(N_ALUMNOS)) %>% head(5))
cat("INGRESO_COLEGIO resumen:\n"); print(summary(df_final$INGRESO_COLEGIO))
cat("ingreso 99 en B:", sum(d1$INGRESO_PERCAPITA_GRUPO_FA==99, na.rm=TRUE), "\n")
cat("ANYO_EGRESO 2025 vs SITUACION_EGRESO:\n"); if ("SITUACION_EGRESO" %in% names(d1)) print(table(d1$SITUACION_EGRESO[d1$ID_aux %in% df_final$ID_aux], useNA="ifany"))
cat("N_ALUMNOS: share de inscritos del colegio que no egresaron 2025:", mean(d1$ANYO_EGRESO!=2025, na.rm=TRUE), "\n")
cat("TIPO_PREF por estudiante (n tipos distintos):\n"); print(table(d3 %>% group_by(ID_aux) %>% summarise(k=n_distinct(TIPO_PREF)) %>% pull(k)))
cat("PACE/BEA valores:\n"); print(table(df_final$PACE, useNA="ifany")); print(table(df_final$BEA, useNA="ifany"))
cat("cols D:", names(d3), "\n"); cat("cols M:", names(d4), "\n")
cat("RINDIO tabla en B:\n"); print(table(d1$RINDIO_PROCESO_ACTUAL, useNA="ifany"))
cat("TIPO_MATRICULA x VIA:\n"); print(table(d4$VIA, d4$TIPO_MATRICULA, useNA="ifany"))
cat("PREFERENCIA de matriculados promocion via1 tipo1:\n"); print(table(cut(d4$PREFERENCIA[d4$VIA==1 & d4$TIPO_MATRICULA==1], c(0,1,2,3,10,100)), useNA="ifany"))
