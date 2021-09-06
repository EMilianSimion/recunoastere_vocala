import numpy as np
from scipy.fft import rfft, rfftfreq
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
from scipy.io import wavfile
import os


class Record:
    def sync_record(self, filename, duration, fs, channels):
        print('recording')
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
        sd.wait()
        sf.write(filename, myrecording, fs)
        print('done recording')

    def generate_sine_wave(self, freq=2, sample_rate=44100, duration=5):
        x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
        frequencies = x * freq
        # 2pi because np.sin takes radians
        y = np.sin((2 * np.pi) * frequencies)
        plt.plot(x, y)
        plt.show()

    def remove_noise(self, filename):
        # now use sox to denoise using the noise profile
        data, samplerate = sf.read(filename)
        duration = data / samplerate
        first_data = samplerate / 10
        filter_data = list()
        for i in range(int(first_data)):
            filter_data.append(data[i])
        noisefile = 'noise.wav'
        sf.write(noisefile, filter_data, samplerate)
        os.system('sox %s -n noiseprof noise.prof' % (noisefile))
        filename2 = 'tempfile.wav'
        filename3 = 'tempfile2.wav'
        noisereduction = "sox %s %s noisered noise.prof 0.21 " % (
            filename, filename2)
        command = noisereduction
        # run command
        os.system(command)
        print(command)
        # reduce silence again
        # os.system(silenceremove)
        # print(silenceremove)
        # rename and remove files
        os.remove(filename)
        os.rename(filename2, filename)
        # os.remove(filename2)
        os.remove(noisefile)
        # os.remove('noise.prof')
        return filename

    def afiasre_plot_input_eliminareZgomot(self):
        fs, signal = wavfile.read("test/pass.wav")
        fs1, signal2 = wavfile.read("test/noise.wav")

        fig, axs = plt.subplots(2)
        axs[0].plot(signal)
        axs[1].plot(signal2)
        plt.show()

    def myRfft(self, pathSemnal):
        fs, signal = wavfile.read(pathSemnal)
        N = len(signal)
        yf = rfft(signal)
        xf = rfftfreq(N, 1 / fs)
        return xf, yf

    def filtering(self, pathSemnal="model/inputCuZgomot.wav", pathZgomot="model/noise.wav",
                  pathVaded="model/vaded.wav", ):
        xS, yS = self.myRfft(pathSemnal)
        xZ, yZ = self.myRfft(pathZgomot)
        xV, yV = self.myRfft(pathVaded)

        fig, axs = plt.subplots(2, 2)
        axs[0, 0].plot(xS, np.abs(yS))
        axs[1, 0].plot(xZ, np.abs(yZ))
        axs[0, 1].plot(xV, np.abs(yV))

        plt.show()


# afiasre_plot_input_eliminareZgomot()
# filtering()
# main
# sync_record('noise1.wav', 5, 16000, 1)

# remove_noise("inputCuZgomot.wav")

#
# xS, yS = myRfft('model/inputCuZgomot.wav')
# xZ, yZ = myRfft('model/log1.wav')
# xP, yP = myRfft('model/removed.wav')
# xR, yR = myRfft('model/removedlog1.wav')
#
#
# plt.plot(xS, np.abs(yS))
# plt.plot(xZ, np.abs(yZ))
# plt.plot(xP, np.abs(yP))
# plt.plot(xR, np.abs(yR))
#
#
# plt.show()

# logmmse_from_file('test/pass.wav', 'test/removedpass1.wav')
# sync_record('e2_ana.wav', 5, 16000, 1)
# print(remove_noise('resources/original/parola_este1.1.wav'))
# filtering("test/pass.wav", "test/noise.wav", "test/removedpass1.wav")
# afiasre_plot_input_eliminareZgomot()
# rec = Record()
# for i in range(0, 10):
#     rec.sync_record(f'tilia{i}.wav', 5, 16000, 1)
