#!/usr/bin/env python
import argparse

import pipeline as plm

import numpy as np
import numpy.linalg as la
import scipy.optimize as opt
import os
import astropy.units as u
import astropy.time

parser = argparse.ArgumentParser(description='Do the SVD.')
pltparser = parser.add_argument_group(
        'plotting', 'arguments for plotting'
)

parser.add_argument('npz_loc', help='where the data file is')
parser.add_argument('time_bin_sz', type=int, help='# of samples in time bins')
parser.add_argument('freq_bin_sz', type=int, help='# of channels in freq bins')
parser.add_argument('runname', help='the name of this run')

# optional arguments for plotting purposes only
pltparser.add_argument('time_total', type=float, nargs='?', default=25,
        help='the total number of ms time')
pltparser.add_argument('minfreq', type=float, nargs='?', default=400,
        help='the minimum frequency')
pltparser.add_argument('maxfreq', type=float, nargs='?', default=800,
        help='the maximum frequency')
args = parser.parse_args()

plot_save_loc = 'eat-plots/'
data_save_loc = 'eat-data/'


if plot_save_loc:
    import matplotlib.pyplot as plt
    plt.rcParams['figure.figsize'] = (16, 12)

npz = np.load(args.npz_loc, allow_pickle=True)
data = npz['data']
upperdm = float(npz['upperdm'] or 0) * u.pc/u.cm**3
lowerdm = float(npz['lowerdm'] or 0) * u.pc/u.cm**3
freq_index = int(npz['freqind'])
freqval = float(npz['freqval'] or 0) * u.MHz
starttime = astropy.time.Time(npz['starttime'])

# prefer to plot nans, but svd needs zeros
svd_data = plm.remove_rfi(data, data[-100:], fill=0)
data = plm.remove_rfi(data, data[-100:], fill='nan')
# subtract off-pulse stuff
offpulse = np.nanmean(data[:100])
data -= offpulse
svd_data[np.logical_not(np.isnan(data))] -= offpulse
# (we don't want to subtract from removed RFI bands)

# bio
binneddata = plm.bin_data(
        data, args.time_bin_sz, args.freq_bin_sz
)
binnedsvd_data = plm.bin_data(
        svd_data, args.time_bin_sz, args.freq_bin_sz
)

# RFI
binneddata[:, 11] = np.nan
binnedsvd_data[:, 11] = 0

# SVD
if freq_index == -1:
    bdat_u, bdat_s, bdat_vh = la.svd(binnedsvd_data, full_matrices=False)
    if bdat_vh[0, 0] < 0:
        bdat_u *= -1
        bdat_vh *= -1
    bdat_s[1:] = 0
    svd_modeone = (bdat_u * bdat_s @ bdat_vh)
else:
    binnedsvd_top = binnedsvd_data.copy()
    binnedsvd_bot = binnedsvd_data.copy()
    binnedsvd_top[:, freq_index:] = 0
    binnedsvd_bot[:, :freq_index] = 0

    bdat_u_top,bdat_s_top,bdat_vh_top=la.svd(binnedsvd_top, full_matrices=False)
    if bdat_vh_top[0, 0] < 0:
        bdat_u_top *= -1
        bdat_vh_top *= -1

    bdat_u_bot,bdat_s_bot,bdat_vh_bot=la.svd(binnedsvd_bot, full_matrices=False)
    if bdat_vh_bot[0, 0] < 0:
        bdat_u_bot *= -1
        bdat_vh_bot *= -1

    bdat_s_m1_top = bdat_s_top.copy()
    bdat_s_m1_top[1:] = 0  # or some other larger number
    svd_modeone_top = (bdat_u_top * bdat_s_m1_top @ bdat_vh_top)
    
    bdat_s_m1_bot = bdat_s_bot.copy()
    bdat_s_m1_bot[1:] = 0  # or some other larger number
    svd_modeone_bot = (bdat_u_bot * bdat_s_m1_bot @ bdat_vh_bot)

    svd_modeone = svd_modeone_top + svd_modeone_bot

svd_resid = binneddata - svd_modeone

# crop to desired frequencies
model_freq = np.linspace(800, 400, binneddata.shape[1])
freq_allowed = np.less_equal(args.minfreq, model_freq) \
        & np.less_equal(model_freq, args.maxfreq)
binneddata = binneddata[:, freq_allowed]
svd_modeone = svd_modeone[:, freq_allowed]
svd_resid = svd_resid[:, freq_allowed]
svd_resid_mn = np.nanmean(svd_resid)

assert binneddata.shape == svd_modeone.shape == svd_resid.shape

if plot_save_loc:
    plt.rcParams['figure.figsize'] = (24, 8)
    # combined data/model/residual plot
    fig, (ax0, ax1, ax2) = plt.subplots(
            1,
            3,
            sharex='all',
            sharey='all',
            constrained_layout=True
    )
    cb_min = np.nanmin([svd_resid, binneddata, svd_modeone])
    cb_max = np.nanmax([svd_resid, binneddata, svd_modeone])

    im = ax0.imshow(
            binneddata.T,
            extent=[0,
                args.time_total,
                np.min(model_freq[freq_allowed]),
                np.max(model_freq[freq_allowed])],
            vmin=cb_min, vmax=cb_max, aspect='auto'
    )
    ax1.imshow(svd_modeone.T,
            extent=[0,
                args.time_total,
                np.min(model_freq[freq_allowed]),
                np.max(model_freq[freq_allowed])],
            vmin=cb_min, vmax=cb_max, aspect='auto'
    )
    ax2.imshow(svd_resid.T,
            extent=[0,
                args.time_total,
                np.min(model_freq[freq_allowed]),
                np.max(model_freq[freq_allowed])],
            vmin=cb_min, vmax=cb_max, aspect='auto'
    )
    ax0.set_ylabel('frequency (MHz)')
    ax0.set_xlabel('time (ms)')
    ax1.set_xlabel('time (ms)')
    ax2.set_xlabel('time (ms)')
    # plt.tight_layout()
    suptitle = ''
    if freq_index == -1:
        # i.e., single dm
        suptitle = 'Pulse at {}, dm = {}'.format(starttime, upperdm)
    else:
        # i.e., 2 dms
        suptitle = ('Pulse at {}, dm = {} for freq < {f}, '
                'dm = {} for freq >= {f}') \
                .format(starttime, lowerdm, upperdm, f=freqval)
    
    if args.maxfreq < 800 or args.minfreq > 400:
        suptitle += ', closeup'
    
    plt.suptitle(suptitle)
    ax0.set_title('data')
    ax1.set_title('model')
    ax2.set_title('residual (mean: {})'.format(svd_resid_mn))
    fig.colorbar(im, ax=(ax0, ax1, ax2), shrink=0.6)
    ax0.set_ylim((args.minfreq, args.maxfreq))

    plt.savefig(
            os.path.join(plot_save_loc, args.runname)
            + '.png'
    )


if data_save_loc:
    np.savez(os.path.join(data_save_loc, args.runname),
            data=data,
            binneddata=binneddata,
            svd_resid=svd_resid,
#             svd_u=bdat_u,
#             svd_s=bdat_s,
#             svd_vh=bdat_vh
    )
