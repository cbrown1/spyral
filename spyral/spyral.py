# -*- coding: utf-8 -*-

import numpy as np
from .tools import generate_cfs, generate_bands, make_fir_filter

def spyral(input, fs, electrodes, n_carriers, spread, **kwargs):
    """Spyral: vocoder that utilizes multiple sinusoidal carriers to simulate current spread

        Parameters
        ----------
        input : array
            The input signal
        fs : scalar
            The sampling frequency
        electrodes : scalar or array
            If type==scalar, it represents the number of electrodes and each electrode will be 
            linearely distributed on an ERB scale between analysis_lo and analysis_hi.

            If type==array, each element represents the corresponding best frequency of each 
            electrode, and the number of electrodes is inferred from its length. Among other 
            things, this can be used to simulate warping, in which the cfs of analysis bands 
            may be different than the electrode positions.

        n_carriers : scalar
            Number of tone carriers
        spread : scalar
            Current spread [in -dB/Oct (negative!!)]. 
            Typical (Oxenham & Kreft 2014 + Nelson etal 2011) = -8 dB/octave.

        Kwargs
        ------
        analysis_lo : scalar 
            Lower bound of analysis filters, in Hz [default = 120 (Friesen et al.,2001)]
        analysis_hi : scalar 
            Upper bound of analysis filters, in Hz [default = 8658]
        carrier_lo : scalar 
            Lower bound of carriers, in Hz [default = 20]
        carrier_hi : scalar 
            Higher bound of carriers, in Hz [default = 20,000]
        analysis_cutoffs : array
            An array of cutoff frequencies to use. analysis_hi and lo are ignored. Must
            be one more than the number of electrodes.
        filt_env : scalar 
            Envelope filter cutoff, in Hz [default = 50]

        Returns
        -------
        out : array
            Vocoded input

        Example
        -------
        >>> out = spyral(signal, 44100, 20, 80, -8)

    """
    analysis_lo = kwargs.get('analysis_lo', 120) 
    analysis_hi = kwargs.get('analysis_hi', 8658)
    analysis_cutoffs = kwargs.get('analysis_cutoffs', None)
    carrier_lo = kwargs.get('carrier_lo', 20) 
    carrier_hi = kwargs.get('carrier_hi', 20000) 
    filt_env = kwargs.get('filt_env', 50)
    in_phase = kwargs.get('in_phase', False)
    fs = np.float32(fs)

    rms_in = np.sqrt(np.mean(np.power(input, 2)))
    lp_filter = make_fir_filter(0, filt_env, fs)       # generate low-pass filter,  default 50Hz
    if np.isscalar(electrodes):
        cfs = np.array(generate_cfs(analysis_lo, analysis_hi, electrodes))     # electrodes' centre frequencies
    else:
        cfs = np.array(electrodes) # If not scalar, assume a list of cfs
    carrier_fs = generate_cfs(carrier_lo, carrier_hi, n_carriers) # tone carrier frequencies
    t = np.arange(0, len(input) / fs, 1 / fs)
    t_carrier = np.zeros((n_carriers, len(input)))
    if analysis_cutoffs is None:
        ip_bands = analysis_cutoffs # User specified cutoffs
    else:
        ip_bands = np.array(generate_bands(analysis_lo, analysis_hi, cfs.size)) # lower/upper limits of each analysis band
    ip_bank = np.zeros((cfs.size, 512))
    envelope = np.zeros((cfs.size, len(input)))       # envelopes extracted per electrode
    mixed_envelope = np.zeros((n_carriers, len(input)))   # mixed envelopes to modulate carriers

    # Envelope extraction
    for j in range(cfs.size):
        ip_bank[j, :] = make_fir_filter(ip_bands[j, 0], ip_bands[j, 1], fs)   # analysis filterbank
        speechband = np.convolve(input, ip_bank[j, :], mode='same')
        envelope[j, :] = np.convolve(np.maximum(speechband,0), lp_filter, mode='same') # low-pass filter envelope

    # weights applied to power envelopes
    for i in range(n_carriers):
        for j in range(cfs.size):
            mixed_envelope[i, :] += 10. ** (spread / 10. * np.abs(np.log2(cfs[j] / carrier_fs[i]))) * envelope[j, :] ** 2.

    # sqrt to get back to amplitudes
    mixed_envelope = np.sqrt(mixed_envelope)
    out = np.zeros(len(input))

    if in_phase:
        phases = np.zeros(n_carriers)
    else:
        phases = np.random.rand(n_carriers) * 2 * np.pi

    # Generate carriers, modulate; randomise tone phases (particularly important for binaural!)
    for i in range(n_carriers):
#        t_carrier[i, :] = np.sin(2 * np.pi * (carrier_fs[i] * t + np.random.rand()))
        t_carrier[i, :] = np.sin(phases[i] + (2. * np.pi * carrier_fs[i] * t))

        out += mixed_envelope[i, :] * t_carrier[i, :]             # modulate carriers with mixed envelopes
#    out = out * 0.05 * np.sqrt(len(out)) / np.linalg.norm(out)    # rms scaled, to avoid saturation
    return out * (np.sqrt(np.mean(np.square(input))) / np.sqrt(np.mean(np.square(out))))
