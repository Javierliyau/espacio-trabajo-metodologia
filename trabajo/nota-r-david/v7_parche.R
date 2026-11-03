# =============================================================================
# ECONOMETRIA II - USACH | ETAPA 2 - VERSION INTEGRAL CORREGIDA DEL EQUIPO DE DAVID - 2026-10-28
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
# OPCION 1: completar una ruta absoluta a la carpeta con los CSV (entre comillas).
# OPCION 2: dejar vacio y seleccionar carpeta en RStudio.
# OPCION 3: definir variable de entorno DEMRE_DATOS.
ruta_manual <- "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos" # OPCIONAL: ruta absoluta a carpeta que contiene los cuatro CSV
ruta_datos <- if (nzchar(ruta_manual)) ruta_manual else Sys.getenv("DEMRE_DATOS", unset = "")
if (!nzchar(ruta_datos)) {
  cat("Seleccionar la carpeta con los CSV DEMRE (si RStudio es interactivo).\n")
  if (interactive() && requireNamespace("rstudioapi", quietly = TRUE) &&
      rstudioapi::isAvailable()) ruta_datos <- rstudioapi::selectDirectory(caption = "Carpeta CSV DEMRE")
}
if (is.null(ruta_datos) || !nzchar(ruta_datos) || !dir.exists(ruta_datos))
  stop("Indique ruta_manual o DEMRE_DATOS, o seleccione la carpeta en RStudio.")
ruta_salida <- file.path(ruta_datos, "resultados_etapa2_david")
dir.create(ruta_salida, recursive = TRUE, showWarnings = FALSE)
dir_graficos <- file.path(ruta_salida, "graficos_woe")
dir.create(dir_graficos, recursive = TRUE, showWarnings = FALSE)
guardar <- function(x, nombre) write.csv2(x, file.path(ruta_salida, nombre), row.names = FALSE, na = "")
buscar <- function(patron) {
  f <- list.files(ruta_datos, recursive = TRUE, full.names = TRUE)
  f <- f[basename(f) == patron & !grepl("resultados_etapa2_david", f, fixed = TRUE)]
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
if (length(cols_previas) < 12) stop("Se esperaban columnas de rendiciones anteriores e invierno; solo se encontraron ", length(cols_previas), ". Revise los encabezados.")
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
if (anyNA(base$ID_aux) || anyNA(ins$ID_aux)) stop("IDs faltantes: revise el origen.")
# La rendicion YA contiene RBD, RAMA_EDUCACIONAL, GRUPO_DEPENDENCIA y
# CODIGO_REGION. No traer esas columnas nuevamente desde inscripcion.
# Control del conflicto que detuvo una version previa.
columnas_necesarias <- c("RBD", "RAMA_EDUCACIONAL", "GRUPO_DEPENDENCIA", "CODIGO_REGION")
if (!all(columnas_necesarias %in% names(base)))
  stop("Rendicion no contiene alguna columna escolar esperada: ",
       paste(setdiff(columnas_necesarias, names(base)), collapse=", "))
mat_regular <- mat %>% filter(VIA == 1, TIPO_MATRICULA == 1) %>%
  select(ID_aux, PREFERENCIA)
if (anyDuplicated(mat_regular$ID_aux)) stop("Mas de una matricula regular por ID.")
if (anyNA(mat_regular$ID_aux)) stop("Hay IDs vacios en matricula regular.")
ins <- ins %>% mutate(INGRESO_PERCAPITA_GRUPO_FA =
                         ifelse(INGRESO_PERCAPITA_GRUPO_FA == 99, NA_real_,
                                INGRESO_PERCAPITA_GRUPO_FA))
# Es un agregado del grupo de inscritos por RBD, NO la matricula total del colegio.
colegio <- ins %>% filter(!is.na(RBD), RBD != 0) %>% group_by(RBD) %>%
  summarise(N_INSCRITOS_RBD = n(),
            INGRESO_COLEGIO = if (all(is.na(INGRESO_PERCAPITA_GRUPO_FA))) NA_real_ else
              median(INGRESO_PERCAPITA_GRUPO_FA, na.rm = TRUE), .groups = "drop")
# Detectar otras colisiones inesperadas antes de hacer el join.
variables_ins <- c("ID_aux", "FECHA_NACIMIENTO", "SEXO", "BEA", "PACE",
                   "INGRESO_PERCAPITA_GRUPO_FA")
colisiones <- intersect(setdiff(variables_ins, "ID_aux"), names(base))
if (length(colisiones)) stop("Columnas repetidas en inscripcion/rendicion: ",
                             paste(colisiones, collapse=", "),
                             ". Revisar fuente y seleccionar una version.")
base <- base %>%
  # RBD y variables del colegio YA existen en rendicion. Evitar sufijos .x/.y.
  left_join(ins %>% select(ID_aux, FECHA_NACIMIENTO, SEXO, BEA, PACE,
                           INGRESO_PERCAPITA_GRUPO_FA), by = "ID_aux") %>%
  mutate(FLAG_POSTULA = as.integer(ID_aux %in% unique(pos$ID_aux))) %>%
  left_join(mat_regular, by = "ID_aux") %>%
  left_join(colegio, by = "RBD") %>%
  mutate(PREF_TOP3_DUMMY = as.integer(!is.na(PREFERENCIA) & PREFERENCIA %in% 1:3))
stopifnot("RBD" %in% names(base),
          nrow(base) == n_distinct(base$ID_aux),
          all(base$PREF_TOP3_DUMMY %in% 0:1))
# Comparaciones de referencia para los CSV DEMRE de admision 2026 de la clase.
# Son pruebas de consistencia: si no coinciden, investigar la definicion de muestra.
N_referencia <- 168714L
Y_referencia <- 60234L
if (nrow(base) != N_referencia || sum(base$PREF_TOP3_DUMMY) != Y_referencia)
  stop("Control de poblacion FALLIDO: N=", nrow(base), " (esperado 168714), Y=1=",
       sum(base$PREF_TOP3_DUMMY), " (esperado 60234). Verificar filtros y CSV; NO interpretar resultados posteriores.")
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
  EDAD_MESES = {
    f <- suppressWarnings(as.numeric(FECHA_NACIMIENTO))
    mes <- f %/% 10000
    anio <- f %% 10000
    ifelse(is.na(f) | mes < 1 | mes > 12 | anio < 1900 | anio > 2025, NA_real_,
           (2025 - anio) * 12 + (12 - mes))
  },
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
# Tabla de frecuencias para categoricas y binarias (incluye NA).
vars_frecuencia <- candidatas[vapply(dt[candidatas], function(z)
  !is.numeric(z) || length(unique(z[!is.na(z)])) <= 10L, logical(1))]
frecuencias <- dplyr::bind_rows(lapply(vars_frecuencia, function(v) {
  x <- as.character(dt[[v]])
  x[is.na(x)] <- "SIN_DATO"
  zz <- as.data.frame(table(x), stringsAsFactors=FALSE)
  names(zz) <- c("categoria", "n")
  zz$variable <- v
  zz$pct <- 100 * zz$n / sum(zz$n)
  zz[, c("variable", "categoria", "n", "pct")]
}))
guardar(frecuencias, "01b_frecuencias.csv")
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
# Indicador de inconsistencia: no se emplea como predictor.
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

# 4. EXCLUSION DOCUMENTADA. El profesor usa WOE para tratar NA como tramo.
# Por tanto NO se elimina ingreso familiar solo por superar 5% de NA.
# Un NA estructural debe evaluarse y documentarse mediante el IV y los bins.
fuera_const <- setdiff(inspeccion$variable[inspeccion$n_unicos <= 1], "PREF_TOP3_DUMMY")
# Mantener indicadores de rendicion hasta conocer su IV (sin veto arbitrario).
x_analisis <- setdiff(candidatas, fuera_const)
exclusiones_previas <- data.frame(variable=fuera_const, motivo=rep("Sin variacion suficiente", length(fuera_const)))
guardar(exclusiones_previas, "04b_exclusiones_previas.csv")
cat("Candidatas con mas de 5% NA (se mantienen para WOE):\n")
print(inspeccion[inspeccion$variable %in% x_analisis & inspeccion$pct_na > 5,
                 c("variable", "pct_na")])
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
    # Con pocos cortes distintos se conserva el valor; no forzar cuantiles duplicados.
  }
  data.frame(tramo=ifelse(is.na(x), "SIN_DATO", as.character(x)),
             y=dt$PREF_TOP3_DUMMY) %>% group_by(tramo) %>%
    summarise(n=n(), tasa_y=mean(y), .groups="drop") %>% mutate(variable=v, .before=1)
}
if (length(x_analisis)) guardar(bind_rows(lapply(x_analisis, bivar)), "05_bivariado.csv")

# 6. WOE + IV SEGUN GERMAN CREDIT DEL PROFESOR
if (length(x_analisis) < 2) stop("Muy pocas variables candidatas. Revise perdidos y codificacion.")
dt_modelo <- as.data.frame(dt[, c("PREF_TOP3_DUMMY", x_analisis), drop=FALSE])
if (anyNA(dt_modelo$PREF_TOP3_DUMMY)) stop("La variable respuesta tiene NA.")
if (any(vapply(dt_modelo[x_analisis], function(x) all(is.na(x)), logical(1))))
  stop("Hay variables enteramente faltantes; excluirlas documentadamente antes del WOE.")
bins <- scorecard::woebin(dt_modelo, y="PREF_TOP3_DUMMY", positive="1", print_info=FALSE)
if (!length(bins) || !all(x_analisis %in% names(bins)))
  stop("WOE no genero bins para todas las candidatas; revisar variables constantes o faltantes.")
# Revisión: tasas por tramo. Numericas necesitan interpretacion y monotonia;
# categoricas se agrupan segun criterio sustantivo, no solo correlacion.
tasa_col <- intersect(c("posprob", "badprob"), names(bins[[1]]))[1]
if (is.na(tasa_col)) stop("scorecard: no se encontro la columna de tasa del evento.")
es_monotona <- function(b) {
  b <- as.data.frame(b)
  p <- b[[tasa_col]][!grepl("missing", b$bin, ignore.case=TRUE)]
  if (length(p) < 3) return(TRUE)
  all(diff(p) >= -1e-10) || all(diff(p) <= 1e-10)
}
# Monotonia solo tiene sentido para variables con orden inherente.
ordenadas <- c("PROMEDIO_NOTAS", "PORC_SUP_NOTAS", "PTJE_NEM", "PTJE_RANKING",
              "CLEC_REG_ACTUAL", "MATE1_REG_ACTUAL", "EDAD_MESES",
              "INGRESO_PERCAPITA_GRUPO_FA", "N_INSCRITOS_RBD", "INGRESO_COLEGIO")
mono_inicial <- data.frame(variable=names(bins),
                           monotona=vapply(names(bins), function(v)
                             if (v %in% ordenadas) es_monotona(bins[[v]]) else NA, logical(1)))
guardar(mono_inicial, "06_monotonia_inicial.csv")

# Retr amificacion (retramificacion) revisable:
# No imponer 19 anios sin contrastar WOE, monotonia y tamanos de tramos.
# La propuesta se calcula como alternativa y se exporta para revision humana.
bins_adj <- bins
ajustes <- data.frame(variable=character(), decision=character(), detalle=character())
if ("EDAD_MESES" %in% names(bins_adj)) {
  bins_edad_alt <- scorecard::woebin(dt_modelo, y="PREF_TOP3_DUMMY",
                     x="EDAD_MESES", positive="1",
                     breaks_list=list(EDAD_MESES=c(228)), print_info=FALSE)
  guardar(as.data.frame(bins[["EDAD_MESES"]]), "06b_edad_bins_automaticos.csv")
  guardar(as.data.frame(bins_edad_alt[["EDAD_MESES"]]), "06c_edad_bins_19anios_alternativa.csv")
  auto_mono <- es_monotona(bins[["EDAD_MESES"]])
  alt_mono <- es_monotona(bins_edad_alt[["EDAD_MESES"]])
  # Solo sustituir por un corte con suficientes casos en ambos tramos.
  tabla_alt <- as.data.frame(bins_edad_alt[["EDAD_MESES"]])
  n_edad <- sum(!is.na(dt_modelo$EDAD_MESES))
  sin_missing <- !grepl("missing", tabla_alt$bin, ignore.case=TRUE)
  tamanos_ok <- sum(sin_missing) >= 2 &&
    all(tabla_alt$count[sin_missing] >= max(30, floor(0.05*n_edad)))
  # Solo reemplaza el automatico si corrige no monotonia y cumple tamanos.
  usar_alt <- !auto_mono && alt_mono && tamanos_ok
  if (usar_alt) bins_adj[["EDAD_MESES"]] <- bins_edad_alt[["EDAD_MESES"]]
  ajustes <- rbind(ajustes, data.frame(variable="EDAD_MESES",
             decision=if (usar_alt) "alternativa 19 anios" else "automatico",
             detalle=paste("monotonia inicial:", auto_mono, "; alternativa:", alt_mono, "; tamanos OK:", tamanos_ok)))
}
guardar(ajustes, "06d_decisiones_retramificacion.csv")
# DEPENDENCIA_3 se agrupo por tipo institucional, no por supuesto orden numerico.
monotonia <- data.frame(variable=names(bins_adj),
             monotona=vapply(names(bins_adj), function(v)
               if (v %in% ordenadas) es_monotona(bins_adj[[v]]) else NA, logical(1)))
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
# Tamanos por bin (necesarios para auditar los extremos y IV exagerados).
reporte_bins <- dplyr::bind_rows(lapply(names(bins_adj), function(v) {
  b <- as.data.frame(bins_adj[[v]])
  b$variable_revisada <- v
  b
}))
guardar(reporte_bins, "08a_todos_los_bins.csv")
# Se solicita revisar cualquier tramo que agrupe menos de 1% de la muestra.
reporte_bins$alerta_muestra_pequena <- reporte_bins$count / nrow(dt_modelo) < 0.01
guardar(reporte_bins[reporte_bins$alerta_muestra_pequena, ], "08a_bins_pequenos.csv")
cat("IV >= 0.5: verificar posible fuga y codificacion:\n")
print(iv_tab[iv_tab$IV>=.5,])
# IV alto no equivale automaticamente a fuga. PAES y notas se conocen antes
# de matricula y son predictores sustantivos; revisar codificacion y tramos.
revision_iv <- iv_tab %>% filter(IV >= .5) %>%
  mutate(diagnostico = ifelse(variable %in% c("CLEC_REG_ACTUAL", "MATE1_REG_ACTUAL",
                 "PROMEDIO_NOTAS", "PTJE_NEM", "PTJE_RANKING"),
                 "Predictor previo a matricula; IV alto plausible, revisar bins",
                 "Revisar fuga, codificacion, tamanos de bins y definicion temporal"))
guardar(revision_iv,"08b_revision_iv_altos.csv")
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
  stopifnot(all(is.finite(v_final)), all(v_final <= 2+1e-8))
} else {
  m_final <- glm(reformulate(paste0(x_finales,"_woe"), response="PREF_TOP3_DUMMY"),
                 family=binomial(), data=woe)
  print(summary(m_final))
}
# CONVENCION WOE: para y=1 y positive="1", verificar con los porcentajes
# de eventos/no-eventos en los bins, porque invertir el WOE invierte beta.
# Bajo la convencion scorecard WOE=ln(distribucion no-eventos/eventos),
# un beta NEGATIVO puede ser la direccion esperada del modelo.
# Por ello NO se eliminan variables automaticamente solo por beta < 0.
# Diagnostico exploratorio del modelo: coeficientes, signos, valor p e IV.
# Con positive="1", scorecard puede definir WOE como log(%Y=0 / %Y=1).
# En ese caso NO se deben imponer beta positivos sin verificar convencion:
# un beta negativo puede ser el signo esperado por la definicion de WOE.
sm <- summary(m_final)$coefficients
coef_tab <- data.frame(termino=rownames(sm), beta=sm[,1], error_std=sm[,2],
                       z=sm[,3], p_valor=sm[,4], row.names=NULL)
coef_tab$variable <- sub("_woe$", "", coef_tab$termino)
coef_tab$IV <- iv_tab$IV[match(coef_tab$variable, iv_tab$variable)]
coef_tab$significativo_5pct <- coef_tab$p_valor < .05
# scorecard puede codificar WOE como ln(distribucion eventos/distribucion no eventos)
# o el inverso, segun la version/configuracion. Verificar CON LOS BINS,
# no exigir signo positivo o negativo de forma universal.
coef_tab$observacion <- ifelse(coef_tab$termino == "(Intercept)",
 "Intercepto", ifelse(coef_tab$significativo_5pct,
 "Revisar signo segun convencion WOE y sentido economico",
 "No significativo al 5%; discutir sin eliminar mecanicamente"))
guardar(coef_tab, "12_diagnostico_coeficientes.csv")
cat("Coeficientes negativos o sin significancia al 5% (revisar, no borrar sin criterio):\n")
print(coef_tab[coef_tab$termino != "(Intercept)" &
                (coef_tab$beta < 0 | !coef_tab$significativo_5pct), ])
# Bins, diagnosticos y modelo se guardan para transparencia y futura etapa.
# El modelo aqui solo permite verificar las X finales: modelamiento comparativo,
# train/test, KS, AUC, Gini, ROC y scorecard corresponden a una etapa posterior.
# Consolidado final interpretable para el informe.
resultado_x <- data.frame(variable=x_finales,
  IV=iv_tab$IV[match(x_finales,iv_tab$variable)],
  pct_NA=inspeccion$pct_na[match(x_finales,inspeccion$variable)],
  beta=coef_tab$beta[match(paste0(x_finales,"_woe"),coef_tab$termino)],
  p_valor=coef_tab$p_valor[match(paste0(x_finales,"_woe"),coef_tab$termino)])
resultado_x$VIF <- if (exists("v_final")) as.numeric(v_final[paste0(x_finales,"_woe")]) else NA_real_
guardar(resultado_x, "13_resumen_X_definitivas.csv")
cat("Variables definitivas:", paste(x_finales,collapse=", "), "\n")
print(resultado_x)
# Al definir X, IV y WOE en la muestra completa, hay optimismo si se reutiliza
# sin recalibrar en una prueba externa: para Etapa 3 recalcular con train.
# RESUMEN DE CALIDAD, util para anexo y defensa de la seleccion.
calidad <- data.frame(
 chequeo=c("N poblacion", "Y positivos", "IDs duplicados", "Tasa evento", 
           "X candidatas", "X con IV >= 0.02", "X finales", "VIF maximo final"),
 valor=c(nrow(base), sum(base$PREF_TOP3_DUMMY), anyDuplicated(base$ID_aux),
         mean(base$PREF_TOP3_DUMMY), length(x_analisis), length(vars_iv),
         length(x_finales), if (exists("v_final")) max(v_final) else NA_real_))
guardar(calidad, "00_resumen_controles.csv")
write.csv2(data.frame(ID_aux=base$ID_aux, Y=base$PREF_TOP3_DUMMY),
           file.path(ruta_salida,"00_ids_y.csv"),row.names=FALSE)
saveRDS(list(variables=x_finales, bins=bins_adj, modelo=m_final,
             ranking_iv=iv_tab, historial_vif=historial),
        file.path(ruta_salida,"seleccion_etapa2.rds"))
cat("ETAPA 2 TERMINADA. Resultados en:", ruta_salida,"\n")
