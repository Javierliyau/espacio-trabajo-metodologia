library(tidyverse)
library(scorecard)
rm(list = ls())
graphics.off()
cat("\014")

# cambiar a la carpeta donde estan los 4 csv
setwd("/Users/david/Downloads/econometria-ii-demre/datos/crudos/base de datos")
getwd()

df1 <- read_csv2("ArchivoB_Adm2026REG.csv")    # inscritos (para las X extra)
df2 <- read_csv2("ArchivoC_Adm2026REG.csv")    # rinden: es la "A" del profe, la base maestra
df3 <- read_csv2("ArchivoD_Adm2026REG.csv")    # postulaciones: la "B" del profe
df4 <- read_csv2("ArchivoMatr_Adm2026.csv")    # matricula: la "C" del profe
nrow(df2)



############## FILTROS EN LA BASE MAESTRA (df2) #######################
# ahora no se hace full_join: se parte de los que rinden y se filtra paso a paso
p1 <- df2 %>%
  filter(SITUACION_EGRESO == 1)

# primera vez: sin puntaje de invierno actual ni de ningun proceso anterior
p2 <- p1 %>%
  filter(is.na(CLEC_INV_ACTUAL), is.na(MATE1_INV_ACTUAL), is.na(MATE2_INV_ACTUAL),
         is.na(HCSOC_INV_ACTUAL), is.na(CIEN_INV_ACTUAL), is.na(MODULO_INV_ACTUAL),
         is.na(CLEC_REG_ANTERIOR), is.na(MATE1_REG_ANTERIOR), is.na(MATE2_REG_ANTERIOR),
         is.na(HCSOC_REG_ANTERIOR), is.na(CIEN_REG_ANTERIOR), is.na(MODULO_REG_ANTERIOR),
         is.na(CLEC_INV_ANTERIOR), is.na(MATE1_INV_ANTERIOR), is.na(MATE2_INV_ANTERIOR),
         is.na(HCSOC_INV_ANTERIOR), is.na(CIEN_INV_ANTERIOR), is.na(MODULO_INV_ANTERIOR))

# ojo: >= 100, con > 100 da 168.678
p3 <- p2 %>%
  filter(CLEC_REG_ACTUAL >= 100, MATE1_REG_ACTUAL >= 100)

p4 <- p3 %>%
  filter(CIEN_REG_ACTUAL >= 100 | HCSOC_REG_ACTUAL >= 100)

p5 <- p4 %>%
  filter(PROMEDIO_NOTAS != 0)

cat("PASOS:", nrow(df2), nrow(p1), nrow(p2), nrow(p3), nrow(p4), nrow(p5), "\n")



############## FLAG_POSTULA Y VARIABLE I #######################
# de df3 no se pega nada, solo se marca si el ID aparece ("existe", dijo el profe)
postulantes <- df3 %>%
  distinct(ID_aux) %>%
  mutate(flag_postula = 1)
nrow(postulantes)

base <- p5 %>%
  left_join(postulantes, by = "ID_aux")
base$flag_postula <- ifelse(is.na(base$flag_postula), 0, 1)
table(base$flag_postula)

# matricula regular por via 1, despues se pega con left_join
matricula <- df4 %>%
  filter(VIA == 1, TIPO_MATRICULA == 1) %>%
  select(ID_aux, PREFERENCIA)
nrow(matricula)

base <- base %>%
  left_join(matricula, by = "ID_aux")
# los que no postularon o no se matricularon quedan con NA en PREFERENCIA -> I = 0
base$I <- ifelse(base$PREFERENCIA %in% c(1, 2, 3), 1, 0)
table(base$I)
table(base$flag_postula, base$I)

tasa_I_redondeado <- round(100 * mean(base$I), 2)
cat("N:", nrow(base), " I = 1:", sum(base$I), " tasa:", tasa_I_redondeado, "%\n")



############## VARIABLES DEL COLEGIO #######################
colegio <- df1 %>%
  filter(!is.na(RBD)) %>%
  mutate(INGRESO_AUX = ifelse(INGRESO_PERCAPITA_GRUPO_FA == 99, NA, INGRESO_PERCAPITA_GRUPO_FA)) %>%
  group_by(RBD) %>%
  summarise(N_ALUMNOS = n(),
            INGRESO_COLEGIO = median(INGRESO_AUX, na.rm = TRUE))
colegio



############## X CANDIDATAS #######################
inscritos <- df1 %>%
  select(ID_aux, FECHA_NACIMIENTO, SEXO, PACE, BEA, INGRESO_PERCAPITA_GRUPO_FA)

# FECHA_NACIMIENTO viene como mmaaaa (082007 = agosto 2007)
inscritos$FECHA_NUM <- as.numeric(inscritos$FECHA_NACIMIENTO)
inscritos$MES <- round((inscritos$FECHA_NUM - 2000) / 10000)
inscritos$ANIO <- inscritos$FECHA_NUM - inscritos$MES * 10000
inscritos$EDAD_MESES <- (2025 - inscritos$ANIO) * 12 + (12 - inscritos$MES)

inscritos$PACE <- ifelse(is.na(inscritos$PACE), 0, 1)
inscritos$BEA <- ifelse(is.na(inscritos$BEA), 0, 1)
inscritos$INGRESO_PERCAPITA_GRUPO_FA <- ifelse(inscritos$INGRESO_PERCAPITA_GRUPO_FA == 99, NA, inscritos$INGRESO_PERCAPITA_GRUPO_FA)

df_final <- base %>%
  left_join(inscritos, by = "ID_aux") %>%
  left_join(colegio, by = "RBD")
nrow(df_final)   # tiene que seguir en 168.714

df_final$TP_DUMMY <- ifelse(df_final$RAMA_EDUCACIONAL %in% c("T1", "T2", "T3", "T4", "T5"), 1, 0)
df_final$RINDE_CIEN <- ifelse(df_final$CIEN_REG_ACTUAL >= 100, 1, 0)
df_final$RINDE_HCSOC <- ifelse(df_final$HCSOC_REG_ACTUAL >= 100, 1, 0)
df_final$RINDE_M2 <- ifelse(df_final$MATE2_REG_ACTUAL >= 100, 1, 0)
# las categoricas como texto para que woebin no las corte como numero
df_final$GRUPO_DEPENDENCIA <- as.character(df_final$GRUPO_DEPENDENCIA)
df_final$CODIGO_REGION <- as.character(df_final$CODIGO_REGION)
df_final$SEXO <- as.character(df_final$SEXO)

# N_MATRICULADOS y PTJE_POND no van: se saben despues de la matricula
dt <- df_final %>%
  select(I, PROMEDIO_NOTAS, PORC_SUP_NOTAS, PTJE_NEM, PTJE_RANKING, CLEC_REG_ACTUAL, MATE1_REG_ACTUAL,
         RINDE_CIEN, RINDE_HCSOC, RINDE_M2, GRUPO_DEPENDENCIA, TP_DUMMY, CODIGO_REGION, SEXO,
         PACE, BEA, INGRESO_PERCAPITA_GRUPO_FA, EDAD_MESES, N_ALUMNOS, INGRESO_COLEGIO)
summary(dt)



############## UNIVARIADO: NA Y TUKEY #######################
# mas de 5 % de NA -> la variable no se usa
for (v in names(dt)) {
  porc_na <- round(100 * mean(is.na(dt[[v]])), 2)
  cat(v, ":", porc_na, "% NA\n")
}

# atipicos con Tukey, solo se informan (son casos reales, no se borran)
numericas <- c("PROMEDIO_NOTAS", "PTJE_NEM", "PTJE_RANKING", "CLEC_REG_ACTUAL", "MATE1_REG_ACTUAL",
               "EDAD_MESES", "N_ALUMNOS", "INGRESO_COLEGIO")
for (v in numericas) {
  x <- dt[[v]]
  q1 <- quantile(x, 0.25, na.rm = TRUE)
  q3 <- quantile(x, 0.75, na.rm = TRUE)
  ric <- IQR(x, na.rm = TRUE)
  lim_inf <- q1 - 1.5 * ric
  lim_sup <- q3 + 1.5 * ric
  n_fuera <- sum(x < lim_inf | x > lim_sup, na.rm = TRUE)
  cat(v, ": limites", lim_inf, "y", lim_sup, "| fuera:", n_fuera, "\n")
}
boxplot(dt$EDAD_MESES, main = "Edad en meses")



############## BIVARIADO: WOEBIN E IV #######################
# scorecard calcula woe = ln(%I1 / %I0): woe positivo = tramo con mas matricula top 3
bins <- woebin(dt, y = "I")

tabla_iv <- data.frame()
for (v in names(bins)) {
  fila <- data.frame(variable = v,
                     IV = round(bins[[v]]$total_iv[1], 3),
                     tramos = nrow(bins[[v]]))
  tabla_iv <- rbind(tabla_iv, fila)
}
tabla_iv <- tabla_iv %>%
  arrange(desc(IV)) %>%
  mutate(poder = case_when(IV < 0.02 ~ "inutil",
                           IV < 0.1 ~ "debil",
                           IV < 0.3 ~ "medio",
                           IV < 0.5 ~ "fuerte",
                           TRUE ~ "sospechoso"))
tabla_iv

# monotonia: la tasa de I = 1 por tramo tiene que subir siempre o bajar siempre
for (v in names(bins)) {
  tramos_sin_na <- bins[[v]] %>%
    filter(bin != "missing")
  tasa <- round(100 * tramos_sin_na$posprob, 1)
  saltos <- diff(tasa)
  monotona <- ifelse(sum(saltos >= 0) == length(saltos) | sum(saltos <= 0) == length(saltos), "si", "no")
  cat(v, ":", paste(tasa, collapse = " | "), "-> monotona:", monotona, "\n")
}

woebin_plot(bins$CLEC_REG_ACTUAL)
woebin_plot(bins$EDAD_MESES)



############## RETRAMIFICAR #######################
# edad: 3 tramos que suben y bajan -> un solo corte en 228 meses (19 anios)
bins_edad <- woebin(dt, y = "I", x = "EDAD_MESES", breaks_list = list(EDAD_MESES = c(228)))
bins_edad$EDAD_MESES
woebin_plot(bins_edad$EDAD_MESES)

# dependencia: municipal (3) y SLEP (4) juntos como publico, por juicio experto
dt$DEPENDENCIA_3 <- case_when(dt$GRUPO_DEPENDENCIA == "1" ~ "pagado",
                              dt$GRUPO_DEPENDENCIA == "2" ~ "subvencionado",
                              dt$GRUPO_DEPENDENCIA %in% c("3", "4") ~ "publico")
table(dt$GRUPO_DEPENDENCIA, dt$DEPENDENCIA_3)
bins_dep <- woebin(dt, y = "I", x = "DEPENDENCIA_3")
bins_dep$DEPENDENCIA_3
woebin_plot(bins_dep$DEPENDENCIA_3)



############## VIF Y X DEFINITIVAS #######################
# primero con todas las que pasan IV >= 0.02 y tienen menos de 5 % de NA
bins_iv <- list(CLEC_REG_ACTUAL = bins$CLEC_REG_ACTUAL, MATE1_REG_ACTUAL = bins$MATE1_REG_ACTUAL,
                PROMEDIO_NOTAS = bins$PROMEDIO_NOTAS, PTJE_NEM = bins$PTJE_NEM,
                PTJE_RANKING = bins$PTJE_RANKING, PORC_SUP_NOTAS = bins$PORC_SUP_NOTAS,
                TP_DUMMY = bins$TP_DUMMY, INGRESO_COLEGIO = bins$INGRESO_COLEGIO,
                DEPENDENCIA_3 = bins_dep$DEPENDENCIA_3, EDAD_MESES = bins_edad$EDAD_MESES,
                BEA = bins$BEA, RINDE_M2 = bins$RINDE_M2)
dt_iv <- dt %>%
  select(I, CLEC_REG_ACTUAL, MATE1_REG_ACTUAL, PROMEDIO_NOTAS, PTJE_NEM, PTJE_RANKING, PORC_SUP_NOTAS,
         TP_DUMMY, INGRESO_COLEGIO, DEPENDENCIA_3, EDAD_MESES, BEA, RINDE_M2)
dt_iv_woe <- woebin_ply(dt_iv, bins_iv)
modelo_iv <- glm(I ~ ., family = binomial(), data = dt_iv_woe)
vif(modelo_iv, merge_coef = TRUE)   # VIF > 2 -> sale

# las notas se pisan entre ellas (queda PROMEDIO), sale PORC_SUP y queda dependencia en vez de ingreso del colegio
bins_finales <- list(CLEC_REG_ACTUAL = bins$CLEC_REG_ACTUAL, MATE1_REG_ACTUAL = bins$MATE1_REG_ACTUAL,
                     PROMEDIO_NOTAS = bins$PROMEDIO_NOTAS, TP_DUMMY = bins$TP_DUMMY,
                     DEPENDENCIA_3 = bins_dep$DEPENDENCIA_3, EDAD_MESES = bins_edad$EDAD_MESES,
                     BEA = bins$BEA, RINDE_M2 = bins$RINDE_M2)
dt_finales <- dt %>%
  select(I, CLEC_REG_ACTUAL, MATE1_REG_ACTUAL, PROMEDIO_NOTAS, TP_DUMMY, DEPENDENCIA_3, EDAD_MESES, BEA, RINDE_M2)
dt_finales_woe <- woebin_ply(dt_finales, bins_finales)
modelo_final <- glm(I ~ ., family = binomial(), data = dt_finales_woe)
vif(modelo_final, merge_coef = TRUE)
