#!/bin/env python3

import sys
import os
import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt
import astropy.time as astime
import astropy.units as u

pulse_t = [0, -1]   # time samples which have pulse
rfi_freq = np.array([
    [110, 130],
    [140, 183],
    [320, 337],
    [410, 450],
    [507, 515],
    [520, 560],
    [580, 604],
    [628, 728],
    [734, 737],
    [755, 770],
    [780, 800],
    [820, 846],
    [866, 873],
    [960, 968]],
    dtype=np.int32
)

def ind2time(index, data):
    return np.interp(index, [0, data.shape[0]], [0, timelen.to(u.ms).value])

try:
    monthyear = sys.argv[1]
except IndexError:
    monthyear = '0818'

startindex = int(sys.argv[2])  # between 0..39 inclusive

plt.ion()


def safe_input(prompt, errmsg, the_type):
    err_state = False
    while not err_state:
        try:
            return the_type(input(prompt))
        except (ValueError, TypeError) as e:
            err_state = True
            print(errmsg)


def draw_line_pair(prompt, ax, horizontal=False, **kwargs):
    '''draw line pair'''
    l_line_t, r_line_t = None, None
    l_line_ln, r_line_ln = None, None
    rect = None
    print(prompt)

    while (l_line_t is None or r_line_t is None
            or l_line_t >= r_line_t):
        l_line_t = safe_input('Give line index', 'no', int)
        if l_line_ln is not None:
            ax.lines.remove(l_line_ln)
        if horizontal:
            l_line_ln = ax.axhline(l_line_t, **kwargs)
        else:
            l_line_ln = ax.axvline(l_line_t, **kwargs)
        plt.draw()

        r_line_t = safe_input('Give line index', 'no', int)
        if r_line_ln is not None:
            ax.lines.remove(r_line_ln)
        if horizontal:
            r_line_ln = ax.axhline(r_line_t, **kwargs)
        else:
            r_line_ln = ax.axvline(r_line_t, **kwargs)
        plt.draw()

        if l_line_t >= r_line_t:
            print('err: first line must be left of/above second line')
    return l_line_t, r_line_t


def safe_yesno(prompt, default=None):
    if default not in ['y', 'n', None]:
        raise ValueError("default must be 'y' or 'n' but is {}".format(default))

    while True:
        answer = input(prompt).lower()
        if answer == 'y':
            return True
        plt.imshow(pltdata)
        plt.show()
        if answer == 'n':
            return False
        input('try again.')

partialsdir = 'partials' + monthyear
candidatesdir = 'candidates' + monthyear
dirs = sorted(os.listdir(partialsdir))

for filename in dirs[startindex::40]:
    if filename.endswith(".npz"): 
        print(filename)
        npz = np.load(os.path.join(partialsdir, filename))
        data = npz['data']
        starttime = npz['time']
        
        pltdata = data.copy()

        for rfi_hi, rfi_lo in (rfi_freq):
            rfi_hi, rfi_lo = int(rfi_hi), int(rfi_lo)
            pltdata[:, rfi_hi:rfi_lo] = np.nan

        intns = np.nanmean(pltdata, 1)
        intns -= np.mean(intns[:3000])
        sig = intns.max()
        if True or sig >= 0.3:
            print("let's do this")
            plt.figure()
            plt.imshow(np.clip(pltdata, -5, 5).T, aspect='auto')
            plt.show()
            plt.figure()
            plt.plot(intns)
            plt.show()
            input()
            plt.close('all')
        else:
            print('snr too small, skipping')
            continue

#         fig, ax = plt.subplots(1)
#         im = ax.imshow(np.clip(pltdata, -2, 5).T, aspect='auto', zorder=-100)
#         fig.colorbar(im)
#         fig.suptitle(str(starttime))
#         # hardcode the rfi frequencies because I can
#         # - 0.5 bc it would be in the middle otherwise
# 
#         plt.show()

#         if not safe_yesno('pulse present? (y/n) '):
#             plt.close()
#             continue
#         
#         # check if this has good pulse
#         if True or pulse_t is not None:
#             line1 = ax.axvline(pulse_t[0])
#             line2 = ax.axvline(pulse_t[1])
#             if not safe_yesno('pulse well captured? (y/n)'):
#                 ax.lines.remove(line1)
#                 ax.lines.remove(line2)
#                 pulse_t = None
#         if pulse_t is None:
#             pulse_t = draw_line_pair("give pulse times", ax, False)
        
    # cp and sav
#         np.savez_compressed(os.path.join(candidatesdir, filename),
#                 data=data,
#                 time=starttime,
#                 pulse=np.array(pulse_t),
#         )
