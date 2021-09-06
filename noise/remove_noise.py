import soundfile as sf
import os

"""Remove noise from JIM Schwoebel - Introduction to Voice Computing in Python"""


def remove_noise(filename):
    # now use sox to denoise using the noise profile
    data, samplerate = sf.read(filename)
    duration = data / samplerate
    first_data = samplerate / 10
    filter_data = list()
    for i in range(int(first_data)):
        filter_data.append(data[i])
    noisefile = 'noiseprof.wav'
    sf.write(noisefile, filter_data, samplerate)
    os.system('sox %s -n noiseprof noise.prof' % (noisefile))
    filename2 = 'tempfile.wav'
    filename3 = 'tempfile2.wav'
    noisereduction = "sox %s %s noisered noise.prof 1 " % (filename, filename2)
    command = noisereduction
    # run command
    os.system(command)
    print(command)
    # reduce silence again
    # os.system(silenceremove)
    # print(silenceremove)
    # rename and remove files
    # os.remove(filename)
    # os.rename(filename2, filename)
    # os.remove(filename2)
    # os.remove(noisefile)
    # os.remove('noise.prof')
    return filename


# cica main
print(remove_noise('resources/original/noise1.wav'))
# print(remove_noise('resources/parola_este1.1.wav'))
