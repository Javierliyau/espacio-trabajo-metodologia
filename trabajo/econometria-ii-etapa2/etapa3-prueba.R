suppressPackageStartupMessages({library(tidyverse); library(scorecard)})
v <- readRDS("etapa2-verificacion.rds"); dt <- v$dt; bins <- v$bins
b2 <- woebin(dt, y = "I", x = "EDAD_MESES", breaks_list = list(EDAD_MESES = c(228)), print_step = 0)
x_fin <- c("CLEC_REG_ACTUAL","MATE1_REG_ACTUAL","PROMEDIO_NOTAS","TP_DUMMY","GRUPO_DEPENDENCIA","EDAD_MESES","BEA","RINDE_M2")
bins_fin <- bins[x_fin]; bins_fin$EDAD_MESES <- b2$EDAD_MESES
dl <- split_df(dt[, c("I", x_fin)], y = "I", ratio = 0.7, seed = 2026)
cat("tasa train:", mean(dl$train$I), " test:", mean(dl$test$I), " n:", nrow(dl$train), nrow(dl$test), "\n")
tr <- woebin_ply(dl$train, bins_fin, print_step = 0); te <- woebin_ply(dl$test, bins_fin, print_step = 0)
f <- as.formula(paste("I ~", paste(paste0(x_fin, "_woe"), collapse = " + ")))
m1 <- glm(f, family = binomial(), data = tr)
m2 <- step(m1, direction = "both", trace = 0)
top <- v$iv %>% filter(variable %in% x_fin) %>% slice_max(IV, n = 6) %>% pull(variable)
m3 <- glm(as.formula(paste("I ~", paste(paste0(top, "_woe"), collapse = " + "))), family = binomial(), data = tr)
print(AIC(m1, m2, m3)); print(BIC(m1, m2, m3)); print(formula(m2))
for (m in list(m1, m2, m3)) { a <- perf_eva(pred = predict(m, tr, type = "response"), label = tr$I, show_plot = FALSE)$binomial_metric$dat
  b <- perf_eva(pred = predict(m, te, type = "response"), label = te$I, show_plot = FALSE)$binomial_metric$dat
  print(rbind(train = a, test = b)) }
