#!/bin/bash
#SBATCH --time=2:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=40

cd $SLURM_SUBMIT_DIR
export OMP_NUM_THREADS=1
module load gnu-parallel
. ~/quickenvsetup.sh

parallel --joblog ratecands_joblog_${1} -j $SLURM_TASKS_PER_NODE "yes | python ratecands.py $1 {}" ::: {00..39}
