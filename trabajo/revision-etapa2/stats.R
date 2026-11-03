setwd("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre")
src <- readLines("C:/Users/javie/Downloads/MINEDUC Trabajo etapa 2 econometria.II v2.R", encoding = "UTF-8")
src <- src[!(grepl("write_xlsx", src, fixed=TRUE) | grepl("woebin_plot", src, fixed=TRUE) | grepl("boxplot", src, fixed=TRUE))]
pdf(NULL); suppressMessages(invisible(capture.output(eval(parse(text = src), envir = globalenv()))))
cat("PREF:\n"); p <- df_final$PREFERENCIA; print(c(p1=sum(p==1,na.rm=T),p2=sum(p==2,na.rm=T),p3=sum(p==3,na.rm=T),p4mas=sum(p>=4,na.rm=T),nomat=sum(is.na(p))))
cat("flag x Y:\n"); print(table(df_final$FLAG_POSTULA, df_final$PREF_TOP3_DUMMY))
cat("colegios:", n_distinct(df_final$RBD, na.rm=TRUE), " cols:", ncol(df_final), "\n"); print(table(df_final$SEXO))
cat("PACE/BEA/TP/M2:", sum(dt$PACE), sum(dt$BEA), sum(dt$TP_DUMMY), sum(dt$RINDE_M2), "\n")
num <- c("PROMEDIO_NOTAS","PTJE_NEM","PTJE_RANKING","CLEC_REG_ACTUAL","MATE1_REG_ACTUAL","EDAD_MESES","N_ALUMNOS","INGRESO_COLEGIO","MAT_TOTAL","EXP_DOCENTE","IVE_MEDIA")
print(t(sapply(dt[num], function(x) round(c(min=min(x,na.rm=T), med=median(x,na.rm=T), mean=mean(x,na.rm=T), max=max(x,na.rm=T)),3))))
for (v in c("MAT_TOTAL","EXP_DOCENTE","IVE_MEDIA")) { x<-dt[[v]]; q<-quantile(x,c(.25,.75),na.rm=T); r<-diff(q); cat(v, "atip:", sum(x<q[1]-1.5*r | x>q[2]+1.5*r, na.rm=T), "\n") }
cat("reglas: edad<16a", sum(dt$EDAD_MESES<192), " edad>=20a", sum(dt$EDAD_MESES>=240), " edad>=30a", sum(dt$EDAD_MESES>=360), " prom fuera[4,7]", sum(dt$PROMEDIO_NOTAS<4|dt$PROMEDIO_NOTAS>7), " NEM fuera[100,1000]", sum(dt$PTJE_NEM<100|dt$PTJE_NEM>1000), " MAT_TOTAL=0:", sum(dt$MAT_TOTAL==0,na.rm=T), "colegios MAT0:", n_distinct(df_final$RBD[df_final$MAT_TOTAL==0 & !is.na(df_final$MAT_TOTAL)]), " dupID:", sum(duplicated(df_final$ID_aux)), "\n")
for (v in c("PROMEDIO_NOTAS","MATE1_REG_ACTUAL","TP_DUMMY","BEA","INGRESO_COLEGIO","PORC_SUP_NOTAS")) print(as.data.frame(bins[[v]])[,c("variable","bin","count_distr","posprob","woe")])
print(as.data.frame(bins$EDAD_MESES)[,c("bin","count_distr","posprob","woe","total_iv")]); print(as.data.frame(bins_dep$DEPENDENCIA_3)[,c("bin","count_distr","posprob","woe","total_iv")]); print(as.data.frame(bins$GRUPO_DEPENDENCIA)[,c("bin","count_distr","posprob")])
cw <- cor(as.data.frame(dt_woe)[,-1]); print(round(cw[c("PROMEDIO_NOTAS_woe","PTJE_NEM_woe","PTJE_RANKING_woe","PORC_SUP_NOTAS_woe","INGRESO_COLEGIO_woe"), c("PTJE_NEM_woe","PTJE_RANKING_woe","PORC_SUP_NOTAS_woe","DEPENDENCIA_3_woe")],2))
# orden VIF, restringido a VIF>2
iv_all <- sapply(bins_iv, function(b) b$total_iv[1]); d <- as.data.frame(dt_woe); vs <- x_iv
repeat { m <- glm(as.formula(paste("PREF_TOP3_DUMMY ~", paste(paste0(vs,"_woe"),collapse="+"))), family=binomial(), data=d)
 v <- suppressMessages(vif(m)); v$variable <- sub("_woe$","",v$variable); v$IV <- iv_all[v$variable]; v$ratio <- v$gvif/v$IV
 if (max(v$gvif) <= 2) break; vv <- v[v$gvif>2,]; s <- vv$variable[which.max(vv$ratio)]
 cat("Sale:", s, "VIF", round(vv$gvif[vv$variable==s],2), "IV", round(iv_all[s],3), "ratio", round(max(vv$ratio),1), "\n"); vs <- setdiff(vs, s) }
print(vs)
fig <- "C:/Proyecto Metodologia de estudio/datos/trabajos/econometria-ii/etapa-2/entrega/figuras/"
g <- woebin_plot(bins[c("CLEC_REG_ACTUAL","MATE1_REG_ACTUAL","PROMEDIO_NOTAS","TP_DUMMY","EDAD_MESES","IVE_MEDIA")])
for (n in names(g)) { png(paste0(fig, n, ".png"), width=1600, height=1000, res=200); print(g[[n]]); dev.off() }
png(paste0(fig, "EDAD_MESES_retramificada.png"), width=1600, height=1000, res=200); print(woebin_plot(bins_edad)[[1]]); dev.off()
png(paste0(fig, "DEPENDENCIA_3.png"), width=1600, height=1000, res=200); print(woebin_plot(bins_dep)[[1]]); dev.off()
