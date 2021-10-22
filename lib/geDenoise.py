# -*- coding: utf-8 -*-

# GammaEyes
#
# Created at: 2021.07.19
#
# A class for gamma spectrum denoising
import numpy as np
import pywt
from statsmodels.robust import mad
from scipy import signal
from scipy import interpolate

class geDenoise:
    # def __init__(self):
    #     pass

    def fit_denoise(self, spec, point_num):
        print(spec)
        yLen = len(spec)  #
        spec_smooth = np.zeros(len(spec))
        spec_smooth = spec

        if point_num=="5":
            for i in range(0, yLen - 2):
                if spec[i] != 0:  # 能谱前几道计数可能为0，到能谱不等于0的时候开始循环，作平滑处理
                    break
                for n in range(i + 2, yLen - 2):
                    spec_smooth[n] = (12 * spec[n - 1] - 3 * spec[n - 2] + 17 * spec[n] + 12 * spec[n + 1] - 3 * spec[n + 2]) / 35  # 五点拟合公式

        elif point_num=="7":
            for i in range(0, yLen - 3):
                if spec[i] != 0:  # 能谱前几道计数可能为0，到能谱不等于0的时候开始循环，作平滑处理
                    break
                for n in range(i + 3, yLen - 3):
                    # ySmooth[n] = (y[n - 1]+y[n - 2] + y[n] + y[n + 1] + y[n + 2])/5
                    spec_smooth[n] = (-2*spec[n-3]+ 3 * spec[n - 2]+6 * spec[n - 1] +7* spec[n] + 6 * spec[n + 1]+3 * spec[n + 2]-2*spec[n+3])/21  # 七点拟合公式

        elif point_num=="9":
            for i in range(0, yLen - 4):
                if spec[i] != 0:  # 能谱前几道计数可能为0，到能谱不等于0的时候开始循环，作平滑处理
                    break
                for n in range(i + 4, yLen - 4):
                    spec_smooth[n]=(-21*spec[n-4]+14*spec[n-3]+39*spec[n-2]+54*spec[n-1]+59*spec[n]+54*spec[n+1]+39*spec[n+2]+14*spec[n+3]-21*spec[n+4])/231    # 九点拟合公式

        return spec_smooth

    def wavelet_denoise(self, spec, wavelet, mode, level):
        w = pywt.Wavelet(wavelet)
        # maxlevel = pywt.dwt_max_level(len(spec), w.dec_len)
        coeff = pywt.wavedec(spec, wavelet, mode, level)
        sigma = mad(coeff[level])
        uthesh = sigma * np.sqrt(2 * np.log(len(spec)))
        coeff[1:] = (pywt.threshold(i, value=uthesh, mode='soft') for i in coeff[1:])  # 将噪声滤波
        specSmooth = pywt.waverec(coeff, wavelet, mode)  # 将信号进行小波重构
        specSmooth = np.array(specSmooth)

        return specSmooth

    def lowpass_denoise(self, spec, b, a):
        b1, a1 = signal.butter(b, a, 'lowpass')
        return signal.filtfilt(b1, a1, spec)

    def emd(self,spec):

        imf = []
        kkk = 0
        while not self.ismonotonic(spec):
            x1 = spec
            sd = np.inf

            while sd > 0.1 or (not self.isImf(x1)):

                self.isImf(x1)
                s1 = self.getspline(x1)  # emax(t)
                s2 = -self.getspline(-1 * x1)  # emin(t)
                # x2 = x1 - (s1 + s2) / 2
                x2 = x1 - (s1 + (s2 - s1) * 1 + s1) / 2
                sd = np.sum((x1 - x2) ** 2) / np.sum(x1 ** 2)
                x1 = x2

                kkk += 1
                if kkk > 500:
                    break

            imf.append(x1)
            spec = spec - x1
        imf.append(spec)
        return imf

    def getspline(self,x):
        N = np.size(x)
        peaks = self.findpeaks(x)

        if (len(peaks) <= 3):
            if (len(peaks) < 2):
                peaks = np.concatenate(([0], peaks))
                peaks = np.concatenate((peaks, [N - 1]))
            t = interpolate.splrep(peaks, y=x[peaks], w=None, xb=None, xe=None, k=len(peaks) - 1)
            return interpolate.splev(np.arange(N), t)
        t = interpolate.splrep(peaks, y=x[peaks])
        return interpolate.splev(np.arange(N), t)

    def isImf(self,x):
        N = np.size(x)
        pass_zero = np.sum(x[0:N - 2] * x[1:N - 1] < 0)
        peaks_num = np.size(self.findpeaks(x)) + np.size(self.findpeaks(-x))
        if abs(pass_zero - peaks_num) > 1:
            return False
        else:
            return True

    def findpeaks(self,x):
        return signal.argrelextrema(x, np.greater)[0]

    def ismonotonic(self,x):
        max_peaks = signal.argrelextrema(x, np.greater)[0]
        min_peaks = signal.argrelextrema(x, np.less)[0]
        all_num = len(max_peaks) + len(min_peaks)
        if all_num > 0:
            return False
        else:
            return True




