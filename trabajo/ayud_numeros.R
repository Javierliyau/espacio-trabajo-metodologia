suppressMessages({library(AER); library(scorecard); library(dplyr)})
data("PSID1976")
m <- data.frame(inlf=as.integer(PSID1976$participation=="yes"),
  nwifeinc=(PSID1976$fincome-PSID1976$hours*PSID1976$wage)/1000,
  educ=PSID1976$education, exper=PSID1976$experience, age=PSID1976$age,
  kidslt6=PSID1976$youngkids, kidsge6=PSID1976$oldkids)
m$expersq <- m$exper^2
f <- inlf ~ nwifeinc + educ + exper + expersq + age + kidslt6 + kidsge6
cat("== tabla inlf\n"); print(table(m$inlf))
mpl <- lm(f, m); lo <- glm(f, binomial, m); pr <- glm(f, binomial(link="probit"), m)
cat("== coefs\n"); print(round(cbind(MPL=coef(mpl), Logit=coef(lo), Probit=coef(pr)),4))
cat("== rango pred MPL\n"); print(round(range(fitted(mpl)),3)); cat("n<0:",sum(fitted(mpl)<0)," n>1:",sum(fitted(mpl)>1),"\n")
v <- c("nwifeinc","educ","exper","expersq","age","kidslt6","kidsge6")
med <- colMeans(m[,v]); cat("== medias\n"); print(round(med,3))
zb <- sum(coef(lo)*c(1,med)); Pb <- plogis(zb); gb <- dlogis(zb)
cat("zbar",zb," P(zbar)",Pb," g(zbar)",gb,"\n")
cat("EPeP educ",gb*coef(lo)["educ"]," regla/4 educ",coef(lo)["educ"]/4,"\n")
cat("EPP educ", mean(dlogis(predict(lo)))*coef(lo)["educ"], " mean g_i", mean(dlogis(predict(lo))),"\n")
cat("kidslt6 +1 en medias: G(zb+b)-G(zb)=", plogis(zb+coef(lo)["kidslt6"])-Pb,"\n")
cat("dP/dexper en media:", gb*(coef(lo)["exper"]+2*coef(lo)["expersq"]*med["exper"]),"\n")
cat("== OR\n"); print(round(exp(coef(lo)),3))
L0 <- as.numeric(logLik(glm(inlf~1,binomial,m))); L1 <- as.numeric(logLik(lo))
cat("lnL modelo",L1," lnL0",L0," McFadden",1-L1/L0,"\n")
p <- fitted(lo); cm <- table(obs=m$inlf, pred=as.integer(p>=0.5)); cat("== confusion 0.5\n"); print(cm)
auc <- function(y,p){r<-rank(p); n1<-sum(y==1); n0<-sum(y==0); (sum(r[y==1])-n1*(n1+1)/2)/(n1*n0)}
cat("AUC",auc(m$inlf,p),"\n")
cs <- sort(unique(p)); J <- sapply(cs,function(c){pp<-p>=c; mean(pp[m$inlf==1])+mean(!pp[m$inlf==0])-1})
c0 <- cs[which.max(J)]; cat("Youden corte",c0," J",max(J),"\n"); print(table(obs=m$inlf, pred=as.integer(p>=c0)))
cat("ratios logit/probit:\n"); print(round(coef(lo)[-1]/coef(pr)[-1],2)); print(round(coef(mpl)[-1]/coef(lo)[-1],3))
# ---- germancredit
data("germancredit"); g <- germancredit; g$creditability <- ifelse(g$creditability=="bad",1,0)
cat("== tasa malos", mean(g$creditability),"\n")
t <- g %>% group_by(status.of.existing.checking.account) %>% summarise(n=n(),buenos=sum(creditability==0),malos=sum(creditability==1)) %>%
  mutate(dB=buenos/sum(buenos), dM=malos/sum(malos), WOE=log(dB/dM)*100, IV=(dB-dM)*log(dB/dM))
print(as.data.frame(t), digits=4); cat("IV total", sum(t$IV),"\n")
dl <- split_df(g, y="creditability", ratio=0.7, seed=2026); tr <- dl$train; te <- dl$test
ivt <- iv(tr, y="creditability"); vv <- setdiff(ivt$variable[ivt$info_value>=0.02],"foreign.worker")
trf <- as.data.frame(tr %>% select(all_of(vv), creditability))
b <- suppressMessages(woebin(trf, y="creditability", print_step=0))
trw <- woebin_ply(trf, b, print_step=0); mod <- glm(creditability~., binomial, trw)
card <- scorecard(b, mod, points0=600, odds0=1/50, pdo=20)
cat("== basepoints\n"); print(card$basepoints)
cat("== card checking account\n"); print(names(card)); print(as.data.frame(card[["status.of.existing.checking.account"]]))
sc <- scorecard_ply(te, card, print_step=0); d <- data.frame(score=sc$score, malo=te$creditability)
cortes <- seq(min(d$score), max(d$score), by=10)
pol <- do.call(rbind, lapply(cortes, function(c){a<-d[d$score>=c,]; data.frame(corte=c, aprob=nrow(a), tasa=nrow(a)/nrow(d), malos=sum(a$malo))}))
pol$buenos <- pol$aprob-pol$malos; pol$util <- 100*pol$buenos-500*pol$malos
print(pol); print(pol[which.max(pol$util),])
# ---- Fatalities
data("Fatalities"); F <- Fatalities; F$fr <- F$fatal/F$pop*1e4
a <- subset(F,year==1988); z <- subset(F,year==1982)
cat("== simple 1988\n"); print(coef(lm(fr~beertax,a))); cat("== PD\n"); print(coef(lm(I(a$fr-z$fr)~I(a$beertax-z$beertax))))
