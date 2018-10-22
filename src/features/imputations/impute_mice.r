################################
# Description: Performs a chained imputation (mice: Multivariate Imputation by Chained Equations) to impute missing data
# Reference: https://www.jstatsoft.org/article/view/v045i03/v45i03.pdf
# https://cran.r-project.org/web/packages/mice/mice.pdf
# https://datascienceplus.com/imputing-missing-data-with-r-mice-package/
# http://www.gerkovink.com/miceVignettes/Convergence_pooling/Convergence_and_pooling.html
# for parallel computation, checkout library(micemd)/mice.par

library(mice)

maxIterations <- 200 # maximum iterations of imputations per chain before imputation terminates
isDetailed <- FALSE

# load data from csv
cat("Loading data from csv...")
miData<-read.csv("../../data/raw_myocardial_ischemia.csv",sep=",",header=TRUE)
cat("Done.\n")

if (isDetailed){
  print("Inspect raw data for properties:")
  md.pattern(miData) # simple summary of missing data
  
  summary(miData) # show properties of miData
  
  # histogram and visual representation of missing data
  library(VIM)
  aggr_plot <- aggr(miData, col=c('navyblue','red'), numbers=TRUE, sortVars=TRUE, labels=names(data), cex.axis=.7, gap=3, ylab=c("Histogram of missing data","Pattern"))
  
  marginplot(miData[c(1,2)]) # special box plot to compare missingness of two variables

}

# methods(mice) returns all imputation methods
tempData <- mice(miData, m=5, maxit=maxIterations, meth='pmm', seed=500)
summary(tempData)



if (isDetailed){
  tempData$meth # show method of imputation
  plot(tempData) # show convergence of imputation
  densityplot(tempData) # compare densities of different data
  stripplot(tempData, chl, pch = 19, xlab = "Imputation number")  # inspect quality of imputations
}

completedData <- complete(tempData,1)