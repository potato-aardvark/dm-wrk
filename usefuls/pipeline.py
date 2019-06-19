import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from baseband import vdif
from scintillometry.functions import Square
from scintillometry.dispersion import Dedisperse
from scintillometry.integration import Fold

class WaterfallIntensityPipeline:
    def __init__(self, source_strm, dm, reference_frequency=None,
        samples_per_frame=None, frequencies=None, sideband=None, fft=None):
        if isinstance(source_strm, list):
            self.fh = vdif.open(source_strm)
        else:
            self.fh = source_strm
        self.dedispersed = Dedisperse(self.fh, dm,
            reference_frequency=reference_frequency,
            samples_per_frame=samples_per_frame, 
            frequency=frequencies, 
            sideband=sideband, FFT=fft)
        self.squared = Square(self.dedispersed)

        self.outstream = self.squared

    def read_raw(self, count=None):
        """Read from the stream, without summing over the polarisation axis."""
        return self.squared.read(count)

    def read_count(self, count=None):
        """Read and return from the stream."""
        return self.read_raw(count).sum(1)

    def read_time(self, timedelta):
        """
        Read a number of samples corresponding to a particular time
        interval. Rounds down.
        """
        num_samples = int((self.outstream.sample_rate * timedelta).to(u.one))
        return self.read_count(num_samples)

    def read_time_div(self, timedelta, num):
        """Read a number of samples corresponding to a particular time
        interval, making sure that the nmber of samples read is divisible
        by num. 

        Returns (data, num_samples_read, time_interval_read). 
        """
        num_samples = int((self.outstream.sample_rate * timedelta).to(u.one))
        return self.read_count(num_samples - (num_samples % num))

class FoldPipeline:
    def __init__(self, prevline, n_phase, phase, step=None, start=0,
        average=True, samples_per_frame=1):
        self._prevline = prevline
        self.folded = Fold(
            self._prevline.squared, n_phase, phase, step=step, start=start,
            average=average, samples_per_frame=samples_per_frame
        )

        self.outstream = self.folded

def remove_rfi(data, emptysample=None, fill=np.nan):
    """Return data with RFI frequencies removed, replacing them with nans
    or zeroes.
    
    If fill is 'nan' or nan, set to nans. If fill is 0, '0', or 'zero', set
    to zeroes.
    """
    if emptysample is None:
        emptysample = data
    if fill in ['nan', np.nan]:
        fill = np.nan
    elif fill in [0, '0', 'zero']:
        fill = 0
    # i guess i could add a valueerror here if i wanted to

    emptysample = np.nansum(emptysample, 0)  # over time
    baseline = np.median(emptysample)
    peak = np.max(emptysample)
    threshold = 0.8 * baseline + 0.2 * peak
    return np.where(emptysample > threshold, fill, data) 

def bin_data(data, time_bin_sz, freq_bin_sz):
    """Bin the data to the desired bin sizes."""

    return data.reshape(
            data.shape[0] // time_bin_sz,
            time_bin_sz,
            *(data.shape[1:-1]),  # also include other axes in the middle!
            data.shape[-1] // freq_bin_sz,
            freq_bin_sz).mean((1, 3))
