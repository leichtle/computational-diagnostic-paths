oda.probit <- function(xo, zo, niter, burnin, lam.spec=1, coeffShrink=0, ridgeLassoBlend=0)
{
    library(MASS)
    library(glmnet)
    xo <- as.matrix(xo)
    zo <- as.vector(zo)
    no <- nrow(xo)
    p <- ncol(xo)
    xomean <- apply(xo, 2, mean)
    sqrtvar <- sqrt(apply(xo, 2, var)) * sqrt((no - 1) / no)
    xo <- scale(xo, center = F, scale = sqrtvar)
    xo <- scale(xo, center = T, scale = F)
    xoxo <- t(xo) %*% xo
    na <- (p + 1)
    xoin <- cbind(1, xo)
    lamc <- max(eigen(t(xoin) %*% xoin)$values)
    xaxain <- round((0.001 + lamc) * diag(p + 1), 10) - round(t(xoin) %*% xoin, 10)
    xain <- chol(xaxain)
    xa <- xain[, - 1]
    xcin <- rbind(xoin, xain)
    xc <- xcin[, - 1]
    xcxc <- diag(diag(t(xc) %*% xc))
    xcxcin <- diag(diag(t(xcin) %*% xcin))
    dj <- diag(t(xcin) %*% xcin)
    s = sum(zo == 1)
    priorincprob <- rep(1 / 2, p)
    oddsmat <- matrix(NA, niter, p)
    postincprob <- matrix(NA, niter, p)
    betamat <- matrix(NA, niter, p)
    alphavec <- rep(NA, niter)

    # betaolso is the least sq estimate of alpha and beta
    # for the observed matrix xoin
    # betaolsc is the matrix of least sq estimates of
    # alpha and beta corresponding to xcin and yc from
    # different iterations

    betaolsc <- matrix(NA, niter, (p + 1))
    gammamat <- matrix(NA, niter, p)
    checkpd <- sum(eigen(xaxain)$values < 0)
    lam <- rep(lam.spec, p)
    gamma <- rbinom(p, 1, as.vector(priorincprob))
    betatemp <- rep(NA, p)
    yo <- rep(0, no)
    phi <- 1
    if (checkpd == 0)
    {
        for (i in 1 : niter)
        {
            gammamat[i,] <- gamma
            if (sum(gamma) >= 1)
            {
                xogamma <- xo[, gamma == 1]
                xoxogamma <- xoxo[gamma == 1, gamma == 1]
                lamgamma <- lam[gamma == 1]
				if (coeffShrink == 0 || sum(gamma) <= 1) {  # if no coefficient shrinking is applied, we keep the original linear model
                    # or if lasso is involved and only one feature (algo limitation: https://stackoverflow.com/questions/29231123/why-cant-pass-only-1-coulmn-to-glmnet-when-it-is-possible-in-glm-function-in-r)
					gamma.lm <- lm(yo ~ xogamma)
					betaogamma <- gamma.lm$coefficients[-1]
				}
				else {  # if coefficient shrinking is applied, we use a ridge regression instead
                    if (ridgeLassoBlend == 0){
					    gamma.lm <- lm.ridge(yo ~ xogamma, lambda=coeffShrink)
					    betaogamma <- coef(gamma.lm)[-1]
                    }
                    else{
                        glmmod <- glmnet(xogamma, y=yo, alpha=ridgeLassoBlend, lambda=coeffShrink, standardize=False)
                        betaogamma <-coef(glmmod)[-1]
                    }
				}

                betaogamma <- as.matrix(betaogamma)
                if (sum(gamma) == 1) {
                    sigmatildeogamma <- 1 / (xoxogamma + (1 / lamgamma))
                } else {
                    sigmatildeogamma <- solve(xoxogamma + diag(1 / lamgamma))
                }
                betatildeogamma <- sigmatildeogamma %*% xoxogamma %*% betaogamma
                xagamma <- xa[, gamma == 1]
                xagamma <- as.matrix(xagamma)
                muya <- xain[, 1] * mean(yo) + xagamma %*% betatildeogamma
                varya1 <- (xain[, 1] %*% t(xain[, 1])) / no
                varya2 <- xagamma %*% sigmatildeogamma %*% t(xagamma)
                varya3 <- diag(na)

                varya <- (varya1 + varya2 + varya3) / phi
                ya <- mvrnorm(1, muya, varya)
            }
            else {
                muya <- xain[, 1] * mean(yo)
                varya1 <- (xain[, 1] %*% t(xain[, 1])) / no
                varya3 <- diag(na)
                varya <- (varya1 + varya3) / phi
                ya <- mvrnorm(1, muya, varya)
            }
            yc <- c(yo, ya)

			if (coeffShrink == 0 || sum(gamma) <= 1) {  # if no coefficient shrinking is applied, we keep the original linear model
                # or if ridge/lasso is involved and only one feature (algo limitation: https://stackoverflow.com/questions/29231123/why-cant-pass-only-1-coulmn-to-glmnet-when-it-is-possible-in-glm-function-in-r)
				fullc.lm <- lm(yc ~ xcin - 1)
				betaolsc[i,] <- as.vector(fullc.lm$coefficients)
			}
			else {  # if coefficient shrinking is applied, we use a ridge regression instead
				if (ridgeLassoBlend == 0){
					fullc.lm <- lm.ridge(yc ~ xcin - 1, lambda=coeffShrink)
					betaolsc[i,] <- as.vector(coef(fullc.lm))
				}
				else{
					glmmod <- glmnet(xcin - 1, y=yc, alpha=ridgeLassoBlend, lambda=coeffShrink, standardize=False)
					betaolsc[i,] <- as.vector(coef(glmmod)[-1])
				}
			}

            odds <- rep(0, p)
            odds1 <- priorincprob / (1 - priorincprob)
            odds2 <- (lam * dj[- 1] + 1) ^ (- 0.5)
            odds3 <- (as.vector(betaolsc[i, - 1]) * dj[- 1]) ^ 2 / (dj[- 1] + (1 / lam))
            logodds <- log(odds1) + log(odds2) + (odds3 * phi / 2)
            logodds[logodds > 700] <- 700
            odds <- exp(logodds)
            oddsmat[i,] <- odds
            postincprob[i,] <- odds / (1 + odds)
            temp_vec <- as.vector(postincprob[i,])
            temp_vec[is.na(temp_vec)] <- 0
            gamma <- rbinom(p, 1, temp_vec)

            if (sum(gamma) >= 1)
            {
                if (sum(gamma) == 1)
                {
                    Pbeta <- (lam[gamma == 1] + xcxc[gamma == 1, gamma == 1]) * phi
                    Vbeta <- 1 / Pbeta
                } else {
                    Pbeta <- phi * (diag(lam[gamma == 1]) + xcxc[gamma == 1, gamma == 1])
                    Vbeta <- solve(Pbeta)
                }
                Ebeta <- phi * as.matrix(Vbeta) %*% xcxc[gamma == 1, gamma == 1] %*% as.matrix(betaolsc[i, - 1][gamma == 1])

                betatemp[gamma == 1] <- mvrnorm(1, Ebeta, Vbeta)
                betatemp[gamma == 0] <- 0
            } else if (sum(gamma) == 0)# end if (sum(gamma)==1) execution else
                betatemp[gamma == 0] <- 0
            betamat[i,] <- betatemp
            Ealpha <- betaolsc[i, 1]
            Palpha <- phi * dj[1]
            alpha <- rnorm(1, Ealpha, sqrt(1 / Palpha))
            alphavec[i] <- alpha

            muz <- xoin %*% as.matrix(c(alphavec[i], betamat[i,]))
            yo[zo == 1] <- muz[zo == 1] + qnorm(runif(s, 0, 1) * pnorm(muz[zo == 1]) + pnorm(- muz[zo == 1]))
            yo[zo == 0] <- muz[zo == 0] + qnorm(runif(no - s, 0, 1) * pnorm(- muz[zo == 0]))
            if (i %% 10000 == 0)
                print(paste("iter", i, sep = " "))
        }
        beta0.hat <- mean(betaolsc[- c(1 : burnin), 1])
        d <- round(lamc + 0.001, 10)
        beta.hat <- apply(betaolsc[- c(1 : burnin), - 1] * postincprob[- c(1 : burnin),], 2, mean) * (d / (d + lam.spec))
        beta.hat <- beta.hat / sqrtvar
        beta0.hat <- beta0.hat - sum(beta.hat * xomean)
        incprob.rb <- apply(postincprob[- c(1 : burnin),], 2, mean)
        return(list(betabma = c(beta0.hat, beta.hat), incprob.rb = incprob.rb, incprob = postincprob, gamma = gammamat, odds = oddsmat))
    }
    else
    return(c("xa is not psd"))
}
