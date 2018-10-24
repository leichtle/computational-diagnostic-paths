import numpy as np
from numpy.linalg import eigvals, cholesky
from scipy.stats import norm
import pandas as pd
from sklearn.linear_model import LinearRegression


def perform_oda_probit(xo: pd.DataFrame, zo: pd.DataFrame, niter: int, burn_in: int, lam_spec: int=1):
    ROW_AXIS = 0  # row axis constant
    COL_AXIS = 1  # column axis constant

    xo: np.ndarray = xo.values                                                                              # xo <- as.matrix(xo)
    zo: np.ndarray = zo.values                                                                              # zo <- as.vector(zo)
    no = xo.shape[0]                                                                                        # no <- nrow(xo)
    p = xo.shape[1]                                                                                         # p <- ncol(xo)
    xomean = np.mean(xo, axis=ROW_AXIS)                                                                     # xomean <- apply(xo, 2, mean)
    sqrtvar = np.sqrt(np.var(xo, axis=ROW_AXIS)) * np.sqrt((no - 1) / no)                                   # sqrtvar <- sqrt(apply(xo, 2, var)) * sqrt((no - 1) / no)
    xo = np.apply_along_axis(lambda x: x/sqrtvar, COL_AXIS, xo)                                             # xo <- scale(xo, center = F, scale = sqrtvar)
    xo_temp_mean = np.mean(xo, axis=ROW_AXIS)                                                               # xo <- scale(xo, center = T, scale = F)
    xo = np.apply_along_axis(lambda x: x-xo_temp_mean, COL_AXIS, xo)
    xoxo = np.dot(np.transpose(xo), xo)                                                                     # xoxo <- t(xo) %*% xo
    na = p + 1                                                                                              # na <- (p + 1)
    xoin = np.hstack((np.ones((no, 1)), xo))                                                                # xoin <- cbind(1, xo)
    lamc = max(eigvals(np.dot(np.transpose(xoin), xoin)))                                                   # lamc <- max(eigen(t(xoin) %*% xoin)$values)
    xaxain = ((0.001 + lamc) * np.eye(p + 1)).round(10) - np.dot(np.transpose(xoin), xoin).round(10)        # xaxain <- round((0.001 + lamc) * diag(p + 1), 10) - round(t(xoin) %*% xoin, 10)
    xain = np.transpose(cholesky(xaxain))                                                                   # xain <- chol(xaxain)
    xa = xain[:, 1:]                                                                                        # xa <- xain[, - 1]
    xcin = np.vstack((xoin, xain))                                                                          # xcin <- rbind(xoin, xain)
    xc = xcin[:, 1:]                                                                                        # xc <- xcin[, - 1]
    xcxc = np.diag(np.diag(np.dot(np.transpose(xc), xc)))                                                   # xcxc <- diag(diag(t(xc) %*% xc))
    xcxcin = np.diag(np.diag(np.dot(np.transpose(xcin), xcin)))                                             # xcxcin <- diag(diag(t(xcin) %*% xcin))
    dj = np.diag(np.dot(np.transpose(xcin), xcin))                                                          # dj <- diag(t(xcin) %*% xcin)
    s = np.count_nonzero(zo == 1)                                                                           # s = sum(zo == 1)
    priorincprob = np.ones(p) * 0.5                                                                         # priorincprob <- rep(1 / 2, p)
    oddsmat = np.zeros((niter, p)) * np.nan                                                                 # oddsmat <- matrix(NA, niter, p)
    postincprob = np.zeros((niter, p)) * np.nan                                                             # postincprob <- matrix(NA, niter, p)
    betamat = np.zeros((niter, p)) * np.nan                                                                 # betamat <- matrix(NA, niter, p)
    alphavec = np.zeros(niter) * np.nan                                                                     # alphavec <- rep(NA, niter)

    # betaolso is the least sq estimate of alpha and beta
    # for the observed matrix xoin
    # betaolsc is the matrix of least sq estimates of
    # alpha and beta corresponding to xcin and yc from
    # different iterations

    betaolsc = np.zeros((niter, p + 1)) * np.nan                                                            # betaolsc <- matrix(NA, niter, (p + 1))
    gammamat = np.zeros((niter, p)) * np.nan                                                                # gammamat <- matrix(NA, niter, p)
    checkpd = sum((v for v in eigvals(xaxain) if v < 0))                                                    # checkpd <- sum(eigen(xaxain)$values < 0)
    lam = np.ones(p) * lam_spec                                                                             # lam <- rep(lam.spec, p)
    gamma = np.random.binomial(1, priorincprob, p)                                                          # gamma <- rbinom(p, 1, as.vector(priorincprob))
    betatemp = np.zeros(p) * np.nan                                                                         # betatemp <- rep(NA, p)
    yo = np.zeros(no)                                                                                       # yo <- rep(0, no)
    phi = 1                                                                                                 # phi <- 1

    if checkpd == 0:                                                                                        # if (checkpd == 0)
                                                                                                            # {
        for i in range(0, niter):                                                                           #     for (i in 1 : niter)
                                                                                                            #     {
            gammamat[i, ] = gamma                                                                           #         gammamat[i,] <- gamma
            if sum(gamma) >= 1:                                                                             #         if (sum(gamma) >= 1)
                                                                                                            #         {
                xogamma = xo[:, gamma == 1]                                                                 #             xogamma <- xo[, gamma == 1]
                xoxogamma = xoxo[gamma == 1, :][:, gamma == 1]                                              #             xoxogamma <- xoxo[gamma == 1, gamma == 1]
                lamgamma = lam[gamma == 1]                                                                  #             lamgamma <- lam[gamma == 1]
                gamma_lm = LinearRegression()                                                               #             gamma.lm <- lm(yo ~ xogamma)
                gamma_lm.fit(xogamma, yo)
                betaogamma = gamma_lm.coef_[0:]                                                             #             betaogamma <- gamma.lm$coefficients[- 1]
                                                                                                            #             betaogamma <- as.matrix(betaogamma)
                if sum(gamma) == 1:                                                                         #             if (sum(gamma) == 1) {
                    sigmatildeogamma = 1 / (xoxogamma + (1/lamgamma))                                       #                 sigmatildeogamma <- 1 / (xoxogamma + (1 / lamgamma))
                else:                                                                                       #             } else
                                                                                                            #             {
                   sigmatildeogamma = np.linalg.inv(xoxogamma + np.diag(1/lamgamma))                        #                 sigmatildeogamma <- solve(xoxogamma + diag(1 / lamgamma))
                                                                                                            #             }
                betatildegamma = np.dot(np.dot(sigmatildeogamma, xoxogamma), betaogamma)                    #             betatildeogamma <- sigmatildeogamma %*% xoxogamma %*% betaogamma
                xagamma = xa[:, gamma == 1]                                                                 #             xagamma <- xa[, gamma == 1]
                                                                                                            #             xagamma <- as.matrix(xagamma)
                muya = xain[:, 1] * np.mean(yo) + np.dot(xagamma, betatildegamma)                           #             muya <- xain[, 1] * mean(yo) + xagamma %*% betatildeogamma
                varya1 = (np.outer(xain[:, 0], xain[:, 0])) / no                                            #             varya1 <- (xain[, 1] %*% t(xain[, 1])) / no
                varya2 = np.dot(np.dot(xagamma, sigmatildeogamma), np.transpose(xagamma))                   #             varya2 <- xagamma %*% sigmatildeogamma %*% t(xagamma)
                varya3 = np.eye(na)                                                                         #             varya3 <- diag(na)

                varya = (varya1 + varya2 + varya3) / phi                                                    #             varya <- (varya1 + varya2 + varya3) / phi
                ya = np.random.multivariate_normal(muya, varya)                                             #             ya <- mvrnorm(1, muya, varya)
                                                                                                            #         }
            else:                                                                                           #         else {
                muya = xain[1, ] * np.mean(yo)                                                              #             muya <- xain[, 1] * mean(yo)
                varya1 = np.dot(xain[1, ], np.transpose(xain[1, ])) / no                                    #             varya1 <- (xain[, 1] %*% t(xain[, 1])) / no
                varya3 = np.eye(na)                                                                         #             varya3 <- diag(na)
                varya = (varya1 + varya3) / phi                                                             #             varya <- (varya1 + varya3) / phi
                ya = np.random.multivariate_normal(muya, varya)                                             #             ya <- mvrnorm(1, muya, varya)
                                                                                                            #         }
            yc = np.hstack((yo, ya))                                                                        #         yc <- c(yo, ya)
            fullc_lm = LinearRegression()                                                                   #         fullc.lm <- lm(yc ~ xcin - 1)
            fullc_lm.fit(xcin - 1, yc)
            betaolsc[i, ] = fullc_lm.coef_                                                                  #         betaolsc[i,] <- as.vector(fullc.lm$coefficients)
            # odds = np.zeros(p)                                                                            #         odds <- rep(0, p)
            odds1 = priorincprob/(1 - priorincprob)                                                         #         odds1 <- priorincprob / (1 - priorincprob)
            odds2 = np.sqrt(lam * dj[1:] + 1)                                                               #         odds2 <- (lam * dj[- 1] + 1) ^ (- 0.5)
            odds3 = np.power(betaolsc[i, 1:] * dj[1:], 2) / (dj[1:] + (1 / lam))                                     #         odds3 <- (as.vector(betaolsc[i, - 1]) * dj[- 1]) ^ 2 / (dj[- 1] + (1 / lam))
            logodds = np.log(odds1) + np.log(odds2) + np.log(odds3 * phi / 2)                               #         logodds <- log(odds1) + log(odds2) + (odds3 * phi / 2)
            logodds[logodds > 700] = 700                                                                    #         logodds[logodds > 700] <- 700
            odds = np.exp(logodds)                                                                          #         odds <- exp(logodds)
            oddsmat[i, ] = odds                                                                             #         oddsmat[i,] <- odds
            postincprob[i, ] = odds / (1 + odds)                                                            #         postincprob[i,] <- odds / (1 + odds)
            gamma = np.random.binomial(1, postincprob[i, ], p)                                              #         gamma <- rbinom(p, 1, as.vector(postincprob[i,]))

            if sum(gamma) >= 1:                                                                             #         if (sum(gamma) >= 1)
                                                                                                            #         {
                if sum(gamma) == 1:                                                                         #             if (sum(gamma) == 1)
                                                                                                            #             {
                    pbeta = (lam[gamma == 1] + xcxc[gamma == 1, gamma == 1]) * phi                          #                 Pbeta <- (lam[gamma == 1] + xcxc[gamma == 1, gamma == 1]) * phi
                    vbeta = 1 / pbeta                                                                       #                 Vbeta <- 1 / Pbeta
                else:                                                                                       #             } else {
                    pbeta = phi * (np.diag(lam[gamma == 1]) + xcxc[gamma == 1, :][:, gamma == 1])           #                 Pbeta <- phi * (diag(lam[gamma == 1]) + xcxc[gamma == 1, gamma == 1])
                    vbeta = np.linalg.inv(pbeta)                                                            #                 Vbeta <- solve(Pbeta)
                                                                                                            #             }
                ebeta = phi * np.dot(np.dot(vbeta, xcxc[gamma == 1, :][:, gamma == 1]), betaolsc[i, 1:][gamma == 1]) #             Ebeta <- phi * as.matrix(Vbeta) %*% xcxc[gamma == 1, gamma == 1] %*% as.matrix(betaolsc[i, - 1][gamma == 1])

                betatemp[gamma == 1] = np.random.multivariate_normal(ebeta, vbeta)                          #             betatemp[gamma == 1] <- mvrnorm(1, Ebeta, Vbeta)
                betatemp[gamma == 0] = 0                                                                    #             betatemp[gamma == 0] <- 0
            elif sum(gamma) == 0:                                                                           #         } else if (sum(gamma) == 0)  # end if (sum(gamma)==1) execution else
                betatemp[gamma == 0] = 0                                                                    #               betatemp[gamma == 0] <- 0

            betamat[i, ] = betatemp                                                                         #             betamat[i,] <- betatemp
            ealpha = betaolsc[i, 0]                                                                         #             Ealpha <- betaolsc[i, 1]
            palpha = phi * dj[0]                                                                            #             Palpha <- phi * dj[1]
            alpha = np.random.normal(ealpha, np.sqrt(1/palpha))                                             #             alpha <- rnorm(1, Ealpha, sqrt(1 / Palpha))
            alphavec[i] = alpha                                                                             #             alphavec[i] <- alpha

            muz = np.dot(xoin, np.hstack((alphavec[i], betamat[i, ])))                                      #             muz <- xoin %*% as.matrix(c(alphavec[i], betamat[i,]))
            cdf = np.random.uniform(0, 1, s) * norm.cdf(muz[zo == 1]) + norm.cdf(-muz[zo == 1])
            capped_cdf = [v if v < 1 else 0.99999999999 for v in cdf]                                       # prevent probabilities from being 1
            capped_cdf = [v if v > 0 else 0.00000000001 for v in capped_cdf]                                # prevent probabilities from being 0
            cdf2 = np.random.uniform(0, 1, no-s) * norm.cdf(-muz[zo == 0])
            capped_cdf2 = [v if v < 1 else 0.99999999999 for v in cdf2]                                     # prevent probabilities from being 1
            capped_cdf2 = [v if v > 0 else 0.00000000001 for v in capped_cdf2]                              # prevent probabilities from being 0
            yo[zo == 1] = muz[zo == 1] + norm.ppf(capped_cdf)                                               #             yo[zo == 1] <- muz[zo == 1] + qnorm(runif(s, 0, 1) * pnorm(muz[zo == 1]) + pnorm(- muz[zo == 1]))
            yo[zo == 0] = muz[zo == 0] + norm.ppf(capped_cdf2)                                              #             yo[zo == 0] <- muz[zo == 0] + qnorm(runif(no - s, 0, 1) * pnorm(- muz[zo == 0]))

            assert(np.isfinite(muz).all())
            assert(np.isfinite(capped_cdf).all())
            assert(np.isfinite(capped_cdf2).all())
            assert(np.isfinite(yo[zo == 0]).all())
            assert(np.isfinite(yo[zo == 1]).all())

            if i % 1000 == 0:                                                                               #             if (i %% 10000 == 0)
                print("iteration: ", i)                                                                     #                 print(paste("iter", i, sep = " "))
                                                                                                            #     }

        beta0_hat = np.mean(betaolsc[burn_in:, 1])                                                          #     beta0.hat <- mean(betaolsc[- c(1 : burnin), 1])
        d = round(lamc + 0.001, 10)                                                                         #     d <- round(lamc + 0.001, 10)
        beta_hat = np.mean(betaolsc[burn_in:, 1:] * postincprob[burn_in:, ], axis=ROW_AXIS) * (d / (d + lam_spec))                   #     beta.hat <- apply(betaolsc[- c(1 : burnin), - 1] * postincprob[- c(1 : burnin),], 2, mean) * (d / (d + lam.spec))
        beta_hat = beta_hat / sqrtvar                                                                       #     beta.hat <- beta.hat / sqrtvar
        beta0_hat = beta0_hat - sum(beta_hat * xomean)                                                      #     beta0.hat <- beta0.hat - sum(beta.hat * xomean)
        incprob_rb = np.mean(postincprob[burn_in:, ], axis=ROW_AXIS)                                        #     incprob.rb <- apply(postincprob[- c(1 : burnin),], 2, mean)
        return {
            "betama": [beta0_hat, beta_hat],
            "incprob_rb": incprob_rb,
            "incprob": postincprob,
            "gamma": gammamat,
            "odds": oddsmat
        }                                                                                               #     return(list(betabma = c(beta0.hat, beta.hat), incprob.rb = incprob.rb, incprob = postincprob, gamma = gammamat, odds = oddsmat))
                                                                                                            # }
    else:                                                                                                   # else
        raise Exception("xa is not psd")                                                                    #     return(c("xa is not psd"))