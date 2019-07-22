#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (12, 8)

t_ind, intensity = np.loadtxt('/mnt/scratch-lustre/haoxu/out/testrun/testrun.txt', unpack=True)
times = t_ind * 0.005
plt.plot(times, intensity)
plt.xlabel('time (s)')
plt.ylabel('intensity (arb. units)')
plt.show()

