import os
import sys
from datetime import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import threading

from PyQt5.QtWidgets import QTextBrowser
from sounddevice import wait

from noise import p1
from word_match import mongo
from word_match import speech
from gmm import train
from gmm import test
from silence import silence
from record import record
from actualizare_amprenta import actamp
from color import Color

from PyQt5.QtCore import pyqtSlot
from shutil import copyfile
from os import listdir


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gui.ui", self)
        self._color = Color()
        self._color.add_color([self.inregistrare, self.autentificare], [], self.menubar, self.centralwidget, None)

        self._speechRecognition = speech.Speech()
        self._randomWord = mongo.RandomWord()
        self._train = train.Train(source="../gmm/development_set\\", dest="../gmm/speaker_models\\",
                                  train_file="../gmm/development_set_enroll.txt", countFiles=5)
        self._test = test.Test(source="../gmm/development_set\\", modelPath="../gmm/speaker_models\\",
                               testFile="../gmm/development_set_test.txt")
        self._silence = silence.Silence()
        self._record = record.Recorder()
        self._updateVoicePrint = actamp.updateVoicePrint()
        # self._record = p1.Record()

        self._user = None
        self._dbPass = None
        self._recognisePass = None
        self._probability = None
        self._error = None
        self.threshProbability = 0.7
        self.lineInTraining = 0

        self.location = None
        self.text = None

        self.contor = 0

        self.threadStart = threading.Thread(target=self.startCallback)
        self.threadPrint = threading.Thread(target=self.printLog)
        self.threadAutentificare = threading.Thread(target=self.callAutentificare)

        self.inregistrare.clicked.connect(self.pushStart)
        self.antrenare.clicked.connect(self.pushAntrenare)
        self.autentificare.clicked.connect(self.pushAutentificare)

        self.Menu.addAction('Inregistrare', self.pushMenuInregistreaza)
        self.Menu.addAction('Autentificare', self.pushMenuAutentificare)

        self.inregistrare.setVisible(False)
        self.autentificare.setVisible(False)
        self.antrenare.setVisible(False)

        # clear enroll file
        open("../gmm/development_set_enroll.txt", "w").close()
        # open("../gmm/development_set_test.txt", "w").close()

        self.users = self._test.speakers

    def hideAll(self):
        self.textBrowser.setVisible(False)
        self.textBrowser_2.setVisible(False)
        self.log.setVisible(False)
        self.inputName.setVisible(False)

        self.name.setVisible(False)
        self.readWords.setVisible(False)
        self.readWords_2.setVisible(False)
        self.readWords_3.setVisible(False)

        self.inregistrare.setVisible(False)

    def printLog(self):
        self.threadPrint = threading.Thread(target=self.printLog)
        self.location.append(self.text)

    def startCallback(self):
        """Inregistrarea unui utilizator, o sa primeasca 3 fraze ce vor trebui a fi citite"""
        self.threadStart = threading.Thread(target=self.startCallback)
        self._user = self.inputName.displayText()
        if self._user != "":
            self._dbPass = self._randomWord.takePhraseForDB(self._user)
            if self._dbPass != 0:
                self.log.append("Se extrag cuvintele din baza de date\n")
                print(self._dbPass)
                self.afisare(self.textBrowser, self._dbPass)
                self.afisare(self.log, "Pentru a porni inregistrarea fa putin zgomot\n")
                path = f"../gmm/development_set/{self._user}/wav/"
                file = f"readme.txt"
                filename = f"../gmm/development_set/{self._user}/wav/{self._user}{self.contor}.wav"
                filename_write = f"{self._user}/wav/{self._user}{self.contor}.wav"
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(os.path.join(path, file), 'w') as fp:
                    print('il creaza din nou')
                    pass

                # self._record.sync_record(filename, 5, 16000, 1)
                self._record.listen(filename)
                self.afisare(self.log, "Inregistrare finalizata\n")
                self._recognisePass = self._speechRecognition.recognizeText(filename)
                if self._recognisePass != -1:
                    self.afisare(self.textBrowser_2, self._recognisePass)
                    d, self._probability = self._randomWord.distance_levenshtein(self._dbPass.lower(),
                                                                                 self._recognisePass.lower())
                    self.afisare(self.log,
                                 f"Probabilitatea ca cele 2 stringuri sa se asemene este de {self._probability}")
                    if self._probability > self.threshProbability:
                        self._silence.task(filename, filename)
                        self.createInputTrain(filename_write, self._user)
                        self.lineInTraining += 1
                        if self.lineInTraining == 5:
                            self.antrenare.setVisible(True)
                            self.inregistrare.setVisible(False)

                else:
                    self.afisare(self.log, f"Eroare la recunoastere {self._speechRecognition.error}\n")
            else:
                self._error = self._randomWord.error
                self.log.append(f"Eroare {self._error}")
        else:
            self.afisare(self.log, f"Eroare nu ati completat la nume utilizator\n")

    def createInputTrain(self, path, user):
        with open('../gmm/development_set_enroll.txt', 'a') as f:
            f.write(path)
            f.write('\n')
        with open(f'../gmm/development_set/{user}/wav/records.txt', 'a') as f:
            f.write(path)
            f.write('\n')

    @pyqtSlot()
    def pushStart(self):
        self.inputName.setDisabled(True)
        self.log.clear()
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.threadStart.start()
        self.contor += 1

    @pyqtSlot()
    def pushMenuAutentificare(self):
        self._test = test.Test(source="../gmm/development_set\\", modelPath="../gmm/speaker_models\\",
                               testFile="../gmm/development_set_test.txt")
        self.users = self._test.speakers
        self.antrenare.setVisible(False)
        self.inputName.setDisabled(False)
        self.inregistrare.setVisible(False)
        self.autentificare.setVisible(True)

    @pyqtSlot()
    def pushMenuInregistreaza(self):
        self.autentificare.setVisible(False)
        self.inregistrare.setVisible(True)

    @pyqtSlot()
    def pushAntrenare(self):
        self._train.train()

    @pyqtSlot()
    def pushAutentificare(self):
        self.log.clear()
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.threadAutentificare.start()

    def callAutentificare(self):
        self.threadAutentificare = threading.Thread(target=self.callAutentificare)
        self._user = self.inputName.displayText()
        if self._user in self.users:
            if self._user != "":
                self._dbPass = self._randomWord.takePhraseForDB(self._user)
                if self._dbPass != 0:
                    self.log.append("Se extrag cuvintele din baza de date\n")
                    print(self._dbPass)
                    self.afisare(self.textBrowser, self._dbPass)
                    self.afisare(self.log, "Pentru a porni inregistrarea fa putin zgomot\n")

                    path = f"../gmm/development_set/test/wav/test.wav"

                    # self._record.sync_record(path, 5, 16000, 1)
                    self._record.listen(path)
                    self.afisare(self.log, "Inregistrare finalizata\n")

                    self._recognisePass = self._speechRecognition.recognizeText(path)
                    if self._recognisePass != -1:
                        self.afisare(self.textBrowser_2, self._recognisePass)
                        d, self._probability = self._randomWord.distance_levenshtein(self._dbPass.lower(),
                                                                                     self._recognisePass.lower())
                        self.afisare(self.log,
                                     f"Probabilitatea ca cele 2 stringuri sa se asemene este de {self._probability}")
                        if self._probability > self.threshProbability:
                            self._silence.task(path, path)
                            self._test.test()
                            if self._test.winner == self.inputName.displayText():
                                self.afisare(self.log, "Autentificarea a avut loc cu succes\n")
                                if self._test.score > -113:
                                    number_of_files = len(listdir(f"../gmm/development_set/{self._user}/wav/"))
                                    copyfile(f"../gmm/development_set/test/wav/test.wav",
                                             f"../gmm/development_set/{self._user}/wav/{self._user}{number_of_files + 1}.wav")
                                    with open(f'../gmm/development_set/{self._user}/wav/records.txt', 'a') as f:
                                        f.write(f'{self._user}/wav/{self._user}{number_of_files + 1}.wav')
                                        f.write('\n')
                                    self._updateVoicePrint.actualizareAmprenta(self._user)
                                    self.afisare(self.log, 'Actualizare amprenta\n')
                            else:
                                self.afisare(self.log, "Autentificarea nu a avut loc \n")
                    else:
                        self.afisare(self.log, f"Eroare la recunoastere {self._speechRecognition.error}\n")
            else:
                self.afisare(self.log, f"Eroare nu ati completat la nume utilizator\n")
        else:
            self.afisare(self.log, f"Utilizatorul nu exista\n")

    def afisare(self, location, text):
        self.location = location
        self.text = text
        self.threadPrint.start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    # window.pushAutentificare()
