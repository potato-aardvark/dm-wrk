#!/bin/bash

python makeplot.py 2018-08-16T10:38:25.595 25 26.6787 20.9wrongdm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python makeplot.py 2018-08-16T10:38:40.600 25 26.6765 35.9wrongdm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python makeplot.py 2018-08-16T10:38:44.175 25 26.6759 39.5wrongdm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python makeplot.py 2018-08-16T10:39:14.895 25 26.6743 70.25wrongdm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
python makeplot.py 2018-08-16T10:39:29.900 25 26.6803 85.3wrongdm 1 1 correctdmplots/ correctdmdata/ --data /mnt/scratch-lustre/haoxu/B0329data/0818/000{0000..1999}.vdif &
wait
