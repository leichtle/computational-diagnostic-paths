## Datenbasis
Datenmatrix <- read.table("/home/alex/Desktop/MI_comb_20_iter.csv", header=TRUE, sep=",", na.strings="NA", 
  dec=".", strip.white=TRUE)

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


