suppressMessages({library(AER)})
data("Fatalities"); F <- Fatalities; F$fr <- F$fatal/F$pop*1e4
a <- subset(F,year==1988); z <- subset(F,year==1982)
cat("n",nrow(a),"\n"); cat("medias fr 82/88:",mean(z$fr),mean(a$fr)," tax 82/88:",mean(z$beertax),mean(a$beertax),"\n")
s88 <- summary(lm(fr~beertax,a)); print(round(coef(s88),4)); cat("R2",s88$r.squared,"\n")
s82 <- summary(lm(fr~beertax,z)); print(round(coef(s82),4))
d <- summary(lm(I(a$fr-z$fr)~I(a$beertax-z$beertax))); print(round(coef(d),4)); cat("R2",d$r.squared,"\n")
cat("mean dtax", mean(a$beertax-z$beertax)," mean dfr",mean(a$fr-z$fr),"\n")
# 2x2: estados que subieron vs no subieron impuesto real
up <- (a$beertax - z$beertax) > 0; cat("n sube",sum(up)," n no",sum(!up),"\n")
cat("fr82 sube",mean(z$fr[up]),"fr88 sube",mean(a$fr[up]),"fr82 no",mean(z$fr[!up]),"fr88 no",mean(a$fr[!up]),"\n")
set.seed(123); p <- runif(100,0,1); y <- rbinom(100,1,p)
auc <- function(y,p){r<-rank(p); n1<-sum(y==1); n0<-sum(y==0); (sum(r[y==1])-n1*(n1+1)/2)/(n1*n0)}
cat("AUC",auc(y,p)," n1",sum(y),"\n")
for(c in c(0.5,0.4)) {cat("corte",c,"\n"); print(table(obs=y,pred=as.integer(p>=c)))}
