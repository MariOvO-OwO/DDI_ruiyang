import scipy.fftpack
import numpy as np
import scipy.io.wavfile as wavfile

'''
params:
    signal: data to be converted to fft
    sampleInterval: time in seconds between signals
return:
    freqs_side: X value's for fft plotting
    FFT_side: Y value's for fft plotting
'''
def fft(signal,sampleInterval,low_range=0,high_range=None):
    FFT = np.real(scipy.fftpack.fft(signal))
    FFT_side = FFT[range(len(signal)//2)] # one side FFT range
    freqs = scipy.fftpack.fftfreq(len(signal),sampleInterval)
    freqs_side = freqs[range(len(signal)//2)] # one side frequency range

    fs_rate = round(freqs_side[-1]) *2
    # print(f'testing: max freq: {fs_rate}')
    if not high_range:
        high_range = len(freqs_side)
    signal_og_len = len(freqs_side)
    freqs_side_og = freqs_side
    interval = fs_rate/2/len(freqs_side)

    low_range = int(low_range/interval)  # result is in index
    high_range = int(high_range/interval)
    # print(f'testing ranges: low: {low_range} and high: {high_range}  len: {len(freqs_side)} fs: {fs_rate}')
    freqs_side = freqs_side[low_range:high_range]
    FFT_side = FFT_side[low_range:high_range]

    return freqs_side, FFT_side

def getChannelSignal(fileName):
    if fileName.endswith('.wav'):
        fs_rate, signal = wavfile.read(fileName)
        l_audio = len(signal.shape)
        L = []
        R = []

        if l_audio == 2:
            for arr in signal:
                L.append(arr[0])
                R.append(arr[1])
            L = np.array(L)
            R = np.array(R)
        else:
            L = signal

        return fs_rate,L

    else:
        xs = []
        ys = []
        zs = []
        with open(fileName,'r') as intFile:
            while intFile:
                try:
                    xs.append(float(intFile.readline()))
                    ys.append(float(intFile.readline()))
                    zs.append(float(intFile.readline()))
                except:
                    # print(f"exception Probablly just newline at end of int file")
                    break
        return 400, ys

def sampleDistanceByHz(signal,sample_interval,fs_rate,hz_width):
    # freqs_side, _ = fft(signal,sample_interval)
    freqs = scipy.fftpack.fftfreq(len(signal),sample_interval)
    freqs_side = freqs[range(len(signal)//2)] # one side frequency range
    freq_interval = fs_rate/2/len(freqs_side)
    distance = int(hz_width / freq_interval)
    return distance