# -*- coding: utf-8 -*-

# GammaEyes
#
# Created at: 2021.07.19
#
# A class for gamma spectrum
import numpy as np
import pywt
from statsmodels.robust import mad
import scipy.interpolate as spi

class geStabilization:
    # ====================================================================================
    def __init__(self, spectrum):
        self.spec = spectrum
        self.channel_total = len(spectrum)
        # self.spec_smooth = self.waveletDenoise()

    # def peaksSearch(self, peak_roi):
    #     """
    #     search peak
    #     :param peak_roi:
    #     :return:
    #     """
    #     spec_roi = self.spec_smooth[peak_roi[0]:peak_roi[1] + 1].tolist()
    #     peak = spec_roi.index(max(spec_roi)) + peak_roi[0]
    #     return peak

    def channelIndex_3rp(self, peaks, peaks_standard, energys, mode="nonlinear"):
        """
        calculate the channels
        :param peaks:             reference peaks in spectrum
        :param peaks_standard:    reference peaks in standard spectrum
        :param energys:           reference peaks' energy
        :param mode:              linear calibration or nonlinear calibration
        :return:                  the channels
        """
        channels = np.zeros(self.channel_total)
        if mode == "nonlinear":
            # calculate the parameters (a, b, c)
            a_co, b_co, c_co = np.power(peaks, 2), peaks, np.ones(3)
            A = np.vstack((a_co, b_co, c_co)).T
            a, b, c = np.linalg.solve(A, energys)
            # print(a,b,c)
            # calculate the standard parameters (as, bs, cs)
            a_co_s, b_co_s, c_co_s = np.power(peaks_standard, 2), peaks_standard, np.ones(3)
            A_s = np.vstack((a_co_s, b_co_s, c_co_s)).T
            a_s, b_s, c_s = np.linalg.solve(A_s, energys)
            # print(a_s, b_s, c_s)
            for i in range(self.channel_total):
                ener = a_s * i * i + b_s * i + c_s
                c_0 = c - ener
                channels[i] = ((-b) + np.sqrt(b * b - a * c_0 * 4)) / (2 * a)
        elif mode == "linear":
            # calculate the parameters (a, b, c)
            a_co, b_co = peaks, np.ones(2)
            A = np.vstack((a_co, b_co)).T
            a, b = np.linalg.solve(A, energys)

            # calculate the standard parameters (as, bs, cs)
            a_co_s, b_co_s = peaks_standard, np.ones(2)
            A_s = np.vstack((a_co_s, b_co_s)).T
            a_s, b_s = np.linalg.solve(A_s, energys)

            for i in range(self.channel_total):
                ener = a_s * i + b_s
                b_0 = ener - b
                channels[i] = b_0 / a

        self.channel = channels

    def stable(self, n):
        """
        function for stablilization
        :param n:  n means 2n+1 points are using for spline
        :return:   stabled spectrum
        """
        spec_stabled = np.zeros(self.channel_total)
        x_chan = np.linspace(0.5, self.channel_total - 0.5, self.channel_total)

        for i in range(self.channel_total):

            if i - n < 0 or i + n > self.channel_total - 1:
                continue

            c_l = self.channel[i - 1]
            c_r = self.channel[i]

            if int(c_r) - int(c_l) == 1:  # c_l and c_r cross a channel
                chan_1 = int(c_l) + 1  # 1st channel - drift spectra
                chan_2 = int(c_r) + 1  # 2nd channel - drift spectra
                if chan_1 - n < 0 or chan_2 + n > self.channel_total - 1:
                    continue
                x1 = x_chan[chan_1 - n:chan_1 + n + 1]
                x2 = x_chan[chan_2 - n:chan_2 + n + 1]

                y1 = self.spec[chan_1 - n: chan_1 + n + 1]
                y2 = self.spec[chan_2 - n: chan_2 + n + 1]

                sp1 = spi.UnivariateSpline(x1, y1, s=3)
                sp2 = spi.UnivariateSpline(x2, y2, s=3)

                area1 = sp1.integral(c_l, chan_1)

                if sp1.integral(chan_1 - 1, chan_1) > 0:
                    area1 = area1 / sp1.integral(chan_1 - 1, chan_1) * self.spec[chan_1]
                else:
                    area1 = 0
                if sp2.integral(chan_1, chan_1 + 1) > 0:
                    area2 = sp2.integral(chan_1, c_r)
                    area2 = area2 / sp2.integral(chan_1, chan_1 + 1) * self.spec[chan_2]
                else:
                    area2 = 0
                spec_stabled[i] = area1 + area2
            elif int(c_r) - int(c_l) == 2:  # c_l and c_r cross 2 channel
                chan_1 = int(c_l) + 1
                chan_2 = int(c_r) + 1
                chan_mid = int(c_r)
                if chan_1 - n < 0 or chan_2 + n > 1023:
                    continue

                x1 = x_chan[chan_1 - n:chan_1 + n + 1]
                x2 = x_chan[chan_2 - n:chan_2 + n + 1]

                y1 = self.spec[chan_1 - n: chan_1 + n + 1]
                y2 = self.spec[chan_2 - n: chan_2 + n + 1]

                sp1 = spi.UnivariateSpline(x1, y1, s=3)
                sp2 = spi.UnivariateSpline(x2, y2, s=3)

                area1 = sp1.integral(c_l, chan_1)

                if sp1.integral(chan_1 - 1, chan_1) > 0:
                    area1 = area1 / sp1.integral(chan_1 - 1, chan_1) * self.spec[chan_1]
                else:
                    area1 = 0

                if sp2.integral(chan_2 - 1, chan_2) > 0:
                    area2 = sp2.integral(chan_2 - 1, c_r)
                    area2 = area2 / sp2.integral(chan_2 - 1, chan_2) * self.spec[chan_2]
                else:
                    area2 = 0

                spec_stabled[i] = area1 + area2 + self.spec[chan_mid]

            elif int(c_r) - int(c_l) == 0:
                chan_1 = int(c_l) + 1

                if chan_1 - n < 0 or chan_1 + n > 1023:
                    continue

                x1 = x_chan[chan_1 - n:chan_1 + n + 1]
                y1 = self.spec[chan_1 - n: chan_1 + n + 1]
                sp1 = spi.UnivariateSpline(x1, y1, s=3)
                area1 = sp1.integral(c_l, c_r)
                if sp1.integral(chan_1 - 1, chan_1) * self.spec[chan_1] > 0:
                    spec_stabled[i] = area1 / sp1.integral(chan_1 - 1, chan_1) * self.spec[chan_1]
                else:
                    spec_stabled[i] = 0
            else:
                print("error: ", i, "-th channel, c_r-c_l=", int(c_r) - int(c_l), c_l, c_r)
        return spec_stabled

    # def waveletDenoise(self, wavelet='coif3', mode='per', level=3):
    #     """
    #     function for wavelet denoising
    #     :param wavelet:
    #     :param mode:
    #     :param level:
    #     :return:
    #     """
    #     coeff = pywt.wavedec(self.spec, wavelet, mode, level)
    #     sigma = mad(coeff[level])
    #     uthesh = sigma * np.sqrt(2 * np.log(len(self.spec)))
    #     coeff[1:] = (pywt.threshold(i, value=uthesh, mode='soft') for i in coeff[1:])
    #     ySmooth = pywt.waverec(coeff, wavelet, mode)
    #     ySmooth = np.array(ySmooth)
    #
    #     return ySmooth



