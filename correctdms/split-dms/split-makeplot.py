# TODO: correct reference_frequency. Should be 540 MHz + corresponding
# time adjustment if not negligible

from pipeline import *
import numpy as np
from numpy.linalg import svd
from baseband import vdif
import astropy.time as astrotime
import astropy.units as u
import matplotlib.pyplot as plt
import os  # for path.join
import argparse

FREQ_CUTOFF = int(np.floor(np.interp(540, [400, 800], [1023, 0])))

# python makeplot.py starttime timeinterval dm runname 
#   timebin_sz freqbin_sz --data files
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

datasave_loc = 'makeplot-data/'
plotsave_loc = 'makeplot-plots/'

# set up the pipeline
plhi = WaterfallIntensityPipeline(
        args.data, args.dm, reference_frequency=800*u.MHz,
        samples_per_frame=2**18,
        frequencies=np.linspace(800, 400, 1024)*u.MHz, sideband=1
)
plhi.outstream.seek(args.starttime)
rawdatahi = plhi.read_time_div(args.timedelta, args.timebin_sz)

pllo = WaterfallIntensityPipeline(
        args.data, args.dm2, reference_frequency=800*u.MHz,
        samples_per_frame=2**18,
        frequencies=np.linspace(800, 400, 1024)*u.MHz, sideband=1
)
pllo.outstream.seek(args.starttime)
rawdatalo = pllo.read_time_div(args.timedelta, args.timebin_sz)

rawdata = np.concatenate(rawdatahi[:FREQ_CUTOFF], rawdatalo[FREQ_CUTOFF:])

print(rawdata.shape[1])
assert rawdata.shape[1] == 1024

data = bin_data(rawdata, args.timebin_sz, args.freqbin_sz)
rfifind = bin_data(pl.read_count(1000), args.timebin_sz, args.freqbin_sz)
rfirmdata = remove_rfi(data, rfifind, 0)
plt.imshow(
        rfirmdata.transpose(),
        aspect='auto',
        extent=[0, args.timedelta.to(u.ms).value, 400, 800]
)
plt.xlabel('time (ms)')
plt.ylabel('freq (MHz)')
if plotsave_loc:
    plt.savefig(os.path.join(plotsave_loc, args.runname + '.png'))
if datasave_loc:
    np.savez(os.path.join(datasave_loc, args.runname + '.npz'), rawdata)

print(svd(rfirmdata)[1][0])
