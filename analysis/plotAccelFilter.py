#!/usr/bin/python3
from string import whitespace
import matplotlib
import scipy.fftpack
import scipy.interpolate
from scipy.signal import butter, lfilter

import numpy as np
from matplotlib import pyplot as plt

import sys


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=2):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def FileAccelPlotter(fileName):
    xs = []
    ys = []
    zs = []

    with open(fileName,'r') as intFile:
        while intFile:
            try:
                    xs.append(int(intFile.readline()))
                    ys.append(int(intFile.readline()))
                    zs.append(int(intFile.readline()))
            except:
                    print(f"exception Probablly just newline at end of int file")
                    break

    signal = ys
    fs_rate = 400
    sampleCount = len(signal)
    secs = sampleCount / float(fs_rate)

    sampleInterval = 1.0/fs_rate # sampling interval in time
    print ("Timestep between samples sampleInterval", sampleInterval)

    t = np.arange(0, secs, sampleInterval) # time vector as scipy arange field / numpy.ndarray

    FFT = abs(scipy.fftpack.fft(signal))
    FFT_side = FFT[range(sampleCount//2)] # one side FFT range
    freqs = scipy.fftpack.fftfreq(len(signal), t[1]-t[0])
    freqs_side = freqs[range(sampleCount//2)] # one side frequency range

    cutMin = int(len(freqs_side)/200)


    ## NEW SIMPLE TWO PLOT
    fig, axs = plt.subplots(nrows=2,ncols=2)
    fig.set_size_inches(25,12)
    #L TIME
    l_plt = axs[0][0]
    l_plt.plot(t[cutMin:],signal[cutMin:], "g") # plotting the signal
    l_plt.set_title("Original Time")
    # l_plt.set_xlabel('Time')
    # l_plt.set_ylabel('Amplitude')

    #LEFT CHANNEL STUFF, FREQ
    # cutMin = int(len(freqs_side)/200)
    l_plt = axs[1][0]
    l_plt.plot(freqs_side[cutMin:], FFT_side[cutMin:], "g") # plotting the positive fft spectrum
    l_plt.set_title(f"ABS freq range: {freqs_side[cutMin]:.2f} to {freqs_side[-1]:.2f}")
    # l_plt.set_xlabel('Frequency (Hz)')
    # l_plt.set_ylabel('ABS Amplitude')

    # plt.subplot(211)
    # p1 = plt.plot(t, signal, "g") # plotting the signal
    # plt.xlabel('Time')
    # plt.ylabel('Amplitude')

    # cutMin = int(len(freqs_side)/200)
    # print(f'Cutting indexes: {cutMin} Frequency range: {freqs_side[cutMin]:.2f} to {freqs_side[-1]:.2f}')
    # plt.subplot(212)
    # p3 = plt.plot(freqs_side[cutMin:], FFT_side[cutMin:], "b") # plotting the positive fft spectrum
    # plt.title(f'Frequency range: {freqs_side[cutMin]:.2f} to {freqs_side[-1]:.2f}')
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Count single-sided')

    # plt.figure(figsize=(20, 10))



    # reprocess for filter test
    cutoff = 50#hz
    fs = 400
    order = 2
    signal = butter_lowpass_filter(signal,cutoff,fs,order)

    FFT = abs(scipy.fftpack.fft(signal))
    FFT_side = FFT[range(sampleCount//2)] # one side FFT range
    freqs = scipy.fftpack.fftfreq(len(signal), t[1]-t[0])
    freqs_side = freqs[range(sampleCount//2)] # one side frequency range


    #L TIME
    l_plt = axs[0][1]
    l_plt.plot(t[cutMin:],signal[cutMin:], "g") # plotting the signal
    l_plt.set_title("Filtered TIME")
    # l_plt.set_xlabel('Time')
    # l_plt.set_ylabel('Amplitude')



    #LEFT CHANNEL STUFF, FREQ
    cutMin = int(len(freqs_side)/200)
    l_plt = axs[1][1]
    l_plt.plot(freqs_side[cutMin:], FFT_side[cutMin:], "g") # plotting the positive fft spectrum
    l_plt.set_title("Filtered Freq")


    plt.show()



if len(sys.argv) < 1:
    print('give file arg')

FileAccelPlotter(sys.argv[1])
