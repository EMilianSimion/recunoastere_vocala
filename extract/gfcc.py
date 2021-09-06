from spafe.features.gfcc import gfcc
from spafe.features.mfcc import mfcc
import python_speech_features as mfccc
import scipy.io.wavfile
from spafe.utils import vis
import numpy as np


class GFCC:
    def __init__(self, num_ceps=15, nfilts=55):
        self.num_ceps = num_ceps
        self.low_freq = 0
        self.high_freq = None
        self.nfilts = nfilts
        self.nfft = 512
        self.dct_type = 2
        self.use_energy = False
        self.lifter = 22
        self.normalize = False

    def extractGFCC(self, sig, fs):
        # fs, sig = scipy.io.wavfile.read(path)

        gfccs = gfcc(sig=sig,
                     fs=fs,
                     num_ceps=self.num_ceps,
                     nfilts=self.nfilts,
                     nfft=self.nfft,
                     low_freq=self.low_freq,
                     high_freq=self.high_freq,
                     lifter=self.lifter,
                     normalize=self.normalize,
                     )
        # mfccs = mfcc(sig=sig, fs=fs, num_ceps=39, nfilts=78)
        # mfccs2 = extract_features(sig, fs)
        # vis.spectogram(sig, fs)
        # vis.visualize_features(gfccs, 'GFCC Index', 'Frame Index')
        #
        # vis.visualize_features(mfccs, 'MFCC Index', 'Frame Index')
        # vis.visualize_features(mfccs2, 'MFCC2 Index', 'Frame Index')
        # print(mfccs)
        return gfccs

    def extractMFCC(self, sig, fs):
        return mfcc(sig=sig, fs=fs, num_ceps=self.num_ceps, nfilts=self.nfilts)

    def extractGFCC13_delta_deltaDelta(self, sig, fs):
        gfccs = gfcc(sig=sig,
                     fs=fs,
                     num_ceps=13,
                     nfilts=self.nfilts,
                     nfft=self.nfft,
                     low_freq=self.low_freq,
                     high_freq=self.high_freq,
                     lifter=self.lifter,
                     normalize=self.normalize,
                     )
        delta = mfccc.delta(gfccs, 2)
        delta_delta = mfccc.delta(delta, 2)
        all_feat = np.hstack((gfccs, delta, delta_delta))
        return all_feat
