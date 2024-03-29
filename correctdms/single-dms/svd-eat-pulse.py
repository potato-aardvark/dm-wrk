import argparse

import pipeline as plm

import numpy as np
import numpy.linalg as la
import scipy.optimize as opt
import os

parser = argparse.ArgumentParser(description='Do the SVD.')
pltparser = parser.add_argument_group(
        'plotting', 'arguments for plotting'
)

parser.add_argument('npz_loc', help='where the data file is')
parser.add_argument('time_bin_sz', type=int, help='# of samples in time bins')
parser.add_argument('freq_bin_sz', type=int, help='# of channels in freq bins')
parser.add_argument('runname', help='the name of this run')
pltparser.add_argument('plot_save_loc', nargs='?', help='save the plot here')
parser.add_argument('data_save_loc', nargs='?', help='save the residual here')

# optional arguments for plotting purposes only
pltparser.add_argument('time_total', type=float, nargs='?', default=25,
        help='the total number of ms time')
pltparser.add_argument('minfreq', type=float, nargs='?', default=400,
        help='the minimum frequency')
pltparser.add_argument('maxfreq', type=float, nargs='?', default=800,
        help='the maximum frequency')
pltparser.add_argument('suptitle', nargs='?')

args = parser.parse_args()

if args.plot_save_loc:
    import matplotlib.pyplot as plt
    plt.rcParams['figure.figsize'] = (16, 12)

data = np.load(args.npz_loc)
# I don't remember how the data was saved
try:
    data = data['arr_0']
except KeyError:
    try:
        data = data['data']
    except KeyError:
        data = data['fulldata']

# prefer to plot nans, but svd needs zeros
svd_data = plm.remove_rfi(data, data[-100:], fill=0)
data = plm.remove_rfi(data, data[-100:], fill='nan')
binneddata = plm.bin_data(
        data, args.time_bin_sz, args.freq_bin_sz
)
binnedsvd_data = plm.bin_data(
        svd_data, args.time_bin_sz, args.freq_bin_sz
)

# RFI
binneddata[:, 11] = np.nan
binnedsvd_data[:, 11] = 0

bdat_u, bdat_s, bdat_vh = la.svd(binnedsvd_data.T, full_matrices=False)
if bdat_vh[0, 0] < 0:
    bdat_u *= -1
    bdat_vh *= -1

bdat_s_m1 = bdat_s.copy()
bdat_s_m1[1:] = 0  # or some other larger number
svd_modeone = (bdat_u * bdat_s_m1 @ bdat_vh).T

svd_resid = binneddata - svd_modeone

if args.plot_save_loc:
    # pulse as waterfall
    plt.imshow(binneddata.transpose(),
            aspect='auto',
            extent=[0, args.time_total, args.minfreq, args.maxfreq]
    )
    plt.suptitle(args.suptitle)
    plt.xlabel('time (ms)')
    plt.ylabel('frequency (MHz)')
    plt.savefig(
            os.path.join(args.plot_save_loc, args.runname) + 'pulse.png'
    )
    
    # residuals as waterfall
    plt.imshow(svd_resid.transpose(),
            aspect='auto',
            extent=[0, args.time_total, args.minfreq, args.maxfreq]
    )
    plt.suptitle(args.suptitle)
    plt.xlabel('time (ms)')
    plt.ylabel('frequency (MHz)')
    plt.savefig(os.path.join(args.plot_save_loc, args.runname) + '_resids.png')
    
    # svd mode 1 as waterfall
    plt.imshow(svd_modeone.transpose(),
            aspect='auto',
            extent=[0, args.time_total, args.minfreq, args.maxfreq]
    )
    plt.suptitle(args.suptitle)
    plt.xlabel('time (ms)')
    plt.ylabel('frequency (MHz)')
    plt.savefig(os.path.join(args.plot_save_loc, args.runname) + '_svdmd1.png')
    
    plt.rcParams['figure.figsize'] = (12, 80)
    
    # pulse as lines
    resid_scale = -2
    plt.figure()
    for freq_index in range(binneddata.shape[1]):
        plt.plot(
                np.linspace(0, args.time_total, binneddata.shape[0]),
                binneddata[:, freq_index] + resid_scale * freq_index
        )
        if not np.any(np.isnan(binneddata[:, freq_index])):
            plt.axhline(resid_scale * freq_index, color='black', lw=0.5)
    plt.xlabel('time (ms)')
    plt.ylabel('frequency')
    plt.savefig(
            os.path.join(args.plot_save_loc, args.runname) + '_pulseprf.png'
    )
    
    # residual as lines
    plt.figure()
    for freq_index in range(svd_resid.shape[1]):
        plt.plot(
                np.linspace(0, args.time_total, binneddata.shape[0]),
                svd_resid[:, freq_index] + resid_scale * freq_index
        )
        if not np.any(np.isnan(svd_resid[:, freq_index])):
            plt.axhline(resid_scale * freq_index, color='black', lw=0.5)
    plt.xlabel('time (ms)')
    plt.ylabel('frequency')
    plt.savefig(
            os.path.join(args.plot_save_loc, args.runname) + '_residsprf.png'
    )
    
    # mode one as lines
    plt.figure()
    for freq_index in range(svd_modeone.shape[1]):
        plt.plot(
                np.linspace(0, args.time_total, binneddata.shape[0]),
                svd_modeone[:, freq_index] + resid_scale * freq_index
        )
        if not np.any(np.isnan(svd_modeone[:, freq_index])):
            plt.axhline(resid_scale * freq_index, color='black', lw=0.5)
    plt.xlabel('time (ms)')
    plt.ylabel('frequency')
    plt.savefig(
            os.path.join(args.plot_save_loc, args.runname) + '_modeoneprf.png'
    )

if args.data_save_loc:
    np.savez(os.path.join(args.data_save_loc, args.runname),
            data=data,
            binneddata=binneddata,
            svd_resid=svd_resid,
            svd_u=bdat_u,
            svd_s=bdat_s,
            svd_vh=bdat_vh
    )
