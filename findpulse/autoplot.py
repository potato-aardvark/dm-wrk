#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (12, 8)

tmf, intensity = np.loadtxt('/mnt/scratch-lustre/haoxu/out/testrun/0818find.txt', unpack=True)
times = tmf * 0.005
tim_ind = np.argsort(times)
plt.plot(times[tim_ind], intensity[tim_ind])
plt.xlabel('time (s)')
plt.ylabel('intensity (arb. units)')
plt.show()

