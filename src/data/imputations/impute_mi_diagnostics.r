################################
# Description: Performs a chained imputation to impute missing data
# Reference: https://cran.r-project.org/web/packages/mi/vignettes/mi_vignette.pdf

library(mi) # multiple imputation method to complete missing values in datasets
library(optparse) # parse script arguments in a pythonic way

option_list = list(
  make_option(c("--dataset"),
              type="character", default=NULL, help="Path to the dataset file", metavar="character"),
  make_option(c("--csvSeparator"),
              type="character", default=",", help="Separator for csv columns", metavar="character"),
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
datasetPath <-  opt$dataset
csvSeparator <- opt$csvSeparator
processingCoreQty <- opt$processingCoreQty
chainQty <- opt$chainQty
untilConvergence <- opt$untilConvergence
rHatsConvergence <- opt$rHatsConvergence
maxIterations <- opt$maxIterations
isDetailed <- opt$isDetailed

options(mc.cores = processingCoreQty) # set the number of cores used for imputation

# load data from csv
cat("Loading data from csv...")
miData<-read.csv(datasetPath, sep=csvSeparator, header=TRUE)
cat("Done.\n")

if (isDetailed){
  print("Show raw data before imputation")
  print(miData) # print dataframe for inspection
}

# split data frame into non-numeric and numeric data frames
is.nonnumeric <- function(x) { !is.numeric(x)}
nonNumericColumns <- Filter(is.nonnumeric, miData)
numericColumns <- Filter(is.numeric, miData)

mdf <- missing_data.frame(numericColumns) # create missing data dataframe

if (isDetailed){
    print("Inspect raw data for properties:")
    image(mdf) # print an image of missing datapoints
    summary(mdf) # summarize mdf by providing statistics
    show(mdf) # show assumptions on the data types of the columns
    hist(mdf) # show histogram of columns
}


# TODO: max.minutes seems to be not setable via a variable
mdf <- mi(mdf, n.chains = chainQty, n.iter = 0, max.minutes = 1000000) # initiate mutiple imputation
epoch <- 0
isNotConverged <- TRUE
isFirstRun <- TRUE
while (isFirstRun | untilConvergence & isNotConverged) {
  print(paste0("Performing imputation epoch ", epoch, "..."))
  then <- Sys.time()
  mdf <- mi(mdf, n.iter = maxIterations) # run multiple imputation for indicated maximum iterations and minutes
  latestRHat <-Rhats(mdf)
  
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
  else{
    print("Imputation converged.")
  }
  epoch <- epoch + 1
  isFirstRun <- FALSE
}
cat("Done.\n")

cat("Check if enough iterations were performed...")
round(mipply(mdf, mean, to.matrix = TRUE), 3)

if (isDetailed){
  plot(mdf) # plot the match of imputed and observed data (used to debug convergence)
}

imputedData <- complete(mdf)

imputedDataFrame <- cbind(nonNumericColumns, imputedData)  # merge non-numeric and imputed, numeric data together

# write imputed data to file with timestamp
cat("Writing imputed data to file...")
fileName <- sub(pattern = "(.*?)\\..*$", replacement = "\\1", basename(datasetPath))

# prepare dataset store path
path <- 'data/interim/'
if(!grepl("[0-9]{14}", fileName)){  # try to find a timestamp with 4 digit year and each 2 digits for month, day, hour, minute, second
    # write imputed data to file with timestamp
    cat("Writing imputed data to file...")
    now <- Sys.time()
    path <- paste0(path, format(now, "%Y%m%d%H%M%S"), "_")
}
path <- paste0(path, fileName, "_impType_MI_nIter_", maxIterations, "_chainQty_", chainQty, "_rHatsConvergence_", rHatsConvergence, ".csv")
print(path)
write.csv(imputedDataFrame, file=path, row.names = FALSE)
cat("Done.")
