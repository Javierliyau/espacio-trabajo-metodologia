library(readxl)
d <- read_excel("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/final/resultado_final_postulantes.xlsx")
v <- c("MATE1_REG_ACTUAL","PROMEDIO_NOTAS","GRUPO_DEPENDENCIA","INGRESO_PERCAPITA_GRUPO_FA","SEXO")
str(d[, v])
print(table(d$GRUPO_DEPENDENCIA, useNA="ifany"))
print(table(d$INGRESO_PERCAPITA_GRUPO_FA, useNA="ifany"))
print(aggregate(cbind(MATE1_REG_ACTUAL, PROMEDIO_NOTAS) ~ GRUPO_DEPENDENCIA, data=d, FUN=mean))
m1 <- lm(MATE1_REG_ACTUAL ~ PROMEDIO_NOTAS, data=d)
m2 <- lm(MATE1_REG_ACTUAL ~ PROMEDIO_NOTAS + factor(GRUPO_DEPENDENCIA) + factor(INGRESO_PERCAPITA_GRUPO_FA), data=d)
print(coef(summary(m1))); cat("R2 m1:", summary(m1)$r.squared, "n:", nobs(m1), "\n")
print(coef(summary(m2))); cat("R2 m2:", summary(m2)$r.squared, "n:", nobs(m2), "\n")
# mismo n para comparar
m1b <- lm(MATE1_REG_ACTUAL ~ PROMEDIO_NOTAS, data=model.frame(m2))
cat("beta notas m1 en muestra de m2:", coef(m1b)[2], "\n")
# muestra chica: precision vs sesgo
set.seed(1); s <- d[sample(nrow(d), 500), ]
ms <- lm(MATE1_REG_ACTUAL ~ PROMEDIO_NOTAS, data=s); print(coef(summary(ms)))
