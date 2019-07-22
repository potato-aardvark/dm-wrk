#!/usr/bin/env python
'''Quickly plot a 30-ms interval around the pulse to see if microstructure.'''

import argparse

import numpy as np
import matplotlib.pyplot as plt
from pipeline import *
from datareduce import datareduce
from baseband import vdif
import astropy.units as u

parser = argparse.ArgumentParser()
parser.add_argument('offset', type=float, help='the offset, in seconds, where'
        'plotting should start')
parser.add_argument('--data', 
        default=['/mnt/scratch-lustre/haoxu/B0329data/0818/{:0>7}.vdif' \
                .format(i) for i in range(41000)
                ],
        nargs='+',
        help='where the data be'
)

args = parser.parse_args()

start, out, end = datareduce(args.data, 26.67, None, args.offset * u.s, 30. * u.ms, 1,
        16, None)
out = remove_rfi(out)
out = np.clip(out, -1, 5)
out = bin_data(out, 1, 16)


fig = plt.figure()
im = plt.imshow(out.T, extent=[0, 30, 400, 800], aspect='auto')
plt.xlabel('time (ms)')
plt.ylabel('frequency (MHz)')
plt.suptitle(
        'Quick plot of pulse at offset {} (time {})' \
                .format(args.offset, start.value)
)
plt.colorbar(im)
plt.show()

if input('save? ') == 'y':
   fig.savefig('pulseprev{}.png'.format(args.offset)) 
