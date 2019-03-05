
/* R CMD SHLIB callmodelprobs.c */

/* callmodelprobs.c */

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>
#include <time.h>
#include <limits.h>
#include "arrays.hpp" /*dynamic memory allocation routines */



void callmodelprobs(int *starnmod, int *starniter, int *starp, int *gammamat, double *probmat, double *modelprobs)
{
	int i,j,k, nmod=*starnmod, p=*starp, niter=*starniter;
	// int i, j, k, ngammamat=32768, nprobmat=300000, p=15;   
	double tempsum, tempprod;
 
	for (i = 0; i < nmod; i++)
	{
		tempsum = 0.0;
		for(j = 0; j < niter; j++)
		{
			tempprod = 1.0;
			for(k = 0; k < p; k++)
			{
				// tempprod *= pow(postincprob[j][k],(double)(gamma[i][k]))*pow((1-postincprob[j][k]),(double)(1-gamma[i][k]));  
				if (gammamat[i + k * nmod] == 1)  {
					tempprod *= probmat[j + k * niter];
				}
				else
				{
					tempprod *= (1.0 - probmat[j + k * niter]);
				}
			}
			tempsum += tempprod;
		}
		modelprobs[i] = tempsum / (double)(niter);
	}
}
