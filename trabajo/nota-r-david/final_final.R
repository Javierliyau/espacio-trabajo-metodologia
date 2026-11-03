############## ECONOMETRÍA II — USACH #######################
############## TRABAJO: ETAPA 2 #######################
# Nombres: David Cuevas, Javier Li-Yau, Benjamín Lizana y Ana Nacif
# Modelo logit con WOE. Variable objetivo: PREF_TOP3_DUMMY
# (1 = quedó matriculado en una de sus 3 primeras preferencias)

rm(list = ls())
bf <- function(n) list.files("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos", pattern = paste0("^", n, "$"), recursive = TRUE, full.names = TRUE)[1]

library(writexl)
library(tidyverse)
library(scorecard)

options(scipen = 999, digits = 4)
set.seed(2026)

# read.csv2: separador ";" y decimales con coma, como vienen los archivos del DEMRE
df1 <- read.csv2(bf("ArchivoB_Adm2026REG.csv"))
df2 <- read.csv2(bf("ArchivoC_Adm2026REG.csv"))
df3 <- read.csv2(bf("ArchivoD_Adm2026REG.csv"))
df4 <- read.csv2(bf("ArchivoMatr_Adm2026.csv"))

############## VARIABLES DEL COLEGIO #######################
# 99 = "prefiero no responder" -> NA
df1 <- df1 %>%
  mutate(INGRESO_PERCAPITA_GRUPO_FA = ifelse(INGRESO_PERCAPITA_GRUPO_FA == 99, NA,
                                             INGRESO_PERCAPITA_GRUPO_FA))

# N_MATRICULADOS no se incluye: se conoce después de la matrícula (ex post)
colegio <- df1 %>%
  filter(!is.na(RBD)) %>%
  group_by(RBD) %>%
  summarise(N_ALUMNOS = n(),
            INGRESO_COLEGIO = median(INGRESO_PERCAPITA_GRUPO_FA, na.rm = TRUE))


############## FILTRAR DATOS #######################
df1 <- df1 %>%
  select(ID_aux, FECHA_NACIMIENTO, RBD, RAMA_EDUCACIONAL, GRUPO_DEPENDENCIA,
         CODIGO_REGION, SEXO, PACE, BEA, INGRESO_PERCAPITA_GRUPO_FA)

# Solo rinden la regular actual: todas las columnas de invierno y del año
# anterior vacías (read.csv2 deja "" en las de texto, por eso se revisan las dos cosas)
otras <- df2 %>% select(CLEC_INV_ACTUAL:MODULO_INV_ANTERIOR)
df2$SOLO_REGULAR <- apply(otras, 1, function(x) sum(!is.na(x) & x != "") == 0)

# Base maestra: los que rinden (df2)
df2 <- df2 %>%
  filter(SITUACION_EGRESO == 1) %>%
  filter(SOLO_REGULAR) %>%
  filter(CLEC_REG_ACTUAL >= 100, MATE1_REG_ACTUAL >= 100) %>%
  filter(CIEN_REG_ACTUAL >= 100 | HCSOC_REG_ACTUAL >= 100) %>%
  filter(PROMEDIO_NOTAS != 0) %>%
  select(ID_aux, PROMEDIO_NOTAS, PORC_SUP_NOTAS, PTJE_NEM, PTJE_RANKING,
         CLEC_REG_ACTUAL, MATE1_REG_ACTUAL, CIEN_REG_ACTUAL, HCSOC_REG_ACTUAL,
         MATE2_REG_ACTUAL)

# Postulaciones: solo se marca si postuló; el que no postuló queda con Y = 0
df3 <- df3 %>%
  distinct(ID_aux) %>%
  mutate(FLAG_POSTULA = 1)

# El filtro de vía y tipo se hace en la matrícula, no en la base
df4 <- df4 %>%
  filter(VIA == 1 & TIPO_MATRICULA == 1) %>%
  select(ID_aux, PREFERENCIA)

# all.x = TRUE: se queda todo el que rinde, aunque no cruce con las otras bases
df_final <- merge(df2, df1, by = "ID_aux", all.x = TRUE)
df_final <- merge(df_final, df3, by = "ID_aux", all.x = TRUE)
df_final <- merge(df_final, df4, by = "ID_aux", all.x = TRUE)
df_final <- merge(df_final, colegio, by = "RBD", all.x = TRUE)
nrow(df_final)


################ CREACIÓN DE VARIABLES ########################
df_final$PREF_TOP3_DUMMY <- ifelse(df_final$PREFERENCIA %in% c(1, 2, 3), 1, 0)
table(df_final$PREF_TOP3_DUMMY)

df_final$FLAG_POSTULA <- ifelse(is.na(df_final$FLAG_POSTULA), 0, 1)
table(df_final$FLAG_POSTULA, df_final$PREF_TOP3_DUMMY)

df_final$TP_DUMMY <- ifelse(df_final$RAMA_EDUCACIONAL %in% c("T1", "T2", "T3", "T4", "T5"), 1, 0)

# vacío = no tiene el beneficio
df_final$PACE <- ifelse(is.na(df_final$PACE) | df_final$PACE == "", 0, 1)
df_final$BEA  <- ifelse(is.na(df_final$BEA) | df_final$BEA == "", 0, 1)

df_final$RINDE_CIEN  <- ifelse(df_final$CIEN_REG_ACTUAL >= 100, 1, 0)
df_final$RINDE_HCSOC <- ifelse(df_final$HCSOC_REG_ACTUAL >= 100, 1, 0)
df_final$RINDE_M2    <- ifelse(df_final$MATE2_REG_ACTUAL >= 100, 1, 0)

# FECHA_NACIMIENTO
fecha <- as.numeric(df_final$FECHA_NACIMIENTO)
df_final$EDAD_MESES <- (2025 - fecha %% 10000) * 12 + (12 - fecha %/% 10000)

# Las categóricas como texto para que woebin no las corte como número
df_final$GRUPO_DEPENDENCIA <- as.character(df_final$GRUPO_DEPENDENCIA)
df_final$CODIGO_REGION     <- as.character(df_final$CODIGO_REGION)
df_final$SEXO              <- as.character(df_final$SEXO)

write_xlsx(df_final, file.path(tempdir(), "base.xlsx"))


# =============================================================================
# 1. DESCRIPCIÓN DE LOS DATOS Y TASA DE Y = 1
# =============================================================================
dt <- df_final %>%
  select(PREF_TOP3_DUMMY, PROMEDIO_NOTAS, PORC_SUP_NOTAS, PTJE_NEM, PTJE_RANKING,
         CLEC_REG_ACTUAL, MATE1_REG_ACTUAL, RINDE_CIEN, RINDE_HCSOC, RINDE_M2,
         GRUPO_DEPENDENCIA, TP_DUMMY, CODIGO_REGION, SEXO, PACE, BEA,
         INGRESO_PERCAPITA_GRUPO_FA, EDAD_MESES, N_ALUMNOS, INGRESO_COLEGIO)

dim(dt)
cat("Tasa de Y = 1 (top 3):", round(100 * mean(dt$PREF_TOP3_DUMMY), 1), "%\n")

# =============================================================================
# 2. INSPECCIÓN DE COLUMNAS
# =============================================================================

# 2.1 Resumen por columna: tipo, faltantes, valores distintos y rango
inspeccion <- data.frame(
  variable  = names(dt),
  tipo      = sapply(dt, function(x) class(x)[1]),
  n_na      = sapply(dt, function(x) sum(is.na(x))),
  pct_na    = sapply(dt, function(x) round(100 * mean(is.na(x)), 2)),
  n_unicos  = sapply(dt, function(x) length(unique(x))),
  minimo    = sapply(dt, function(x) if (is.numeric(x)) min(x, na.rm = TRUE) else NA),
  maximo    = sapply(dt, function(x) if (is.numeric(x)) max(x, na.rm = TRUE) else NA),
  row.names = NULL
)
inspeccion

# Más de 5 % de NA -> la variable no se usa
vars_na_alto <- inspeccion$variable[inspeccion$pct_na > 5]
vars_na_alto   # INGRESO_PERCAPITA_GRUPO_FA (27,66 %)

# Numéricas continuas: descriptivos y atípicos por regla de Tukey
vars_num <- names(dt)[sapply(dt, is.numeric)]
vars_num <- setdiff(vars_num, "PREF_TOP3_DUMMY")
vars_num <- vars_num[sapply(dt[, vars_num], function(x) length(unique(x)) > 2)]
summary(dt[, vars_num])

atipicos_iqr <- function(x) {
  q   <- quantile(x, c(0.25, 0.75), na.rm = TRUE)
  ric <- q[2] - q[1]
  sum(x < q[1] - 1.5 * ric | x > q[2] + 1.5 * ric, na.rm = TRUE)
}
sapply(dt[, vars_num], atipicos_iqr)


# 10 numéricas continuas -> 2 filas de 5
par(mfrow = c(2, 5))
for (v in vars_num) boxplot(dt[[v]], main = v, cex.main = 0.7, col = "lightblue")
par(mfrow = c(1, 1))

#Cualitativas
vars_cat <- names(dt)[sapply(dt, function(x) is.factor(x) | is.character(x))]
for (v in vars_cat) {
  cat("\n---", v, "---\n")
  print(table(dt[[v]], useNA = "ifany"))
}

#Consistencia: repetidos y valores fuera de la escala oficial
reglas <- data.frame(
  regla = c("ID_aux duplicado",
            "Promedio de notas fuera de 4,0 a 7,0",
            "Puntaje NEM fuera de 100 a 1.000",
            "Edad menor de 16 años",
            "Edad de 20 años o más",
            "Edad de 30 años o más"),
  casos = c(sum(duplicated(df_final$ID_aux)),
            sum(dt$PROMEDIO_NOTAS < 4 | dt$PROMEDIO_NOTAS > 7, na.rm = TRUE),
            sum(dt$PTJE_NEM < 100 | dt$PTJE_NEM > 1000, na.rm = TRUE),
            sum(dt$EDAD_MESES < 16 * 12, na.rm = TRUE),
            sum(dt$EDAD_MESES >= 20 * 12, na.rm = TRUE),
            sum(dt$EDAD_MESES >= 30 * 12, na.rm = TRUE))
)
reglas
max(dt$EDAD_MESES, na.rm = TRUE) / 12   # edad máxima en años
# no se elimina ninguno: las edades altas son egresados de educación de adultos

# =============================================================================
# 3. EXCLUSIÓN DE VARIABLES CON MÁS DE 5 % DE NA
# =============================================================================
dt <- dt[, setdiff(names(dt), vars_na_alto)]
colSums(is.na(dt))[colSums(is.na(dt)) > 0]

# =============================================================================
# 4. BINNING (WOE) E INFORMATION VALUE CON scorecard
# =============================================================================
# woe = ln(%Y1 / %Y0): WOE positivo = tramo con más matrícula en el top 3
bins <- woebin(dt, y = "PREF_TOP3_DUMMY")

woebin_plot(bins$CLEC_REG_ACTUAL)
woebin_plot(bins$MATE1_REG_ACTUAL)
woebin_plot(bins$PROMEDIO_NOTAS)
woebin_plot(bins$TP_DUMMY)

# Monotonía: la tasa de Y = 1 por tramo debe subir siempre o bajar siempre
monotonia <- data.frame(
  variable = names(bins),
  monotona = sapply(bins, function(b) {
    tasa <- b$posprob[b$bin != "missing"]
    sum(diff(tasa) < 0) == 0 | sum(diff(tasa) > 0) == 0
  }),
  row.names = NULL
)
monotonia

# =============================================================================
# 5. RETRAMIFICACIÓN
# =============================================================================

# Edad: la tasa sube y baja -> un solo corte en 228 meses (19 años)
woebin_plot(bins$EDAD_MESES)
bins_edad <- woebin(dt, y = "PREF_TOP3_DUMMY", x = "EDAD_MESES",
                    breaks_list = list(EDAD_MESES = c(228)))
woebin_plot(bins_edad$EDAD_MESES)

#Dependencia: municipal (3) y SLEP (4) juntos como "publico"
dt$DEPENDENCIA_3 <- case_when(dt$GRUPO_DEPENDENCIA == "1" ~ "pagado",
                              dt$GRUPO_DEPENDENCIA == "2" ~ "subvencionado",
                              dt$GRUPO_DEPENDENCIA %in% c("3", "4") ~ "publico")
table(dt$GRUPO_DEPENDENCIA, dt$DEPENDENCIA_3)
bins_dep <- woebin(dt, y = "PREF_TOP3_DUMMY", x = "DEPENDENCIA_3")
woebin_plot(bins_dep$DEPENDENCIA_3)

# 5.3 Tramos definitivos
bins_adj <- c(bins[setdiff(names(bins), c("EDAD_MESES", "GRUPO_DEPENDENCIA"))],
              bins_edad, bins_dep)

# IV por variable, de mayor a menor
iv_tab <- data.frame(
  variable = names(bins_adj),
  IV       = sapply(bins_adj, function(b) b$total_iv[1]),
  row.names = NULL
)
iv_tab <- iv_tab[order(-iv_tab$IV), ]
iv_tab$poder <- cut(iv_tab$IV, breaks = c(-Inf, 0.02, 0.1, 0.3, 0.5, Inf),
                    labels = c("Inútil", "Débil", "Medio", "Fuerte", "Sospechoso"),
                    right = FALSE)
iv_tab

# IV < 0,02 -> fuera
vars_iv <- iv_tab$variable[iv_tab$IV >= 0.02]
vars_iv

# =============================================================================
# 6. MULTICOLINEALIDAD (VIF) SOBRE VARIABLES WOE
# =============================================================================
dt_woe   <- as.data.frame(woebin_ply(dt[, c(vars_iv, "PREF_TOP3_DUMMY")], bins_adj[vars_iv]))
vars_woe <- paste0(vars_iv, "_woe")

f_full <- as.formula(paste("PREF_TOP3_DUMMY ~", paste(vars_woe, collapse = " + ")))
m_full <- glm(f_full, family = binomial(), data = dt_woe)
vif(m_full, merge_coef = TRUE)

round(cor(dt_woe[, vars_woe]), 2)


# mientras haya VIF > 2, sale la de mayor VIF/IV, pero solo entre las que
# pasan el umbral (las de VIF bajo no son colineales, no hay por qué sacarlas)
umbral_vif <- 2
vars_sel <- vars_iv
repeat {
  f <- as.formula(paste("PREF_TOP3_DUMMY ~",
                        paste(paste0(vars_sel, "_woe"), collapse = " + ")))
  m <- glm(f, family = binomial(), data = dt_woe)
  v <- vif(m)
  v$variable <- sub("_woe$", "", v$variable)
  v <- merge(v, iv_tab[, c("variable", "IV")], by = "variable")
  v$ratio <- v$gvif / v$IV
  if (max(v$gvif) <= umbral_vif) {
    cat("Ninguna variable supera VIF =", umbral_vif, "\n")
    print(v[order(-v$ratio), ])
    break
  }
  v_alto <- v[v$gvif > umbral_vif, ]
  sale <- v_alto$variable[which.max(v_alto$ratio)]
  cat("Se elimina:", sale, "| VIF =", round(v$gvif[v$variable == sale], 2),
      "| IV =", round(v$IV[v$variable == sale], 3),
      "| VIF/IV =", round(v$ratio[v$variable == sale], 1), "\n")
  vars_sel <- setdiff(vars_sel, sale)
}
vars_sel

# Selección final (juicio experto): el VIF deja INGRESO_COLEGIO, pero se usa
# DEPENDENCIA_3 (casi igual IV y VIF; es un rasgo observado del colegio)
x_finales <- c("CLEC_REG_ACTUAL", "MATE1_REG_ACTUAL", "PROMEDIO_NOTAS", "TP_DUMMY",
               "DEPENDENCIA_3", "EDAD_MESES", "BEA", "RINDE_M2")
setdiff(vars_sel, x_finales)
setdiff(x_finales, vars_sel)

# =============================================================================
# 7. MODELO FINAL
# =============================================================================
dt_woe_final <- as.data.frame(
  woebin_ply(dt[, c("PREF_TOP3_DUMMY", x_finales)], bins_adj[x_finales])
)
modelo_final <- glm(PREF_TOP3_DUMMY ~ ., family = binomial(), data = dt_woe_final)
summary(modelo_final)
vif(modelo_final, merge_coef = TRUE)
