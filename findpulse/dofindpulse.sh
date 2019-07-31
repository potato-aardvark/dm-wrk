#!/bin/bash -l
#PBS -l nodes=1:ppn=1
#PBS -l walltime=48:00:00
#PBS -r n
#PBS -j oe
#PBS -q workq

module load python/conda3-5.3
source ~/.virtualenvs/vscint/bin/activate 
module load use.own
module load scintpipe

# cd $PBS_O_WORKDIR
python findpulse.py 5 run0818 $1 $2 $3 --data /mnt/scratch-lustre/haoxu/B0329data/0818/ --datafilestart 0 --datafileend 199999 --out /mnt/scratch-lustre/haoxu/out/testrun/0818find.txt
