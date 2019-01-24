################################
# Description: Performs a chained imputation to impute missing data
# Reference: https://cran.r-project.org/web/packages/mi/vignettes/mi_vignette.pdf

# some imports are inline with their usage because their method names collide due R's lack of namespaces

library(optparse) # parse script arguments in a pythonic way

optionList = list(
make_option(c("--dataset"),
    type = "character", default = "./data/raw/myocardial_ischemia_16.csv ", help = "Path to the dataset file", metavar = "character"),
make_option(c("--csvSeparator"),
    type = "character", default = ",", help = "Separator for csv columns", metavar = "character"),
make_option(c("--imputationPackage"),
    type = "character", default = "mice", help = "Package of imputation: mi or mice", metavar = "character"),
make_option(c("--imputationMethod"),
    type = "character", default = "cart", help = "Method of imputation in mice: e.g. ppn or cart", metavar = "character"),
make_option(c("--processingCoreQty"),
    type = "integer", default = 4, help = "Number of cores to run imputation on", metavar = "integer"),
make_option(c("--normalizedImputation"),
    type = "logical", default = FALSE, help = "If data should be normalized before and denormalized after imputation", metavar = "logical"),
make_option(c("--chainQty"),
    type = "integer", default = 4, help = "Number of separate imputation chains", metavar = "integer"),
make_option(c("--untilConvergence"),
    type = "logical", default = TRUE, help = "If chains should be imputed until convergence", metavar = "logical"),
make_option(c("--rHatsConvergence"),
    type = "double", default = 1.1, help = "Consider imputation converged if variance_across_chains/variance_within_chain <= rHatsConvergence", metavar = "double"),
make_option(c("--maxIterations"),
    type = "integer", default = 100, help = "Total iterations of imputations per chain before imputation checks for convergence or finishes", metavar = "integer"),
make_option(c("--clusterSeed"),
    type = "integer", default = 7, help = "The seed for randomness to generate random seeds for the different cluster nodes to randomize mice", metavar = "integer"),
make_option(c("--storeAllImputations"),
    type = "logical", default = FALSE, help = "Save all imputations to disk with a ordinal postfix e.g. _1", metavar = "logical"),
make_option(c("--isDetailed"),
    type = "logical", default = FALSE, help = "Perform extra prints and outputs", metavar = "logical"),
make_option(c("--showPlots"),
    type = "logical", default = FALSE, help = "Show plots", metavar = "logical")
)

# parse script arguments
optParser = OptionParser(option_list=optionList)
opt = parse_args(optParser)

datasetPath <-  opt$dataset
csvSeparator <- opt$csvSeparator
imputationPackage <- opt$imputationPackage
imputationMethod <- opt$imputationMethod
processingCoreQty <- opt$processingCoreQty
normalizedImputation <- opt$normalizedImputation
chainQty <- opt$chainQty
untilConvergence <- opt$untilConvergence
rHatsConvergence <- opt$rHatsConvergence
maxIterations <- opt$maxIterations
clusterSeed <- opt$clusterSeed
storeAllImputations <- opt$storeAllImputations
isDetailed <- opt$isDetailed
showPlots <- opt$showPlots

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

if (normalizedImputation){
    print("Normalize data before imputation...")
    numericColumns <- scale(numericColumns)
    print("mean coefficients:")
    print(attr(numericColumns, "scaled:center"))
    print("variance coefficients:")
    print(attr(numericColumns, "scaled:scale"))
}

epoch <- 1
imputedData <- NULL
if (imputationPackage == 'mi'){
    library(mi) # multiple imputation method to complete missing values in datasets
    options(mc.cores = processingCoreQty) # set the number of cores used for imputation

    mdf <- missing_data.frame(numericColumns) # create missing data dataframe

    if (isDetailed){
        print("Inspect raw data for properties:")
        summary(mdf) # summarize mdf by providing statistics
        show(mdf) # show assumptions on the data types of the columns
    }

    if (showPlots){
        image(mdf) # print an image of missing datapoints
        hist(mdf) # show histogram of columns

        summary(mdf) # show properties of miData

        # histogram and visual representation of missing data
        library(VIM)
        aggr(mdf, col=c('navyblue','red'), numbers=TRUE, sortVars=TRUE, labels=names(data), cex.axis=.7, gap=3, ylab=c("Histogram of missing data", "Pattern"))

        marginplot(mdf[c(1,2)]) # special box plot to compare missingness of two variables
    }

    # TODO: max.minutes seems to be not setable via a variable
    mdf <- mi(mdf, n.chains = chainQty, n.iter = 0, max.minutes = 1000000) # initiate mutiple imputation
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

        # print rhat convergence
        print(paste0("Rhat to measure convergence of imputation (should be < ", rHatsConvergence, "):"))
        print(latestRHat)
        isNotConverged <- any(latestRHat > rHatsConvergence)
        if (isNotConverged){
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

    if (showPlots){
        plot(mdf) # plot the match of imputed and observed data (used to debug convergence)
    }

    if (storeAllImputations){
        imputedDatasets <- complete(mdf)
        for (i in 1:chainQty){
            imputedData[[i]] <- subset(imputedDatasets[[i]], select=colnames(numericColumns)) # stores all imputations
        }
    }else{
        imputedData <- subset(complete(mdf, m = 1), select=colnames(numericColumns)) # m=1 just takes the first imputation chain
    }
} else if (imputationPackage == 'mice'){
    library(mice)
    library(miceadds)
    
    set.seed(clusterSeed)
    if (processingCoreQty < 0){
        processingCoreQty <- parallel::detectCores() - 1
    }

    if (isDetailed){
        summary(numericColumns)  # get an overview of the data
        md.pattern(numericColumns) # check the missingness pattern
        mdf$predictorMatrix  # The predictor matrix is a square matrix that specifies the variables that are used to impute each incomplete variable
        # Reference for mids members: https://rdrr.io/cran/mice/man/mids-class.html
    }

    print(paste0("Performing imputation..."))
    then <- Sys.time()
    

    # parlmice produces m = n.core * m.imp.core number of chains
    print(paste0("Starting ", processingCoreQty, " cores, each imputing ", chainQty, " chains..."))
    if (Sys.info()[['sysname']] == "Windows"){
        mdf <- parlmice(numericColumns, method=imputationMethod, maxit = maxIterations,  n.core = processingCoreQty, n.imp.core = chainQty, cluster.seed = clusterSeed, print = TRUE)
    }
    else{
        mdf <- parlmice(numericColumns, method=imputationMethod, cl.type='FORK', maxit = maxIterations,  n.core = processingCoreQty, n.imp.core = chainQty, cluster.seed = clusterSeed, print = TRUE)
    }
    latestRHat <- miceadds::Rhat.mice(mdf)
    
    # calculate and print imputations per minute
    now <- Sys.time()
    diff <- as.numeric(difftime(now, then, units="secs"))
    cat("Imputation speed:")
    cat(maxIterations/diff*60)
    print("/min")

    # print rhat convergence
    print(paste0("Rhat to measure convergence of imputation (should be < ", rHatsConvergence, "):"))
    print(latestRHat)
    isNotConverged <- any(na.omit(latestRHat["Rhat.M.imp"]) > rHatsConvergence)
    if(isNotConverged){
        print("Imputation not converged. Continuing...")
    }
    else{
        print("Imputation converged.")
    }


    if (showPlots){
        plot(mdf)  # plot convergence of algorithm, mean and standard deviation
        densityplot(mdf) # compare densities of different data
        stripplot(mdf)  # inspect quality of imputations
    }

    if (storeAllImputations){
        chainQty <- processingCoreQty * chainQty # adjust total number of chains
        for (i in 1:chainQty){
            imputedData[[i]] <- complete(mdf, i) # stores all imputations
        }
    }else{
        imputedData <- complete(mdf, 1)
    }
}


if (normalizedImputation){
    print("Denormalize data after imputation...")
    if (storeAllImputations){
        for (i in 1:chainQty){
            imputedData[[i]] <-t(apply(imputedData[[i]], 1, function(r)r*attr(numericColumns,'scaled:scale') + attr(numericColumns, 'scaled:center')))
        }
    }else{
        imputedData <-t(apply(imputedData, 1, function(r)r*attr(numericColumns,'scaled:scale') + attr(numericColumns, 'scaled:center')))
    }
}

imputedDataFrame <- NULL
if (storeAllImputations){
    for (i in 1:chainQty){
        imputedDataFrame[[i]] <- cbind(nonNumericColumns, imputedData[[i]])  # merge non-numeric and imputed, numeric data together
    }
}else{
    imputedDataFrame <- cbind(nonNumericColumns, imputedData)  # merge non-numeric and imputed, numeric data together
}

# write imputed data to file with timestamp
cat("Writing imputed data to file...")
fileName <- sub(pattern = "(.*?)\\.[a-zA-Z]*$", replacement = "\\1", basename(datasetPath))

# prepare dataset store path
path <- 'data/interim/'
if(!grepl("[0-9]{14}", fileName)){  # try to find a timestamp with 4 digit year and each 2 digits for month, day, hour, minute, second
    # write imputed data to file with timestamp
    cat("Writing imputed data to file...")
    now <- Sys.time()
    path <- paste0(path, format(now, "%Y%m%d%H%M%S"), "_")
}

if (storeAllImputations){
    for (i in 1:chainQty){
        filePath <- paste0(path, fileName, "_impType_",imputationPackage,"_nIter_", maxIterations*epoch, "_chainQty_", chainQty, "_rHatsConvergence_", rHatsConvergence, "_normImputation_", normalizedImputation , "_", i , ".csv")
        print(filePath)
        write.csv(imputedDataFrame[[i]], file=filePath, row.names = FALSE)
    }
}else{
    path <- paste0(path, fileName, "_impType_",imputationPackage,"_nIter_", maxIterations*epoch, "_chainQty_", chainQty, "_rHatsConvergence_", rHatsConvergence, "_normImputation_", normalizedImputation , ".csv")
    print(path)
    write.csv(imputedDataFrame, file=path, row.names = FALSE)
}
cat("Done.")
