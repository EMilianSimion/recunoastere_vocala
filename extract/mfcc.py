from python_speech_features import mfcc
from python_speech_features import logfbank
from python_speech_features import delta
import scipy.io.wavfile as wav

(rate, sig) = wav.read("../facultate_teste/s_p_ana.wav")
mfcc_feat = mfcc(sig, rate)
d_mfcc_feat = delta(mfcc_feat, 2)
fbank_feat = logfbank(sig, rate)
print("Prof")
# print(d_mfcc_feat[2, :])
print(fbank_feat[1:3, :])


(rate, sig) = wav.read("../facultate_teste/s_e_ana.wav")
mfcc_feat = mfcc(sig, rate)
d_mfcc_feat = delta(mfcc_feat, 2)
fbank_feat = logfbank(sig, rate)

print(fbank_feat[1:4, :])
print("Emi")
# print(d_mfcc_feat[2, :])
