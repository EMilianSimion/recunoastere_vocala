import speech_recognition as sr


class Speech:
    def __init__(self, *args, **kwargs):
        self.error = None

    def recognizeText(self, sourceFile):
        r = sr.Recognizer()

        harvard = sr.AudioFile(sourceFile)
        try:
            with harvard as source:
                audio = r.record(source)

            return r.recognize_google(audio)
        except Exception as e:
            self.error = e
            return -1
