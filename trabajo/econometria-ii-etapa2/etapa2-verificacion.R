# Verificación del instructivo Etapa 2 (Econometría II, Pfeng) — 23-10-2026
# Reproduce la base del profesor (clase 5, 22-10) y corre el análisis bivariado.
suppressPackageStartupMessages({library(tidyverse); library(scorecard)})
options(width = 160, scipen = 999)
ruta <- "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/"

# ---------- Paso 0: leer ----------
A  <- read_csv2(paste0(ruta, "2-rinden-paes-archivo-C/ArchivoC_Adm2026REG.csv"), show_col_types = FALSE)
Bi <- read_csv2(paste0(ruta, "1-inscritos-archivo-B/ArchivoB_Adm2026REG.csv"), show_col_types = FALSE)
B  <- read_csv2(paste0(ruta, "3-postulaciones-archivo-D/ArchivoD_Adm2026REG.csv"), show_col_types = FALSE)
C  <- read_csv2(paste0(ruta, "4-matricula/ArchivoMatr_Adm2026.csv"), show_col_types = FALSE)
cat("A:", nrow(A), " B:", nrow(B), " C:", nrow(C), " inscritos:", nrow(Bi), "\n")

# ---------- Paso 1: filtros en A ----------
cols_prev <- names(A)[str_detect(names(A), "_(REG|INV)_ANTERIOR$|_INV_ACTUAL$")]
emb <- c(inicial = nrow(A))
A1 <- A %>% filter(SITUACION_EGRESO == 1);                       emb["egreso"] <- nrow(A1)
A1 <- A1 %>% filter(if_all(all_of(cols_prev), is.na));           emb["primera_vez"] <- nrow(A1)
A1 <- A1 %>% filter(CLEC_REG_ACTUAL >= 100, MATE1_REG_ACTUAL >= 100); emb["obligatorias"] <- nrow(A1)
A1 <- A1 %>% filter(CIEN_REG_ACTUAL >= 100 | HCSOC_REG_ACTUAL >= 100); emb["electiva"] <- nrow(A1)
A1 <- A1 %>% filter(PROMEDIO_NOTAS != 0);                        emb["notas"] <- nrow(A1)
print(emb)

# ---------- Paso 2: B' y flag_postula ----------
B_unico <- unique(B$ID_aux); cat("postulantes unicos:", length(B_unico), "\n")
A2 <- A1 %>% mutate(flag_postula = as.integer(ID_aux %in% B_unico))
print(table(A2$flag_postula))

# ---------- Paso 3: C' y left_join; I ----------
C1 <- C %>% filter(VIA == 1, TIPO_MATRICULA == 1) %>% select(ID_aux, PREFERENCIA)
cat("C filtrado:", nrow(C1), " IDs repetidos:", sum(duplicated(C1$ID_aux)), "\n")
base <- A2 %>% left_join(C1, by = "ID_aux") %>%
  mutate(I = as.integer(PREFERENCIA %in% 1:3))
cat("N:", nrow(base), "\n"); print(table(base$I)); print(round(100 * prop.table(table(base$I)), 2))
print(table(postula = base$flag_postula, I = base$I))

# ---------- Paso 4: X candidatas ----------
colegio <- Bi %>% filter(!is.na(RBD)) %>%
  mutate(INGRESO_PERCAPITA_GRUPO_FA = na_if(INGRESO_PERCAPITA_GRUPO_FA, 99)) %>%
  group_by(RBD) %>% summarise(N_ALUMNOS = n(), INGRESO_COLEGIO = median(INGRESO_PERCAPITA_GRUPO_FA, na.rm = TRUE))
ins <- Bi %>% select(ID_aux, FECHA_NACIMIENTO, SEXO, PACE, BEA, INGRESO_PERCAPITA_GRUPO_FA, REGIMEN) %>%
  mutate(INGRESO_PERCAPITA_GRUPO_FA = na_if(INGRESO_PERCAPITA_GRUPO_FA, 99),
         PACE = as.integer(!is.na(PACE)), BEA = as.integer(!is.na(BEA)),
         mes = as.integer(substr(FECHA_NACIMIENTO, 1, 2)), anio = as.integer(substr(FECHA_NACIMIENTO, 3, 6)),
         EDAD_MESES = (2025 - anio) * 12 + (12 - mes))
dt <- base %>%
  left_join(ins, by = "ID_aux") %>%
  left_join(colegio, by = "RBD") %>%
  mutate(TP_DUMMY = as.integer(str_starts(RAMA_EDUCACIONAL, "T")),
         RINDE_CIEN = as.integer(CIEN_REG_ACTUAL >= 100), RINDE_HCSOC = as.integer(HCSOC_REG_ACTUAL >= 100),
         RINDE_M2 = as.integer(MATE2_REG_ACTUAL >= 100), GRUPO_DEPENDENCIA = as.character(GRUPO_DEPENDENCIA),
         CODIGO_REGION = as.character(CODIGO_REGION), SEXO = as.character(SEXO)) %>%
  select(ID_aux, I, PROMEDIO_NOTAS, PORC_SUP_NOTAS, PTJE_NEM, PTJE_RANKING, CLEC_REG_ACTUAL, MATE1_REG_ACTUAL,
         RINDE_CIEN, RINDE_HCSOC, RINDE_M2, GRUPO_DEPENDENCIA, TP_DUMMY, CODIGO_REGION, SEXO, PACE, BEA,
         INGRESO_PERCAPITA_GRUPO_FA, EDAD_MESES, N_ALUMNOS, INGRESO_COLEGIO, flag_postula)

# ---------- Etapa 2a: univariado ----------
cat("\n% NA por variable:\n"); print(round(100 * colMeans(is.na(dt)), 2))
tukey <- function(x) { q <- quantile(x, c(.25, .75), na.rm = TRUE); r <- q[2] - q[1]
  c(lim_inf = unname(q[1] - 1.5 * r), lim_sup = unname(q[2] + 1.5 * r), n_fuera = sum(x < q[1] - 1.5 * r | x > q[2] + 1.5 * r, na.rm = TRUE),
    min = min(x, na.rm = TRUE), max = max(x, na.rm = TRUE)) }
num <- c("PROMEDIO_NOTAS", "PTJE_NEM", "PTJE_RANKING", "CLEC_REG_ACTUAL", "MATE1_REG_ACTUAL", "EDAD_MESES", "N_ALUMNOS", "INGRESO_COLEGIO")
print(round(t(sapply(dt[num], tukey)), 2))

# ---------- Etapa 2b: bivariado con woebin ----------
bins <- woebin(dt, y = "I", var_skip = c("ID_aux", "flag_postula"), print_step = 0)
iv <- map_dfr(bins, ~ tibble(variable = .x$variable[1], IV = .x$total_iv[1], tramos = nrow(.x))) %>% arrange(desc(IV)) %>%
  mutate(clase = cut(IV, c(-Inf, .02, .1, .3, .5, Inf), c("inutil", "debil", "medio", "fuerte", "sospechoso"), right = FALSE))
print(iv, n = 50)
mono <- map_dfr(bins, function(b) { r <- b %>% filter(bin != "missing") %>% pull(posprob); d <- diff(r)
  tibble(variable = b$variable[1], monotona = all(d >= 0) || all(d <= 0), tasa_por_tramo = paste(round(100 * r, 1), collapse = " | ")) })
print(mono, n = 50, width = 200)
for (v in c("EDAD_MESES", "PTJE_RANKING", "INGRESO_PERCAPITA_GRUPO_FA")) print(bins[[v]][, c("variable", "bin", "count", "count_distr", "posprob", "woe", "bin_iv")])
saveRDS(list(dt = dt, bins = bins, iv = iv), "etapa2-verificacion.rds")
