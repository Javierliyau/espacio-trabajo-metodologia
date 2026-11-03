suppressPackageStartupMessages({library(tidyverse)})
v <- readRDS("etapa2-verificacion.rds"); dt <- v$dt
ruta <- "C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre/datos/crudos/"
C <- read_csv2(paste0(ruta, "4-matricula/ArchivoMatr_Adm2026.csv"), show_col_types = FALSE)
Creg <- C %>% filter(VIA == 1, TIPO_MATRICULA == 1) %>% select(ID_aux, PREFERENCIA)
Cotra <- C %>% filter(!(VIA == 1 & TIPO_MATRICULA == 1)) %>% distinct(ID_aux)
d <- dt %>% select(ID_aux, I, flag_postula) %>% left_join(Creg, by = "ID_aux") %>%
  mutate(grupo = case_when(I == 1 ~ "I1: top 3 regular", flag_postula == 0 & ID_aux %in% Cotra$ID_aux ~ "0: no postuló, matr. otra vía",
    flag_postula == 0 ~ "0: rindió y no postuló", !is.na(PREFERENCIA) ~ "0: matr. regular pref 4+",
    ID_aux %in% Cotra$ID_aux ~ "0: postuló, matr. otra vía/tipo", TRUE ~ "0: postuló y no se matriculó"))
print(count(d, grupo)); print(table(C$VIA, C$TIPO_MATRICULA, useNA = "ifany"))
