setwd("C:/Espacio de trabajo Metodologia de estudio/trabajo/econometria-ii-demre")
src <- readLines("C:/Users/javie/Downloads/Trabajo etapa 2 econometria.II (1).R", encoding = "UTF-8")
src <- src[!(grepl("write_xlsx", src, fixed=TRUE) | grepl("woebin_plot", src, fixed=TRUE) | grepl("boxplot", src, fixed=TRUE))]
pdf(NULL); suppressMessages(invisible(capture.output(eval(parse(text = src), envir = globalenv()))))
iv_all <- sapply(bins_iv, function(b) b$total_iv[1]); print(round(iv_all[x_iv],3))
dt_woe <- as.data.frame(dt_woe); vars_sel <- x_iv
repeat {
  m <- glm(as.formula(paste("PREF_TOP3_DUMMY ~", paste(paste0(vars_sel, "_woe"), collapse=" + "))), family=binomial(), data=dt_woe)
  v <- suppressMessages(vif(m)); v$variable <- sub("_woe$","",v$variable); v$IV <- iv_all[v$variable]; v$ratio <- v$gvif/v$IV
  if (max(v$gvif) <= 2) { print(v[order(-v$ratio),]); break }
  vv <- v[v$gvif > 2, ]; sale <- vv$variable[which.max(vv$ratio)]; cat("Sale:", sale, "VIF", round(max(v$gvif[v$variable==sale]),2), "IV", round(iv_all[sale],3), "\n")
  vars_sel <- setdiff(vars_sel, sale) }
print(vars_sel); print(summary(m)$coefficients |> round(3))
