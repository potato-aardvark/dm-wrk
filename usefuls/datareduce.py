'''Literally just contains a function to reduce data'''

import numpy as np
import matplotlib.pyplot as plt
import pipeline as plm
from baseband import vdif
import astropy.time as astrotime
import astropy.units as u
import matplotlib.pyplot as plt

def datareduce(data, dmhi, dmlo, starttime, timedelta, timebin_sz, freqbin_sz, 
        freqsplit):
    '''Reduce the data. 

    Params
    -----
    data: list of filepaths
    dmhi: dm for the data with frequency > freqsplit
    dmlo: dm for the data with frequency <= freqsplit, or None if no split.
    starttime: where to start
    timedelta: how long a time interval to read for
    timebin_sz, freqbin_sz: shape of returned data guaranteed to be divisible
        by these numbers, e.g. for future binning. this function doesn't bin
        the data itself though. 
    freqsplit: frequency to split, or None if no split.

    Returns
    ------
    the absolute start time
    the data, duh (no rfi removed yet)
    the absolute end time
    '''
    plhi = plm.WaterfallIntensityPipeline(
            data, dmhi, reference_frequency=800*u.MHz,
            samples_per_frame=2**18,
            frequencies=np.linspace(800, 400, 1024)*u.MHz, sideband=1
    )
    plhi.outstream.seek(starttime)
    absstart = plhi.outstream.tell('time')
    rawdatahi = plhi.read_time_div(timedelta, timebin_sz)
    absend = plhi.outstream.tell('time')
    
    if freqsplit is None:
        pllo = plhi
        rawdata = rawdatahi
    else:
        pllo = plm.WaterfallIntensityPipeline(
                data, dmlo, reference_frequency=800*u.MHz,
                samples_per_frame=2**18,
                frequencies=np.linspace(800, 400, 1024)*u.MHz, sideband=1
        )
        pllo.outstream.seek(starttime)
        rawdatalo = pllo.read_time_div(timedelta, timebin_sz)
        
        rawdata = np.concatenate(
                (rawdatahi[:, :freqsplit], rawdatalo[:, freqsplit:]),
                axis=1
        )
    
    return absstart, rawdata, absend
