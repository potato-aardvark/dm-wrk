from pipeline import *

import argparse
import numpy as np
from numpy.linalg import svd
import astropy.units as u
from astropy import time
from baseband import vdif
from scintillometry import shaping

parser = argparse.ArgumentParser()
parser.add_argument(
        'starttime',
        type=(lambda s: time.Time(s, format='isot', scale='utc')),
        help='the start time'
)
parser.add_argument(
        'timedelta',
        type=(lambda s: time.TimeDelta(float(s) / 1000, format='sec')),
        help='the time delta in ms'
)
parser.add_argument(
        'dm',
        type=float,
        help='the min dm'
)
parser.add_argument(
        'dm2',
        type=float,
        help='the max dm'
)
parser.add_argument(
        'dm_step_sz',
        type=float,
        help='the dm step size'
)
parser.add_argument(
        'dm_index',
        type=int,
        help='the dm index'
)
parser.add_argument('runname', default='myrun', help='the name of the run')
parser.add_argument('--data', nargs='+', default=[], help='the baseband data files')
parser.add_argument('--out', nargs='?', help='where to write the data')
parser.add_argument(
        '--freqsplit',
        default=None,
        type=float,
        help='where the frequency split is (MHz)'
)

args = parser.parse_args()

if args.freqsplit is None:
    freqsplit_ind = None
else:
    freqsplit_ind = int(np.floor(np.interp(540, [400, 800], [1023, 0])))


fhv = vdif.open(args.data)
output = open(args.out, 'w')


def get_svd_data(data):
    """Get the rating of the svd fit for the dedispersed data."""
    svd_s = svd(data)[1]
    return svd_s[0]

def get_svd_pipeline(pl):
    """Get the rating of the svd fit for the dedispersed data."""
    return get_svd_data(pl.read_time(args.timedelta))

def setup_pipeline(dm):
    """Construct, prepare, and return the pipeline using the specified dm."""
    pl = WaterfallIntensityPipeline(
            fhv, dm, reference_frequency=800*u.MHz,
            samples_per_frame=2**18,
            frequencies=np.linspace(800, 400, 1024)*u.MHz, sideband=1
    )
    pl.outstream.seek(args.starttime)
    return pl

def get_svd_dm(dm):
    return get_svd_pipeline(setup_pipeline(dm))

curr_dm = np.arange(args.dm, args.dm2 + args.dm_step_sz, args.dm_step_sz)\
                [args.dm_index]
pl = setup_pipeline(curr_dm)
data = pl.read_time(args.timedelta)

if freqsplit_ind is None:
    svd = svd(data, full_matrices=False)[1][0]
    output.write('{} {}\n'.format(curr_dm, svd)
else:
    upper_data = data[:, :int(np.floor(np.interp(540, [400, 800], [1023, 0])))]
    lower_data = data[:, int(np.ceil(np.interp(540, [400, 800], [1023, 0]))):]
    svd_upper = svd(upper_data, full_matrices=False)[1][0] 
    svd_lower = svd(lower_data, full_matrices=False)[1][0]
    output.write('{} {} {}\n'.format(curr_dm, svd_upper, svd_lower))
