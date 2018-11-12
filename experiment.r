###
# Perform bayesian variable selection to obtain inclusion probabilities.
###

library(optparse) # parse script arguments in a pythonic way
source("./src/models/bayesian_model_averaging/oda_bma/oda.bma.r", chdir=TRUE)

# configure parser and parse arguments
optionList = list(
make_option(c("--dataset"),
type="character", default="./data/interim/20140721000003_myocardial_ischemia_16_impType_MI_nIter_20_label.csv", help="Path to the dataset file", metavar="character"),
make_option(c("--label"),
type="character", default="diagnostic_outcome", help="Label of the dataset", metavar="character"),
make_option(c("--niter"),
type="integer", default=1000, help="The number of iterations to perform", metavar = "integer"),
make_option(c("--burnIn"),
type="integer", default=500, help="The number of iterations we discard to tune the initial probabilities (burn-in)", metavar = "integer"),
make_option(c("--lambda"),
type="double", default=1, help="lambda", metavar = "double"),
make_option(c("--appendix"),
type="character", help="Optional repetition id of the experiment to explore convergence across multiple chains", metavar = "character"))

# parse script arguments
optParser <- OptionParser(option_list=optionList)
opt <- parse_args(optParser)

if (is.null(opt$dataset)){  # print and stop script if dataset file path is missing
    print_help(optParser)
    stop("Missing dataset file argument")
}
datasetPath <- opt$dataset
iterationQty <- opt$niter
burnIn <- opt$burnIn
lambda <- opt$lambda
label <- opt$label
if (is.null(opt$appendix)){
    appendix <- ""
} else {
    appendix <- paste0("_", opt$appendix)
}

# load data from csv
cat("Loading data from csv...")
miData<-read.csv(opt$dataset, sep=",", header=TRUE)
cat("Done.\n")

# Calculate oda inclusion probabilities for ICD-10
cat("Sanity check for dataset:\n") # check if dimensions and names of matrix look sane
print(dim(miData)) # 3424 15
print(names(miData))
print("---------------------")

# extract feature names
columnNames <- colnames(miData)
isNotLabel <- function(x){x != label}
featureNames <- Filter(isNotLabel, columnNames)

print("Features:")
print(featureNames)
print("Label:")
print(label)

features <- subset(miData, select=featureNames)  # extract features
labels <- miData[label]  # extract label

odaResults <- oda.bma(x = features, y = labels, niter = iterationQty, burnin = burnIn, lambda = lambda, model = "probit", prior = "normal")

# print(odaResults$incprob.rb)
# print(odaResults$betabma)
# print(odaResults$incprob)
# print(odaResults$gamma)
# print(odaResults$odds)

# create a new dataset for inclusion probabilities
incprobsDf <- data.frame(matrix(ncol = length(featureNames), nrow = 0))
colnames(incprobsDf) <- featureNames
incprobsDf[1,] <- odaResults$incprob.rb

print("Results:")
print(incprobsDf)

cat("Writing dataset to file...")
fileName <- sub(pattern = "(.*?)\\.[a-zA-Z]*$", replacement = "\\1", basename(datasetPath))

# prepare dataset store path
path <- 'data/interim/'
if(!grepl("[0-9]{14}", fileName)){  # try to find a timestamp with 4 digit year and each 2 digits for month, day, hour, minute, second
    # write imputed data to file with timestamp
    cat("Writing imputed data to file...")
    now <- Sys.time()
    path <- paste0(path, format(now, "%Y%m%d%H%M%S"), "_")
}
path <- paste0(path, fileName, "_niter_", iterationQty, "_burnIn_", burnIn, "_lambda_", lambda, "_incprobs", appendix, ".csv")
print(path)
write.csv(incprobsDf, file=path, row.names = FALSE)
cat("...Done.")

