#!/bin/bash
#SBATCH -J cdp_experimental
#SBATCH -o cluster/log/%j_experimental_std.log
#SBATCH -e cluster/log/%j_experimental_err.log
#SBATCH -t 700:00:00
#SBATCH -p nodes
#SBATCH -A insel

echo $1 $2
source /home/INSEL/i0325777/miniconda3/bin/activate evidence-based-diagnostic-paths # conda activate evidence-based-diagnostic-paths # source venv3/bin/activate
python $1 $2

