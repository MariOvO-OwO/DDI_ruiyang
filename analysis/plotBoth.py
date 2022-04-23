#!/usr/bin/python3
from matplotlib import pyplot as plt
import sys

from mySignal import fft,getChannelSignal
from myPlot import accelPlot, micPlot


def plot():
    if len(sys.argv) < 1:
        print('Give subFileName on CL')
    try:


        totalPlots = 2
        fig, axs = plt.subplots(nrows=2,ncols=totalPlots)
        fig.set_size_inches(20,10)
        subFileName = sys.argv[1]


        accelPlot(axs,subFileName + "Accel",total_plots=totalPlots, plot_col=0)

        low_range=1
        high_range=200
        # micPlot(axs,subFileName + "Mic.wav",low_range=low_range,high_range=high_range,total_plots=totalPlots, plot_col=0)
        micPlot(axs,subFileName + "Mic.wav",low_range=low_range,high_range=high_range,total_plots=totalPlots, plot_col=1)
        # cutPlot = 200
        # micPlot(axs,1,subFileName,high_range=cutPlot)
        # micPlot(axs,2,subFileName,cutPlot)

        plt.show()

    except KeyboardInterrupt:

        plt.close(fig)

plot()

