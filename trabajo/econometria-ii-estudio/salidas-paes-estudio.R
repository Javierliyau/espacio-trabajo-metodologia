# Salidas de estudio con la base PAES del grupo (N = 168.714, I = 1 para 60.234)
# Base armada igual que etapa-2-script-david.R (datos/trabajos/econometria-ii del PROYECTO).
# Deja en salidas-paes-estudio.txt una salida por modulo de la ruta (M2-M8) para
# interpretar en las sesiones, y guarda la base en base-paes-168714.rds para no rearmarla.
suppressPackageStartupMessages({
  library(tidyverse); library(scorecard); library(lmtest); library(sandwich); library(car)
})
options(width = 120, scipen = 6)

aqui <- "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-estudio"
crudos <- "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos"
rds <- file.path(aqui, "base-paes-168714.rds")

if (file.exists(rds)) {
  df_final <- readRDS(rds)
} else {
  df1 <- read_csv2(file.path(crudos, "1-inscritos-archivo-B/ArchivoB_Adm2026REG.csv"), show_col_types = FALSE)
  df2 <- read_csv2(file.path(crudos, "2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv"), show_col_types = FALSE)
  df3 <- read_csv2(file.path(crudos, "3-postulaciones-archivo-D/ArchivoD_Adm2026REG.csv"), show_col_types = FALSE)
  df4 <- read_csv2(file.path(crudos, "4-matricula/ArchivoMatr_Adm2026.csv"), show_col_types = FALSE)

  p5 <- df2 %>%
    filter(SITUACION_EGRESO == 1) %>%
    filter(is.na(CLEC_INV_ACTUAL), is.na(MATE1_INV_ACTUAL), is.na(MATE2_INV_ACTUAL),
           is.na(HCSOC_INV_ACTUAL), is.na(CIEN_INV_ACTUAL), is.na(MODULO_INV_ACTUAL),
           is.na(CLEC_REG_ANTERIOR), is.na(MATE1_REG_ANTERIOR), is.na(MATE2_REG_ANTERIOR),
           is.na(HCSOC_REG_ANTERIOR), is.na(CIEN_REG_ANTERIOR), is.na(MODULO_REG_ANTERIOR),
           is.na(CLEC_INV_ANTERIOR), is.na(MATE1_INV_ANTERIOR), is.na(MATE2_INV_ANTERIOR),
           is.na(HCSOC_INV_ANTERIOR), is.na(CIEN_INV_ANTERIOR), is.na(MODULO_INV_ANTERIOR)) %>%
    filter(CLEC_REG_ACTUAL >= 100, MATE1_REG_ACTUAL >= 100) %>%
    filter(CIEN_REG_ACTUAL >= 100 | HCSOC_REG_ACTUAL >= 100) %>%
    filter(PROMEDIO_NOTAS != 0)

  postulantes <- df3 %>% distinct(ID_aux) %>% mutate(flag_postula = 1)
  matricula <- df4 %>% filter(VIA == 1, TIPO_MATRICULA == 1) %>% select(ID_aux, PREFERENCIA)
  base <- p5 %>% left_join(postulantes, by = "ID_aux") %>% left_join(matricula, by = "ID_aux")
  base$flag_postula <- ifelse(is.na(base$flag_postula), 0, 1)
  base$I <- ifelse(base$PREFERENCIA %in% c(1, 2, 3), 1, 0)

  colegio <- df1 %>%
    filter(!is.na(RBD)) %>%
    mutate(INGRESO_AUX = ifelse(INGRESO_PERCAPITA_GRUPO_FA == 99, NA, INGRESO_PERCAPITA_GRUPO_FA)) %>%
    group_by(RBD) %>%
    summarise(N_ALUMNOS = n(), INGRESO_COLEGIO = median(INGRESO_AUX, na.rm = TRUE))
  inscritos <- df1 %>% select(ID_aux, FECHA_NACIMIENTO, SEXO, PACE, BEA)
  inscritos$FECHA_NUM <- as.numeric(inscritos$FECHA_NACIMIENTO)
  inscritos$MES <- round((inscritos$FECHA_NUM - 2000) / 10000)
  inscritos$ANIO <- inscritos$FECHA_NUM - inscritos$MES * 10000
  inscritos$EDAD_MESES <- (2025 - inscritos$ANIO) * 12 + (12 - inscritos$MES)
  inscritos$BEA <- ifelse(is.na(inscritos$BEA), 0, 1)

  df_final <- base %>% left_join(inscritos, by = "ID_aux") %>% left_join(colegio, by = "RBD")
  df_final$TP_DUMMY <- ifelse(df_final$RAMA_EDUCACIONAL %in% c("T1", "T2", "T3", "T4", "T5"), 1, 0)
  df_final$RINDE_M2 <- ifelse(!is.na(df_final$MATE2_REG_ACTUAL) & df_final$MATE2_REG_ACTUAL >= 100, 1, 0)
  df_final$DEPENDENCIA_3 <- case_when(df_final$GRUPO_DEPENDENCIA == 1 ~ "pagado",
                                      df_final$GRUPO_DEPENDENCIA == 2 ~ "subvencionado",
                                      df_final$GRUPO_DEPENDENCIA %in% c(3, 4) ~ "publico")
  df_final <- df_final %>%
    select(I, flag_postula, CLEC_REG_ACTUAL, MATE1_REG_ACTUAL, PROMEDIO_NOTAS, PTJE_NEM, PTJE_RANKING,
           PORC_SUP_NOTAS, TP_DUMMY, DEPENDENCIA_3, EDAD_MESES, BEA, RINDE_M2, INGRESO_COLEGIO)
  saveRDS(df_final, rds)
}

d <- df_final %>% filter(!is.na(DEPENDENCIA_3))
d$DEPENDENCIA_3 <- relevel(factor(d$DEPENDENCIA_3), ref = "publico")
d$M1_100 <- d$MATE1_REG_ACTUAL / 100     # M1 en cientos de puntos (para leer betas)
d$LEC_100 <- d$CLEC_REG_ACTUAL / 100

sink(file.path(aqui, "salidas-paes-estudio.txt"))
titulo <- function(x) cat("\n\n==================== ", x, " ====================\n")

titulo("CONTROL DE LA BASE")
cat("N =", nrow(df_final), "| I = 1:", sum(df_final$I), "| tasa:", round(100 * mean(df_final$I), 2), "%\n")
cat("N sin NA en dependencia (el que se usa abajo):", nrow(d), "\n")
print(summary(d %>% select(I, MATE1_REG_ACTUAL, CLEC_REG_ACTUAL, PROMEDIO_NOTAS, EDAD_MESES)))

titulo("M1-M2 · MCO: MATE1 ~ PROMEDIO_NOTAS + TP + DEPENDENCIA_3")
m_mco <- lm(MATE1_REG_ACTUAL ~ PROMEDIO_NOTAS + TP_DUMMY + DEPENDENCIA_3, data = d)
print(summary(m_mco))
titulo("M2 · Prueba F conjunta: H0 las 2 dummies de dependencia = 0")
m_r <- lm(MATE1_REG_ACTUAL ~ PROMEDIO_NOTAS + TP_DUMMY, data = d)
print(anova(m_r, m_mco))
cat("R2 restringido:", round(summary(m_r)$r.squared, 4), "| R2 no restringido:", round(summary(m_mco)$r.squared, 4), "\n")
titulo("M2 · VIF (MCO con las 3 notas juntas: PROMEDIO, NEM, RANKING)")
m_col <- lm(MATE1_REG_ACTUAL ~ PROMEDIO_NOTAS + PTJE_NEM + PTJE_RANKING + TP_DUMMY + DEPENDENCIA_3, data = d)
print(round(coef(summary(m_col)), 4))
print(vif(m_col))
titulo("M2 · Breusch-Pagan (studentizado, LM = n R2) del MCO")
print(bptest(m_mco))
titulo("M2 · Errores usuales vs. robustos HC1 del MCO")
print(coeftest(m_mco))
print(coeftest(m_mco, vcov = vcovHC(m_mco, type = "HC1")))

titulo("M3 · MPL: I ~ M1_100 + LEC_100 + PROMEDIO_NOTAS + TP + DEPENDENCIA_3 (robustos HC1)")
m_mpl <- lm(I ~ M1_100 + LEC_100 + PROMEDIO_NOTAS + TP_DUMMY + DEPENDENCIA_3, data = d)
print(coeftest(m_mpl, vcov = vcovHC(m_mpl, type = "HC1")))
p_mpl <- fitted(m_mpl)
cat("Predicciones < 0:", sum(p_mpl < 0), "| > 1:", sum(p_mpl > 1), "| de", length(p_mpl), "\n")
print(bptest(m_mpl))

titulo("M4 · LOGIT con las mismas X")
m_logit <- glm(I ~ M1_100 + LEC_100 + PROMEDIO_NOTAS + TP_DUMMY + DEPENDENCIA_3, family = binomial(), data = d)
print(summary(m_logit))
cat("Odds ratios exp(b):\n"); print(round(exp(coef(m_logit)), 4))
m_probit <- glm(I ~ M1_100 + LEC_100 + PROMEDIO_NOTAS + TP_DUMMY + DEPENDENCIA_3, family = binomial(link = "probit"), data = d)
cat("\nPROBIT coeficientes:\n"); print(round(coef(m_probit), 4))
cat("Cociente logit/probit:\n"); print(round(coef(m_logit) / coef(m_probit), 2))
cat("Cociente MPL/logit:\n"); print(round(coef(m_mpl) / coef(m_logit), 3))
m0 <- glm(I ~ 1, family = binomial(), data = d)
cat("\nlogL nr:", round(logLik(m_logit), 1), "| logL0:", round(logLik(m0), 1),
    "| RV = 2(Lnr - L0):", round(2 * (logLik(m_logit) - logLik(m0)), 1),
    "| pseudo R2 McFadden:", round(1 - logLik(m_logit) / logLik(m0), 4), "\n")

titulo("M4-M5 · Dos postulantes para calcular P a mano")
perfiles <- data.frame(M1_100 = c(5.0, 7.5), LEC_100 = c(5.5, 7.5), PROMEDIO_NOTAS = c(5.6, 6.5),
                       TP_DUMMY = c(1, 0), DEPENDENCIA_3 = factor(c("publico", "pagado"), levels = levels(d$DEPENDENCIA_3)))
perfiles$z <- predict(m_logit, perfiles, type = "link")
perfiles$P_logit <- predict(m_logit, perfiles, type = "response")
perfiles$P_mpl <- predict(m_mpl, perfiles)
print(perfiles)

titulo("M5 · Efectos parciales del logit: en el promedio (EPeP) vs. promedio (EPP)")
X <- model.matrix(m_logit); b <- coef(m_logit)
xbar <- colMeans(X); zbar <- sum(xbar * b)
epep <- dlogis(zbar) * b
epp <- mean(dlogis(X %*% b)) * b
print(round(data.frame(beta = b, EPeP = epep, EPP = epp), 4))
cat("Factor g(z en el promedio):", round(dlogis(zbar), 4), "| factor promedio:", round(mean(dlogis(X %*% b)), 4), "\n")
# efecto discreto de TP (0 -> 1) en el promedio
x0 <- xbar; x0["TP_DUMMY"] <- 0; x1 <- xbar; x1["TP_DUMMY"] <- 1
cat("Efecto discreto TP en el promedio: G(z1) - G(z0) =", round(plogis(sum(x1 * b)) - plogis(sum(x0 * b)), 4), "\n")

titulo("M6 · Matriz de confusion del logit (corte 0,5 y corte = tasa media)")
p_hat <- fitted(m_logit)
for (corte in c(0.5, round(mean(d$I), 3))) {
  pred <- ifelse(p_hat >= corte, 1, 0)
  tab <- table(real = d$I, predicho = pred)
  cat("\nCorte", corte, "\n"); print(tab)
  VP <- tab["1", "1"]; VN <- tab["0", "0"]; FP <- tab["0", "1"]; FN <- tab["1", "0"]
  cat("Exactitud:", round((VP + VN) / sum(tab), 4), "| Sensibilidad:", round(VP / (VP + FN), 4),
      "| Especificidad:", round(VN / (VN + FP), 4), "| Precision:", round(VP / (VP + FP), 4), "\n")
}
pf <- perf_eva(pred = p_hat, label = d$I, show_plot = FALSE)
cat("\nAUC, KS y Gini (perf_eva):\n"); print(pf$binomial_metric)

titulo("M7 · WOE e IV: tablas para calcular a mano (scorecard usa ln(%I1/%I0))")
bins <- woebin(d %>% select(I, DEPENDENCIA_3, TP_DUMMY, PROMEDIO_NOTAS, EDAD_MESES, MATE1_REG_ACTUAL, CLEC_REG_ACTUAL),
               y = "I", print_step = 0)
for (v in names(bins)) {
  cat("\n--", v, "--\n")
  print(bins[[v]] %>% select(bin, count, count_distr, neg, pos, posprob, woe, bin_iv, total_iv) %>%
          mutate(across(where(is.numeric), ~ round(.x, 4))))
}
bins_edad <- woebin(d %>% select(I, EDAD_MESES), y = "I", breaks_list = list(EDAD_MESES = c(228)), print_step = 0)
cat("\n-- EDAD retramificada (corte 228 meses) --\n")
print(bins_edad$EDAD_MESES %>% select(bin, count, count_distr, neg, pos, posprob, woe, bin_iv, total_iv) %>%
        mutate(across(where(is.numeric), ~ round(.x, 4))))

titulo("M8 · Logit woeizado, train/test 70/30 (semilla 2026), KS/AUC/Gini, PSI y scorecard")
dw <- d %>% select(I, MATE1_REG_ACTUAL, CLEC_REG_ACTUAL, PROMEDIO_NOTAS, TP_DUMMY, DEPENDENCIA_3, EDAD_MESES)
dw$DEPENDENCIA_3 <- as.character(dw$DEPENDENCIA_3)
partes <- split_df(dw, y = "I", ratios = c(0.7, 0.3), seed = 2026)
bins_tr <- woebin(partes$train, y = "I", breaks_list = list(EDAD_MESES = c(228)), print_step = 0)
tr_woe <- woebin_ply(partes$train, bins_tr, print_step = 0)
te_woe <- woebin_ply(partes$test, bins_tr, print_step = 0)
m_woe <- glm(I ~ ., family = binomial(), data = tr_woe)
print(summary(m_woe)$coefficients %>% round(4))
cat("\nVIF del logit woeizado:\n"); print(vif(m_woe, merge_coef = TRUE))
p_tr <- predict(m_woe, tr_woe, type = "response"); p_te <- predict(m_woe, te_woe, type = "response")
ev <- perf_eva(pred = list(train = p_tr, test = p_te), label = list(train = tr_woe$I, test = te_woe$I), show_plot = FALSE)
print(ev$binomial_metric)
# scorecard: 600 puntos con odds 50:1, PDO 20 (los de la clase); scorecard() usa odds0 = malo/bueno
card <- scorecard(bins_tr, m_woe, points0 = 600, odds0 = 1/50, pdo = 20)
cat("\nScorecard (puntos por tramo):\n"); print(bind_rows(card) %>% select(variable, bin, points))
s_tr <- scorecard_ply(partes$train, card); s_te <- scorecard_ply(partes$test, card)
psi <- perf_psi(score = list(train = s_tr, test = s_te), label = list(train = partes$train$I, test = partes$test$I), show_plot = FALSE)
cat("\nPSI train vs. test:\n"); print(psi$pic_data %>% head(0)); print(psi$psi)
sink()
cat("listo\n")
