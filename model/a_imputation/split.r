# Title     : TODO
# Objective : TODO
# Created by: I0325777
# Created on: 2018-10-12


dataMatrix <- read.table("../a_imputation/results/20140721000000-mi-imputation_comb_20_iter.csv", header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)
dataMatrix1 <- subset(dataMatrix, select=c(Klasse, HDIA, ALAT.1,AP.1,ASAT.1,CA.1,CK.1,CREA.1,CRP.1,GGT.1,GL.1,I200_I2519, KA.1,LDH.1,NA.1,TNT.1,UREA.1))
colnames(dataMatrix1) <- c("Klasse", "HDIA", "ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "I200_I2519", "KA","LDH","NA.","TNT","UREA")

dataMatrix2 <- subset(dataMatrix, select=c(Klasse, HDIA, ALAT.2,AP.2,ASAT.2,CA.2,CK.2,CREA.2,CRP.2,GGT.2,GL.2,I200_I2519, KA.2,LDH.2,NA.2,TNT.2,UREA.2))
colnames(dataMatrix2) <- c("Klasse", "HDIA","ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "I200_I2519", "KA","LDH","NA.","TNT","UREA")

dataMatrix3 <- subset(dataMatrix, select=c(Klasse, HDIA, ALAT.3,AP.3,ASAT.3,CA.3,CK.3,CREA.3,CRP.3,GGT.3,GL.3,I200_I2519, KA.3,LDH.3,NA.3,TNT.3,UREA.3))
colnames(dataMatrix3) <- c("Klasse", "HDIA","ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "I200_I2519", "KA","LDH","NA.","TNT","UREA")

# write imputed data to file with timestamp
cat("Writing imputed data to file...")
now <- Sys.time()
fileName <- paste0("./results/", format(now, "%Y%m%d%H%M%S-"), "mi-imputation1.csv")
print(fileName)
write.csv(dataMatrix1, file=fileName, row.names=FALSE)
cat("Done.")

# write imputed data to file with timestamp
cat("Writing imputed data to file...")
now <- Sys.time()
fileName <- paste0("./results/", format(now, "%Y%m%d%H%M%S-"), "mi-imputation2.csv")
print(fileName)
write.csv(dataMatrix2, file=fileName, row.names=FALSE)
cat("Done.")

# write imputed data to file with timestamp
cat("Writing imputed data to file...")
now <- Sys.time()
fileName <- paste0("./results/", format(now, "%Y%m%d%H%M%S-"), "mi-imputation3.csv")
print(fileName)
write.csv(dataMatrix3, file=fileName, row.names=FALSE)
cat("Done.")
