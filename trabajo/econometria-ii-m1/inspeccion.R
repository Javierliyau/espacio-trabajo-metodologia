library(readxl)
for (f in c("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/final/resultado_final_postulantes.xlsx",
            "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/final/resultado_final.xlsx")) {
  cat("==", basename(f), "\n"); print(excel_sheets(f))
  d <- read_excel(f, sheet = 1)
  cat("filas:", nrow(d), " cols:", ncol(d), "\n"); print(names(d))
}
