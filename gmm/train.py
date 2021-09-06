# train_models.py
import os
from _pickle import dump
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture
from extract import speakerfeatures, gfcc
import warnings

warnings.filterwarnings("ignore")


class Train:
    def __init__(self, source="development_set\\", dest="speaker_models\\",
                 train_file="development_set_enroll.txt", countFiles=5):
        # path to training data
        self.source = source

        # path where training speakers will be saved
        self.dest = dest
        self.finalDest = ['combined\\', 'gfcc\\', 'mfcc\\']

        self.train_file = train_file
        self.countFiles = countFiles

        self.features = np.asarray(())
        self.fmfcc = np.asarray(())
        self.fgfcc = np.asarray(())

        self._gfcc = gfcc.GFCC()

    def train(self):
        print("Train start")
        file_paths = open(self.train_file, 'r')

        count = 1

        # Extracting features for each speaker (5 files per speakers)

        for path in file_paths:
            if path != "\n":
                path = path.strip()
                print(path)

                # read the audio
                sr, audio = read(self.source + path)

                # extract 40 dimensional MFCC & delta MFCC features
                # vector = speakerfeatures.extract_features(audio, sr)
                vector1 = speakerfeatures.extract_features(audio, sr)
                vector2 = self._gfcc.extractGFCC(audio, sr)
                vector1 = vector1[:len(vector2)]
                # vector = _gfcc.extractMFCC(audio, sr)
                vector = np.hstack((vector1, vector2))

                if self.features.size == 0:
                    self.features = vector
                    self.fmfcc = vector1
                    self.fgfcc = vector2
                else:
                    self.features = np.vstack((self.features, vector))
                    self.fmfcc = np.vstack((self.fmfcc, vector1))
                    self.fgfcc = np.vstack((self.fgfcc, vector2))

                # when features of 3 files of speaker are concatenated, then do model training
                if count == self.countFiles:
                    print("Done with mfcc now train")
                    features = [self.features, self.fgfcc, self.fmfcc]
                    for i in range(len(self.finalDest)):
                        gmm = GaussianMixture(n_components=16, covariance_type='diag', n_init=3)
                        gmm.fit(features[i])

                        # dumping the trained gaussian model
                        picklefile = path.split("/")[0] + ".gmm"
                        filename = str(self.dest) + str(self.finalDest[i]) + str(picklefile)
                        os.makedirs(os.path.dirname(filename), exist_ok=True)
                        dump(gmm, open(filename, 'wb'))
                        print('+ modeling completed for speaker:', picklefile, " with data point = ",
                              features[i].shape)
                    self.features = np.asarray(())
                    self.fmfcc = np.asarray(())
                    self.fgfcc = np.asarray(())
                    count = 0
                count = count + 1

#
# if __name__ == '__main__':
#     tr = Train()
#     tr.train()
