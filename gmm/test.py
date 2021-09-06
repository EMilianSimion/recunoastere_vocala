import os
from _pickle import load
import numpy as np
from scipy.io.wavfile import read
from extract import speakerfeatures, gfcc
import warnings

import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
import time


class Test:
    def __init__(self, source="development_set\\", modelPath="speaker_models\\",
                 testFile="development_set_test.txt"):
        # path to training data
        self.source = source

        self.modelpath = modelPath
        self.modelpathCategory = ['combined\\', 'gfcc\\', 'mfcc\\']

        self.test_file = testFile

        self.modelsCombined = None
        self.modelsGFCC = None
        self.modelsMFCC = None

        self.speakers = None
        self.winner = ""
        self.score = 0
        self.loadGaussianModels()

        self._gfcc = gfcc.GFCC()

    def loadGaussianModels(self):
        gmm_files_modelsCombined = [os.path.join(str(self.modelpath) + str(self.modelpathCategory[0]), fname) for fname
                                    in
                                    os.listdir(str(self.modelpath) + str(self.modelpathCategory[0])) if
                                    fname.endswith('.gmm')]
        gmm_files_modelsGFCC = [os.path.join(str(self.modelpath) + str(self.modelpathCategory[1]), fname) for fname
                                in
                                os.listdir(str(self.modelpath) + str(self.modelpathCategory[1])) if
                                fname.endswith('.gmm')]
        gmm_files_modelsMFCC = [os.path.join(str(self.modelpath) + str(self.modelpathCategory[2]), fname) for fname
                                in
                                os.listdir(str(self.modelpath) + str(self.modelpathCategory[2])) if
                                fname.endswith('.gmm')]
        # Load the Gaussian Models
        self.modelsCombined = [load(open(fname, 'rb')) for fname in gmm_files_modelsCombined]
        self.modelsGFCC = [load(open(fname, 'rb')) for fname in gmm_files_modelsGFCC]
        self.modelsMFCC = [load(open(fname, 'rb')) for fname in gmm_files_modelsMFCC]

        self.speakers = [fname.split("\\")[-1].split(".gmm")[0] for fname
                         in gmm_files_modelsCombined]

        print(self.speakers)

    def test(self):
        file_paths = open(self.test_file, 'r')

        # Read the test directory and get the list of test audio files
        for path in file_paths:
            if path != "\n":
                path = path.strip()
                print(path)
                sr, audio = read(self.source + path)

                vector1 = speakerfeatures.extract_features(audio, sr)
                vector2 = self._gfcc.extractGFCC(audio, sr)
                vector1 = vector1[:len(vector2)]
                vector3 = np.hstack((vector1, vector2))
                vector = [vector3, vector2, vector1]
                indexVector = 0
                log_likelihood = np.zeros(len(self.modelsCombined))

                for models in (self.modelsCombined, self.modelsGFCC, self.modelsMFCC):
                    for i in range(len(models)):
                        gmm = models[i]  # checking with each model one by one
                        scores = np.array(gmm.score(vector[indexVector]))
                        log_likelihood[i] = scores.sum()
                        # print(f'-> {gmm.score(vector)} {self.speakers[i]}')
                        # print(f'->{gmm.predict(vector)} {self.speakers[i]}')
                        # plt.scatter(vector[:, 0], vector[:, 1], c=gmm.predict(vector), s=40, cmap=('viridis'))
                        # print((np.exp(gmm.score_samples(vector))))
                    winner = np.argmax(log_likelihood)
                    # log_likelihood = np.array([log_likelihood[i] for i in range(len(log_likelihood)) if i != winner])
                    # second = np.argmax(log_likelihood)
                    print("\tdetected as - ", self.speakers[winner])
                    # print("\t\t second identified- ", self.speakers[second])
                    self.winner = self.speakers[winner]
                    # time.sleep(1.0)
                    ranking = {}
                    for i in range(len(log_likelihood)):
                        ranking[self.speakers[i]] = log_likelihood[i]
                    ranking_sort = {k: v for k, v in sorted(ranking.items(), key=lambda item: item[1], reverse=True)}
                    self.score = ranking_sort[self.winner]
                    print("--------------sorted ranking----------------------")
                    print(ranking_sort)
                    print("------------------------------------")
                    # s = ''
                    # for e in ranking_sort:
                    #     s += f'{e}: {ranking_sort[e]}, '
                    # s += '\n'
                    # with open('gasire_prag.txt', 'a') as f:
                    #     f.write(f'{self.winner} ->')
                    #     f.write(s)
                    indexVector += 1

    def getWinner(self):
        return self.winner
