import os
from pathlib import Path
import os
from _pickle import dump
import numpy as np
from scipy.io.wavfile import read
from sklearn.mixture import GaussianMixture
from extract import speakerfeatures, gfcc
import warnings

warnings.filterwarnings("ignore")


class updateVoicePrint:
    def __init__(self):
        self._source = '../gmm/development_set\\'
        self._dest = '../gmm/speaker_models\\'
        self.finalDest = ['combined\\', 'gfcc\\', 'mfcc\\']
        self.mfccDirectory = None
        self.gfccDirectory = None

        self.features = np.asarray(())
        self.fmfcc = np.asarray(())
        self.fgfcc = np.asarray(())

        self._gfcc = gfcc.GFCC()

    def creareDirectoryIfNotExists(self, user):
        directory = os.path.dirname(f'../gmm/development_set/{user}/wav/coeff/')
        self.mfccDirectory = f'../gmm/development_set/{user}/wav/coeff/mfcc/'
        self.gfccDirectory = f'../gmm/development_set/{user}/wav/coeff/gfcc/'
        if not os.path.exists(directory):
            os.makedirs(directory)
            mfccDirectory = os.path.dirname(self.mfccDirectory)
            gfccDirectory = os.path.dirname(self.gfccDirectory)
            os.makedirs(mfccDirectory)
            os.makedirs(gfccDirectory)

    def actualizareAmprenta(self, user='emi'):
        self.creareDirectoryIfNotExists(user)
        directory_path = f'../gmm/development_set/{user}/wav/records.txt'
        list_of_records = []
        with open(directory_path, 'r') as f:
            for x in f:
                list_of_records.append(x[:len(x) - 1])
        if len(list_of_records) > 10:
            list_of_records = list_of_records[len(list_of_records) - 10:]

        print(list_of_records)
        for file in list_of_records:
            sr, audio = read(self._source + file)
            # am inregistrarea, caut fisierul cu coeficienti, daca exista il iau, daca nu il calculez
            file_save_coeff_name = file.split('/')[-1].split('wav')[0]
            if os.path.exists(f'{self.mfccDirectory}/{file_save_coeff_name}npy'):
                vector1 = np.load(f"{self.mfccDirectory}/{file_save_coeff_name}npy")
                vector2 = np.load(f"{self.gfccDirectory}/{file_save_coeff_name}npy")
                print('gasite in cache')
            else:
                print('salvate in cache')
                vector1 = speakerfeatures.extract_features(audio, sr)
                vector2 = self._gfcc.extractGFCC(audio, sr)
                vector1 = vector1[:len(vector2)]
                np.save(f"{self.mfccDirectory}/{file_save_coeff_name}npy", vector1)
                np.save(f"{self.gfccDirectory}/{file_save_coeff_name}npy", vector2)

            vector = np.hstack((vector1, vector2))

            if self.features.size == 0:
                self.features = vector
                self.fmfcc = vector1
                self.fgfcc = vector2
            else:
                self.features = np.vstack((self.features, vector))
                self.fmfcc = np.vstack((self.fmfcc, vector1))
                self.fgfcc = np.vstack((self.fgfcc, vector2))
        # when features of last 10 files of speaker are concatenated, then do model training
        features = [self.features, self.fgfcc, self.fmfcc]
        for i in range(len(self.finalDest)):
            gmm = GaussianMixture(n_components=16, covariance_type='diag', n_init=3)
            gmm.fit(features[i])

            # dumping the trained gaussian model
            picklefile = f'{user}.gmm'
            filename = str(self._dest) + str(self.finalDest[i]) + str(picklefile)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            dump(gmm, open(filename, 'wb'))
            print('+ update voiceprint completed for speaker:', picklefile, " coeff ", self.finalDest[i],
                  " with data point = ", self.features.shape)


# act = updateVoicePrint()
#
# act.actualizareAmprenta()
