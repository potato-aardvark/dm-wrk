'''Summarise and plot stuff in the candidates folder,
using data in the svds folder.'''
import os
import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt
from scintillometry.generators import EmptyStreamGenerator
from scintillometry.dispersion import Dedisperse


def extract_best_dms(monthyear, plot=False):
    foldername = 'svds' + monthyear
    summary_foldername = 'summary' + monthyear
    if foldername == 'svds0418':
        foldername = 'svds0418old'
    for filename in os.listdir(foldername):
        if filename.startswith('.'):
            continue
        dms, intns_hi, intns_lo = np.loadtxt(
                os.path.join(foldername, filename), unpack=True
        )
        if dms.size < 1000:
            continue
        try:
            time = float(filename[:-4].replace('svd{}_'.format(monthyear), ''))
        except ValueError as e:
            continue   # invalid time format
        bestdm_hi = dms[np.argmax(intns_hi)]
        bestdm_lo = dms[np.argmax(intns_lo)]

        with open(os.path.join(summary_foldername, monthyear), 'a') as f:
            f.write('{} {} {}\n'.format(time, bestdm_hi, bestdm_lo))

        # print(time, bestdm_hi, bestdm_lo)

        if plot:
            print(filename, 26.67 + bestdm_hi, 26.67 + bestdm_lo)
            plt.figure()
            plt.plot(dms, intns_hi, 'b.')
            plt.gca().tick_params(color='blue')
            plt.twinx()
            plt.plot(dms, intns_lo, 'r.')
            plt.gca().tick_params(color='red')
            plt.show()
            plt.close()

def cp_cand_to_svds(monthyear, filename):
    '''dedisperse the data in the best dm as determined by the svds/ files,
    and then plot:
     - the data, split and dedispersed at the best dms;
     - the dm vs. svd plot
     
    filename should be the name of the file in the candidates folder, i.e.,
    look something like this:
      25.3929512.npz
    where there are two spaces at the start of the filename.
    ''' 
    
    with np.load(os.path.join('candidates' + monthyear, filename)) as cand_npz:
        try:
            cand_data = cand_npz['arr_0']
        except KeyError:
            cand_data = cand_npz['data']
        



if __name__ == '__main__':
    # this fancy line is here because maybe i'll want to import the functions
    # up there into an ipython thing or something
    import argparse
    parser = argparse.ArgumentParser(description='summarise & plot')
    parser.add_argument('monthyear', help='e.g. 0818')
    parser.add_argument('--plotlims', nargs=2, default=[None, None], type=int,
            help='left and right indices of data to plot')
    parser.add_argument('--basedm', type=float,
            help='add this to dm from candidates folder')
    parser.add_argument('--plot', action='store_true', help='plot if present')
    args = parser.parse_args()
    
    extract_best_dms(args.monthyear, plot=args.plot)
