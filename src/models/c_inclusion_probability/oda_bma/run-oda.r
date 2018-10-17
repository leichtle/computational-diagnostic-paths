
##################### DOCUMENTATION FOR oda.bma() #######################################################################################
# DESCRIPTION
# -------------------
# oda.bma() is an R function for implementing the ODA algorithm for Bayesian
# variable selection and Bayesian model averaging in linear and probit regression. A description of the
# methods can be found in the paper: "Rao-Blackwellization for Bayesian Variable Selection and Model
# Averaging in Linear and Binary Regression: A Novel Data Augmentation Approach"
#
# USAGE
# -------
# oda.bma function(x,y,niter,burnin,model="lm",prior="Students-t",lambda=1,alpha=1)
#
# ARGUMENTS
# ---------
# x: 		design matrix (not standardized) without the column corresponding to the intercept
# y: 		vector of response variables
# niter: 	Number of MCMC iterations
# burnin: 	Burn-in used for calculating Rao-Blackwellized estimates from MCMC output
# model:  	Use model="lm" for linear regression and model="probit" for binary regression with probit link
# prior: 	prior="normal" or prior="Students-t" can be used for linear regression
#        	prior="normal" is the only option for probit regression available at this time
# lambda: 	An optional scale parameter used in the normal prior for regression coefficients, the recommended
#         	default value is 1 as the design matrix is standardized within the code
# alpha:  	An optional degrees of freedom parameter used in the Student's-t prior for regression coefficients,
#         	the default value is 1, leading to a Cauchy prior on regression coefficients
#
# VALUE
# -------
# betabma:    Rao-Blackwellized estimate of the vector of regression coefficients using Bayesian model averaging (BMA)
# incprob.rb: Rao-Blackwellized estimate of the vector of posterior marginal inclusion probabilities (Prob(beta_j !=0 |Y) for each j)
# incprob:    Matrix of posterior marginal inclusion probabilities for all MCMC iterations
# gamma:      Matrix of sampled models for all MCMC iterations
# odds:       Matrix of posterior-odds for all MCMC iterations
# phi:        Matrix (with one column) of precision parameter (reciprocal of error variance) for all MCMC iterations
#
# NOTE
# -----
# To calculate Rao-Blackwellized estimates of individual model probabilities, use the function modelprobs.rb()
######################  DOCUMENTATION FOR oda.bma()  #############################################################################################


source("oda.bma.r")


# test run for linear regression using nott-kohn simulated data
n = 50
sigma = 2.5
betatrue = c(4,2,0,0,0,-1,0,1.5, 0,0,0,1,0,.5,0,0)

set.seed(100)
Z = matrix(rnorm(n*10, 0, 1), ncol=10, nrow=n)
X = cbind(Z, (Z[,1:5] %*% c(.3, .5, .7, .9, 1.1) %*% t(rep(1,5)) + matrix(rnorm(n*5, 0, 1), ncol=5, nrow=n)))

Y = 4 + 2*X[,1] - X[,5] + 1.5*X[,7] + X[,11] + 0.5*X[,13] + rnorm(n, 0, sigma)

simdata = data.frame(X,Y)


burnin.sim <- 500;
Gtot <- 1000;

oda.c <- oda.bma(x = simdata[,-16], y = simdata$Y, niter = Gtot, burnin = burnin.sim, model = "lm") 									# Cauchy prior for lm (default)
oda.n <- oda.bma(x = simdata[,-16], y = simdata$Y, niter = Gtot, burnin = burnin.sim, model = "lm", prior = "normal") 					# Normal prior for lm 
oda.t <- oda.bma(x = simdata[,-16], y = simdata$Y, niter = Gtot, burnin = burnin.sim, model = "lm", prior = "Students-t", alpha = 4) 	# t_4 prior for lm

names(oda.c)
names(oda.n)

oda.c$incprob.rb
oda.n$incprob.rb
oda.t$incprob.rb

oda.c$betabma
oda.n$betabma
oda.t$betabma


# test run for probit regression using Pima Indians diabetes data
burnin.sim <- 500;
Gtot <- 1000;
library(MASS)
data(Pima.tr)
data(Pima.te)
pima <- rbind(Pima.tr,Pima.te)
dim(pima) # 532 8
names(pima)
pimay <- pima$type
pimay <- as.numeric(pimay);
pimay[pimay==1] <- 0; pimay[pimay==2] <- 1;
pimax <- pima[,1:7]

oda.pima <- oda.bma(x=pimax,y=pimay,niter=Gtot,burnin=burnin.sim,lambda=1,model="probit",prior="normal");

names(oda.pima)
oda.pima$incprob.rb
oda.pima$betabma
