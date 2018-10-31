###
# Perform bayesian variable selection to obtain inclusion probabilities.
###

library(optparse) # parse script arguments in a pythonic way
source("./src/models/bayesian_model_averaging/oda_bma/oda.bma.r", chdir=TRUE)

# configure parser and parse arguments
option_list = list(
make_option(c("--dataset"),
type="character", default="./data/interim/20140721000003_myocardial_ischemia_16_impType_MI_nIter_20_label.csv", help="Path to the dataset file", metavar="character"),
make_option(c("--label"),
type="character", default="diagnostic_outcome", help="Label of the dataset", metavar="character"),
make_option(c("--niter"),
type="integer", default=100000, help="The number of iterations to perform", metavar = "integer"),
make_option(c("--burn_in_sim"),
type="integer", default=500, help="Burn in sim", metavar = "integer"),
make_option(c("--lam_spec"),
type="double", default=1, help="lam spec", metavar = "double"))

# parse script arguments
opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

if (is.null(opt$dataset)){  # print and stop script if dataset file path is missing
print_help(opt_parser)
stop("Missing dataset file argument")
}
datasetPath <- opt$dataset
iterationQty <- opt$niter
burnInSim = opt$burn_in_sim
lamSpec = opt$lam_spec
label = opt$label

# load data from csv
cat("Loading data from csv...")
miData<-read.csv(opt$dataset, sep=",", header=TRUE)
cat("Done.\n")

# TODO: improve extraction of features by discarding HDIA and Klasse from dataset in add_label_row
#feature_names = [column_name for column_name in mi_df.colums if column_name is not label]
featureNames <- c("ALAT", "AP", "ASAT", "CA", "CK", "CREA", "CRP", "GGT", "GL", "KA", "LDH", "NA.", "TNT", "UREA")

# Calculate oda inclusion probabilities for ICD-10
cat("Sanity check for dataset:\n") # check if dimensions and names of matrix look sane
print(dim(miData)) # 3424 15
print(names(miData))
print("---------------------")

features <- subset(miData, select=featureNames)  # extract features
label = miData[label]  # extract label

odaResults <- odaResult <- oda.bma(x = features, y = label, niter = iterationQty, burnin = burnInSim, lambda = lamSpec, model = "probit", prior = "normal")

print("Results:")
print(odaResults$incprob.rb)
print(odaResults)
print(featureNames)
print(odaResults$names)

# print(odaResult$betabma)
# print(odaResult$incprob)
# print(odaResult$gamma)
# print(odaResult$odds)

# create a new dataset for inclusion probabilities
incprobsDf <- data.frame(matrix(ncol = length(featureNames), nrow = 0))
colnames(incprobsDf) <- featureNames
incprobsDf[1,] <- odaResults$incprob.rb

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
path <- paste0(path, fileName, "_incprobs.csv")
print(path)
write.csv(incprobsDf, file=path, row.names = FALSE)
cat("...Done.")

