#!/usr/bin/python3
from cProfile import label
from curses.ascii import FF
from dis import dis
import scipy.fftpack
import scipy.interpolate
import scipy.io.wavfile as wavfile
from scipy import signal
from scipy.signal import butter, lfilter, freqz, find_peaks
import numpy as np
from matplotlib import pyplot as plt

import sys
from mySignal import getChannelSignal, fft, sampleDistanceByHz

from mySignal import fft




##############################################ACCEL PLOTTER
def accelPeaks(subFileName,height=10,low_range=0,high_range=None,hz_width=1,plot=False):
    print("#########################################")
    #####ONLY PROCESS Y AXIS
    fs_rate,signal = getChannelSignal(subFileName + "Accel")

    #FFT
    sampleInterval = 1.0/fs_rate # sampling freq_interval in time
    freqs_side,FFT_side = fft(signal,sampleInterval,low_range,high_range)

    #distance is minimum distance between peaks
    distance = sampleDistanceByHz(signal,sampleInterval,fs_rate,hz_width)
    #result has two dimensions. 1) is the locations of peaks 2) is the peak value
    testPeak = find_peaks(FFT_side,height=height,distance=distance)
    # testPeak = find_peaks(FFT_side)

    # print(f'Diganostic: How many Peaks: {len(testPeak[0])}')
    if not high_range:
        high_range = fs_rate / 2
    print(f'Diganostic: Freq Range: {low_range} to {high_range} How many Peaks: {len(testPeak[0])}')
    print('Accel Peaks at Freq')
    try:
        indexes = testPeak[0]
        print(freqs_side[indexes])
        t = testPeak[1]['peak_heights']
        print("Max Value in range: " ,t.max())
    except Exception as e:
        print(f'********EXCEPTION: {e}')
        # pass

    print("\n#########################################\n")
    if plot:
        plt.plot(freqs_side,FFT_side,'g',label="Accel Freq")
        plt.show()







###########MIC PLOTTER
def micPeaks(subFileName,height=1.7e10,low_range=0,high_range=None,hz_width=1,plot=False):
    print("#########################################")
    # fs_rate, signal = wavfile.read(subFileName + "Mic.wav")
    fs_rate, signal = getChannelSignal(subFileName + "Mic.wav")

    ######################CLEAN DIRTY SPIKE
    cutOff = int(.01 * len(signal))
    signal = signal[cutOff:] # cut 5% for noice reduction
    # print(f'Mic signal. Clipping {cutOff} of {len(signal)} to clean initial spike.')


    sampleInterval = 1.0/fs_rate # sampling freq_interval in time

    #LEFT CHANNEL STUFF, FREQ
    freqs_side, FFT_side = fft(signal,sampleInterval,low_range,high_range)

    #distance is minimum distance
    distance = sampleDistanceByHz(signal,sampleInterval,fs_rate,hz_width)

    testPeak = find_peaks(FFT_side,height=height,distance=distance)
    if not high_range:
        high_range = fs_rate / 2
    print(f'Diganostic: Freq Range: {low_range} to {high_range} How many Peaks: {len(testPeak[0])}')
    print('Mic Peaks at Freq')
    try:
        indexes = testPeak[0]
        print(freqs_side[indexes])
        t = testPeak[1]['peak_heights']
        print("Max Value in range: " ,int(t.max()))
    except Exception as e:
        print(f'********EXCEPTION: {e}')

    if plot:
        plt.plot(freqs_side,FFT_side,'r',label="Mic Freq")
        plt.show()
    print("\n#########################################\n")


def plot():
    if len(sys.argv) < 1:
        print('Give subFileName on CL')
    subFileName = sys.argv[1]

    low_range=1
    high_range=None
    accelPeaks(subFileName,height=2.5,low_range=low_range,high_range=high_range, hz_width=10,plot=False)

    low = 1
    high = 200
    micPeaks(subFileName,height=47150835308,low_range=low,high_range=high, hz_width=20)


plot()

