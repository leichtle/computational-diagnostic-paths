###
# Bootstrap
###

library(optparse) # parse script arguments in a pythonic way
library(boot)

# configure parser and parse arguments
optionList = list(
make_option(c("--datasets"),
type="character", help="Paths to the dataset files (separated by ;)", metavar="character"))

# parse script arguments
optParser <- OptionParser(option_list=optionList)
opt <- parse_args(optParser)

if (is.null(opt$datasets)){  # print and stop script if dataset file path is missing
    print_help(optParser)
    stop("Missing dataset files argument")
}

dataset_paths <- strsplit(opt$datasets, ";")

datasetList <- c()
i <- 1
for (path in dataset_paths){
    datasetList[[i]] <- read.csv(path, sep=",", header=TRUE)
}

# join datasets

inclusionProbDf <- rbindlist(datasetList)

cat("Calculate median and confidence intervalls...")

# use the bootstrap library to calculate median and confidence intervalls

## Bootstrap of the inclusion probabilities
median_function <-function(x,d){
    return(quantile(x[d],probs=c(0.5)))
}


medians<- boot(inclusionProbDf, median_function, R=1000) # find the medians by sampling
medians

confidenceIntervalls<-boot.ci(medians, conf=0.95, R=1000) # calculate the 95% confidence intervalls by sampling
confidenceIntervalls

cat("...Done.")




