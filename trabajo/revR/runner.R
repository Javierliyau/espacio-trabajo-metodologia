B <- "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos"
s <- readLines("C:/Users/javie/Downloads/FINAL FINAL DEFINITIVO econometria_etapa2_codigo_final_final.R", encoding = "UTF-8")
for (n in c("ArchivoB_Adm2026REG.csv","ArchivoC_Adm2026REG.csv","ArchivoD_Adm2026REG.csv","ArchivoMatr_Adm2026.csv")) {
  f <- list.files(B, pattern = paste0("^", n, "$"), recursive = TRUE, full.names = TRUE)[1]
  s <- sub(paste0('"/Users/david/[^"]*', n, '"'), paste0('"', f, '"'), s)
}
s <- s[!grepl("^write_xlsx", s)]
cat(grep("read_csv2", s, value = TRUE), sep = "\n")
pdf(NULL)
t0 <- Sys.time()
eval(parse(text = s, encoding = "UTF-8"))
cat("\n== PACE / BEA ==\n"); print(table(df_final$PACE)); print(table(df_final$BEA))
cat("== problemas readr (df1..df4) ==\n"); for (d in list(df1, df2, df3, df4)) print(nrow(readr::problems(d)))
cat("== iv_tab ==\n"); print(iv_tab)
cat("== x_def ==\n"); print(x_def[order(-x_def$IV), ])
print(Sys.time() - t0)
