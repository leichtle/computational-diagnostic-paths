#!/bin/bash
#SBATCH -J feature_evidence-based-diagnostic-paths
#SBATCH -o cluster/log/%j_feature_std.log
#SBATCH -e cluster/log/%j_feature_err.log
#SBATCH -t 08:00:00
#SBATCH -p nodes
#SBATCH -A insel
#SBATCH --mem-per-cpu=180000

echo $1
source /home/INSEL/i0325777/miniconda3/bin/activate evidence-based-diagnostic-paths # conda activate evidence-based-diagnostic-paths # source venv3/bin/activate
python feature.py $1

