#!/bin/bash

python svd-split-makeplot.py 2018-08-16T10:38:25.598 15 26.6797 0 20.9svd-dm 1 1 makeplot-plots/ makeplot-data/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python svd-split-makeplot.py 2018-08-16T10:38:40.604 15 26.6775 0  35.9svd-dm 1 1 makeplot-plots/ makeplot-data/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python svd-split-makeplot.py 2018-08-16T10:38:44.175 15 26.6769 0 39.5svd-dm 1 1 makeplot-plots/ makeplot-data/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python svd-split-makeplot.py 2018-08-16T10:39:14.896 15 26.6753 0 70.25svd-dm 1 1 makeplot-plots/ makeplot-data/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python svd-split-makeplot.py 2018-08-16T10:39:29.900 15 26.6817 0 85.3svd-dm 1 1 makeplot-plots/ makeplot-data/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
wait
