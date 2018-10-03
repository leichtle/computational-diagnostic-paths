## Bootstrap of the inclusion probabilities
MED <-function(x,d){
  return(quantile(x[d],probs=c(0.5)))
}
library(boot)
a<-t(Datenmatrix)
x<-as.numeric(a[2:4,14])

med<- boot(x, MED, R=1000)

med
bcim<-boot.ci(med, R=1000)
bcim
