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
parser.add_argument('start', type=float, help='the start time (in sec)')
parser.add_argument('pulsenum', type=int, help='the number of pulses')
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
dedisp = Dedisperse(fh, 26.67, 800*u.MHz,
        frequency=np.linspace(800, 400, 1024)*u.MHz, sideband=1)


pl.outstream.seek(args.start * u.s, 'start')
for i in range(args.pulsenum):
    data = pl.read_time(READ_SZ)
    np.savez(
            args.out.format(pl.outstream.tell(u.s).value),
            data=data,
            time=pl.outstream.tell(u.s)
    )
    pl.outstream.seek(PERIOD - READ_SZ, 'current')
