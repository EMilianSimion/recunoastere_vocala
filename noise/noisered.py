#!/usr/bin python3
# -*- coding: UTF-8 -*-
# File: noisered.py
# Date: Fri Dec 27 04:23:28 2013 +0800

from scipy.io import wavfile
import os
from random import Random
from silence.silence import remove_silence

NOISE_WAV = "model/noise.wav"
NOISE_MODEL = "model/noise.ppyrof"
THRES = 0.21
r = Random()


class NoiseReduction(object):

    def init_noise(self, fs, signal):
        wavfile.write(NOISE_WAV, fs, signal)
        os.system("sox {0} -n noiseprof {1}".format(NOISE_WAV, NOISE_MODEL))

    def filter(self, fs, signal):
        rand = r.randint(1, 100000)
        fname = "model/tmp{0}.wav".format(rand)
        # signal = monophonic(signal)
        wavfile.write(fname, fs, signal)
        fname_clean = "model/tmp{0}-clean.wav".format(rand)
        wavfile.write(fname_clean, fs, signal)
        os.system("sox {0} {1} noisered {2} {3}".format(fname, fname_clean,
                                                        NOISE_MODEL, THRES))
        fs, signal = wavfile.read(fname_clean)
        # signal = monophonic(signal)

        os.remove(fname)
        os.remove(fname_clean)
        return signal


if __name__ == "__main__":
    fs, bg = wavfile.read("noise.wav")
    nr = NoiseReduction()
    nr.init_noise(fs, bg)

    fs, sig = wavfile.read("inputCuZgomot.wav")
    vaded = nr.filter(fs, sig)
    wavfile.write('model/vaded.wav', fs, vaded)

    removed = remove_silence(fs, vaded)
    wavfile.write("model/removed.wav", fs, removed)
