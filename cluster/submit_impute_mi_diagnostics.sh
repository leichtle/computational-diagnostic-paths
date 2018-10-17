#!/bin/bash
#SBATCH -J dataset
#SBATCH -o cluster/log/%j_dataset_std.log
#SBATCH -e cluster/log/%j_dataset_err.log
#SBATCH -t 16:00:00
#SBATCH -p nodes
#SBATCH -A insel
#SBATCH --mem-per-cpu=180000

echo $1
export PATH=/software/bin:$PATH # append R location to path before running it
Rscript ./impute_mi_diagnostics.r --file $1
deactivate