from mySignal import fft,getChannelSignal
import numpy as np
##############################################ACCEL PLOTTER
def accelPlot(axs,fileName,low_range=0,high_range=None,total_plots=1,plot_col=1):
    #####ONLY PROCESS Y AXIS
    fs_rate,signal = getChannelSignal(fileName)
    sampleCount = len(signal)
    secs = sampleCount / float(fs_rate)

    ###TIME AXIS
    sampleInterval = 1.0/fs_rate # sampling interval in time
    time_axis = np.arange(0, secs, sampleInterval) # time vector as scipy arange field / numpy.ndarray

    #L TIME ACCEL
    l_plt = None
    if total_plots == 1:
        l_plt = axs[0]
    else:
        l_plt = axs[0][plot_col]
    l_plt.plot(time_axis,signal, "g") # plotting the signal
    l_plt.set_title("Accel Y Axis Time Domain")
    l_plt.set_xlabel('Time')
    l_plt.set_ylabel('Amplitude')

    #LEFT FREQ ACCEL
    freqs_side,FFT_side = fft(signal,sampleInterval,low_range,high_range)

    l_plt = None
    if total_plots == 1:
        l_plt = axs[1]
    else:
        l_plt = axs[1][plot_col]
    cutMin = 1
    l_plt.plot(freqs_side[cutMin:], FFT_side[cutMin:], "g") # plotting the positive fft spectrum
    l_plt.set_title(f"ABS freq range: {freqs_side[cutMin]:.2f} to {freqs_side[-1]:.2f}")
    l_plt.set_xlabel('Frequency (Hz)')
    l_plt.set_ylabel('Amplitude')



################################################MIC PLOTTER
def micPlot(axs,fileName,low_range=1,high_range=None,total_plots=1,plot_col=1):
    fs_rate,signal = getChannelSignal(fileName)
    ######################CLEAN DIRTY SPIKE
    cutOff = int(.01 * len(signal))
    signal = signal[cutOff:] # cut 5% for noice reduction
    print(f'Mic signal. Clipping {cutOff} of {len(signal)} to clean initial spike.')

    sampleCount = len(signal)
    secs = sampleCount / float(fs_rate)
    sampleInterval = 1.0/fs_rate # sampling interval in time

    time_axis = np.arange(0, secs, sampleInterval) # time vector as scipy arange field / numpy.ndarray

    ####L TIME
    l_plt = None
    if total_plots  == 1:
        l_plt = axs[0]
    else:
        l_plt = axs[0][plot_col]
    l_plt.plot(time_axis,signal, "r",label="Left Channel") # plotting the signal
    l_plt.set_title(f"Single Channel Audio Time Domain")
    l_plt.set_xlabel('Time')
    l_plt.set_ylabel('Amplitude')

    #LEFT CHANNEL STUFF, FREQ
    freqs_side, FFT_side = fft(signal,sampleInterval,low_range,high_range)


    l_plt = None
    if total_plots  == 1:
        l_plt = axs[1]
    else:
        l_plt = axs[1][plot_col]
    l_plt.plot(freqs_side, FFT_side, "r") # plotting the positive fft spectrum
    l_plt.set_title(f"Audio ABS freq range: {freqs_side[0]:.2f} to {freqs_side[-1]:.2f}")
    l_plt.set_xlabel('Frequency (Hz)')
    l_plt.set_ylabel('ABS Amplitude')
