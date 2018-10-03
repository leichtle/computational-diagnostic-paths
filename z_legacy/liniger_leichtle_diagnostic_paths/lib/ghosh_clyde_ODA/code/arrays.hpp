/*-------------------------------------MEMORY ALLOCATION----------*/
#include<stdlib.h>
#include<stdio.h>
#define freevector(p) {if(p){free(p);p=NULL;}}
double *vector(int n);
int *ivector(int n);
double **matrix(int n,int m);
void freematrix(double **a);

/*-------------------------------(Dynamic Memory allocation stuff)------*/
double *vector(int n)
{
    double *t;
        if((t=(double *)calloc(n,sizeof(double)))==NULL)
        {fprintf(stderr,"Memory allocation error(V)\n");exit(1);}
        return(t);
}
int *ivector(int n)
{
        int *t;
        if((t=(int *)calloc(n,sizeof(int)))==NULL)
        {fprintf(stderr,"Memory allocation error(I)\n");exit(1);}
        return(t);
}
/*--------------------------------------------------------------------------*/
/*-----------------------------------------------------------*/
/*-----------------------------------------------------------*/
double **matrix(int n,int m) /* double **a=matrix[0..n-1][0..m-1] */
{
        int i;
        double **matrx;
        matrx=(double **)calloc(n,sizeof(double*));
        if(matrx==NULL)
        {fprintf(stderr,"Memory allocation error(M)\n");exit(1);}
        matrx[0]=vector(n*m);/* flat memory model */
        for(i=1;i<n;++i)
                matrx[i]=matrx[0]+i*m;
        return(matrx); /* return memory for matrix */
}
/*-------------------------------(Dynamic Memory allocation stuff)------*/
void freematrix(double **a)
{
        freevector(a[0]);
        freevector(a);
}
/*--------------------------------------------------------------------------*/
 



