#!/usr/bin/python3
from string import whitespace
import matplotlib
import scipy.fftpack
import scipy.interpolate

import numpy as np
from matplotlib import pyplot as plt
import sys
from myPlot import accelPlot

def plot():
     if len(sys.argv) < 1:
          print('give file arg')
          exit()

     fig, axs = plt.subplots(2)
     fig.set_size_inches(20,10)
     subFileName = sys.argv[1]


     accelPlot(axs,subFileName)
     plt.show()

plot()