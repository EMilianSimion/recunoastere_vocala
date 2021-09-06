import os
import soundfile as sf
from word_match import speech


class Sox:

    def remove(self, filename, destination):
        data, samplerate = sf.read(filename)
        duration = len(data) / samplerate
        print(duration)

        os.system(f'sox {filename} -n trim {duration - 2} {2} noiseprof speech.noise-profile')

        os.system(f'sox {filename} {destination} noisered speech.noise-profile {0.2}')
        # os.remove("speech.noise-profile")

    def removeWithDuration(self, duration, filename):
        os.system(f'sox {filename} -n trim {duration - 1} {1} noiseprof speech.noise-profile')

        os.system(f'sox {filename} cleaned.wav noisered speech.noise-profile {0.2}')
        os.remove("speech.noise-profile")


# if __name__ == '__main__':
#     _speechRecognition = speech.Speech()
#     s = Sox()
#     s.remove("test.wav", "cleaned.wav")
#     _recognisePass = _speechRecognition.recognizeText("cleaned.wav")
#     print(_recognisePass)
