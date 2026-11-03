# M1 (19-10): beta con dummy (TP_DUMMY) y con log, base de postulantes
suppressMessages(library(readxl))
d <- read_excel("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/final/resultado_final_postulantes.xlsx")
d <- d[!is.na(d$MATE1_REG_ACTUAL) & d$MATE1_REG_ACTUAL > 0 & !is.na(d$PROMEDIO_NOTAS) & !is.na(d$TP_DUMMY), ]
cat("n =", nrow(d), "\n")
print(aggregate(cbind(MATE1_REG_ACTUAL, PROMEDIO_NOTAS) ~ TP_DUMMY, d, function(x) round(mean(x), 2)))
print(table(d$TP_DUMMY))
m1 <- lm(MATE1_REG_ACTUAL ~ TP_DUMMY, d)
m2 <- lm(MATE1_REG_ACTUAL ~ PROMEDIO_NOTAS + TP_DUMMY, d)
m3 <- lm(log(MATE1_REG_ACTUAL) ~ PROMEDIO_NOTAS, d)
m4 <- lm(log(MATE1_REG_ACTUAL) ~ PROMEDIO_NOTAS + TP_DUMMY, d)
for (m in list(m1, m2, m3, m4)) { print(formula(m)); print(round(summary(m)$coefficients, 4)); cat("R2 =", round(summary(m)$r.squared, 4), "\n\n") }
