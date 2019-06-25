#!/bin/bash

python svd-split-seek.py 2018-08-16T10:38:25.595 25 26.67 26.72 0.0001 20.9dm-split-seek --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif  &
python svd-split-seek.py 2018-08-16T10:38:40.600 25 26.67 26.72 0.0001 35.9dm-split-seek --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif  &
python svd-split-seek.py 2018-08-16T10:38:44.175 25 26.67 26.72 0.0001 39.5dm-split-seek --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif  &
python svd-split-seek.py 2018-08-16T10:39:14.895 25 26.67 26.72 0.0001 70.25dm-split-seek --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python svd-split-seek.py 2018-08-16T10:39:29.900 25 26.67 26.72 0.0001 85.3dm-split-seek --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif  &
wait
