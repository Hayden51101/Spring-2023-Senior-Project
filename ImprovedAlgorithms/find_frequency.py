import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from numpy import arange
from scipy.signal import find_peaks



def get_frequency(x, sf, notes_array, DEBUG = False):
    """
    Derive frequency spectrum of a signal from time domain
    :param x: signal in the time domain
    :param sf: sampling frequency
    :returns: frequencies and their content distribution
    """
    x = x - np.average(x)  # zero-centering

    n = len(x)
    k = arange(n)
    tarr = n / float(sf)
    frqarr = k / float(tarr)  # two sides frequency range

    frqarr = frqarr[range(n // 2)]  # one side frequency range

    x = fft(x) / n  # fft computing and normalization
    x = x[range(n // 2)]

    peak_indicies, props = find_peaks(x, height=0.015)
    max_mag = 0
    note_freq = 0
    for i, peak in enumerate(peak_indicies):
        freq = frqarr[peak]
        magnitude = props["peak_heights"][i]
        if(max_mag < magnitude):
            max_mag = magnitude
            note_freq = freq

    note = "None"
    for fr in notes_array:
        if(abs(note_freq - notes_array[fr]) < 5):
            note = str(fr)

    if(DEBUG):
        plt.plot(frqarr, abs(x))
        plt.xlabel('Freq (Hz)')
        plt.ylabel('|X(freq)|')
        plt.tight_layout()
        plt.title(note)
        plt.show()

    return note