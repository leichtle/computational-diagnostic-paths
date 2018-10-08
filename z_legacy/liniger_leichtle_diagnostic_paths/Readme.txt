Da die Skripte gegenseitig aufeinander verweisen, sollten sie im gleichen Ordner liegen und R daraus gestartet werden (Working Directory - getwd() bzw. setwd().
Primär muß die C-Datei geladen werden, das am besten direkt in der linux-Shell
( R CMD SHLIB callmodelprobs.c ). 
Manchmal klappt das nicht und linux sagt, es habe nichts zu tun. Dann mit gedit die C-Datei öffnen und wieder speichern. Dann glaubt linux, sie sei verändert und compiliert neu. Auf korrekte Rechnerzeit achten!
Danach den Erfolg des Ladens testen:

dyn.load("callmodelprobs.so") 
is.loaded("callmodelprobs") # make sure it is loaded

Dann kann man das PIMA-Beispiel aus calc-modelprobs rechnen. Gegebenenfalls müssen die R-Skripte im Verzeichnins noch separat ausgeführt werden. Zu beachten ist, daß als "y" der Klassifikator  bezeichnet wird, mit "x" die Parameterdaten

Weiter im Text:
source("oda.bma.r")
## Datenbasis
Datenmatrix <- read.table("MI_comb_20_iter.csv", header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)

## Test run for ICD-10 analogous to PIMA (MI_1)
burnin.sim <- 500;
Gtot <- 1000;
library(MASS)
subset_1 <- subset(Datenmatrix, select=c(ALAT.1,AP.1,ASAT.1,CA.1,CK.1,CREA.1,CRP.1,GGT.1,GL.1,I200_I2519,
  KA.1,LDH.1,NA.1,TNT.1,UREA.1))
dim(subset_1) # 3424 15
names(subset_1)
icd_1y <- subset_1$I200_I2519
icd_1x <- subset_1[,c(1:9,11:15)]
oda.icd_1 <- oda.bma(x=icd_1x,y=icd_1y,niter=Gtot,burnin=burnin.sim,lambda=1,model="probit",prior="normal");
names(oda.icd_1)
oda.icd_1$incprob.rb
oda.icd_1$betabma
oda.icd_1$incprob
oda.icd_1$gamma
oda.icd_1$odds

## Test run for ICD-10 analogous to PIMA (MI_2)
burnin.sim <- 500;
Gtot <- 1000;
library(MASS)
subset_2 <- subset(Datenmatrix, select=c(ALAT.2,AP.2,ASAT.2,CA.2,CK.2,CREA.2,CRP.2,GGT.2,GL.2,I200_I2519,
  KA.2,LDH.2,NA.2,TNT.2,UREA.2))
dim(subset_2) # 3424 15
names(subset_2)
icd_2y <- subset_2$I200_I2519
icd_2x <- subset_2[,c(1:9,11:15)]
oda.icd_2 <- oda.bma(x=icd_2x,y=icd_2y,niter=Gtot,burnin=burnin.sim,lambda=1,model="probit",prior="normal");
names(oda.icd_2)
oda.icd_2$incprob.rb
oda.icd_2$betabma
oda.icd_2$incprob
oda.icd_2$gamma
oda.icd_2$odds

## Test run for ICD-10 analogous to PIMA (MI_3)
burnin.sim <- 500;
Gtot <- 1000;
library(MASS)
subset_3 <- subset(Datenmatrix, select=c(ALAT.3,AP.3,ASAT.3,CA.3,CK.3,CREA.3,CRP.3,GGT.3,GL.3,I200_I2519,
  KA.3,LDH.3,NA.3,TNT.3,UREA.3))
dim(subset_3) # 3424 15
names(subset_3)
icd_3y <- subset_3$I200_I2519
icd_3x <- subset_3[,c(1:9,11:15)]
oda.icd_3 <- oda.bma(x=icd_3x,y=icd_3y,niter=Gtot,burnin=burnin.sim,lambda=1,model="probit",prior="normal");
names(oda.icd_3)
oda.icd_3$incprob.rb
oda.icd_3$betabma
oda.icd_3$incprob
oda.icd_3$gamma
oda.icd_3$odds


Damit sind für die drei Imputationsketten jeweils die Rao-Blackwell-Einschlußwahrscheinlichkeiten berechnet, unter oda.icd_X$incprob.rb


Nun werden die Einschlußwahrscheinlichkeiten in einer separaten Datei (neue Datenmatrix) zusammengestellt:

Daraus werden nun mittels Bootstrap die Mediane und deren Konfidenzintervalle berechnet:

## Bootstrap of the inclusion probabilities
MED <-function(x,d){
  return(quantile(x[d],probs=c(0.5)))
}
library(boot)

med<- boot(x, MED, R=1000) ## Achtung: Ist das korrekt?
med
bcim<-boot.ci(med, R=1000)
bcim


Danach kann die Datenmatrix für die Abbildung erstellt werden:

Aus dieser Datei wird dann die Abbildung generiert:

library(gplots, pos=4)
l<-Datenmatrix$lCI_Bca
l
u<-Datenmatrix$uCI_Bca
u
barplot2(Datenmatrix$Median,plot.ci = TRUE,ci.l=l,ci.u=u,axes=TRUE,axisnames=TRUE, names=n)
## ggf kann Names direkt aus der Datenmatrix gelesen werden
Datenmatrix$Median
d<-(Datenmatrix$Median)
d
colnames(Datenmatrix)<- n
n
e
n<-as.character(Datenmatrix$Name)
rownames(Datenmatrix$Median)<-n


Visualisierung der Modelle:
# matrix of unique models from ODA
gamma.u <- unique(oda.icd_1$gamma[-c(1:burnin.sim),])

# vector of RB estimates of model probabilities corresponding to models in gamma.u
probest <- modelprobs.rb(n.unique=nrow(gamma.u),niter=nrow(oda.icd_1$incprob[-c(1:burnin.sim),]),p=ncol(gamma.u),
         gammaunique=t(gamma.u),probmat.oda=t(oda.icd_1$incprob[-c(1:burnin.sim),]))

# Estimated posterior probability of unsampled models

library(devEMF, pos=4)
library(bipartite, pos=4)
1-sum(probest) 
gamma.u
probest
dev.cur()
emf(file="icd_1.emf")
visweb(gamma.u,type="None")
dev.off()

Betabma zeigt die Modellparameter für die einzelnen Werte.
