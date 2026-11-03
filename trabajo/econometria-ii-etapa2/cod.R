suppressPackageStartupMessages(library(readxl))
p <- "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/"
f <- list.files(p, pattern = "ArchivoC.xlsx|ArchivoB.xlsx", recursive = TRUE, full.names = TRUE)
for (ff in f) for (s in excel_sheets(ff)) { d <- read_excel(ff, sheet = s, col_names = FALSE); d <- as.data.frame(lapply(d, as.character))
  i <- which(apply(d, 1, function(r) any(grepl("GRUPO_DEPENDENCIA|RAMA_EDUCACIONAL|SITUACION_EGRESO", r))))
  for (k in i) print(d[k:min(k+8, nrow(d)), 1:min(5, ncol(d))]) }
