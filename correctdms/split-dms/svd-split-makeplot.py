#!/usr/bin/env python
'''Read from baseband and save data to disc as .npz file'''

from pipeline import *
from datareduce import datareduce
import numpy as np
from numpy.linalg import svd
from baseband import vdif
import astropy.time as astrotime
import astropy.units as u
import matplotlib.pyplot as plt
import os  # for path.join
import argparse

freq2index = lambda f: int(np.floor(np.interp(f, [400, 800], [1023, 0])))

parser = argparse.ArgumentParser()
parser.add_argument(
        'starttime',
        type=(lambda s: astrotime.Time(s, format='isot', scale='utc')),
        help='the start time'
)
parser.add_argument(
        'timedelta',
        type=(lambda s: astrotime.TimeDelta(float(s) / 1000, format='sec')),
        help='the time delta in ms'
)
parser.add_argument(
        'dm',
        type=(lambda d: float(d) * u.pc/u.cm**3),
        help='the dm for the higher frequencies'
)
parser.add_argument(
        'dm2',
        type=(lambda d: float(d) * u.pc/u.cm**3),
        help='the dm for the lower frequencies'
)
parser.add_argument('runname', help='the name of the run')
parser.add_argument(
        'timebin_sz',
        type=int,
        nargs='?',
        default=1,
        help='the size of the time bins'
)
parser.add_argument(
        'freqbin_sz',
        type=int,
        nargs='?',
        default=1,
        help='the size of the frequency bins'
)
parser.add_argument('--data', nargs='+', default=[], help='the data files')
parser.add_argument('--freqsplit', default=None, help='where the split is')
args = parser.parse_args()

datasave_loc = 'makeplot-data/'
plotsave_loc = 'makeplot-plots/'
freqsplit = None if args.freqsplit is None else freq2index(args.freqsplit)

# reduce the data: i.e., dedisperse, read, etc.
_, rawdata, _ = datareduce(args.data, args.dm, args.dm2, args.starttime,
        args.timedelta, args.timebin_sz, args.freqbin_sz, freqsplit)

data = bin_data(rawdata, args.timebin_sz, args.freqbin_sz)
rfirmdata = remove_rfi(data, fill=0)
plt.imshow(
        np.clip(rfirmdata, 0, 5).transpose(),
        aspect='auto',
        extent=[0, args.timedelta.to(u.ms).value, 400, 800]
)
plt.xlabel('time (ms)')
plt.ylabel('freq (MHz)')
if plotsave_loc:
    plt.savefig(os.path.join(plotsave_loc, args.runname + '.png'))
if datasave_loc:
    np.savez(
        os.path.join(datasave_loc, args.runname + '.npz'),
        data=rawdata,
        freqind=freqsplit if freqsplit is not None else -1,       # the index
        freqval=args.freqsplit,  # the value (MHz)
        upperdm=args.dm,
        lowerdm=args.dm2,
        starttime=args.starttime
    )
