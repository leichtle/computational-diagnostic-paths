################################
# Description: Performs a chained imputation to impute missing data
# Reference: https://cran.r-project.org/web/packages/mi/vignettes/mi_vignette.pdf

library(mi)

options(mc.cores = processingCoreQty) # set the number of cores used for imputation

# flags for the code
processingCoreQty <- 4
chainQty <- processingCoreQty # number of separate imputation chains
maxIterations <- 2 # maximum iterations of imputations per chain before imputation terminates
# maxImputationMinutes <- 1000000000 # maximum minutes before imputation terminates # TODO: This parameter seems to be not setable via a variable

# load data from csv
cat("Loading data from csv...")
miData<-read.csv("../../results/raw_myocardial_ischemia.csv",sep=",",header=TRUE)
cat("Done.\n")

print("Show raw data before imputation")
print(miData) # print dataframe for inspection

mdf <- missing_data.frame(miData) # create missing data dataframe

print("Inspect raw data for properties:")
image(mdf) # print an image of missing datapoints
summary(mdf) # summarize mdf by providing statistics
show(mdf) # show assumptions on the data types of the columns
hist(mdf) # show histogram of columns

# configure and perform imputation
mdf <- change(mdf, y = c("HDIA", "Klasse"), what="type", to = c("irrelevant", "irrelevant")) # set HDIA and Klasse as irrelevant types which are excluded from the imputation

cat("Performing imputation...")
imputedData <- mi(mdf, n.chains = chainQty, n.iter = maxIterations, R.hat = 1.1, max.minutes = 1000000000) # run multiple imputation for indicated maximum iterations and minutes
cat("Done.\n")

cat("Check if enough iterations were performed...")
round(mipply(imputedData, mean, to.matrix = TRUE), 3)

plot(imputedData) # plot the match of imputed and observed data (used to debug convergence)

# write imputed data to file with timestamp
cat("Writing imputed data to file...")
now <- Sys.time()
fileName <- paste0(format(now, "%Y%m%d%H%M%S-"), "mi-imputation.csv")
write.mi(imputedData, file=fileName, format="csv")
cat("Done.")
