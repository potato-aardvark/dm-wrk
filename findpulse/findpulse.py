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
parser.add_argument('num', type=int, help='the number of pulses')
parser.add_argument('skip', type=int, default=None, help='the skip slice bit')
parser.add_argument('polyco_file', help='where the polyco.dat file is')
parser.add_argument('--data', help='the baseband data folder')
parser.add_argument('--datafilestart', type=int, help='the first data file')
parser.add_argument('--datafileend',
        type=int, help='the last data file (inclusive)')
parser.add_argument('pulse_start', type=int,
        help='the phase index where the pulse starts')
parser.add_argument('pulse_end', type=int, 
        help='the phase index where the pulse ends')
parser.add_argument('out', help='where to write the data')
parser.add_argument('--dm', type=float, default=26.67, help='dm')
args = parser.parse_args()

orig_n_phases = 2**18
n_phases = 2**10
# Since the arguments passed in expect n_phases = 2**18, and we have 
# n_phases = 2**10, we need to adjust downwards.
args.pulse_start = (args.pulse_start * n_phases) // orig_n_phases
args.pulse_end = (args.pulse_end * n_phases) // orig_n_phases

fh = vdif.open(
    [
        os.path.join(args.data, '{:0>7}.vdif'.format(i))
        for i in range(args.datafilestart, args.datafileend + 1)
    ]
)

dedisp = Dedisperse(fh, 26.67, reference_frequency=540*u.MHz,
        samples_per_frame=2**18, frequency=np.linspace(800., 400., 1024)*u.MHz,
        sideband=1)

sq_dedisp = Square(dedisp)

# 2 ** 18
stack = Stack(sq_dedisp, n_phases, PolycoPhase(args.polyco_file))
 
for i in range(int(args.start), int(args.start + args.num), int(args.skip)):
    stack.seek(i)
    data = stack.read(1).sum()
    with open(os.path.join(args.out, args.runname), 'a') as outfh:
        outfh.write('{} {}\n'.format(i, data))

