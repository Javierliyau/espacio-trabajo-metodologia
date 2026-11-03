d <- read.csv2("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv")
p1 <- d[d$SITUACION_EGRESO == 1, ]
o <- p1[, which(names(p1) == "CLEC_INV_ACTUAL"):which(names(p1) == "MODULO_INV_ANTERIOR")]
p2 <- p1[apply(o, 1, function(x) sum(!is.na(x) & x != "") == 0), ]
p3 <- p2[p2$CLEC_REG_ACTUAL >= 100 & p2$MATE1_REG_ACTUAL >= 100, ]
p4 <- p3[p3$CIEN_REG_ACTUAL >= 100 | p3$HCSOC_REG_ACTUAL >= 100, ]
p5 <- p4[p4$PROMEDIO_NOTAS != 0, ]
cat(nrow(p1), nrow(p2), nrow(p3), nrow(p4), nrow(p5), "\n")
