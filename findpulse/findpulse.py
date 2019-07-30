import argparse

import numpy as np
import astropy.units as u
from astropy import time
import pipeline as plm
from baseband import vdif

parser = argparse.ArgumentParser()
parser.add_argument(
        'timedelta',
        type=(lambda s: time.TimeDelta(float(s) / 1000, format='sec')),
        help='the time delta in ms'
)
parser.add_argument('runname', default='myrun', help='the name of the run')
parser.add_argument('start', type=int, help='the start index')
parser.add_argument('end', type=int, help='the end index')
parser.add_argument('skip', type=int, default=None, help='the skip slice bit')
parser.add_argument('--data', nargs='+', default=[], help='the baseband data files')
parser.add_argument('--out', nargs='?', help='where to write the data')
parser.add_argument('--dm', type=float, default=26.67, help='dm')
args = parser.parse_args()

fh = vdif.open(args.data)
pl = plm.WaterfallIntensityPipeline(fh,
        args.dm,
        800*u.MHz,
        2**19,    ###
        np.linspace(800, 400, 1024)*u.MHz,
        1
)

for i in range(int(args.start), int(args.end), int(args.skip)):
    pl.outstream.seek(args.timedelta * i)
    data = pl.read_time(args.timedelta)
    data = plm.remove_rfi(data)
    data = np.nansum(data)
    with open(args.out, 'a') as f:
        f.write('{} {}\n'.format(i, data))
