#!/bin/bash

python makeplot.py 2018-08-16T10:38:40.600 25 26.6775 35.9svddm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python makeplot.py 2018-08-16T10:38:44.175 25 26.6769 39.5svddm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python makeplot.py 2018-08-16T10:39:14.895 25 26.6753 70.25svddm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python makeplot.py 2018-08-16T10:39:29.900 25 26.6813 85.3svddm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
wait
