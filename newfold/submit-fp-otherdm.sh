#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=80
#SBATCH --time=12:00:00

# ###############CHANGE QUEUE #
# Check: directories, time

RUNNAME="_otherdm"

source $HOME/quickenvsetup.sh

mkdir $BB_JOB_DIR/partials
cd $SLURM_SUBMIT_DIR
module load gnu-parallel

cleanup () {
    mv -f $BB_JOB_DIR/partials/* $SLURM_SUBMIT_DIR/partials$RUNNAME
}
last_cleanup () {
    cleanup
    rm -rf $BB_JOB_DIR/partials
}

trap "last_cleanup" TERM INT

HOSTS=$(scontrol show hostnames $SLURM_NODELIST | tr '\n' ,)

parallel --env OMP_NUM_THREADS,PATH,LD_LIBRARY_PATH,PYTHONPATH -j 6 --link --joblog $SLURM_SUBMIT_DIR/joblog$RUNNAME  -S $HOSTS "echo {1}; python $HOME/dm-wrk/findpulse/findpulse.py --data $SCRATCH/recalled/B0329+54/0418 --datafilestart 0 --datafileend 160000 --out $BB_JOB_DIR/partials/{:012.7f}.npz --dm 26.69 otherdm {1} 1" :::: startargs0418 &
# use 8 tasks instead of 40 or 80 because memory
PAR_JID=$!

while true; do
    sleep 600
    cleanup
done &

wait $PAR_JID
last_cleanup
