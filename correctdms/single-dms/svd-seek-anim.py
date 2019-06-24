from pipeline import *

import argparse
import logging
import numpy as np
from numpy.linalg import svd
import astropy.units as u
from astropy import time
from baseband import vdif

import matplotlib.pyplot as plt
import matplotlib.animation as anim

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
parser.add_argument('runname', default='myrun', help='the name of the run')
parser.add_argument('--data', nargs='+', default=[], help='the baseband data files')
args = parser.parse_args()

logging.basicConfig(
        filename='logs/{}.log'.format(args.runname),
        level=logging.DEBUG
)

logging.info(args.runname)

fhv = vdif.open(args.data)

def get_svd_data(data):
    """Get the rating of the svd fit for the dedispersed data."""
    svd_s = svd(data)[1]
    return svd_s[0], data

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

curr_max_svd = -1
curr_best_dm = None

ims = []
fig = plt.figure()

for curr_dm in np.arange(args.dm, args.dm2 + args.dm_step_sz, args.dm_step_sz):
    svd_for_dm, data = get_svd_dm(curr_dm)
    if svd_for_dm > curr_max_svd:
        curr_max_svd = svd_for_dm
        curr_best_dm = curr_dm
    logging.info('{:.9f} {:.9f}'.format(curr_dm, svd_for_dm))
    data = np.clip(data, -1, 5)
    ims.append((plt.imshow(data.transpose(), aspect='auto', animated=True),))
    plt.suptitle(curr_dm)
    plt.savefig('anim/test_im' + str(len(ims)) + '.png')
im_anim = anim.ArtistAnimation(
        fig, ims, interval=50, blit=True, repeat_delay=1000
)
im_anim.save('anim/test_im.mp4')

logging.info('best dm/svd: {:.9f} {:.9f}'.format(curr_best_dm, curr_max_svd)) 

