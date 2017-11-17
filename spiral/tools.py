"""
Spiral Python functions.
"""
import numpy as np


def erb2hz(erb):
    """
    Convert equivalent rectangular bandwidth (ERB) to Hertz.
    """
    tmp = np.exp((erb - 43) / 11.17)
    hz = (0.312 - 14.675 * tmp) / (tmp - 1.0) * 1000
    if hz <= 0:
        hz = 1
    return hz


def hz2erb(hz):
    """
    Convert Hertz to equivalent rectangular bandwidth (ERB).
    """
    khz = hz / 1000
    erb = 11.17 * np.log((khz + 0.312) / (khz + 14.675)) + 43
    if erb <= 0:
        erb = 0.1


def generate_bands(lo, hi, n_bands):
    """
    Generates the upper and lower band cut-offs of a series of 'nbands' contiguous frequency bands,
    linearly spaced on an ERB scale, between the frequencies 'lo' and 'hi' (in Hz)
    """
    density = n_bands / (hz2erb(hi) - hz2erb(lo))
    bands = []
    for i in range(1, n_bands + 1):
        bands.append([erb2hz(hz2erb(lo) + (i - 1) / density), erb2hz(hz2erb(lo) + i / density)])
    return bands


def generate_cfs(lo, hi, n_bands):
    """
    Generates a series of 'bands' frequencies in Hz, linearely distributed
    on an ERB scale between the frequencies 'lo' and 'hi' (in Hz).
    These would are the centre frequencies (on an ERB scale) of the bands
    specifications made by 'generate_bands' with the same arguments
    """
    density = nbands / (hz2erb(hi) - hz2erb(lo))
    bands = []
    for i in range(1, n_bands + 1):
        bands.append(erb2hz(hz2erb(lo) + (i - 0.5) / density))
    return bands


def make_fir_filter(lo, hi, sf):
    """
    Makes a 512-point band-pss FIR filter using the host-windowing method
    (Abed & Cain, 1978, The Radio and Electronic Engineer, 46, 293-300).
    The filter is zero-phase (i.e. symmetrical).
    The function loads in a "host" file, 's1023.ir', which needs to be in the current folder.

    Arguments:
        - lo (): Lower limit of the band
        - hi (): Higher limit of the band
        - sf (): Sampling frequency ()

    Returns:
        - out (np.array)
    """
    nspecs = 1000
    nyquist = sf / 2
    host_file = os.path.join(os.path.dirname(__file__), 's1023.ir')
    host = np.fromfile(host_file, dtype='float32')
    specs = np.zeros(1, int(lo / nyquist * nspecs))
    np.ones(1, int(hi / nyquist * nspecs - len(specs)))
    np.zeros(1, nspecs - len(specs))
    band_lo = 0
    win = np.zeros(1, 256)
    for i in range(1000):
        band_hi = np.pi * (i + 1) / nspecs
        for j in range(256):
            b = (j + 1) - 256.5
            win[j] = win[j] + specs[i] * (np.sin(b * band_hi) - np.sin(b * band_lo))
        band_lo = band_hi
    out = np.concatanate((np.transpose(host) * win, np.fliplr(np.transpose(host) * win)))
    return out
