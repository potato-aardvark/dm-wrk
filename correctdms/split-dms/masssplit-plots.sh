#!/bin/bash

python split-makeplot.py 2018-08-16T10:38:25.595 25 26.6702 26.6778 20.9svd-splitdm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python split-makeplot.py 2018-08-16T10:38:40.600 25 26.6939 26.6933 35.9svd-splitdm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python split-makeplot.py 2018-08-16T10:38:44.175 25 26.7175 26.7009 39.5svd-splitdm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python split-makeplot.py 2018-08-16T10:39:14.895 25 26.6785 26.6717 70.25svd-splitdm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python split-makeplot.py 2018-08-16T10:39:29.900 25 26.719 26.6801 85.3svd-splitdm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
wait
