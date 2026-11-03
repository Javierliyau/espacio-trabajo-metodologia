# Ejemplo con datos reales: retramificar, VIF y adelanto de la Etapa 3 (solo para verificar el código del instructivo)
suppressPackageStartupMessages({library(tidyverse); library(scorecard)})
options(width = 160, scipen = 999)
v <- readRDS("etapa2-verificacion.rds"); dt <- v$dt; bins <- v$bins
cols <- c("variable", "bin", "count", "count_distr", "posprob", "woe", "bin_iv", "total_iv")
for (x in c("CLEC_REG_ACTUAL", "GRUPO_DEPENDENCIA", "TP_DUMMY", "BEA", "INGRESO_COLEGIO", "PORC_SUP_NOTAS")) print(bins[[x]][, ..cols])

# Retramificar EDAD_MESES: 3 tramos no monótonos -> 2 tramos
b2 <- woebin(dt, y = "I", x = "EDAD_MESES", breaks_list = list(EDAD_MESES = c(228)), print_step = 0)
print(b2$EDAD_MESES[, ..cols])

# X que pasan el filtro IV >= 0,02 (sin INGRESO_PERCAPITA por NA > 5 %)
x_ok <- c("CLEC_REG_ACTUAL", "MATE1_REG_ACTUAL", "PROMEDIO_NOTAS", "PTJE_NEM", "PTJE_RANKING", "PORC_SUP_NOTAS",
          "TP_DUMMY", "INGRESO_COLEGIO", "GRUPO_DEPENDENCIA", "EDAD_MESES", "BEA", "RINDE_M2")
bins_aj <- bins[x_ok]; bins_aj$EDAD_MESES <- b2$EDAD_MESES
dt_woe <- woebin_ply(dt[, c("I", x_ok)], bins_aj, print_step = 0)
f <- as.formula(paste("I ~", paste(paste0(x_ok, "_woe"), collapse = " + ")))
m <- glm(f, family = binomial(), data = dt_woe)
print(vif(m, merge_coef = TRUE))
print(round(cor(dt_woe[, -1])[c("PROMEDIO_NOTAS_woe", "PTJE_NEM_woe", "PTJE_RANKING_woe"), c("PROMEDIO_NOTAS_woe", "PTJE_NEM_woe", "PTJE_RANKING_woe", "PORC_SUP_NOTAS_woe")], 3))
