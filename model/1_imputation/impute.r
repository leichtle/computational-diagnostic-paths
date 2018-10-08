library(mi)

# load data from csv
cat("Loading data from csv...")
miData<-read.csv("../../data/raw_myocardial_ischemia.csv",sep=",",header=TRUE)
cat("Done.\n")

print("Show raw data before imputation")
print(miData) # print dataframe for inspection

print("Inspect raw data for properties:")
mdf <- mi(miData) # create imputation dataframe for imputation
# image(mdf)
summary(mdf)

options(mc.cores = 4) # set the number of cores used for imputation

# infoMatrix <- mi.info(data=miData)
# infoMatrix <- mi.info.update.include(object=infoMatrix, list=list("HDIA" = FALSE, "Klasse" = FALSE))
# preprocessedData <- mi.preprocess(data=miData, info=infoMatrix)  # preprocess data
# configure and perform imputation
mdf <- change(mdf, y = c("HDIA", "Klasse"), what="type", to = c("irrelevant", "irrelevant")) # set HDIA and Klasse as irrelevant types which are excluded from the imputation

cat("Performing imputation...")
imputedData <- mi(mdf, n.iter = 2000, max.minutes = 5000000) # run multiple imputation for indicated maximum iterations and minutes
cat("Done.\n")

# write imputed data to file with timestamp
cat("Writing imputed data to file...")
now <- Sys.time()
fileName <- paste0(format(now, "%Y%m%d%H%M%S-"), "mi-imputation.csv")
write.mi(imputedData, file=fileName, format="csv")
cat("Done.")
