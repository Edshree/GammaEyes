# -*- coding: utf-8 -*-

# GammaEyes
#
# Created at: 2021.07.19
#
# A class for find the peaks in a gamma spectrum
import numpy as np
# import pywt
# from statsmodels.robust import mad
from scipy import signal

class geFindpeaks:
    # def __init__(self):
    #     pass

    def auto_find(self, spec, para):
        peaks = signal.find_peaks(spec,threshold=para[0],distance=para[1],prominence=para[2],width=para[3])
        return peaks

    def auto_find_cwt(self,spec,para):
        # peaks = signal.find_peaks_cwt(spec,widths=para[0],max_distances=para[1],min_snr=para[2])
        # if para[]

        peaks = signal.find_peaks_cwt(spec, widths=para[0],max_distances=para[1],min_snr=para[2])

        return peaks






