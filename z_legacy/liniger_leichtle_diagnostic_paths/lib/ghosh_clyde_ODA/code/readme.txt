Readme file:
____________

First, code.zip has to be unzipped and all the files need to be stored in one directory.
The two main files that the user would need are 

1. run-oda.r: This R file contains a description of the main function oda.bma()
              and examples of running ODA with simulated and real data used in the paper.
               
2. calc-modelprobs.r: This file contains R code for calculating Rao-Blackwellized estimates 
                      of model probabilities for a set of specific models.  


Other files in code.zip that are required for running the R code in the above two files:

1. arrays.hpp:       Header file required for C code
2. callmodelprobs.c: C code for calculating RB estimates of model probabilities in a post-processing step
3. oda.bma.r:        R function for running ODA 
4. oda.normal.r:     R function for running ODA for linear regression with normal prior on regression coefficients
5. oda.probit.r:     R function for running ODA for probit regression with normal prior on regression coefficients
6. oda.studentst.r:  R function for running ODA for linear regression with Student's-t prior on regression coefficients 
 


  



