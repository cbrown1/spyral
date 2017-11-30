import random
import numpy as np
from tools import make_fir_filter, generate_cfs


def spiral(ipwave, n_electrodes, n_carriers, spread, sf):
    """
    Spiral.

    Arguments:
        - ipwave (list): Input wave
        - n_electrodes (int): Number of electrodes
        - n_carriers (int): Number of tone carriers
        - spread (): Current spread [in -dB/Oct (negative!!)]
        - sf (): Sampling frequency (Hz)

    Returns:

    Example:
        out = spiral(audioread('_wavefilename_'), 20, 80, -8, 44100)

    Notes:
        Typical current spread (Oxenham & Kreft 2014 + Nelson etal 2011) = -8 dB/octave.
    """
    lo = 120                        # lower bound of analysis filters (Hz) (Friesen et al.,2001)
    hi = 8658                        # upper bound of analysis filters (Hz)
    carrier_lo = 20                # lower bound of carriers (Hz)
    carrier_hi = 20000             # higher bound of carriers (Hz)
    lp_filter = make_fir_filter(0, 50, sf)                                 # generate low-pass filter,  default 50Hz
    cfs = generate_cfs(lo, hi, n_electrodes)                               # electrodes' centre frequencies
    carrier_fs = generate_cfs(carrier_lo, carrier_hi, n_carriers)          # tone carrier frequencies
    t = np.arange(0, (len(ipwave) - 1) / sf, 1 / sf)
    t_carrier = np.zeros((len(ipwave), n_carriers))
    ip_bands = generate_bands(lo, hi, n_electrodes)                        # lower/upper limits of each analysis band
    ip_bank = np.zeros((n_electrodes, 512))
    envelope = np.zeros((len(ipwave), n_electrodes))                       # envelopes extracted per electrode
    mixed_envelope = np.zeros((len(ipwave), n_carriers))                   # mixed envelopes to modulate carriers
    for j in range(n_electrodes):
        ip_band[j, :] = make_fir_filter(ip_bands[j, 0], ip_bands[j, 1], sf)   # analysis filterbank
        speechband = np.convolve(ipwave[:, 1], ip_band[j, :], mode='same')    # speech band filtering
        speechband = speechband *   # speechband>0 -> what is this???         # envelope extraction by half-wave rectification
        envelope[:, j] = np.convolve(speechband, lp_filter, mode='same')      # low-pass filter envelope
    for i in range(n_carriers):
        for j in range(n_electrodes):
            # weights applied to power envelopes
            mixed_envelope[:, i] += 10 ** (spread / 10 ** abs(np.log2(cfs[j] / carrier_fs[i]))) * envelope[:, j] ** 2
    mixed_envelope = mixed_envelope ** 0.5                        # sqrt to get back to amplitudes
    out = np.zeros((len(ipwave), 1))
    for i in range(n_carriers):
        # randomise tone phases (particularly important for binaural!)
        t_carrier[:, i] = np.sin(2 * np.pi * (carrier_fs[i] * t + random.random()))
        out += mixed_envelope[:, i] * t_carrier[:, i]             # modulate carriers with mixed envelopes
    out = out * 0.05 * np.sqrt(len(out) / np.linalg.norm(out))    # rms scaled, to avoid saturation
    return out
