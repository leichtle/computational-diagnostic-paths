import numpy as np
from numpy.linalg import solve, eigvals, cholesky
from scipy.stats import norm
import pandas as pd
from sklearn.linear_model import LinearRegression


def oda_probit(xo: pd.DataFrame, zo: pd.DataFrame, niter: int, burnin: int, lam_spec: int=1):
    xo: np.ndarray = xo.as_matrix()                                                                         # xo <- as.matrix(xo)
    zo: np.ndarray = zo.as_matrix()                                                                         # zo <- as.vector(zo)
    no = xo.size[0]                                                                                         # no <- nrow(xo)
    p = xo.size[1]                                                                                          # p <- ncol(xo)
    xomean = np.mean(xo, axis=0)                                                                            # xomean <- apply(xo, 2, mean)
    sqrtvar = np.sqrt(np.var(xo, axis=0) * np.sqrt(no - 1) / no)                                            # sqrtvar <- sqrt(apply(xo, 2, var)) * sqrt((no - 1) / no)
    xo = np.apply_along_axis(lambda x: x/sqrtvar, 0, xo)                                                    # xo <- scale(xo, center = F, scale = sqrtvar)
    xo_temp_mean = np.mean(xo, axis=0)                                                                      # xo <- scale(xo, center = T, scale = F)
    xo = np.apply_along_axis(lambda x: x-xo_temp_mean, 0, xo)
    xoxo = np.transpose(xo) * xo                                                                            # xoxo <- t(xo) %*% xo
    na = p + 1                                                                                              # na <- (p + 1)
    xoin = np.append(np.ones(no), xo, axis=0)                                                               # xoin <- cbind(1, xo)
    lamc = max(eigvals(np.transpose(xoin) * xoin))                                                          # lamc <- max(eigen(t(xoin) %*% xoin)$values)
    xaxain = round((0.001 + lamc) * np.diagonal(p + 1), 10) - round(np.transpose(xoin) * xoin, 10)          # xaxain <- round((0.001 + lamc) * diag(p + 1), 10) - round(t(xoin) %*% xoin, 10)
    xain = cholesky(xaxain)                                                                                 # xain <- chol(xaxain)
    xa = xain[-1, ]                                                                                         # xa <- xain[, - 1]
    xcin = np.append(xoin, xain, axis=1)                                                                    # xcin <- rbind(xoin, xain)
    xc = xcin[-1, ]                                                                                         # xc <- xcin[, - 1]
    xcxc = np.diagonal(np.diagonal(np.transpose(xc) * xc))                                                  # xcxc <- diag(diag(t(xc) %*% xc))
    # xcxcin = np.diagonal(np.diagonal(np.transpose(xcin) * xcin))                                            # xcxcin <- diag(diag(t(xcin) %*% xcin))
    dj = np.diagonal(np.transpose(xcin) * xcin)                                                             # dj <- diag(t(xcin) %*% xcin)
    s = np.count_nonzero(zo == 1)                                                                           # s = sum(zo == 1)
    priorincprob = np.ones(p) * 0.5                                                                         # priorincprob <- rep(1 / 2, p)
    oddsmat = np.empty((niter, p))                                                                          # oddsmat <- matrix(NA, niter, p)
    oddsmat[:] = np.nan
    postincprob = np.empty((niter, p))                                                                      # postincprob <- matrix(NA, niter, p)
    postincprob[:] = np.nan
    betamat = np.empty((niter, p))                                                                          # betamat <- matrix(NA, niter, p)
    betamat[:] = np.nan
    alphavec = np.empty((niter))                                                                            # alphavec <- rep(NA, niter)
    alphavec[:] = np.nan

    # betaolso is the least sq estimate of alpha and beta
    # for the observed matrix xoin
    # betaolsc is the matrix of least sq estimates of
    # alpha and beta corresponding to xcin and yc from
    # different iterations

    betaolsc = np.empty((niter, p))                                                                         # betaolsc <- matrix(NA, niter, (p + 1))
    betaolsc[:] = np.nan
    gammamat = np.empty((niter, p))                                                                         # gammamat <- matrix(NA, niter, p)
    gammamat[:] = np.nan
    checkpd = sum((v for v in eigvals(xaxain) if v < 0))                                                    # checkpd <- sum(eigen(xaxain)$values < 0)
    lam = np.ones(p) * lam_spec                                                                             # lam <- rep(lam.spec, p)
    gamma = np.random.binomial(p, 1, priorincprob)                                                          # gamma <- rbinom(p, 1, as.vector(priorincprob))
    betatemp = np.empty(p)                                                                                  # betatemp <- rep(NA, p)
    betatemp[:] = np.nan
    yo = np.zeros(no)                                                                                       # yo <- rep(0, no)
    phi = 1                                                                                                 # phi <- 1

    if checkpd == 0:                                                                                        # if (checkpd == 0)
                                                                                                            # {
        for i in range(1, niter):                                                                           #     for (i in 1 : niter)
                                                                                                            #     {
            gammamat[i, ] = gamma                                                                           #         gammamat[i,] <- gamma
            if sum(gamma) >= 1:                                                                             #         if (sum(gamma) >= 1)
                                                                                                            #         {
                xogamma = xo[gamma == 1, ]                                                                  #             xogamma <- xo[, gamma == 1]
                xoxogamma = xoxo[gamma == 1, gamma == 1]                                                    #             xoxogamma <- xoxo[gamma == 1, gamma == 1]
                lamgamma = lam[gamma == 1]                                                                  #             lamgamma <- lam[gamma == 1]
                gamma_lm = LinearRegression()                                                               #             gamma.lm <- lm(yo ~ xogamma)
                gamma_lm.fit(xogamma, yo)
                betaogamma = [gamma_lm.coef_[-1]]                                                           #             betaogamma <- gamma.lm$coefficients[- 1]
                                                                                                            #             betaogamma <- as.matrix(betaogamma)
                if sum(gamma) == 1:                                                                         #             if (sum(gamma) == 1) {
                    sigmatildeogamma = -1 / (xoxogamma + (1/lamgamma))                                      #                 sigmatildeogamma <- 1 / (xoxogamma + (1 / lamgamma))
                else:                                                                                       #             } else
                                                                                                            #             {
                    sigmatildeogamma = solve(xoxogamma + np.diagonal(1/lamgamma))                           #                 sigmatildeogamma <- solve(xoxogamma + diag(1 / lamgamma))
                                                                                                            #             }
                betatildegamma = sigmatildeogamma * xoxogamma * betaogamma                                  #             betatildeogamma <- sigmatildeogamma %*% xoxogamma %*% betaogamma
                xagamma = xa[gamma == 1, ]                                                                  #             xagamma <- xa[, gamma == 1]
                                                                                                            #             xagamma <- as.matrix(xagamma)
                muya = xain[1, ] * np.mean(yo) + xagamma * betatildegamma                                   #             muya <- xain[, 1] * mean(yo) + xagamma %*% betatildeogamma
                varya1 = (xain[1, ] * np.transpose(xain[1, ])) / no                                         #             varya1 <- (xain[, 1] %*% t(xain[, 1])) / no
                varya2 = xagamma * sigmatildeogamma * np.transpose(xagamma)                                 #             varya2 <- xagamma %*% sigmatildeogamma %*% t(xagamma)
                varya3 = np.diag(na)                                                                        #             varya3 <- diag(na)

                varya = (varya1 + varya2 + varya3) / phi                                                    #             varya <- (varya1 + varya2 + varya3) / phi
                # ya = np.random.multivariate_normal(muya, varya)                                             #             ya <- mvrnorm(1, muya, varya)
                                                                                                            #         }
            else:                                                                                           #         else {
                muya = xain[1, ] * np.mean(yo)                                                              #             muya <- xain[, 1] * mean(yo)
                varya1 = xain[1, ] * np.transpose(xain[1, ]) / no                                           #             varya1 <- (xain[, 1] %*% t(xain[, 1])) / no
                varya3 = np.diagonal(na)                                                                    #             varya3 <- diag(na)
                varya = (varya1 + varya3) / phi                                                             #             varya <- (varya1 + varya3) / phi
                ya = np.random.multivariate_normal(muya, varya)                                             #             ya <- mvrnorm(1, muya, varya)
                                                                                                            #         }
                yc = [yo, ya]                                                                               #         yc <- c(yo, ya)
                fullc_lm = LinearRegression()                                                               #         fullc.lm <- lm(yc ~ xcin - 1)
                fullc_lm.fit(xcin - 1, yc)
                betaolsc[i, ] = [fullc_lm.coef_]                                                            #         betaolsc[i,] <- as.vector(fullc.lm$coefficients)
                # odds = np.zeros(p)                                                                          #         odds <- rep(0, p)
                odds1 = priorincprob/(1 - priorincprob)                                                     #         odds1 <- priorincprob / (1 - priorincprob)
                odds2 = np.sqrt(lam * dj[-1] + 1)                                                           #         odds2 <- (lam * dj[- 1] + 1) ^ (- 0.5)
                odds3 = (betaolsc[i, -1] * dj[-1] ^ 2 / dj[-1] + (1 / lam))                                 #         odds3 <- (as.vector(betaolsc[i, - 1]) * dj[- 1]) ^ 2 / (dj[- 1] + (1 / lam))
                logodds = np.log(odds1) + np.log(odds2) + np.log(odds3 * phi / 2)                           #         logodds <- log(odds1) + log(odds2) + (odds3 * phi / 2)
                logodds[logodds > 700] = 700                                                                #         logodds[logodds > 700] <- 700
                odds = np.exp(logodds)                                                                      #         odds <- exp(logodds)
                oddsmat[i, ] = odds                                                                         #         oddsmat[i,] <- odds
                postincprob[i, ] = odds / (1 + odds)                                                        #         postincprob[i,] <- odds / (1 + odds)
                gamma = np.random.normal(p, 1, postincprob[i, ])                                            #         gamma <- rbinom(p, 1, as.vector(postincprob[i,]))

                if sum(gamma) >= 1:                                                                         #         if (sum(gamma) >= 1)
                                                                                                            #         {
                    if sum(gamma) == 1:                                                                     #             if (sum(gamma) == 1)
                                                                                                            #             {
                        pbeta = (lam[gamma == 1] + xcxc[gamma == 1, gamma == 1]) * phi                      #                 Pbeta <- (lam[gamma == 1] + xcxc[gamma == 1, gamma == 1]) * phi
                        # vbeta = 1 / pbeta                                                                   #                 Vbeta <- 1 / Pbeta
                    else:                                                                                   #             } else {
                        pbeta = phi * (np.diagonal(lam[gamma == 1]) + xcxc[gamma == 1, gamma == 1])         #                 Pbeta <- phi * (diag(lam[gamma == 1]) + xcxc[gamma == 1, gamma == 1])
                        vbeta = solve(pbeta)                                                                #                 Vbeta <- solve(Pbeta)
                                                                                                            #             }
                        ebeta = phi * vbeta * xcxc[gamma == 1, gamma == 1] * betaolsc[i, -1][gamma == 1]    #             Ebeta <- phi * as.matrix(Vbeta) %*% xcxc[gamma == 1, gamma == 1] %*% as.matrix(betaolsc[i, - 1][gamma == 1])

                        betatemp[gamma == 1] = np.random.multivariate_normal(ebeta, vbeta)                  #             betatemp[gamma == 1] <- mvrnorm(1, Ebeta, Vbeta)
                        betatemp[gamma == 0] = 0                                                            #             betatemp[gamma == 0] <- 0
                elif sum(gamma) == 0:                                                                       #         } else if (sum(gamma) == 0)  # end if (sum(gamma)==1) execution else
                    betatemp[gamma == 0] = 0                                                                #               betatemp[gamma == 0] <- 0

                betamat[i, ] = betatemp                                                                     #             betamat[i,] <- betatemp
                ealpha = betaolsc[i, 1]                                                                     #             Ealpha <- betaolsc[i, 1]
                palpha = phi * dj[1]                                                                        #             Palpha <- phi * dj[1]
                alpha = np.random.normal(1, ealpha, np.sqrt(1/palpha))                                      #             alpha <- rnorm(1, Ealpha, sqrt(1 / Palpha))
                alphavec[i] = alpha                                                                         #             alphavec[i] <- alpha

                muz = xoin * [alphavec[i], betamat[i, ]]                                                    #             muz <- xoin %*% as.matrix(c(alphavec[i], betamat[i,]))
                yo[zo == 1] = muz[zo == 1] + norm.ppf(np.random.uniform(0, 1, s)
                                                      * norm.cdf(muz[zo == 1]
                                                      + norm.cdf(-muz[zo == 1])))                           #             yo[zo == 1] <- muz[zo == 1] + qnorm(runif(s, 0, 1) * pnorm(muz[zo == 1]) + pnorm(- muz[zo == 1]))
                yo[zo == 0] = muz[zo == 0] + norm.ppf(np.random.uniform(0, 1, no-s)
                                                      * norm.cdf(muz[zo == 1]
                                                      + norm.cdf(-muz[zo == 0])))                           #             yo[zo == 0] <- muz[zo == 0] + qnorm(runif(no - s, 0, 1) * pnorm(- muz[zo == 0]))
                if i % 1000 == 0:                                                                           #             if (i %% 10000 == 0)
                    print("iteration: ", i)                                                                 #                 print(paste("iter", i, sep = " "))
                                                                                                            #     }
                beta0_hat = np.mean(betaolsc[-1:-burnin, 1])                                                #     beta0.hat <- mean(betaolsc[- c(1 : burnin), 1])
                d = round(lamc + 0.001, 10)                                                                 #     d <- round(lamc + 0.001, 10)
                beta_hat = np.mean(betaolsc[-1:-burnin, -1], axis=0) * (d/(d + lam_spec))                   #     beta.hat <- apply(betaolsc[- c(1 : burnin), - 1] * postincprob[- c(1 : burnin),], 2, mean) * (d / (d + lam.spec))
                beta_hat = beta_hat / sqrtvar                                                               #     beta.hat <- beta.hat / sqrtvar
                beta0_hat = beta0_hat - sum(beta_hat * xomean)                                              #     beta0.hat <- beta0.hat - sum(beta.hat * xomean)
                incprob_rb = np.mean(postincprob[-1: -burnin, ], axis=0)                                    #     incprob.rb <- apply(postincprob[- c(1 : burnin),], 2, mean)
                return {
                    "betama": [beta0_hat, beta_hat],
                    "incprob_rb": incprob_rb,
                    "incprob": postincprob,
                    "gamma": gammamat,
                    "odds": oddsmat
                }                                                                                           #     return(list(betabma = c(beta0.hat, beta.hat), incprob.rb = incprob.rb, incprob = postincprob, gamma = gammamat, odds = oddsmat))
                                                                                                            # }
    else:                                                                                                   # else
        raise Exception("xa is not psd")                                                                    #     return(c("xa is not psd"))