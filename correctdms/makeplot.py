import wheres, relwheres
from pipeline import *

import numpy as np
import astropy.time as astrotime
import astropy.units as u
import matplotlib.pyplot as plt
import os  # for path.join
import argparse

raise NotImplemented('you should probably implement pipeline.WaterfallIntensityPlot.read_time_div() before running this')

# python makeplot.py starttime timeinterval dm runname 
#   timebin_sz freqbin_sz files
# 
# timeinterval in ms
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
        help='the dm'
)
parser.add_argument('runname', help='the name of the run')
parser.add_argument(
        'timebin_sz',
        type=int,
        nargs='?',
        default=10,
        help='the size of the time bins'
)
parser.add_argument(
        'freqbin_sz',
        type=int,
        nargs='?',
        default=4,
        help='the size of the frequency bins'
)
parser.add_argument(
        'plotsave_loc',
        nargs='?',
        help='where to save the plots'
)
parser.add_argument(
        'datasave_loc', 
        nargs='?',
        help='where to save the data'
)
parser.add_argument('--data', nargs='+', default=[], help='the data files')
args = parser.parse_args()

# set up the pipeline
pl = WaterfallIntensityPipeline(
        args.data, args.dm, reference_frequency=800*u.MHz,
        frequencies=np.linspace(800, 400, 1024)*u.MHz, sideband=1
)
pl.outstream.seek(args.starttime)
rawdata = pl.read_time_div(args.timedelta, args.timebin_sz)
data = bin_data(rawdata, args.timebin_sz, args.freqbin_sz)
rfifind = bin_data(pl.read_count(1000), args.timebin_sz, args.freqbin_sz)
rfirmdata = remove_rfi(data, rfifind, 0)
plt.imshow(
        rfirmdata.transpose(),
        aspect='auto',
        extent=[0, args.timedelta.to(u.ms), 400, 800])
plt.xlabel('time (ms)')
plt.ylabel('freq (MHz)')
if args.plotsave_loc:
    plt.savefig(os.path.join(args.plotsave_loc, args.runname + '.png'))
if args.datasave_loc:
    np.savez(rawdata, os.path.join(args.datasave_loc, args.runname + '.npz'))
