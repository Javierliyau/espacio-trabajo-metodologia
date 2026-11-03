B <- "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos"
s <- readLines("C:/Users/javie/Downloads/FINAL FINAL DEFINITIVO econometria_etapa2_codigo_final_final.R", encoding = "UTF-8")
for (n in c("ArchivoB_Adm2026REG.csv","ArchivoC_Adm2026REG.csv","ArchivoD_Adm2026REG.csv","ArchivoMatr_Adm2026.csv")) {
  f <- list.files(B, pattern = paste0("^", n, "$"), recursive = TRUE, full.names = TRUE)[1]
  s <- sub(paste0('"/Users/david/[^"]*', n, '"'), paste0('"', f, '"'), s)
}
s <- s[!grepl("^write_xlsx", s)]
cat(grep("read_csv2", s, value = TRUE), sep = "\n")
pdf(NULL)

eval(parse(text = s, encoding = "UTF-8"))
cat("\n== PACE / BEA ==\n"); print(table(df_final$PACE)); print(table(df_final$BEA))
cat("== problemas readr (df1..df4) ==\n"); for (d in list(df1, df2, df3, df4)) print(nrow(readr::problems(d)))
cat("== iv_tab ==\n"); print(iv_tab)
cat("== x_def ==\n"); print(x_def[order(-x_def$IV), ])

cat("\n== N TP, M2 ==\n"); print(sum(df_final$TP_DUMMY)); print(sum(df_final$RINDE_M2, na.rm=TRUE))
cat("== pref ==\n"); print(table(df_final$PREFERENCIA, useNA="ifany")); print(table(df_final$FLAG_POSTULA, df_final$PREF_TOP3_DUMMY))
cat("== NA ==\n"); print(inspeccion[inspeccion$n_na > 0, c("variable","n_na","pct_na")])
cat("== summary ==\n"); print(sapply(dt[, intersect(vars_num, names(dt))], function(x) c(min=min(x,na.rm=T), med=median(x,na.rm=T), mean=mean(x,na.rm=T), max=max(x,na.rm=T))))
cat("== atipicos ==\n"); print(sapply(dt[, intersect(vars_num, names(dt))], atipicos_iqr))
cat("== reglas ==\n"); print(reglas); print(max(dt$EDAD_MESES, na.rm=TRUE)/12)
cat("== tasas por tramo ==\n"); for (v in c("MATE1_REG_ACTUAL","PROMEDIO_NOTAS","PORC_SUP_NOTAS","INGRESO_COLEGIO","TP_DUMMY","BEA","EDAD_MESES")) { cat(v, ":", round(100*bins[[v]]$posprob,1), "\n") }
cat("edad retram:", round(100*bins_edad$EDAD_MESES$posprob,1), round(100*bins_edad$EDAD_MESES$count_distr,1), bins_edad$EDAD_MESES$total_iv[1], "\n")
cat("dep orig:", paste(bins$GRUPO_DEPENDENCIA$bin, round(100*bins$GRUPO_DEPENDENCIA$posprob,1)), "\n")
cat("dep3:", paste(bins_dep$DEPENDENCIA_3$bin, round(100*bins_dep$DEPENDENCIA_3$posprob,1)), "\n")
cat("monotonia:\n"); print(monotonia)
