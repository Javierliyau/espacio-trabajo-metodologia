# Corre prueba-david.R y exporta tablas (CSV) y gráficos (PNG) para el informe de la Etapa 2.
# Uso: Rscript exportar-informe.R
pdf(NULL)
source("prueba-david.R", echo = FALSE)
dir.create("informe-salidas", showWarnings = FALSE)
setwd("informe-salidas")

# Embudo de filtros
embudo <- data.frame(paso = c("Archivo C (rinden)", "1. Promocion 2025", "2. Rinde por 1.a vez",
                              "3. Lectora y M1 >= 100", "4. Ciencias o Historia >= 100", "5. Notas distintas de 0"),
                     n = c(nrow(df2), nrow(p1), nrow(p2), nrow(p3), nrow(p4), nrow(p5)))
write.csv(embudo, "embudo.csv", row.names = FALSE)

# Composición de I
comp <- base %>%
  mutate(grupo = case_when(I == 1 ~ "I=1: matricula regular en pref. 1-3",
                           flag_postula == 0 & is.na(PREFERENCIA) ~ "I=0: rindio y no postulo",
                           !is.na(PREFERENCIA) ~ "I=0: matricula regular en pref. 4+",
                           TRUE ~ "I=0: postulo y no se matriculo por via regular")) %>%
  count(grupo)
write.csv(comp, "composicion-I.csv", row.names = FALSE)

# Univariado
uni <- lapply(names(dt)[-1], function(v) {
  x <- dt[[v]]
  num <- is.numeric(x)
  data.frame(variable = v, tipo = ifelse(num, "numerica", "categorica"),
             pct_NA = round(100 * mean(is.na(x)), 2),
             min = if (num) min(x, na.rm = TRUE) else NA,
             mediana = if (num) median(x, na.rm = TRUE) else NA,
             media = if (num) round(mean(x, na.rm = TRUE), 2) else NA,
             max = if (num) max(x, na.rm = TRUE) else NA,
             n_categorias = if (!num) length(unique(na.omit(x))) else NA)
})
write.csv(do.call(rbind, uni), "univariado.csv", row.names = FALSE)

tuk <- lapply(numericas, function(v) {
  x <- dt[[v]]; q1 <- quantile(x, .25, na.rm = TRUE); q3 <- quantile(x, .75, na.rm = TRUE); r <- IQR(x, na.rm = TRUE)
  data.frame(variable = v, lim_inf = q1 - 1.5 * r, lim_sup = q3 + 1.5 * r,
             atipicos = sum(x < q1 - 1.5 * r | x > q3 + 1.5 * r, na.rm = TRUE))
})
write.csv(do.call(rbind, tuk), "tukey.csv", row.names = FALSE)

# IV y monotonía
mono <- sapply(tabla_iv$variable, function(v) {
  t <- bins[[v]] %>% filter(bin != "missing"); d <- diff(t$posprob)
  ifelse(all(d >= 0) | all(d <= 0), "si", "no")
})
tabla_iv$monotona <- mono
write.csv(tabla_iv, "iv.csv", row.names = FALSE)

# Tramos de todas las variables (para anexos) y de las retramificadas
tramos <- do.call(rbind, lapply(names(bins), function(v)
  bins[[v]][, c("variable", "bin", "count_distr", "posprob", "woe", "bin_iv", "total_iv")]))
write.csv(tramos, "tramos-woebin.csv", row.names = FALSE)
retr <- rbind(bins_edad$EDAD_MESES, bins_dep$DEPENDENCIA_3)[, c("variable", "bin", "count_distr", "posprob", "woe", "total_iv")]
write.csv(retr, "tramos-retramificados.csv", row.names = FALSE)

# VIF
write.csv(as.data.frame(vif(modelo_iv, merge_coef = TRUE)), "vif-12.csv", row.names = FALSE)
write.csv(as.data.frame(vif(modelo_final, merge_coef = TRUE)), "vif-finales.csv", row.names = FALSE)

# Gráficos
guardar <- function(b, nombre) {
  p <- woebin_plot(b)[[1]]
  ggsave(paste0(nombre, ".png"), p, width = 6, height = 4, dpi = 200)
}
for (v in c("CLEC_REG_ACTUAL", "MATE1_REG_ACTUAL", "PROMEDIO_NOTAS", "TP_DUMMY", "BEA", "RINDE_M2"))
  guardar(bins[v], paste0("woe-", v))
guardar(bins["EDAD_MESES"], "edad-antes")
guardar(bins_edad["EDAD_MESES"], "edad-despues")
guardar(bins["GRUPO_DEPENDENCIA"], "dependencia-antes")
guardar(bins_dep["DEPENDENCIA_3"], "dependencia-despues")
png("boxplot-edad.png", width = 1000, height = 700, res = 150)
boxplot(dt$EDAD_MESES, main = "Edad en meses", horizontal = TRUE); dev.off()
cat("EXPORTADO\n")
