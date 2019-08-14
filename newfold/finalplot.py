import os
import sys
import numpy as np
import matplotlib.pyplot as plt

monthyear = sys.argv[1]

try:
    times, his, los = np.loadtxt(os.path.join('summary' + monthyear, monthyear),
            unpack=True)
except FileNotFoundError: 
    times, his, los = np.loadtxt(
            os.path.join('summary' + monthyear + 'old', monthyear),
            unpack=True
    )

# account for initial dm offset
diff = his - los

plt.figure()
# plt.plot(times, his, 'C0.', label='DM for freq > 540 MHz')
# plt.plot(times, los, 'C1.', label='DM for freq <= 540 MHz')
plt.plot(times, diff, '.', label='DM difference (upper - lower)')

# plt.axhline(los.mean(), color='C1', label='average DM for freq <= 540 MHz')

if monthyear == '0418':
    datewords = 'April 2018'
elif monthyear == '0818':
    datewords = 'August 2018'
elif monthyear == '1218a':
    datewords = 'December 2018'

plt.suptitle('DM difference for pulses taken on {}'.format(datewords))
plt.xlabel('time (s)')
plt.ylabel('DM (pc/cm^3)')
plt.legend()
plt.savefig('finalfig' + monthyear)
