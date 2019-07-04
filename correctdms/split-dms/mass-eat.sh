#!/bin/bash

python svd-split-eat.py makeplot-data/20.9svd-dm.npz 1 16 20.9svd-dm 15 400 800  &
python svd-split-eat.py makeplot-data/35.9svd-dm.npz 1 16 35.9svd-dm 15 400 800  &
python svd-split-eat.py makeplot-data/39.5svd-dm.npz 1 16 39.5svd-dm 15 400 800  &
python svd-split-eat.py makeplot-data/70.25svd-dm.npz 1 16 70.25svd-dm 15 400 800  &
python svd-split-eat.py makeplot-data/85.3svd-dm.npz 1 16 85.3svd-dm 15 400 800  &
wait
