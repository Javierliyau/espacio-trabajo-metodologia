base <- "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/"
src <- readLines("C:/Proyecto Metodologia de estudio/datos/trabajos/econometria-ii/etapa-2/entrega/codigo-final-etapa-2.R", encoding = "UTF-8")
src <- src[!(grepl("write_xlsx(", src, fixed=TRUE) | grepl("woebin_plot", src, fixed=TRUE) | grepl("boxplot", src, fixed=TRUE))]
pref <- "/Users/david/Desktop/Semestre 2-2026/econometria 2/econometria-ii-demre/datos/crudos/base de datos/"
src <- gsub(paste0(pref, "ArchivoB"), paste0(base, "1-inscritos-archivo-B/ArchivoB"), src, fixed=TRUE)
src <- gsub(paste0(pref, "ArchivoC"), paste0(base, "2-rinden-paes-archivo-C/ArchivoC"), src, fixed=TRUE)
src <- gsub(paste0(pref, "ArchivoD"), paste0(base, "3-postulaciones-archivo-D/ArchivoD"), src, fixed=TRUE)
src <- gsub(paste0(pref, "ArchivoMatr"), paste0(base, "4-matricula/ArchivoMatr"), src, fixed=TRUE)
src <- src[!grepl("rm(list", src, fixed=TRUE)]
pdf(NULL)
out <- capture.output(suppressMessages(eval(parse(text = src, encoding="UTF-8"), envir = globalenv())))
cat(out[grepl("Se elimina|Ninguna", out)], sep = "\n")
cat("N =", nrow(df_final), " Y1 =", sum(df_final$PREF_TOP3_DUMMY), "\n")
print(reglas)
print(inspeccion[inspeccion$n_na > 0, c("variable", "n_na", "pct_na")])
print(iv_tab)
print(monotonia)
cat("vars_sel:", vars_sel, "\n")
print(setdiff(vars_sel, x_finales)); print(setdiff(x_finales, vars_sel))
print(vif(m_full, merge_coef = TRUE))
print(round(summary(modelo_final)$coefficients, 4))
print(vif(modelo_final, merge_coef = TRUE))
