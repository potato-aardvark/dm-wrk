#!/bin/bash
#SBATCH --time=12:00:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=80

RUNNAME=$1

cd $SLURM_SUBMIT_DIR
export OMP_NUM_THREADS=1
module load gnu-parallel
. ~/quickenvsetup.sh

echo "$RUNNAME"
find candidates$RUNNAME -mindepth 1 -maxdepth 1 | parallel --joblog svdsss_joblog_$RUNNAME -j $SLURM_TASKS_PER_NODE --resume-failed "python svd-split-seeksingle.py $RUNNAME '{1}' -0.03 0.07 1000 {2}" :::: - ::: {0..999}
