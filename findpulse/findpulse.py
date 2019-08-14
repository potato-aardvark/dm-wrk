import argparse
import os

import numpy as np
import astropy.units as u
from astropy import time
from baseband import vdif
from scintillometry.integration import Stack
from scintillometry.dispersion import Dedisperse
from scintillometry.functions import Square
from scintillometry.phases import PolycoPhase

parser = argparse.ArgumentParser()
parser.add_argument('runname', default='myrun', help='the name of the run')
parser.add_argument('start', type=int, help='the start index')
parser.add_argument('end', type=int, help='the end index')
parser.add_argument('skip', type=int, default=None, help='the skip slice bit')
parser.add_argument('polyco_file', help='where the polyco.dat file is')
parser.add_argument('--data', help='the baseband data folder')
parser.add_argument('--datafilestart', type=int, help='the first data file')
parser.add_argument('--datafileend',
        type=int, help='the last data file (inclusive)')
parser.add_argument('out', help='where to write the data')
parser.add_argument('--dm', type=float, default=26.67, help='dm')
args = parser.parse_args()


fh = vdif.open(
    [
        os.path.join(args.data, '{:0>7}.vdif'.format(i))
        for i in range(args.datafilestart, args.datafileend + 1)
    ]
)

dedisp = Dedisperse(fh, 26.67, reference_frequency=540*u.MHz,
        frequency=np.linspace(800., 400., 1024)*u.MHz, sideband=1)

sq_dedisp = Square(dedisp)

stack = Stack(sq_dedisp, 2**18, PolycoPhase(args.polyco_file))
 
for i in range(int(args.start), int(args.end), int(args.skip)):
    stack.seek(i)
    rawdata = stack.read(1)
    data = rawdata[0, 110000:135000]
    np.savez_compressed(os.path.join(args.out, str(i)), data=data,
            i=np.array(i))

