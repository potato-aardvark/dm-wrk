#!/bin/bash

for part in {20.9,35.9,39.5,70.25,85.3,98.9,166.09} 
do
    python svd-split-eat.py makeplot-data/${part}svd-splitdm.npz 1 16 ${part}svd-splitdm       15   &
    python svd-split-eat.py makeplot-data/${part}svd-splitdm.npz 1 16 ${part}svd-splitdm-lower 15    400 540 &
    python svd-split-eat.py makeplot-data/${part}svd-splitdm.npz 1 16 ${part}svd-splitdm-upper 15    540 800 &
    python svd-split-eat.py makeplot-data/${part}svd-dm.npz      1 16 ${part}svd-dm            15   &
done

wait
