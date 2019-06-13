import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt
from baseband import vdif
from scintillometry.functions import Square
from scintillometry.dispersion import Dedisperse
from scintillometry.integration import Fold

class WaterfallIntensityPipeline:
    def __init__(self, datafiles, dm, reference_frequency=None,
        samples_per_frame=None, frequencies=None, sideband=None, fft=None):
        self.fh = vdif.open(datafiles)
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

        timedelta = timedelta.to(u.s)
        num_count = int(timedelta * self.fh.info.sample_rate)
        return self.read_count(num_count)

class FoldPipeline:
    def __init__(self, prevline, n_phase, phase, step=None, start=0,
        average=True, samples_per_frame=1):
        self._prevline = prevline
        self.folded = Fold(
            self._prevline.squared, n_phase, phase, step=step, start=start,
            average=average, samples_per_frame=samples_per_frame
        )

        self.outstream = self.folded
