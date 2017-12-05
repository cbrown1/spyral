# -*- coding: utf-8 -*-

import spyral
import pysndfile


(standard,fs,enc) = pysndfile.sndio.read("test_matlab.wav")
(sig,fs,enc) = pysndfile.sndio.read("test_clean.wav")

out = spyral.spyral(sig, fs, 20, 80, -8)
pysndfile.sndio.write('test_out.wav',out,fs,format='wav')
