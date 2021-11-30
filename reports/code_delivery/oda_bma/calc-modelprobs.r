library(parallel)

# reimplementation of modelprobs.rb in pure R
# Arguments:
# n.unique:     Number of unique models for which RB estimates of posterior model probabilities need to be calculated
# niter:        Number of MCMC iterations for which the posterior inclusion probabilities
#               will be used in the calculation
# p:            Number of predictors in the full model
# gammaunique:  An n.unique by p matrix of unique models (denoted by gamma) for which posterior model probabilities
#               are to be estimated.
# probmat.oda:  An niter by p matrix of posterior inclusion probabilities available from the output of oda.bma,
#               based on which the Rao-Blackwellized estimates of model probabilities will be calculated
modelprobs.rb <-function(n.unique, niter, p, gammaunique, probmat.oda) {
    n.unique <- as.integer(n.unique)
    niter <- as.integer(niter)
    p <- as.integer(p)
    gammaunique <- as.integer(gammaunique)
    probmat.oda <- as.double(probmat.oda)
    modelprobs <- double(n.unique)

    cores <- detectCores() # get all available cores
    print(paste0("Available cores:", cores))
    print(paste0("Unique models ", n.unique -1, "/Iterations ", niter - 1, "\n"))

    modelprobs <- mcmapply(function(i, n.unique, niter, p, gammaunique, probmat.oda) {
        print(paste0("\nUnique model " , i, " of " , n.unique - 1, "\n"))
        tempsum <- 0
        print("\nIteration: ")
        for (j in 0:(niter - 1)) {
            cat(paste0(" ", j))
            tempprod <- 1.0
            for (k in 0:(p - 1)) {
                if (gammaunique[1 + i + k * n.unique] == 1) {
                    tempprod <- tempprod * probmat.oda[1 + j + k * niter]
                }
                else{
                    tempprod <- tempprod * (1.0 - probmat.oda[1 + j + k * niter])
                }
            }
            tempsum <- tempsum + tempprod
        }
        return(tempsum / niter)
    }, i=0:(n.unique - 1), MoreArgs=list(n.unique=n.unique, niter=niter, p=p, gammaunique=gammaunique, probmat.oda=probmat.oda), mc.cores=cores-1)

    return(modelprobs)
}


# Usage:
# test run for probit regression using Pima Indians diabetes data
#burnin.sim <- 500;
#Gtot <- 1000;
#library(MASS)
#data(Pima.tr)
#data(Pima.te)
#pima <- rbind(Pima.tr,Pima.te)
#dim(pima) # 532 8
#names(pima)
#pimay <- pima$type
#pimay <- as.numeric(pimay);
#pimay[pimay==1] <- 0; pimay[pimay==2] <- 1;
#pimax <- pima[,1:7]
#source("oda.bma.r")
#
#oda.pima <- oda.bma(x = pimax, y = pimay, niter = Gtot, burnin = burnin.sim, lambda = 1, model = "probit", prior = "normal");
#
# matrix of unique models from ODA
#gamma.u <- unique(oda.pima$gamma[-c(1:burnin.sim),])
#
# vector of RB estimates of model probabilities corresponding to models in gamma.u
#probest <- modelprobs.rb(n.unique=nrow(gamma.u),
#						niter=nrow(oda.pima$incprob[-c(1:burnin.sim),]),
#						p = ncol(gamma.u),
#						gammaunique=t(gamma.u),
#						probmat.oda = t(oda.pima$incprob[-c(1:burnin.sim),]))
#
# Estimated posterior probability of unsampled models
#1-sum(probest)
