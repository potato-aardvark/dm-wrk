from pipeline import *
import os
import argparse
import numpy as np
from numpy.linalg import svd
import astropy.units as u
from astropy import time
from baseband import vdif
from scintillometry.dispersion import Dedisperse
from scintillometry.generators import EmptyStreamGenerator
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument(
        'monthyear',
        help='the month/year (like 0818)'
)
parser.add_argument(
        'filename',
        help='the file'
)
parser.add_argument(
        'dm_start',
        type=float,
        help='the dm to start at (minus 26.67)'
)
parser.add_argument(
        'dm_end',
        type=float,
        help='the dm to end at (minus 26.67)'
)
parser.add_argument(
        'dm_step',
        type=int,
        help='the number of steps to take in between'
)
parser.add_argument(
        'dm_index',
        type=int,
        help='the dm index'
)
parser.add_argument(
        '--plot',
        action='store_true',
        help='whether to actually make the plot'
)

args = parser.parse_args()

freqsplit_ind = int(np.floor(np.interp(540, [400, 800], [1023, 0])))
thisdm = np.linspace(args.dm_start, args.dm_end, args.dm_step)[args.dm_index]
thisnpz = np.load(args.filename)
thisdata = thisnpz['data']
rfis = np.load('rfi_freq_indexs.npz')
for a, b in rfis['arr_0']:
    thisdata[:, a:b] = 0
thisdata -= thisdata[:500, :].mean(0)

# cut down on the things
if args.monthyear == '0818':
    thisdata = thisdata[9000:13500]


esg = EmptyStreamGenerator(
        (1000000, thisdata.shape[1]), time.Time('2018-01-01T0:00:00'),
        1. / (2.56 * u.us),
        frequency=np.linspace(800., 400., thisdata.shape[1])*u.MHz,
        sideband=1
)
dedisp = Dedisperse(
        esg, thisdm, reference_frequency=540*u.MHz,
        samples_per_frame=thisdata.shape[0]
)

tmp = dedisp.task(thisdata)
upper_data = tmp[:, :freqsplit_ind]
lower_data = tmp[:, freqsplit_ind:]

svd_upper = svd(upper_data, full_matrices=False)[1][0] 
svd_lower = svd(lower_data, full_matrices=False)[1][0]
if args.plot:
    print(thisdm, svd_upper, svd_lower)
    plt.figure()
    plt.imshow(np.clip(np.abs(np.concatenate((upper_data, lower_data), 1)).T, -5, 5), aspect='auto')
    plt.colorbar()
    plt.show()
    plt.close()
else:
    with open('svds{0}/svd{0}_{1}'.format(
            args.monthyear, os.path.basename(args.filename)), 'a') as f:
        f.write('{} {} {}\n'.format(thisdm, svd_upper, svd_lower))
