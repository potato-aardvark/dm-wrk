import argparse
import os

import numpy as np
import astropy.units as u
from astropy import time
from baseband import vdif
from scintillometry.integration import Stack
from scintillometry.dispersion import Dedisperse
from scintillometry.functions import Square

parser = argparse.ArgumentParser()
parser.add_argument('runname', default='myrun', help='the name of the run')
parser.add_argument('start', type=int, help='the start index')
parser.add_argument('end', type=int, help='the end index')
parser.add_argument('skip', type=int, default=None, help='the skip slice bit')
parser.add_argument('--data', help='the baseband data folder')
parser.add_argument('--datafilestart', type=int, help='the first data file')
parser.add_argument('--datafileend',
        type=int, help='the last data file (inclusive)')
parser.add_argument('--out', nargs='?', help='where to write the data')
parser.add_argument('--dm', type=float, default=26.67, help='dm')
args = parser.parse_args()

period = 0.714519699726 * u.s

fh = vdif.open(
    [
        os.path.join(args.data, '{:0>7}.vdif'.format(i))
        for i in range(args.datafilestart, args.datafileend + 1)
    ]
)

pl = plm.WaterfallIntensityPipeline(fh,
        args.dm,
        800*u.MHz,
        2**18,    ###
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
