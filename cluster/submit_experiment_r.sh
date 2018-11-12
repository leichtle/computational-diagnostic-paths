#!/bin/bash
#SBATCH -J experiment_evidence-based-diagnostic-paths
#SBATCH -o cluster/log/%j_experiment_std.log
#SBATCH -e cluster/log/%j_experiment_err.log
#SBATCH -t 700:00:00
#SBATCH -p nodes
#SBATCH -A insel
#SBATCH --mem-per-cpu=180000

echo $1
export PATH=/software/bin:$PATH # append R location to path before running it
Rscript experiment.r $1

