
import spyral
import pysndfile


(standard,fs,enc) = pysndfile.sndio.read("test/test_matlab.wav")
(sig,fs,enc) = pysndfile.sndio.read("test/test_clean.wav")

out = spyral.spyral(sig, fs, 20, 80, -8)
pysndfile.sndio.write('test/test_out.wav',out,fs,format='wav')
