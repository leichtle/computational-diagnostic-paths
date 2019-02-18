#!/bin/bash
#SBATCH -J cdp_dataset
#SBATCH -o cluster/log/%j_dataset_std.log
#SBATCH -e cluster/log/%j_dataset_err.log
#SBATCH -t 700:00:00
#SBATCH -p nodes
#SBATCH -A insel

echo $1
export PATH=/software/bin:$PATH # append R location to path before running it
Rscript ./dataset.r $1

