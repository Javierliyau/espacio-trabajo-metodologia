library(writexl)
library(tidyverse)
rm(list = ls())
cat("\014")

df1 <- read_csv2("datos/crudos/1-inscritos-archivo-B/ArchivoB_Adm2026REG.csv")
df2 <- read_csv2("datos/crudos/2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv")
df3 <- read_csv2("datos/crudos/3-postulaciones-archivo-D/ArchivoD_Adm2026REG.csv")
df4 <- read_csv2("datos/crudos/4-matricula/ArchivoMatr_Adm2026.csv")


df1 <- df1 %>%
  mutate(INGRESO_PERCAPITA_GRUPO_FA = na_if(INGRESO_PERCAPITA_GRUPO_FA, 99))
table(df1$INGRESO_PERCAPITA_GRUPO_FA, useNA = "ifany")



############## VARIABLES DEL COLEGIO #######################
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
  filter(SITUACION_EGRESO==1)%>%          
  filter(!is.na(TIPO_PREF))%>%                                    # postulo por via regular (archivo D)
  filter(is.na(VIA) | (VIA==1 & TIPO_MATRICULA==1))%>%            # no matriculado, o matriculado via regular y tipo 1
  filter(RINDIO_PROCESO_ACTUAL==1)%>%
  filter(!is.na(PTJE_NEM), PTJE_NEM != 0)
df_final
df_final <- left_join(df_final, colegio, by = "RBD")
df_final

################ CREACION VARIABLES DUMMY ########################
# Y: 1 si se matriculo en una de sus 3 primeras preferencias;
# 0 si se matriculo en la 4a o mas abajo, o si no se matriculo (PREFERENCIA = NA)
df_final$PREF_TOP3_DUMMY <- ifelse(df_final$PREFERENCIA %in% c(1,2,3), 1, 0)
table(df_final$PREF_TOP3_DUMMY)

df_final$TP_DUMMY <- ifelse(is.na(df_final$RAMA_EDUCACIONAL), NA,
                            ifelse(df_final$RAMA_EDUCACIONAL %in% c("T1","T2","T3","T4","T5"), 1, 0))
table(df_final$TP_DUMMY, useNA = "ifany")

df_final$PACE <- ifelse(is.na(df_final$PACE), 0, 1)
df_final$BEA  <- ifelse(is.na(df_final$BEA), 0, 1)
table(df_final$PACE)
table(df_final$BEA)

table(df_final$PREFERENCIA)

write_xlsx(df_final, "datos/final/resultado_final_postulantes.xlsx")
cat("\n==== REVISION ====\n")
u <- reduce(list(df1,df2,df3,df4), full_join, by="ID_aux"); s <- nrow(u)
for (e in c("ANYO_EGRESO==2025","SITUACION_EGRESO==1","RINDIO_PROCESO_ACTUAL==1","!is.na(PTJE_NEM) & PTJE_NEM!=0","!is.na(TIPO_PREF)","is.na(VIA) | (VIA==1 & TIPO_MATRICULA==1)")) { u <- filter(u, eval(parse(text=e))); s <- c(s, nrow(u)) }
cat("PASOS (orden informe):", s, "\n")
cat("dims:", dim(df_final), " unicos:", n_distinct(df_final$ID_aux), "\n")
print(table(df_final$PREF_TOP3_DUMMY)); print(round(100*prop.table(table(df_final$PREF_TOP3_DUMMY)),1))
cat("no matriculados:", sum(is.na(df_final$PREFERENCIA)), " pref4+:", sum(df_final$PREFERENCIA>=4, na.rm=T), "\n")
f <- function(v) cat(v, ":", paste(round(c(min(df_final[[v]],na.rm=T), median(df_final[[v]],na.rm=T), mean(df_final[[v]],na.rm=T), max(df_final[[v]],na.rm=T)),2), collapse=" | "), "\n")
for (v in c("PROMEDIO_NOTAS","PTJE_NEM","PTJE_RANKING","CLEC_REG_ACTUAL","MATE1_REG_ACTUAL","PTJE_POND","N_ALUMNOS","INGRESO_COLEGIO","N_MATRICULADOS")) f(v)
na <- colSums(is.na(df_final)); print(na[na>0])
cat("colegios:", n_distinct(df_final$RBD, na.rm=T), "\n"); print(table(df_final$SEXO)); print(table(df_final$TP_DUMMY, useNA="ifany")); cat("PACE1:", sum(df_final$PACE), " BEA1:", sum(df_final$BEA), "\n")
