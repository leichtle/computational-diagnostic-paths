################################
# Description: Performs a chained imputation to impute missing data
# Reference: https://cran.r-project.org/web/packages/mi/vignettes/mi_vignette.pdf

library(mi) # multiple imputation method to complete missing values in datasets
library(optparse) # parse script arguments in a pythonic way

option_list = list(
  make_option(c("--dataset"),
              type="character", default=NULL, help="Path to the dataset file", metavar="character"),
  make_option(c("--processingCoreQty"),
              type="integer", default=4, help="Number of cores to run imputation on", metavar = "integer"),
  make_option(c("--chainQty"),
              type="integer", default=4, help="Number of separate imputation chains", metavar = "integer"),
  make_option(c("--untilConvergence"),
              type="logical", default=TRUE, help="If chains should be imputed until convergence", metavar = "logical"),
  make_option(c("--rHatsConvergence"),
              type="double", default=1.1, help="Consider imputation converged if variance_across_chains/variance_within_chain <= rHatsConvergence", metavar = "double"),
  make_option(c("--maxIterations"),
              type="integer", default=200, help="Maximum iterations of imputations per chain before imputation checks for convergence", metavar = "integer"),
  make_option(c("--isDetailed"),
              type="logical", default=FALSE, help="Perform extra prints and outputs", metavar = "logical")
  
)

# parse script arguments 
opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

if (is.null(opt$dataset)){  # print and stop script if dataset file path is missing
  print_help(opt_parser)
  stop("Missing dataset file argument")
}

options(mc.cores = opt$processingCoreQty) # set the number of cores used for imputation

# load data from csv
cat("Loading data from csv...")
miData<-read.csv(opt$dataset, sep=",", header=TRUE)
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
  # TODO: max.minutes seems to be not setable via a variable
  imputedData <- mi(mdf, n.chains = opt$chainQty, n.iter = maxIterations, max.minutes = 200) # run multiple imputation for indicated maximum iterations and minutes
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
print(fileName)
write.mi(imputedData, file=fileName, format="csv")
cat("Done.")
