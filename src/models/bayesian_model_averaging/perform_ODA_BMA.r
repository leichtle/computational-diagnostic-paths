################################
# Description: Perform bayesian model averaging to get inclusion probabilities for different lab measurements (e.g. TNT, CK, LDH)
# Reference: https://www.tandfonline.com/doi/abs/10.1198/jasa.2011.tm10518

library(optparse) # parse script arguments in a pythonic way

source("lib/oda.bma.r")
# if(.Platform$OS.type == "unix") {
#   dyn.load("./lib/callmodelprobs.so")  # Linux/Unix
# } else {
#   dyn.load("./lib/callmodelprobs.dll")  # Windows
# }
#
# if(!is.loaded("callmodelprobs")){ # make sure it is loaded
#     stop('callmodelprobs is not loaded')
# }

option_list = list(
    make_option(c("--dataset"),
        type="character", default=NULL, help="The path to the dataset file", metavar="character")
)

# parse script arguments
opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

if (is.null(opt$dataset)){  # print and stop script if dataset file path is missing
    print_help(opt_parser)
    stop("Missing dataset file argument")
}

# load data
dataMatrix <- read.csv(opt$dataset, header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)


burnin.sim <- 500
Gtot <- 1000

xNames = c("ALAT","AP","ASAT","CA","CK","CREA","CRP","GGT","GL", "KA","LDH","NA.","TNT","UREA")

isDetailed <- FALSE # Enable flag here if detailed information on the oda.bma calculation should be printed

## Test run for ICD-10 analogous to PIMA
cat("Sanity check for dataset:\n") # check if dimensions and names of matrix look sane
print(dim(dataMatrix)) # 3424 15
print(names(dataMatrix))
print("---------------------")

# perform inclusion probability computation
cat("Calculating oda bma...")
icd1Y <- dataMatrix$I200_I2519
icd1X <- subset(dataMatrix, select=xNames)
odaResult <- oda.bma(x = icd1X, y = icd1Y, niter = Gtot, burnin = burnin.sim, lambda = 1, model = "probit", prior = "normal")
cat("Done.\n")

# print results
cat("\nResults for mi dataset:\n")
print("---------------------")
if (isDetailed){
  print(names(odaResult))
}

print("Inclusion probabilities of the following features:")
print(xNames)
print(odaResult$incprob.rb) # print inclusion probability

# if detailed is activated, print additional information
if (isDetailed){
  print(odaResult$betabma)
  print(odaResult$incprob)
  print(odaResult$gamma)
  print(odaResult$odds)
}

cat("\n\n")

