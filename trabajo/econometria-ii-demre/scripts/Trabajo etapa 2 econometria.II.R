############## ECONOMETRÍA 2 #######################
##############TRABAJO: ETAPA 2 #######################
#Nombres: David Cuevas, Javier Li-Yau,Benjamín Lizana y Ana Nacif

library(writexl)
library(tidyverse)
library(scorecard)
rm(list = ls())
cat("\014")

# rutas relativas: abrir econometria-ii-demre.Rproj
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

# Etapa 2: se saca N_MATRICULADOS, porque se conoce despues de la matricula (ex post)



############## FILTRAR DATOS #######################
df1 <- df1 %>%
  select(ID_aux,FECHA_NACIMIENTO,RBD,RAMA_EDUCACIONAL,GRUPO_DEPENDENCIA,CODIGO_REGION,SEXO,PACE,BEA,INGRESO_PERCAPITA_GRUPO_FA)
df1

# Etapa 2: la base maestra es df2 (los que rinden) con los 5 filtros del profesor
df2 <- df2 %>%
  filter(SITUACION_EGRESO==1) %>%                                   # 1. promocion 2025      218.066
  filter(if_all(CLEC_INV_ACTUAL:MODULO_INV_ANTERIOR, is.na)) %>%    # 2. rinde por 1.a vez   217.449
  filter(CLEC_REG_ACTUAL>=100, MATE1_REG_ACTUAL>=100) %>%           # 3. obligatorias        179.347
  filter(CIEN_REG_ACTUAL>=100 | HCSOC_REG_ACTUAL>=100) %>%          # 4. una electiva        170.056
  filter(PROMEDIO_NOTAS != 0) %>%                                   # 5. con notas           168.714
  select(ID_aux,PROMEDIO_NOTAS,PORC_SUP_NOTAS,PTJE_NEM,PTJE_RANKING,CLEC_REG_ACTUAL,MATE1_REG_ACTUAL,
         CIEN_REG_ACTUAL,HCSOC_REG_ACTUAL,MATE2_REG_ACTUAL)
df2

# Etapa 2: de las postulaciones solo se marca si postulo; el que no postulo queda en la base con Y = 0
df3 <- df3 %>%
  distinct(ID_aux) %>%
  mutate(FLAG_POSTULA = 1)
df3

# Etapa 2: el filtro de via y tipo se hace en la matricula, no en la base
df4 <- df4 %>%
  filter(VIA==1 & TIPO_MATRICULA==1) %>%
  select(ID_aux, PREFERENCIA)
df4


lista_dfs <- list(df2, df1, df3, df4)

df_final <- lista_dfs %>%
  reduce(left_join, by = "ID_aux")
df_final
df_final <- left_join(df_final, colegio, by = "RBD")
nrow(df_final)   # 168.714

################ CREACION VARIABLES DUMMY ########################
df_final$PREF_TOP3_DUMMY <- ifelse(df_final$PREFERENCIA %in% c(1,2,3), 1, 0)
table(df_final$PREF_TOP3_DUMMY)   # 1: 60.234

df_final$FLAG_POSTULA <- ifelse(is.na(df_final$FLAG_POSTULA), 0, 1)
table(df_final$FLAG_POSTULA, df_final$PREF_TOP3_DUMMY)   # nadie con Y = 1 sin postular

df_final$TP_DUMMY <- ifelse(df_final$RAMA_EDUCACIONAL %in% c("T1","T2","T3","T4","T5"), 1, 0)
table(df_final$TP_DUMMY, useNA = "ifany")

df_final$PACE <- ifelse(is.na(df_final$PACE), 0, 1)
df_final$BEA  <- ifelse(is.na(df_final$BEA), 0, 1)
table(df_final$PACE)
table(df_final$BEA)

df_final$RINDE_CIEN  <- ifelse(df_final$CIEN_REG_ACTUAL >= 100, 1, 0)
df_final$RINDE_HCSOC <- ifelse(df_final$HCSOC_REG_ACTUAL >= 100, 1, 0)
df_final$RINDE_M2    <- ifelse(df_final$MATE2_REG_ACTUAL >= 100, 1, 0)

# FECHA_NACIMIENTO viene como mmaaaa (082007 = agosto 2007)
df_final$MES  <- round((as.numeric(df_final$FECHA_NACIMIENTO) - 2000) / 10000)
df_final$ANIO <- as.numeric(df_final$FECHA_NACIMIENTO) - df_final$MES * 10000
df_final$EDAD_MESES <- (2025 - df_final$ANIO) * 12 + (12 - df_final$MES)

# las categoricas como texto para que woebin no las corte como numero
df_final$GRUPO_DEPENDENCIA <- as.character(df_final$GRUPO_DEPENDENCIA)
df_final$CODIGO_REGION <- as.character(df_final$CODIGO_REGION)
df_final$SEXO <- as.character(df_final$SEXO)

table(df_final$PREFERENCIA)
summary(df_final)

write_xlsx(df_final, "datos/procesados/base-final-etapa-2.xlsx")



############## UNIVARIADO #######################
dt <- df_final %>%
  select(PREF_TOP3_DUMMY, PROMEDIO_NOTAS, PORC_SUP_NOTAS, PTJE_NEM, PTJE_RANKING, CLEC_REG_ACTUAL, MATE1_REG_ACTUAL,
         RINDE_CIEN, RINDE_HCSOC, RINDE_M2, GRUPO_DEPENDENCIA, TP_DUMMY, CODIGO_REGION, SEXO,
         PACE, BEA, INGRESO_PERCAPITA_GRUPO_FA, EDAD_MESES, N_ALUMNOS, INGRESO_COLEGIO)
summary(dt)

# mas de 5 % de NA -> la variable no se usa
round(100 * colMeans(is.na(dt)), 2)

# atipicos con Tukey: se informan, no se borran (son casos reales y con WOE quedan en su tramo)
numericas <- c("PROMEDIO_NOTAS", "PTJE_NEM", "PTJE_RANKING", "CLEC_REG_ACTUAL", "MATE1_REG_ACTUAL",
               "EDAD_MESES", "N_ALUMNOS", "INGRESO_COLEGIO")
for (v in numericas) {
  x <- dt[[v]]
  lim_inf <- quantile(x, 0.25, na.rm = TRUE) - 1.5 * IQR(x, na.rm = TRUE)
  lim_sup <- quantile(x, 0.75, na.rm = TRUE) + 1.5 * IQR(x, na.rm = TRUE)
  cat(v, ": limites", lim_inf, "y", lim_sup, "| atipicos:", sum(x < lim_inf | x > lim_sup, na.rm = TRUE), "\n")
}
boxplot(dt$EDAD_MESES, main = "Edad en meses")



############## BIVARIADO: WOE E IV #######################
# scorecard calcula woe = ln(%Y1 / %Y0): woe positivo = tramo con mas matricula en el top 3
bins <- woebin(dt, y = "PREF_TOP3_DUMMY")

# IV de los tramos de woebin (iv() lo calcula sin tramificar y da otro numero)
tabla_iv <- data.frame(variable = names(bins),
                       IV = sapply(bins, function(b) round(b$total_iv[1], 3)))
tabla_iv %>% arrange(desc(IV))   # IV < 0.02 -> fuera
bins$CLEC_REG_ACTUAL
woebin_plot(bins$CLEC_REG_ACTUAL)
woebin_plot(bins$MATE1_REG_ACTUAL)
woebin_plot(bins$PROMEDIO_NOTAS)
woebin_plot(bins$TP_DUMMY)

# monotonia: la tasa de Y = 1 por tramo tiene que subir siempre o bajar siempre
for (v in names(bins)) {
  tasa <- bins[[v]] %>% filter(bin != "missing") %>% pull(posprob)
  cat(v, ":", round(100 * tasa, 1), "-> monotona:", all(diff(tasa) >= 0) | all(diff(tasa) <= 0), "\n")
}



############## RETRAMIFICAR #######################
# edad: sube y baja -> un solo corte en 228 meses (19 anios)
woebin_plot(bins$EDAD_MESES)
bins_edad <- woebin(dt, y = "PREF_TOP3_DUMMY", x = "EDAD_MESES", breaks_list = list(EDAD_MESES = c(228)))
woebin_plot(bins_edad$EDAD_MESES)

# dependencia: municipal (3) y SLEP (4) juntos como publico, por juicio experto
dt$DEPENDENCIA_3 <- case_when(dt$GRUPO_DEPENDENCIA == "1" ~ "pagado",
                              dt$GRUPO_DEPENDENCIA == "2" ~ "subvencionado",
                              dt$GRUPO_DEPENDENCIA %in% c("3", "4") ~ "publico")
table(dt$GRUPO_DEPENDENCIA, dt$DEPENDENCIA_3)
bins_dep <- woebin(dt, y = "PREF_TOP3_DUMMY", x = "DEPENDENCIA_3")
woebin_plot(bins_dep$DEPENDENCIA_3)



############## VIF Y X DEFINITIVAS #######################
# con las que pasan IV >= 0.02 y tienen menos de 5 % de NA
x_iv <- c("CLEC_REG_ACTUAL", "MATE1_REG_ACTUAL", "PROMEDIO_NOTAS", "PTJE_NEM", "PTJE_RANKING", "PORC_SUP_NOTAS",
          "TP_DUMMY", "INGRESO_COLEGIO", "DEPENDENCIA_3", "EDAD_MESES", "BEA", "RINDE_M2")
bins_iv <- c(bins[setdiff(x_iv, c("DEPENDENCIA_3", "EDAD_MESES"))], bins_dep, bins_edad)
dt_woe <- woebin_ply(dt[, c("PREF_TOP3_DUMMY", x_iv)], bins_iv)
modelo_iv <- glm(PREF_TOP3_DUMMY ~ ., family = binomial(), data = dt_woe)
vif(modelo_iv, merge_coef = TRUE)   # VIF > 2 -> sale

# las notas se pisan (queda PROMEDIO, mayor IV), sale PORC_SUP y queda dependencia en vez de ingreso del colegio
x_finales <- c("CLEC_REG_ACTUAL", "MATE1_REG_ACTUAL", "PROMEDIO_NOTAS", "TP_DUMMY", "DEPENDENCIA_3",
               "EDAD_MESES", "BEA", "RINDE_M2")
dt_woe_final <- woebin_ply(dt[, c("PREF_TOP3_DUMMY", x_finales)], bins_iv[x_finales])
modelo_final <- glm(PREF_TOP3_DUMMY ~ ., family = binomial(), data = dt_woe_final)
vif(modelo_final, merge_coef = TRUE)   # todas bajo 2
