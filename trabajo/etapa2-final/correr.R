base <- "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/"
src <- readLines("C:/Users/javie/Downloads/econometria_etapa2_codigo_final.R", encoding = "UTF-8")
src <- src[!(grepl("write_xlsx(", src, fixed=TRUE) | grepl("woebin_plot", src, fixed=TRUE) | grepl("boxplot", src, fixed=TRUE))]
pref <- "/Users/david/Desktop/Semestre 2-2026/econometria 2/econometria-ii-demre/datos/crudos/base de datos/"
src <- gsub(paste0(pref, "ArchivoB"), paste0(base, "1-inscritos-archivo-B/ArchivoB"), src, fixed=TRUE)
src <- gsub(paste0(pref, "ArchivoC"), paste0(base, "2-rinden-paes-archivo-C/ArchivoC"), src, fixed=TRUE)
src <- gsub(paste0(pref, "ArchivoD"), paste0(base, "3-postulaciones-archivo-D/ArchivoD"), src, fixed=TRUE)
src <- gsub(paste0(pref, "ArchivoMatr"), paste0(base, "4-matricula/ArchivoMatr"), src, fixed=TRUE)
src <- src[!grepl("rm(list", src, fixed=TRUE)]
print(grep("read_csv2", src, value=TRUE))
pdf(NULL)
out <- capture.output(suppressMessages(eval(parse(text = src, encoding="UTF-8"), envir = globalenv())))
cat("N =", nrow(df_final), " Y1 =", sum(df_final$PREF_TOP3_DUMMY), "\n")
print(iv_tab)
print(monotonia)
cat("vars_iv:", vars_iv, "\n")
# camino del codigo (automatico) ya corrido: vars_sel
cat("vars_sel automatico:", vars_sel, "\n")
# camino del grupo: NEM, RANKING, luego ING_COL, luego PORC_SUP
pasos <- function(sacar) {
  vs <- vars_iv
  for (s in c(sacar, NA)) {
    m <- glm(as.formula(paste("PREF_TOP3_DUMMY ~", paste(paste0(vs, "_woe"), collapse=" + "))), family=binomial(), data=dt_woe)
    v <- suppressMessages(vif(m)); v$variable <- sub("_woe$","",v$variable)
    v <- merge(v, iv_tab[,c("variable","IV")], by="variable"); v$ratio <- v$gvif/v$IV
    print(v[order(-v$ratio), c("variable","gvif","IV","ratio")])
    if (!is.na(s)) { cat(">>> sale", s, "\n"); vs <- setdiff(vs, s) }
  }
  vs
}
fin <- pasos(c("PTJE_NEM","PTJE_RANKING","INGRESO_COLEGIO","PORC_SUP_NOTAS"))
print(setequal(fin, x_finales))
print(round(summary(modelo_final)$coefficients, 4)); print(vif(modelo_final))
# consistencia
cat("dupID", sum(duplicated(df_final$ID_aux)), " prom", sum(dt$PROMEDIO_NOTAS<4|dt$PROMEDIO_NOTAS>7), " nem", sum(dt$PTJE_NEM<100|dt$PTJE_NEM>1000),
    " <16", sum(dt$EDAD_MESES<192,na.rm=T), " >=20", sum(dt$EDAD_MESES>=240,na.rm=T), " >=30", sum(dt$EDAD_MESES>=360,na.rm=T), "\n")
print(reglas)
print(inspeccion[inspeccion$n_na>0, c("variable","n_na","pct_na")])
print(sapply(dt[, vars_num], atipicos_iqr))
print(bins_dep$DEPENDENCIA_3[, c("bin","count","posprob","total_iv")])
