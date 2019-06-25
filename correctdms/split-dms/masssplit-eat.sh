#!/bin/bash

python svd-split-eat.py makeplot-data/20.9svd-splitdm.npz 5 16 20.9svd-splitdm 25 400 800 "Pulse at 2018-08-16T10:38:25.595, split dms" &
python svd-split-eat.py makeplot-data/35.9svd-splitdm.npz 5 16 35.9svd-splitdm 25 400 800 "Pulse at 2018-08-16T10:38:40.600, split dms" &
python svd-split-eat.py makeplot-data/39.5svd-splitdm.npz 5 16 39.5svd-splitdm 25 400 800 "Pulse at 2018-08-16T10:38:44.175, split dms" &
python svd-split-eat.py makeplot-data/70.25svd-splitdm.npz 5 16 70.25svd-splitdm 25 400 800 "Pulse at 2018-08-16T10:39:14.895, split dms" &
python svd-split-eat.py makeplot-data/85.3svd-splitdm.npz 5 16 85.3svd-splitdm 25 400 800 "Pulse at 2018-08-16T10:39:29.900, split dms" &
wait
