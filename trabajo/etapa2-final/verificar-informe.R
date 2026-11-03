base <- "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/"
src <- readLines("C:/Proyecto Metodologia de estudio/datos/trabajos/econometria-ii/etapa-2/entrega/codigo-final-etapa-2.R", encoding = "UTF-8")
src <- src[!(grepl("write_xlsx(", src, fixed=TRUE) | grepl("woebin_plot", src, fixed=TRUE) | grepl("boxplot", src, fixed=TRUE))]
pref <- "/Users/david/Desktop/Semestre 2-2026/econometria 2/econometria-ii-demre/datos/crudos/base de datos/"
src <- gsub(paste0(pref, "ArchivoB"), paste0(base, "1-inscritos-archivo-B/ArchivoB"), src, fixed=TRUE)
src <- gsub(paste0(pref, "ArchivoC"), paste0(base, "2-rinden-paes-archivo-C/ArchivoC"), src, fixed=TRUE)
src <- gsub(paste0(pref, "ArchivoD"), paste0(base, "3-postulaciones-archivo-D/ArchivoD"), src, fixed=TRUE)
src <- gsub(paste0(pref, "ArchivoMatr"), paste0(base, "4-matricula/ArchivoMatr"), src, fixed=TRUE)
src <- src[!grepl("rm(list", src, fixed=TRUE)]
# guardar las bases crudas antes de que el código las filtre
i <- grep("^df4 <- read.csv2", src)
src <- append(src, "n_crudo <- c(nrow(df1), nrow(df2), nrow(df3), nrow(df4)); df2_crudo <- df2", after = i)
pdf(NULL)
out <- capture.output(suppressMessages(eval(parse(text = src, encoding = "UTF-8"), envir = globalenv())))

cat("== archivos:", n_crudo, "\n")
d <- df2_crudo
p1 <- d[d$SITUACION_EGRESO == 1, ]
p2 <- p1[p1$SOLO_REGULAR, ]
p3 <- p2[p2$CLEC_REG_ACTUAL >= 100 & p2$MATE1_REG_ACTUAL >= 100, ]
p4 <- p3[p3$CIEN_REG_ACTUAL >= 100 | p3$HCSOC_REG_ACTUAL >= 100, ]
p5 <- p4[p4$PROMEDIO_NOTAS != 0, ]
cat("== filtros:", nrow(p1), nrow(p2), nrow(p3), nrow(p4), nrow(p5), "\n")
cat("== N, Y1, Y0:", nrow(df_final), sum(df_final$PREF_TOP3_DUMMY), sum(1 - df_final$PREF_TOP3_DUMMY), "\n")
pr <- df_final$PREFERENCIA
cat("== pref 1/2/3, >=4, sin matr, no postula:", sum(pr == 1, na.rm=T), sum(pr == 2, na.rm=T), sum(pr == 3, na.rm=T),
    sum(pr >= 4, na.rm=T), sum(is.na(pr)), sum(df_final$FLAG_POSTULA == 0), "\n")
cat("== TP, PACE, BEA, M2:", sum(df_final$TP_DUMMY), sum(df_final$PACE), sum(df_final$BEA), sum(df_final$RINDE_M2), "\n")
cat("== edad max anos:", max(dt$EDAD_MESES, na.rm=T) / 12, "\n")
vv <- c("PROMEDIO_NOTAS","PTJE_NEM","PTJE_RANKING","CLEC_REG_ACTUAL","MATE1_REG_ACTUAL","EDAD_MESES","N_ALUMNOS","INGRESO_COLEGIO")
print(t(sapply(vv, function(v) { x <- dt[[v]]; round(c(min(x,na.rm=T), median(x,na.rm=T), mean(x,na.rm=T), max(x,na.rm=T), atipicos_iqr(x)), 2) })))
tasas <- function(b) paste(round(100 * b$posprob, 1), collapse = " / ")
for (v in c("MATE1_REG_ACTUAL","PROMEDIO_NOTAS","PORC_SUP_NOTAS","INGRESO_COLEGIO","TP_DUMMY","BEA","EDAD_MESES","GRUPO_DEPENDENCIA"))
  cat("== tasas", v, ":", tasas(bins[[v]]), "| bins:", paste(bins[[v]]$bin, collapse=" "), "\n")
cat("== edad retram:", tasas(bins_edad$EDAD_MESES), "| %base:", paste(round(100*bins_edad$EDAD_MESES$count_distr,1), collapse=" "),
    "| IV", round(bins$EDAD_MESES$total_iv[1],3), "->", round(bins_edad$EDAD_MESES$total_iv[1],3), "\n")
cat("== dep3:", tasas(bins_dep$DEPENDENCIA_3), "| bins:", paste(bins_dep$DEPENDENCIA_3$bin, collapse=" "), "\n")
cat("== tasa por GRUPO_DEPENDENCIA:", round(100*tapply(dt$PREF_TOP3_DUMMY, dt$GRUPO_DEPENDENCIA, mean),1), "\n")
cc <- cor(dt_woe[, vars_woe])
cat("== cor NEM-PROM, RANK-PROM, INGCOL-DEP3, PORC-PROM:",
    round(cc["PTJE_NEM_woe","PROMEDIO_NOTAS_woe"],2), round(cc["PTJE_RANKING_woe","PROMEDIO_NOTAS_woe"],2),
    round(cc["INGRESO_COLEGIO_woe","DEPENDENCIA_3_woe"],2), round(cc["PORC_SUP_NOTAS_woe","PROMEDIO_NOTAS_woe"],2), "\n")
