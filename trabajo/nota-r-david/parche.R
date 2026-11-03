# =============================================================================
# ECONOMETRIA II - USACH | ETAPA 2 - VERSION REVISADA DEL EQUIPO DE DAVID
# Integrantes: David Cuevas, Javier Li-Yau, Benjamin Lizana y Ana Nacif
# Referencia metodologica: GermanCredit_Scorecard.R (Prof. Brian Pfeng)
# Objetivo: Y=1 si matricula REGULAR en preferencias 1, 2 o 3.
# Alcance: descripcion, consistencia, WOE/IV, ajustes de tramos, VIF y X finales.
# NOTA: ejecutar sobre los archivos DEMRE originales; validar resultados antes
#       de entregarlos. No se incluyen cifras inventadas ni resultados simulados.
# =============================================================================
rm(list = ls())
options(scipen = 999, digits = 4)
set.seed(2026)
paquetes <- c("dplyr", "ggplot2", "scorecard", "car")
faltantes <- paquetes[!vapply(paquetes, requireNamespace, logical(1), quietly = TRUE)]
if (length(faltantes)) stop("Instalar paquetes: ", paste(faltantes, collapse = ", "))
suppressPackageStartupMessages({library(dplyr); library(ggplot2); library(scorecard); library(car)})

# CONFIGURACION: editar SOLO esta carpeta, o elegirla interactivamente.
ruta_datos <- Sys.getenv("DEMRE_DATOS", unset = "")
if (!nzchar(ruta_datos)) {
  cat("Seleccionar la carpeta con los CSV DEMRE (si RStudio es interactivo).\n")
  if (interactive() && requireNamespace("rstudioapi", quietly = TRUE) &&
      rstudioapi::isAvailable()) ruta_datos <- rstudioapi::selectDirectory(caption = "Carpeta CSV DEMRE")
}
if (is.null(ruta_datos) || !nzchar(ruta_datos) || !dir.exists(ruta_datos))
  stop("Defina DEMRE_DATOS con la carpeta que contiene los archivos CSV DEMRE.")
ruta_salida <- file.path(ruta_datos, "resultados_parche")
dir.create(ruta_salida, recursive = TRUE, showWarnings = FALSE)
dir_graficos <- file.path(ruta_salida, "graficos_woe")
dir.create(dir_graficos, recursive = TRUE, showWarnings = FALSE)
guardar <- function(x, nombre) write.csv2(x, file.path(ruta_salida, nombre), row.names = FALSE, na = "")
buscar <- function(patron) {
  f <- list.files(ruta_datos, recursive = TRUE, full.names = TRUE)
  f <- f[basename(f) == patron & !grepl("resultados_parche", f, fixed = TRUE)]
  if (length(f) != 1) stop("Se esperaba exactamente un archivo: ", patron, "; encontrados: ", length(f))
  f
}
leer <- function(nombre) read.csv2(buscar(nombre), stringsAsFactors = FALSE)
ins <- leer("ArchivoB_Adm2026REG.csv")
ren <- leer("ArchivoC_Adm2026REG.csv")
pos <- leer("ArchivoD_Adm2026REG.csv")
mat <- leer("ArchivoMatr_Adm2026.csv")

# 0. DEFINICION DE MUESTRA: primera rendicion y promocion del anio
# En CSV hay blancos "" y NA: ambos indican ausencia de rendicion previa.
cols_previas <- grep("(REG_ANTERIOR|INV_ANTERIOR|INV_ACTUAL)$", names(ren), value = TRUE)
if (!length(cols_previas)) stop("No se encontraron columnas de rendiciones previas.")
ausente <- function(x) is.na(x) | trimws(as.character(x)) == ""
base <- ren %>%
  filter(SITUACION_EGRESO == 1,
         if_all(all_of(cols_previas), ausente),
         CLEC_REG_ACTUAL >= 100, MATE1_REG_ACTUAL >= 100,
         coalesce(CIEN_REG_ACTUAL, 0) >= 100 | coalesce(HCSOC_REG_ACTUAL, 0) >= 100,
         PROMEDIO_NOTAS > 0)
if (anyDuplicated(base$ID_aux)) stop("Duplicados en la base maestra; revisar fuente.")
cat("N de la muestra elegible:", nrow(base), "\n")
# El profesor espera contrastar el N de la muestra con la base de Etapa 1.
# No se impone N fijo: si el N difiere, comprobar filtros y version de DEMRE.

# 1. VARIABLE DEPENDIENTE: la matricula NO redefine la poblacion elegible
if (anyDuplicated(ins$ID_aux)) stop("IDs repetidos en inscripcion; revisar antes de unir.")
mat_regular <- mat %>% filter(VIA == 1, TIPO_MATRICULA == 1) %>%
  select(ID_aux, PREFERENCIA)
if (anyDuplicated(mat_regular$ID_aux)) stop("Mas de una matricula regular por ID.")
ins <- ins %>% mutate(INGRESO_PERCAPITA_GRUPO_FA =
                         ifelse(INGRESO_PERCAPITA_GRUPO_FA == 99, NA_real_,
                                INGRESO_PERCAPITA_GRUPO_FA))
# Es un agregado del grupo de inscritos por RBD, NO la matricula total del colegio.
colegio <- ins %>% filter(!is.na(RBD)) %>% group_by(RBD) %>%
  summarise(N_INSCRITOS_RBD = n(),
            INGRESO_COLEGIO = if (all(is.na(INGRESO_PERCAPITA_GRUPO_FA))) NA_real_ else
              median(INGRESO_PERCAPITA_GRUPO_FA, na.rm = TRUE), .groups = "drop")
base <- base %>%
  left_join(ins %>% select(ID_aux, FECHA_NACIMIENTO,
                           SEXO, BEA, PACE,
                           INGRESO_PERCAPITA_GRUPO_FA), by = "ID_aux") %>%
  mutate(FLAG_POSTULA = as.integer(ID_aux %in% unique(pos$ID_aux))) %>%
  left_join(mat_regular, by = "ID_aux") %>%
  left_join(colegio, by = "RBD") %>%
  mutate(PREF_TOP3_DUMMY = as.integer(!is.na(PREFERENCIA) & PREFERENCIA %in% 1:3))
stopifnot(nrow(base) == n_distinct(base$ID_aux), all(base$PREF_TOP3_DUMMY %in% 0:1))
cat("Y=1:", sum(base$PREF_TOP3_DUMMY), " | tasa:", round(100*mean(base$PREF_TOP3_DUMMY), 2), "%\n")
print(table(Postulo=base$FLAG_POSTULA, Top3=base$PREF_TOP3_DUMMY))
if (any(base$PREF_TOP3_DUMMY == 1 & base$FLAG_POSTULA == 0))
  warning("Hay matriculados en top3 sin registro en postulacion; verificar cruces.")

# 2. VARIABLES CANDIDATAS: solo observables previamente al resultado
# BEA/PACE se reservan para descriptivas: vias especiales no son Y=1.
# FLAG_POSTULA se excluye: separacion perfecta por construccion de la Y.
# No se usan PREFERENCIA, PTJE_POND, matricula o seleccion como X.
base <- base %>% mutate(
  TP_DUMMY = as.integer(RAMA_EDUCACIONAL %in% c("T1", "T2", "T3", "T4", "T5")),
  BEA_DUMMY = as.integer(!is.na(BEA) & BEA != ""),
  PACE_DUMMY = as.integer(!is.na(PACE) & PACE != ""),
  RINDE_CIEN = as.integer(coalesce(CIEN_REG_ACTUAL, 0) >= 100),
  RINDE_HCSOC = as.integer(coalesce(HCSOC_REG_ACTUAL, 0) >= 100),
  RINDE_M2 = as.integer(coalesce(MATE2_REG_ACTUAL, 0) >= 100),
  EDAD_MESES = ifelse(is.na(FECHA_NACIMIENTO), NA_real_,
                      (2025 - as.numeric(FECHA_NACIMIENTO) %% 10000) * 12 +
                        (12 - as.numeric(FECHA_NACIMIENTO) %/% 10000)),
  GRUPO_DEPENDENCIA = as.character(GRUPO_DEPENDENCIA),
  CODIGO_REGION = as.character(CODIGO_REGION),
  SEXO = as.character(SEXO),
  DEPENDENCIA_3 = case_when(GRUPO_DEPENDENCIA == "1" ~ "pagado",
                            GRUPO_DEPENDENCIA == "2" ~ "subvencionado",
                            GRUPO_DEPENDENCIA %in% c("3", "4") ~ "publico",
                            TRUE ~ NA_character_))
# Advertencia: edad se calcula al cierre 2025, fecha MMAAAA; controlar plausibilidad.

candidatas <- c("PROMEDIO_NOTAS", "PORC_SUP_NOTAS", "PTJE_NEM", "PTJE_RANKING",
                "CLEC_REG_ACTUAL", "MATE1_REG_ACTUAL", "RINDE_CIEN", "RINDE_HCSOC",
                "RINDE_M2", "TP_DUMMY", "DEPENDENCIA_3", "CODIGO_REGION",
                "SEXO", "INGRESO_PERCAPITA_GRUPO_FA", "EDAD_MESES",
                "N_INSCRITOS_RBD", "INGRESO_COLEGIO")
stopifnot(all(candidatas %in% names(base)))
dt <- as.data.frame(base[, c("PREF_TOP3_DUMMY", candidatas)])

# 3. INSPECCION UNIVARIADA: faltantes, descriptivos, atipicos
res_num <- function(x) if (!length(x) || all(is.na(x))) NA_real_ else min(x, na.rm=TRUE)
inspeccion <- data.frame(
  variable = names(dt), tipo = vapply(dt, function(x) class(x)[1], ""),
  n_na = vapply(dt, function(x) sum(is.na(x)), 0L),
  pct_na = vapply(dt, function(x) 100*mean(is.na(x)), 0.0),
  n_unicos = vapply(dt, function(x) length(unique(x[!is.na(x)])), 0L),
  minimo = vapply(dt, function(x) if (is.numeric(x)) res_num(x) else NA_real_, 0.0),
  maximo = vapply(dt, function(x) if (is.numeric(x) && any(!is.na(x))) max(x, na.rm=TRUE) else NA_real_, 0.0))
guardar(inspeccion, "01_inspeccion.csv")
continuas <- candidatas[vapply(dt[candidatas], function(x) is.numeric(x) &&
                                   length(unique(na.omit(x))) > 10, logical(1))]
num_descriptivo <- lapply(continuas, function(v) {
  x <- dt[[v]]; x <- x[is.finite(x)]
  if (!length(x)) return(data.frame(variable=v, n=0))
  data.frame(variable=v, n=length(x), media=mean(x), sd=sd(x),
             p25=unname(quantile(x,.25)), mediana=median(x),
             p75=unname(quantile(x,.75)), minimo=min(x), maximo=max(x))
})
if (length(num_descriptivo)) guardar(dplyr::bind_rows(num_descriptivo), "02_descriptivos.csv")
iqr_out <- function(x) {
  x <- x[is.finite(x)]; if (length(x)<3) return(NA_integer_)
  q <- quantile(x, c(.25,.75)); z <- 1.5*diff(q)
  sum(x<q[1]-z | x>q[2]+z)
}
atipicos <- data.frame(variable=continuas,
                       n_atipicos=vapply(dt[continuas], iqr_out, 0L))
guardar(atipicos, "03_atipicos.csv")
for (v in continuas) {
  png(file.path(ruta_salida, paste0("box_", v, ".png")), width=900, height=650)
  boxplot(dt[[v]], main=paste("Atipicos:",v), col="lightblue"); dev.off()
}
# Criterio: no borrar un dato real simplemente por exceder 1,5 RIC.
# Reglas de consistencia: detectar, marcar y revisar; no borrar automaticamente.
base$flag_inconsistencia <- as.integer(
  (!is.na(base$PROMEDIO_NOTAS) & (base$PROMEDIO_NOTAS < 4 | base$PROMEDIO_NOTAS > 7)) |
  (!is.na(base$PTJE_NEM) & (base$PTJE_NEM < 100 | base$PTJE_NEM > 1000)) |
  (!is.na(base$PTJE_RANKING) & (base$PTJE_RANKING < 100 | base$PTJE_RANKING > 1000)) |
  (!is.na(base$EDAD_MESES) & (base$EDAD_MESES < 16*12 | base$EDAD_MESES > 100*12)))
reglas <- data.frame(regla=c("IDs duplicados", "Notas fuera 4-7", "NEM fuera 100-1000",
                              "Ranking fuera 100-1000", "Edad fuera de 16 a 100", "Flag inconsistencia"),
                     casos=c(anyDuplicated(base$ID_aux),
                             sum(base$PROMEDIO_NOTAS<4 | base$PROMEDIO_NOTAS>7,na.rm=TRUE),
                             sum(base$PTJE_NEM<100 | base$PTJE_NEM>1000,na.rm=TRUE),
                             sum(base$PTJE_RANKING<100 | base$PTJE_RANKING>1000,na.rm=TRUE),
                             sum(base$EDAD_MESES<192 | base$EDAD_MESES>1200,na.rm=TRUE),
                             sum(base$flag_inconsistencia)))
guardar(reglas, "04_consistencia.csv")

# 4. EXCLUSION: mas de 5% NA, sin variacion, riesgo de fuga, redundancia
# Excepcion: ninguna en esta version; un NA estructural necesita defensa especifica.
fuera_na <- setdiff(inspeccion$variable[inspeccion$pct_na > 5], "PREF_TOP3_DUMMY")
fuera_const <- setdiff(inspeccion$variable[inspeccion$n_unicos <= 1], "PREF_TOP3_DUMMY")
fuera_redundantes <- c("RINDE_HCSOC", "RINDE_CIEN")  # indicadores poco informativos solos
x_analisis <- setdiff(candidatas, union(union(fuera_na, fuera_const), fuera_redundantes))
# Evidencia descriptiva BEA/PACE: no se emplean como explicativas de la Y regular.
for (v in c("BEA_DUMMY", "PACE_DUMMY")) {
  tab <- base %>% group_by(.data[[v]]) %>%
    summarise(n=n(), tasa_top3=mean(PREF_TOP3_DUMMY), .groups="drop")
  print(tab)
}

# 5. ANALISIS BIVARIADO PREVIO AL BINNING
bivar <- function(v) {
  x <- dt[[v]]
  if (is.numeric(x) && length(unique(na.omit(x))) > 10) {
    cortes <- unique(as.numeric(quantile(x, probs=seq(0,1,.2), na.rm=TRUE)))
    if (length(cortes) >= 3) x <- cut(x, breaks=cortes, include.lowest=TRUE)
  }
  data.frame(tramo=ifelse(is.na(x), "SIN_DATO", as.character(x)),
             y=dt$PREF_TOP3_DUMMY) %>% group_by(tramo) %>%
    summarise(n=n(), tasa_y=mean(y), .groups="drop") %>% mutate(variable=v, .before=1)
}
if (length(x_analisis)) guardar(bind_rows(lapply(x_analisis, bivar)), "05_bivariado.csv")

# 6. WOE + IV SEGUN GERMAND CREDIT DEL PROFESOR
if (length(x_analisis) < 2) stop("Muy pocas variables candidatas. Revise perdidos y codificacion.")
dt_modelo <- as.data.frame(dt[, c("PREF_TOP3_DUMMY", x_analisis), drop=FALSE])
bins <- scorecard::woebin(dt_modelo, y="PREF_TOP3_DUMMY", positive="1", print_info=FALSE)
# Revisión: tasas por tramo. Numericas necesitan interpretacion y monotonia;
# categoricas se agrupan segun criterio sustantivo, no solo correlacion.
tasa_col <- intersect(c("posprob", "badprob"), names(bins[[1]]))[1]
if (is.na(tasa_col)) stop("scorecard: no se encontro la columna de tasa del evento.")
es_monotona <- function(b) {
  b <- as.data.frame(b)
  p <- b[[tasa_col]][!grepl("missing", b$bin, ignore.case=TRUE)]
  if (length(p) < 3) return(TRUE)
  all(diff(p) >= 0) || all(diff(p) <= 0)
}
mono_inicial <- data.frame(variable=names(bins),
                           monotona=vapply(bins, es_monotona, logical(1)))
guardar(mono_inicial, "06_monotonia_inicial.csv")

# Ajuste con criterio explicito ya usado en el codigo original de David:
# edad dividida en 19 anios; se registra y puede compararse con bin automatico.
bins_adj <- bins
if ("EDAD_MESES" %in% names(bins_adj)) {
  bins_edad <- scorecard::woebin(dt_modelo, y="PREF_TOP3_DUMMY",
                  x="EDAD_MESES", positive="1",
                  breaks_list=list(EDAD_MESES=c(228)), print_info=FALSE)
  bins_adj$EDAD_MESES <- bins_edad$EDAD_MESES
}
# DEPENDENCIA_3 ya fue agrupada ANTES del binning: publico, subvencionado, pagado.
monotonia <- data.frame(variable=names(bins_adj),
                         monotona=vapply(bins_adj, es_monotona, logical(1)))
guardar(monotonia, "07_monotonia_final.csv")
# Guarda graficos para revisión manual de tramos; no asumir que todos son validos.
plots <- scorecard::woebin_plot(bins_adj)
for (v in names(plots))
  ggplot2::ggsave(file.path(dir_graficos,paste0(v,".png")), plots[[v]],
                  width=7,height=5,dpi=120)

iv_tab <- data.frame(variable=names(bins_adj),
                     IV=vapply(bins_adj, function(b) as.numeric(b$total_iv[1]), 0.0)) %>%
  arrange(desc(IV)) %>% mutate(poder=cut(IV, c(-Inf,.02,.1,.3,.5,Inf),
                 labels=c("Inutil","Debil","Medio","Fuerte","Sospechoso"),
                 right=FALSE))
guardar(iv_tab,"08_ranking_iv.csv")
cat("IV >= 0.5: verificar posible fuga y codificacion:\n")
print(iv_tab[iv_tab$IV>=.5,])
vars_iv <- iv_tab$variable[iv_tab$IV >= .02]
if (length(vars_iv)<2) stop("Menos de dos variables con IV >= 0.02")

# 7. VIF/IV: elimina SOLO dentro de quienes superan VIF=2.
# Compatibilidad: para un GLM de predictores WOE numericos usar VIF clasico.
woe <- as.data.frame(scorecard::woebin_ply(dt_modelo[,c("PREF_TOP3_DUMMY",vars_iv),drop=FALSE],
                                           bins_adj[vars_iv], print_info=FALSE))
vars_sel <- vars_iv
historial <- data.frame(iteracion=integer(), eliminada=character(), VIF=double(),
                        IV=double(), ratio=double())
extraer_vif <- function(modelo) {
  z <- car::vif(modelo)
  if (is.matrix(z)) { # GVIF ajustado si existen terminos de varios grados de libertad
    if ("GVIF^(1/(2*Df))" %in% colnames(z)) return(setNames(z[,"GVIF^(1/(2*Df))"]^2, rownames(z)))
    return(setNames(z[,1], rownames(z)))
  }
  z
}
iter <- 0L
repeat {
  if (length(vars_sel) < 2) break
  x <- paste0(vars_sel,"_woe")
  m <- glm(reformulate(x, response="PREF_TOP3_DUMMY"), family=binomial(), data=woe)
  v <- extraer_vif(m)
  if (any(!is.finite(v))) stop("VIF no finito: revise colinealidad perfecta.")
  malos <- v[v > 2]
  if (!length(malos)) break
  nombres <- sub("_woe$", "", names(malos))
  iv <- iv_tab$IV[match(nombres, iv_tab$variable)]
  ratio <- as.numeric(malos)/iv
  j <- which.max(ratio)
  iter <- iter+1L
  historial <- rbind(historial, data.frame(iteracion=iter, eliminada=nombres[j],
                            VIF=as.numeric(malos[j]), IV=iv[j], ratio=ratio[j]))
  vars_sel <- setdiff(vars_sel, nombres[j])
}
guardar(historial,"09_eliminaciones_vif.csv")
# NO sobrescribir manualmente los seleccionados sin volver a verificar IV/VIF.
x_finales <- vars_sel
if (!length(x_finales)) stop("No quedan variables seleccionadas")
guardar(data.frame(variable=x_finales, IV=iv_tab$IV[match(x_finales,iv_tab$variable)]),
        "10_variables_finales.csv")
if (length(x_finales) >= 2) {
  m_final <- glm(reformulate(paste0(x_finales,"_woe"), response="PREF_TOP3_DUMMY"),
                 family=binomial(), data=woe)
  v_final <- extraer_vif(m_final)
  guardar(data.frame(variable=names(v_final), VIF=as.numeric(v_final)), "11_vif_final.csv")
  print(summary(m_final))
  stopifnot(all(v_final <= 2+1e-8))
} else {
  m_final <- glm(reformulate(paste0(x_finales,"_woe"), response="PREF_TOP3_DUMMY"),
                 family=binomial(), data=woe)
  print(summary(m_final))
}
# El modelo aqui solo permite verificar las X finales: modelamiento comparativo,
# train/test, KS, AUC, Gini, ROC y scorecard corresponden a una etapa posterior.
saveRDS(list(variables=x_finales, bins=bins_adj, modelo=m_final,
             ranking_iv=iv_tab, historial_vif=historial),
        file.path(ruta_salida,"seleccion_etapa2.rds"))
cat("ETAPA 2 TERMINADA. Resultados en:", ruta_salida,"\n")

