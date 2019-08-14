import argparse
import numpy as np
import matplotlib.pyplot as plt
from scintillometry.generators import EmptyStreamGenerator
from scintillometry.dispersion import Dedisperse

# get the cmdline args
parser = argparse.ArgumentParser()
parser.add_argument('candidate', help='the candidate datafile')
parser.add_argument('upper_dm', type=float, help='the upper dm')
parser.add_argument('lower_dm', type=float, help='the lower dm')
args = parser.parse_args()

npz = np.load(args.candidate)

