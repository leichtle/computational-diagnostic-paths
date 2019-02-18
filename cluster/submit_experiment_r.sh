#!/bin/bash
#SBATCH -J cdp_experiment
#SBATCH -o cluster/log/%j_experiment_std.log
#SBATCH -e cluster/log/%j_experiment_err.log
#SBATCH -t 700:00:00
#SBATCH -p nodes
#SBATCH -A insel

echo $1
export PATH=/software/bin:$PATH # append R location to path before running it
Rscript experiment.r $1

