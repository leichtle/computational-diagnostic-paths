################################
# Description: Adds a label row which indicates that the diagnose for this case belongs to a certain target range (e.g. Ischemic heart diseases)
# Reference: https://www.icd10data.com/ICD10CM/Codes/I00-I99/I20-I25

library(stringr)

# load data from csv
cat("Loading data from csv...")
dataMatrix <- read.csv("../1_imputation/results/20140721000000-mi-imputation.csv", header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)
cat("Done.\n")

dataMatrix$I200_I2519<-ifelse(grepl("^I([2-9][0-9][0-9]|1[0-9][0-9][0-9]|2[0-5][0-1][0-9])$", dataMatrix$HDIA),1,0)

# write imputed data to file with timestamp
cat("Writing imputed data with added label column to file...")
now <- Sys.time()
fileName <- paste0("./results/", format(now, "%Y%m%d%H%M%S-"), "mi-imputation+label.csv")
write.csv(dataMatrix, file=fileName)
cat("Done.")
