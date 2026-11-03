suppressPackageStartupMessages({library(tidyverse); library(scorecard)})
v <- readRDS("etapa2-verificacion.rds"); dt <- v$dt; bins <- v$bins
b2 <- woebin(dt, y = "I", x = "EDAD_MESES", breaks_list = list(EDAD_MESES = c(228)), print_step = 0)
x_ok <- c("CLEC_REG_ACTUAL","MATE1_REG_ACTUAL","PROMEDIO_NOTAS","PORC_SUP_NOTAS","TP_DUMMY","INGRESO_COLEGIO","GRUPO_DEPENDENCIA","EDAD_MESES","BEA","RINDE_M2")
bins_aj <- bins[x_ok]; bins_aj$EDAD_MESES <- b2$EDAD_MESES
dt_woe <- woebin_ply(dt[, c("I", x_ok)], bins_aj, print_step = 0)
f <- as.formula(paste("I ~", paste(paste0(x_ok, "_woe"), collapse = " + ")))
print(vif(glm(f, family = binomial(), data = dt_woe), merge_coef = TRUE))
print(round(cor(dt_woe$INGRESO_COLEGIO_woe, dt_woe$GRUPO_DEPENDENCIA_woe),3))
