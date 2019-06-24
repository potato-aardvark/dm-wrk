#!/bin/bash

python svd-eat-pulse.py correctdmdata/20.9svddm.npz 5 16 20.9svddm svd-eat-plots/ svd-eat-data/ 25 400 800 "Pulse at 2018-08-16T10:38:25.595, dm = 26.6797 pc/cm^3" &
python svd-eat-pulse.py correctdmdata/35.9svddm.npz 5 16 35.9svddm svd-eat-plots/ svd-eat-data/ 25 400 800 "Pulse at 2018-08-16T10:38:40.600, dm = 26.6775 pc/cm^3" &
python svd-eat-pulse.py correctdmdata/39.5svddm.npz 5 16 39.5svddm svd-eat-plots/ svd-eat-data/ 25 400 800 "Pulse at 2018-08-16T10:38:44.175, dm = 26.6769 pc/cm^3" &
python svd-eat-pulse.py correctdmdata/70.25svddm.npz 5 16 70.25svddm svd-eat-plots/ svd-eat-data/ 25 400 800 "Pulse at 2018-08-16T10:39:14.895, dm = 26.6753 pc/cm^3" &
python svd-eat-pulse.py correctdmdata/85.3svddm.npz 5 16 85.3svddm svd-eat-plots/ svd-eat-data/ 25 400 800 "Pulse at 2018-08-16T10:39:29.900, dm = 26.6817 pc/cm^3" &
wait
