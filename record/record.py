import pyaudio
import math
import struct
import wave
import time

Threshold = 10

SHORT_NORMALIZE = (1.0 / 32768.0)
chunk = 1024

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

TIMEOUT_LENGTH = 2

f_name_directory = "test"


class Recorder:

    @staticmethod
    def rms(frame):
        """RMS amplitude is defined as the square root of the
        mean over time of the square of amplitude. So we need to convert
        this string of bytes into a string of 16-bit samples"""

        # we will get one short out for each two chars in the string
        count = len(frame) / swidth
        # h -> short, interger 1 octet
        # '2048h' -> 2048 short
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        # iterate over the block
        sum_squares = 0.0
        for sample in shorts:
            # sample is a signed short in +/-32768
            # normalize it to 1.0
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.filename = None
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    def record(self, input):
        print('Noise detected, recording beginning')
        rec = []
        rec.append(input)
        current = time.time()
        initial = current
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:  # or initial + 16 < end

            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold: end = time.time() + TIMEOUT_LENGTH

            current = time.time()
            rec.append(data)

        # self.stream.stop_stream()
        # self.stream.close()

        self.write(b''.join(rec))

    def write(self, recording):
        # n_files = len(os.listdir(f_name_directory))
        # filename = os.path.join(f_name_directory, '{}.wav'.format(n_files))

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        print('Written to file: {}'.format(self.filename))
        print('Returning to listening')

    def listen(self, filename):
        self.filename = filename
        print('Listening beginning')
        ok = 0
        while ok == 0:
            input = self.stream.read(chunk)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                ok = 1
        self.record(input)

# a = Recorder()
# a.listen("test/pere.wav")
