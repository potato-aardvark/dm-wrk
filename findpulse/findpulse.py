import argparse
import os

import numpy as np
import astropy.units as u
from astropy import time
import pipeline as plm
from baseband import vdif

parser = argparse.ArgumentParser()
parser.add_argument('runname', default='myrun', help='the name of the run')
parser.add_argument('start', type=float, help='the start time (in sec)')
parser.add_argument('pulsenum', type=int, help='the number of pulses')
parser.add_argument('--data', help='the baseband data folder')
parser.add_argument('--datafilestart', type=int, help='the first data file')
parser.add_argument('--datafileend',
        type=int, help='the last data file (inclusive)')
parser.add_argument('--out', nargs='?', help='where to write the data')
parser.add_argument('--dm', type=float, default=26.67, help='dm')
args = parser.parse_args()

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

PERIOD = 0.714519699726 * u.s
READ_SZ = 40 * u.ms

pl.outstream.seek(args.start * u.s, 'start')
for i in range(args.pulsenum):
    data = pl.read_time(READ_SZ)
    np.savez(
            args.out.format(pl.outstream.tell(u.s).value),
            data=data,
            time=pl.outstream.tell(u.s)
    )
    pl.outstream.seek(PERIOD - READ_SZ, 'current')
