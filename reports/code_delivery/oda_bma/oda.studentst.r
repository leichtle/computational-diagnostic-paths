##################################################################
oda.studentst <- function(xo,yo,niter,burnin,alpha=1)
  {
    library(MASS);
    xo <- as.matrix(xo); yo <- as.vector(yo);
    no <- nrow(xo);  p <- ncol(xo);
    xomean <- apply(xo,2,mean);
    sqrtvar <- sqrt(apply(xo,2,var))*sqrt((no-1)/no);
    xo <- scale(xo,center=F,scale=sqrtvar);
    xo <-  scale(xo,center=T,scale=F);
    xoxo <- t(xo)%*%xo; 
    na <- (p+1);
    xoin <- cbind(1,xo);                      
    lamc <- max(eigen(t(xoin)%*%xoin)$values);
    xaxain <- round((0.001+lamc)*diag(p+1),10)-round(t(xoin)%*%xoin,10);
    xain <- chol(xaxain);
    xa <- xain[,-1];
    xcin <- rbind(xoin,xain);
    xc <- xcin[,-1];
    xcxc <- t(xc)%*%xc;
    xcxcin <- diag(diag(t(xcin)%*%xcin));dj <- diag(t(xcin)%*%xcin); dj.woint <- dj[-1];
    priorincprob <- rep(1/2,p);
    postincprob <- matrix(NA,niter,p);
    oddsmat <- matrix(NA,niter,p);
    # betaolso is the least sq estimate of alpha and beta
    # for the observed matrix xoin
    # betaolsc is the matrix of least sq estimates of
    # alpha and beta corresponding to xcin and yc from
    # different gibbs iterations
  
    betaolsc <- matrix(NA,niter,(p+1));
    gammamat <- matrix(NA,niter,p);
    phimat <-  matrix(NA,niter,1);
    lammat <- matrix(NA,niter,p);
    checkpd <- sum(eigen(xaxain)$values<0);
    lamtemp <- rep(1,p);
    gamma <- rbinom(p,1,priorincprob);
    betatemp <- rep(0,p);
    if(checkpd==0)
      {
        for(i in 1:niter)
          {
            gammamat[i,] <- gamma;
            lammat[i,] <- lamtemp;
            if(sum(gamma)>=1)
              {
        xogamma <- xo[,gamma==1];
        xoxogamma <- xoxo[gamma==1,gamma==1];
        lamgamma <- lammat[i,gamma==1];
        gamma.lm <- lm(yo~xogamma);
        betaogamma <- gamma.lm$coefficients[-1];
        betaogamma <- as.matrix(betaogamma);
        rssgamma <-  sum((gamma.lm$res)^2);
        if(sum(gamma)==1) { sigmatildeogamma <- 1/(xoxogamma+lamgamma)} else
        {sigmatildeogamma <- solve(xoxogamma+diag(lamgamma))};
        
        aotilde <- no-1;
        botilde <-  rssgamma + t(betaogamma)%*%(xoxogamma-xoxogamma%*%sigmatildeogamma%*%xoxogamma)%*%betaogamma;
        phi <- rgamma(1,shape=aotilde/2,rate=botilde/2);
       
        betatildeogamma <- sigmatildeogamma %*% xoxogamma%*% betaogamma;
        xagamma <- xa[,gamma==1];
        xagamma <- as.matrix(xagamma);
        muya <- xain[,1]*mean(yo)+xagamma%*%betatildeogamma;
        varya1 <-(xain[,1]%*%t(xain[,1]))/no;
        varya2 <- xagamma%*% sigmatildeogamma%*%t(xagamma);
        varya3 <- diag(na);
      
        varya <- (varya1 + varya2 + varya3)/phi;
        ya <- mvrnorm(1,muya,varya);
      }
           else {
         aotilde <- no-1;
         botilde <- sum((yo-mean(yo))^2);
         phi <- rgamma(1,shape=aotilde/2,rate=botilde/2);
         muya <- xain[,1]*mean(yo);
         varya1 <-(xain[,1]%*%t(xain[,1]))/no;
         varya3 <- diag(na);
         varya <- (varya1 + varya3)/phi;
         ya <- mvrnorm(1,muya,varya);
        
      }
        yc <- c(yo,ya);
        fullc.lm <- lm(yc~xcin-1);
        betaolsc[i,] <- as.vector(fullc.lm$coefficients);
       
        odds1 <- priorincprob/(1-priorincprob);
        odds2 <- ((dj[-1]/lammat[i,])+1)^(-0.5);
        odds3 <- (as.vector(betaolsc[i,-1])*dj[-1])^2/(dj[-1]+lammat[i,]);
    
        logodds <- log(odds1)+log(odds2)+ (odds3*phi/2);    
        logodds[logodds>700] <- 700;
        odds <- exp(logodds);
        oddsmat[i,] <- odds;    
        postincprob[i,] <- odds/(1+odds);
        phimat[i,1] <- phi;
        gamma <- rbinom(p,1,as.vector(postincprob[i,]));
       if (sum(gamma)>=1)
           {
                if (sum(gamma)==1)
      {Pbeta <- (lamtemp[gamma==1]+xcxc[gamma==1,gamma==1])*phi;Vbeta <- 1/Pbeta} else
    {Pbeta <- phi*(diag(lamtemp[gamma==1])+xcxc[gamma==1,gamma==1]); Vbeta <- solve(Pbeta);}
    Ebeta <- phi*as.matrix(Vbeta)%*%xcxc[gamma==1,gamma==1]%*%as.matrix(betaolsc[i,-1][gamma==1]);
   
    betatemp[gamma==1] <- mvrnorm(1,Ebeta,Vbeta);
    betatemp[gamma==0] <- 0;
    lamtemp[gamma==1] <- rgamma(1,shape=(alpha+1)/2,rate=(alpha+phi*(betatemp[gamma==1])^2)/2);
    lamtemp[gamma==0] <- rgamma(1,shape=alpha/2,rate=alpha/2);
      } else if (sum(gamma)==0) # end if (sum(gamma)==1) execution else
        {
     betatemp[gamma==0] <- 0;
     lamtemp[gamma==0] <- rgamma(1,shape=alpha/2,rate=alpha/2);
         }
              if (i%%10000==0) print(paste("iter",i,sep=" "));
                }
  beta0.hat <- mean(betaolsc[-c(1:burnin),1]);
  d <- round(lamc+0.001,10);
  beta.hat <- (apply(betaolsc[-c(1:burnin),-1]*postincprob[-c(1:burnin),]*
                     (d/(d+lammat[-c(1:burnin),])),2,mean))
  beta.hat <- beta.hat/sqrtvar;
  beta0.hat <- beta0.hat-sum(beta.hat*xomean)
  incprob.rb <- apply(postincprob[-c(1:burnin),],2,mean);    
  return(list(betabma=c(beta0.hat,beta.hat),incprob.rb=incprob.rb,incprob=postincprob,gamma=gammamat,odds=oddsmat,phi=phimat));
      }
    else
      return(c("xa is not psd"));
  }


