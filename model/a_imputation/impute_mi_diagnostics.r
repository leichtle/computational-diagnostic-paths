################################
# Description: Performs a chained imputation to impute missing data
# Reference: https://cran.r-project.org/web/packages/mi/vignettes/mi_vignette.pdf

library(mi)
library("optparse")

options(mc.cores = processingCoreQty) # set the number of cores used for imputation

# flags for the code
processingCoreQty <- 4
chainQty <- processingCoreQty # number of separate imputation chains
untilConvergence <- TRUE
rHatsConvergence <- 1.1
maxIterations <- 200 # maximum iterations of imputations per chain before imputation terminates
# maxImputationMinutes <- 1000000000 # maximum minutes before imputation terminates # TODO: This parameter seems to be not setable via a variable
isDetailed <- FALSE

option_list = list(
  make_option(c("-f", "--file"), type="character", default=NULL, 
              help="dataset file name", metavar="character")
); 
 
opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

if (is.null(opt$file)){
  print_help(opt_parser)
}

# load data from csv
cat("Loading data from csv...")
miData<-read.csv(opt$file,sep=",",header=TRUE)
cat("Done.\n")

if (isDetailed){
  print("Show raw data before imputation")
  print(miData) # print dataframe for inspection
}

mdf <- missing_data.frame(miData) # create missing data dataframe

if (isDetailed){
  print("Inspect raw data for properties:")
  image(mdf) # print an image of missing datapoints
  summary(mdf) # summarize mdf by providing statistics
  show(mdf) # show assumptions on the data types of the columns
  hist(mdf) # show histogram of columns
}

# configure and perform imputation
mdf <- change(mdf, y = c("HDIA", "Klasse"), what="type", to = c("irrelevant", "irrelevant")) # set HDIA and Klasse as irrelevant types which are excluded from the imputation

cat("Performing imputation...")
isNotConverged = TRUE

while (untilConvergence & isNotConverged) {
  then <- Sys.time()
  imputedData <- mi(mdf, n.chains = chainQty, n.iter = maxIterations, max.minutes = 200) # run multiple imputation for indicated maximum iterations and minutes
  latestRHat <-Rhats(imputedData)
  
  # calculate and print imputations per minute
  now <- Sys.time()
  diff <- as.numeric(difftime(now, then, units="secs"))
  
  cat("Imputation speed:")
  cat(maxIterations/diff*60)
  print("/min")
  print("Rhat to measure convergence of imputation (should be < 1.1):")
  print(latestRHat)
  isNotConverged <- any(latestRHat > rHatsConvergence)
  if(isNotConverged){
    print("Imputation not converged. Continuing...")
  }
}
cat("Done.\n")

cat("Check if enough iterations were performed...")
round(mipply(imputedData, mean, to.matrix = TRUE), 3)

if (isDetailed){
  plot(imputedData) # plot the match of imputed and observed data (used to debug convergence)
}

# write imputed data to file with timestamp
cat("Writing imputed data to file...")
now <- Sys.time()
fileName <- paste0("./results/", format(now, "%Y%m%d%H%M%S-"), "mi-imputation.csv")
write.mi(imputedData, file=fileName, format="csv")
cat("Done.")
