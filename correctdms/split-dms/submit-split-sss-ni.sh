#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=80
#SBATCH --time=12:00:00
#SBATCH --job-name sss-submit8
#SBATCH --mail-type=ALL

# Check: directories, time

source $HOME/quickenvsetup.sh

cd $SLURM_SUBMIT_DIR
module load gnu-parallel

mkdir /dev/shm/workdir

function cleanup_ramdisk {
cd /dev/shm/workdir/
cat *.outtxt > final.txt
cp final.txt $SLURM_SUBMIT_DIR/try8tasks2/  ###
cd $SLURM_SUBMIT_DIR
rm -rf /dev/shm/workdir
}

trap "cleanup_ramdisk" TERM

parallel --joblog slurm-$SLURM_JOBID.log -j 8 "python svd-split-seeksingle.py 2018-08-16T10:39:29.900 25 26.67 26.77 0.0001 {} 85.3snrun --data $SCRATCH/recalled/B0329+54/20180816T103808Z_aro_vdif/untarred/{0000000..0001999}.vdif --out /dev/shm/workdir/{}.outtxt --freqsplit 540" ::: {0..1000}  ###
# use 8 tasks instead of 40 or 80 because memory

cleanup_ramdisk
