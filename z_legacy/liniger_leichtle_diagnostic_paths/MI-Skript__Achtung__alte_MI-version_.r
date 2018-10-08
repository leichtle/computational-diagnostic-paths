# Achtung: ist die benˆtigte "locale" de_CH aktiv?

# Laden der benˆtigten Pakete
library(mi)

#Laden der Daten
MI<-read.csv("/home/alex/Desktop/R_CMD_Scripts/MI.csv",sep=",",header=TRUE)

# TODO[BE]: Use new MI version

#MI
Info_Matrix <- mi.info(data=MI)
Info_Matrix <- mi.info.update.include(object=Info_Matrix, list=list("HDIA" = FALSE, "Klasse" = FALSE))
Preprocessed_Data <- mi.preprocess(data=MI, info=Info_Matrix)
Imputed_Data <- mi(object=Preprocessed_Data, n.iter = 2000, max.minutes = 5000000)  # TODO[BE]: try to activate the imputation for the total number of cores

#Output
write.mi(Imputed_Data, format="csv")