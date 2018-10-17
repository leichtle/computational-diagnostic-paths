

oda.bma <- function(x,y,niter,burnin,model="lm",prior="Students-t",lambda=1,alpha=1)
  {
    source("./lib/oda.normal.r")
    source("./lib/oda.studentst.r")
    source("./lib/oda.probit.r")
    # Error message
    if (model=="probit" & prior!="normal")
       stop ("ODA for Probit regression is available with normal priors only at this time \n Please re-run with prior=normal")
    if (model%in%c("lm","probit")==FALSE)
      stop ("Please re-run specifying the argument model=lm or model=probit")
    if (model=="lm" & prior%in%c("normal","Students-t")==FALSE)
      stop ("ODA for linear regression is available with normal or Students-t prior at this time \n Please re-run with prior=normal or prior=Students-t")
    # Run for appropriate arguments
    if (model=="lm" & prior=="normal")
      result <- oda.normal(xo=x,yo=y,niter=niter,lam.spec=lambda,burnin=burnin)
    else if (model=="lm" & prior=="Students-t")
       result <- oda.studentst(xo=x,yo=y,niter=niter,burnin=burnin,alpha=alpha)
    else if (model=="probit" & prior=="normal")
       result <- oda.probit(xo=x,zo=y,niter=niter,burnin=burnin,lam.spec=lambda)
    return(result)
  }
