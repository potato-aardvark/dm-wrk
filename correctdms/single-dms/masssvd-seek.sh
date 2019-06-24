#!/bin/bash

# TODO: need to deal with upper and lower frequencies separately
python svd-seek.py 2018-08-16T10:38:25.595 25 26.675 26.685 0.0001 35.9dm-seek --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif > out35.9 &
python svd-seek.py 2018-08-16T10:39:29.900 25 26.675 26.685 0.0001 85.3dm-seek --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif > out 85.3 &
python svd-seek.py 2018-08-16T10:38:44.175 25 26.675 26.685 0.0001 39.5dm-seek --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif > out39.5 &
python svd-seek.py 2018-08-16T10:39:14.895 25 26.675 26.685 0.0001 70.25dm-seek --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif > out70.25 &
python svd-seek.py 2018-08-16T10:39:29.900 25 26.675 26.685 0.0001 85.3dm-seek --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif > out 85.3 &
wait
