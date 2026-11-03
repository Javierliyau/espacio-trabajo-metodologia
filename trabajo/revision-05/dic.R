library(readxl)
f <- "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/1-inscritos-archivo-B/Libro_CódigosADM2026_ArchivoB.xlsx"
for (s in excel_sheets(f)) { x <- read_excel(f, sheet=s, col_names=FALSE); x <- as.data.frame(x)
  idx <- which(apply(x,1,function(r) any(grepl("RINDIO_PROCESO_ACTUAL|SITUACION_EGRESO|INGRESO_PERCAPITA", r))))
  for (i in idx) print(x[i:min(i+6,nrow(x)),], right=FALSE) }
