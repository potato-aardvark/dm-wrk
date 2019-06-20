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

data = np.load(args.npz_loc)
# I don't remember how the data was saved
try:
    data = data['arr_0']
except KeyError:
    try:
        data = data['data']
    except KeyError:
        data = data['fulldata']
svd_data = plm.remove_rfi(data, fill=0)  # svd needs data with 0s, not nans
data = plm.remove_rfi(data, fill='nan')  # plotting should use data with nans
binneddata = plm.bin_data(data, args.time_bin_sz, args.freq_bin_sz)
binnedsvd_data = plm.bin_data(svd_data, args.time_bin_sz, args.freq_bin_sz)
bdat_u, bdat_s, bdat_vh = la.svd(binnedsvd_data.T)
if bdat_vh[0, 0] < 0:
    bdat_u *= -1
    bdat_vh *= -1

modeone = bdat_vh[0, :] * bdat_s[0]

fit_modeone_to_data = lambda x, scale, offset: modeone[x] * scale + offset
indices = np.arange(binneddata.shape[0])

svd_resid = np.empty_like(binneddata)

# maybe there's a faster way to do this. idk, but this way is right and 
# has only <1024 iterations anyways
for i in range(binneddata.shape[1]):
    if not np.any(np.isnan(binneddata[:, i]) | np.isinf(binneddata[:, i])):
        (best_scale, best_offset), _ = opt.curve_fit(
                fit_modeone_to_data,
                indices,
                binneddata[:, i],
                p0=(0.01, 1)
        )
        svd_resid[:, i] = (binneddata[:, i]
                - fit_modeone_to_data(indices, best_scale, best_offset))
#         plt.plot(binneddata[:, i])
#         plt.plot(fit_modeone_to_data(indices, best_scale, best_offset))
#         plt.plot(svd_resid[:, i])
#         plt.show()
    else:
        svd_resid[:, i] = np.nan
if args.plot_save_loc:
    plt.figure()
    plt.imshow(binneddata.transpose(),
            aspect='auto',
            extent=[0, args.time_total, args.minfreq, args.maxfreq]
    )
    plt.colorbar()
    plt.suptitle(args.suptitle)
    plt.xlabel('time (s)')
    plt.ylabel('frequency (MHz)')
    plt.savefig(os.path.join(args.plot_save_loc, args.runname)+'_waterfall.png')
    
    plt.figure()
    plt.imshow(svd_resid.transpose(),
            aspect='auto',
            extent=[0, args.time_total, args.minfreq, args.maxfreq]
    )
    plt.colorbar()
    plt.suptitle(args.suptitle + ', residuals')
    plt.xlabel('time (s)')
    plt.ylabel('frequency (MHz)')
    plt.savefig(os.path.join(args.plot_save_loc, args.runname) + '_resids.png')
    
    plt.figure()
    plt.plot(
            np.linspace(0, args.time_total, indices.size),
            fit_modeone_to_data(indices, 1, 0)
    )
    plt.suptitle(args.suptitle + ', first mode of svd')
    plt.xlabel('time (s)')
    plt.ylabel('svd, first mode')
    plt.savefig(os.path.join(args.plot_save_loc, args.runname) + '_svdmd1.png')

if args.data_save_loc:
    np.savez(os.path.join(args.data_save_loc, args.runname),
            data=data,
            binneddata=binneddata,
            svd_resid=svd_resid
    )
