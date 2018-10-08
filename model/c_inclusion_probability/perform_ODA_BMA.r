################################
# Description: Perform bayesian model averaging to get inclusion probabilities for different lab measurements (e.g. TNT, CK, LDH)
# Reference: https://www.tandfonline.com/doi/abs/10.1198/jasa.2011.tm10518

library(MASS)
library(data.table)

source("lib/oda.bma.r")
if(.Platform$OS.type == "unix") {
  dyn.load("./lib/callmodelprobs.so")  # Linux/Unix
} else {
  dyn.load("./lib/callmodelprobs.dll")  # Windows 
}

is.loaded("callmodelprobs") # make sure it is loaded

# load data
dataMatrix <- read.table("../imputation/results/20140721000000_mi_comb_20_iter.csv", header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)
dataMatrix1 <- subset(dataMatrix, select=c(ALAT.1,AP.1,ASAT.1,CA.1,CK.1,CREA.1,CRP.1,GGT.1,GL.1,I200_I2519, KA.1,LDH.1,NA.1,TNT.1,UREA.1))
colnames(dataMatrix1) <- c("ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "I200_I2519", "KA","LDH","NA.","TNT","UREA")

dataMatrix2 <- subset(dataMatrix, select=c(ALAT.2,AP.2,ASAT.2,CA.2,CK.2,CREA.2,CRP.2,GGT.2,GL.2,I200_I2519, KA.2,LDH.2,NA.2,TNT.2,UREA.2))
colnames(dataMatrix2) <- c("ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "I200_I2519", "KA","LDH","NA.","TNT","UREA")

dataMatrix3 <- subset(dataMatrix, select=c(ALAT.3,AP.3,ASAT.3,CA.3,CK.3,CREA.3,CRP.3,GGT.3,GL.3,I200_I2519, KA.3,LDH.3,NA.3,TNT.3,UREA.3))
colnames(dataMatrix3) <- c("ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "I200_I2519", "KA","LDH","NA.","TNT","UREA")

dataMatrix1 <- read.csv("../b_add_label_row/results/20181003161605-mi-imputation+label.csv", header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)
# dataMatrix2 <- read.csv("../imputation/results/20140721000001-mi-imputation.csv", header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)
# dataMatrix3 <- read.csv("../imputation/results/20140721000002-mi-imputation.csv", header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)

burnin.sim <- 500
Gtot <- 1000

xNames = c("ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "KA","LDH","NA.","TNT","UREA")

dataTensor <- list(dataMatrix1, dataMatrix2, dataMatrix3)
odaResultList <- list()

isDetailed <- FALSE # Enable flag here if detailed information on the oda.bma calculation should be printed

for (i in 1:3){
  ## Test run for ICD-10 analogous to PIMA
  cat("Sanity check for mi",i, ":\n") # check if dimensions and names of matrix look sane
  print(dim(dataTensor[[i]])) # 3424 15
  print(names(dataTensor[[i]]))
  print("---------------------")
  
  # perform inclusion probability computation
  cat("Calculating oda bma...")
  icd1Y <- dataTensor[[i]]$I200_I2519
  icd1X <- subset(dataTensor[[i]], select=xNames)
  odaResultList[[i]] <- oda.bma(x = icd1X, y = icd1Y, niter = Gtot, burnin = burnin.sim, lambda = 1, model = "probit", prior = "normal")
  cat("Done.\n")
  
  # print results
  cat("\nResults for mi",i, ":\n")
  print("---------------------")
  if (isDetailed){
    print(names(odaResultList[[i]]))
  }
  
  print("Inclusion probabilities of the following features:")
  print(xNames)
  print(odaResultList[[i]]$incprob.rb) # print inclusion probability
  
  # if detailed is activated, print additional information
  if (isDetailed){
    print(odaResultList[[i]]$betabma)
    print(odaResultList[[i]]$incprob)
    print(odaResultList[[i]]$gamma)
    print(odaResultList[[i]]$odds)
  }
  
  cat("\n\n")
}
