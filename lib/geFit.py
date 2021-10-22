# -*- coding: utf-8 -*-
"""
==========================================
GammaEyes Version 1.0.1                 ==
Created at: 2021.07.19                  ==
Author@Aiyun Sun                        ==
Email say@insmea.cn                     ==
==========================================
GammaEyes is an open source software for
gamma spectrum processing and analysis.

=============== geFit ====================

A class for ROI fitting in a spectrum

"""
import numpy as np
from scipy.optimize import least_squares
import math

class geFit:
    # ==========================================================
    # 1. Scintillator
    def sci_gauss(self,amp,sigma,e0,x_l):
        return amp*np.exp(-(x_l-e0)**2/(2*sigma**2))

    def sci_bg(self,bg,x_l):
        return [bg]*len(x_l)

    def sci_erfc(self,x_l,step,sigma,e0):
        y = np.zeros_like(x_l)
        for i in range(len(y)):
            y[i] = math.erfc((x_l[i]-e0)/(math.sqrt(2)*sigma))
        return np.dot(step,y)

    def sci_peak_fit(self, x_list, y_list, bg_para_init, peak_para_init,energy_fixed):
        self.ef = energy_fixed
        x_list_back = np.linspace(x_list[0], x_list[-1], len(x_list)*100)
        # =================================================
        # energy fixed
        if self.ef:
            self.energy = []
            p0 = [bg_para_init]
            pl = [0]
            pr = [np.inf]

            for i in range(len(peak_para_init)):
                # Amp
                pl.append(0)
                pr.append(np.inf)
                # sigma
                pl.append(0)
                pr.append(np.inf)
                # step
                pl.append(0)
                pr.append(np.inf)

                self.energy.append(peak_para_init[i][0])
                p0.append(peak_para_init[i][1])
                p0.append(peak_para_init[i][2])
                p0.append(peak_para_init[i][3])

            para = least_squares(self.error_sci, p0, args=(x_list, y_list), bounds=(pl, pr))

            para_back = para.x
            para_back_2 = []
            bg = para_back[0]
            para_back_2.append(bg)

            bg_back = self.sci_bg(bg, x_list_back)
            peak_gauss = []
            row_n = int((len(para_back) - 1) / 3)
            for i in range(row_n):
                e0 = self.energy[i]
                amp, sigma, step = para_back[1 + i * 3], para_back[2 + i * 3], para_back[3 + i * 3]
                peak_gauss.append(
                    [self.sci_gauss(amp, sigma, e0, x_list_back), self.sci_erfc(x_list_back, step, sigma, e0)])

                para_back_2.append(e0)
                para_back_2.append(amp)
                para_back_2.append(sigma)
                para_back_2.append(step)
            R2 = self.__R2(y_list, self.sci_peak(para_back, x_list))
            return para_back_2, x_list_back, bg_back, peak_gauss, R2


        # =================================================
        # energy not fixed
        else:
            p0 = [bg_para_init]
            pl=[0]
            pr=[np.inf]

            for i in range(len(peak_para_init)):
                # E0
                pl.append(0)
                pr.append(np.inf)
                # Amp
                pl.append(0)
                pr.append(np.inf)
                # sigma
                pl.append(0)
                pr.append(np.inf)
                # step
                pl.append(0)
                pr.append(np.inf)
                for j in range(len(peak_para_init[i])):
                    p0.append(peak_para_init[i][j])
            # print(pl)
            # print(p0)
            # print(pr)

            para = least_squares(self.error_sci,p0,args=(x_list,y_list),bounds=(pl,pr))

            para_back = para.x
            # print("back: ",para_back)
            bg = para_back[0]
            bg_back = self.sci_bg(bg,x_list_back)
            # bg_step = self.sci_erfc(x_list_back,s)
            peak_gauss = []
            row_n = int((len(para_back) - 1) / 4)
            for i in range(row_n):
                e0, amp, sigma,step = para_back[1+i*4],para_back[2+i*4],para_back[3+i*4],para_back[4+i*4]
                peak_gauss.append([self.sci_gauss(amp,sigma,e0,x_list_back),self.sci_erfc(x_list_back,step,sigma,e0)])
            R2 = self.__R2(y_list,self.sci_peak(para_back,x_list))
            return para_back,x_list_back,bg_back,peak_gauss,R2

    def sci_peak_ef(self,p,x):
        bg = p[0]
        y = self.sci_bg(bg, x)

        row_n = int((len(p) - 1) / 3)
        for i in range(row_n):
            e0 = self.energy[i]
            amp, sigma, step = p[1 + i * 3], p[2 + i * 3], p[3 + i * 3]
            y = y + self.sci_gauss(amp, sigma, e0, x) + self.sci_erfc(x, step, sigma, e0)
        return y

    def sci_peak(self,p,x):
        bg = p[0]
        y = self.sci_bg(bg, x)
        row_n = int((len(p)-1)/4)
        for i in range(row_n):
            e0,amp,sigma,step = p[1+i*4],p[2+i*4],p[3+i*4],p[4+i*4]
            y = y+self.sci_gauss(amp,sigma,e0,x)+self.sci_erfc(x,step,sigma,e0)
        return y

    def error_sci(self,p,x,y):
        # result = None
        if self.ef:
            return self.sci_peak_ef(p,x)-y
        else:
            return self.sci_peak(p,x)-y

    # ================================================================
    # 2. Semiconductor
    def semi_erfc(self,x):
        y = np.zeros_like(x)
        for i in range(len(y)):
            y[i] = math.erfc(x[i])
        return y

    def semi_gauss(self, x_l, Amp, e0, sigma):
        return Amp * np.exp(-(x_l - e0) ** 2 / (2 * sigma ** 2))

    def semi_left_skew(self, x_l, alpha, sigma, beta, e0):
        temp = np.sqrt(np.pi) / 2 * alpha * np.sqrt(2) * sigma * np.exp(
            (sigma / beta / np.sqrt(2)) ** 2 + (x_l - e0) / beta) * self.semi_erfc(
            sigma / beta / np.sqrt(2) + (x_l - e0) / sigma / np.sqrt(2))
        return temp

    def semi_right_skew(self, x_l, phi, sigma, rou, e0):
        temp = np.sqrt(np.pi) / 2 * phi * np.sqrt(2) * sigma * np.exp(
            (sigma / rou / np.sqrt(2)) ** 2 - (x_l - e0) / rou) * self.semi_erfc(
            sigma / rou / np.sqrt(2) - (x_l - e0) / sigma / np.sqrt(2))
        return temp

    def semi_tail(self, x_l, t, sigma, v, e0):
        return np.sqrt(np.pi) / 2 * t * np.sqrt(2) * sigma * np.exp(
            (sigma / v / np.sqrt(2)) ** 2 + (x_l - e0) / v) * self.semi_erfc(
            sigma / v / np.sqrt(2) + (x_l - e0) / sigma / np.sqrt(2))

    def semi_step(self, x_l, SIGMA, sigma, e0):
        steps = np.sqrt(np.pi) / 2 * SIGMA * np.sqrt(2) * sigma * self.semi_erfc((x_l - e0) / sigma)
        return steps

    def semi_trian(self,x_l,Q,t,sigma,e0):
        temp = 0.5*Q*np.exp((e0-x_l)/t)*self.semi_erfc(sigma/np.sqrt(2)/t-(x_l-e0)/sigma/np.sqrt(2))
        return temp

    def semi_boron(self,x_l,N0,lamD,v0,Emax,e0,c):
        #c = 300000000
        y = np.zeros_like(x_l)
        for i in range(len(x_l)):
            if abs(x_l[i]-e0)<=Emax:
                y[i] = 0.5*c*N0/e0/v0*lamD*(1-np.power(c*np.abs(x_l[i]-e0)/e0/v0,1/lamD))
        return y

    def semi_peak_fit(self,x_list, y_list, bg_para_init, peak_para_init,energy_fixed,r_skew_used):
        self.ru = r_skew_used
        self.ef = energy_fixed
        x_list_back = np.linspace(x_list[0], x_list[-1], len(x_list) * 100)

        # =================================================
        if self.ef:                        # energy fixed
            self.energy = []
            p0 = [bg_para_init]
            pl = [0]
            pr = [np.inf]

            for i in range(len(peak_para_init)):
                # Amp
                pl.append(0)
                pr.append(np.inf)
                # sigma
                pl.append(0)
                pr.append(np.inf)
                # A l_skew
                pl.append(0)
                pr.append(np.inf)
                # B l_skew
                pl.append(0)
                pr.append(np.inf)
                # # A r_skew
                # pl.append(-2)
                # pr.append(np.inf)
                # # B r_skew
                # pl.append(-2)
                # pr.append(np.inf)
                # A tail
                pl.append(0)
                pr.append(np.inf)
                # B tail
                pl.append(0)
                pr.append(np.inf)
                # A step
                pl.append(0)
                pr.append(np.inf)

                self.energy.append(peak_para_init[i][0])
                p0.append(peak_para_init[i][1])
                p0.append(peak_para_init[i][2])
                p0.append(peak_para_init[i][3])
                p0.append(peak_para_init[i][4])
                p0.append(peak_para_init[i][5])
                p0.append(peak_para_init[i][6])
                p0.append(peak_para_init[i][7])
                # p0.append(peak_para_init[i][8])
                # p0.append(peak_para_init[i][9])

            para = least_squares(self.error_semi, p0, args=(x_list, y_list), bounds=(pl, pr))

            para_back = para.x
            para_back_2 = []
            bg = para_back[0]
            para_back_2.append(bg)

            bg_back = self.sci_bg(bg, x_list_back)
            peak_gauss = []
            row_n = int((len(para_back) - 1) / 7)
            for i in range(row_n):
                e0 = self.energy[i]
                amp, sigma, a_l_sk, b_l_sk, a_t, b_t, a_step = para_back[1 + i * 7], para_back[
                    2 + i * 7], para_back[3 + i * 7], para_back[4 + i * 7], para_back[5 + i * 7], para_back[6 + i * 7], \
                                                                    para_back[7 + i * 7]

                peak_gauss.append(
                    [self.semi_gauss(x_list_back, amp, e0, sigma),
                     self.semi_left_skew(x_list_back, a_l_sk, sigma, b_l_sk, e0),
                     #self.semi_right_skew(x_list_back, a_r_sk, sigma, b_r_sk, e0),
                     self.semi_tail(x_list_back, a_t, sigma, b_t, e0),
                     self.semi_step(x_list_back, a_step, sigma, e0)
                     ])

                para_back_2.append(e0)
                para_back_2.append(amp)
                para_back_2.append(sigma)
                para_back_2.append(a_l_sk)
                para_back_2.append(b_l_sk)
                # para_back_2.append(a_r_sk)
                # para_back_2.append(b_r_sk)
                para_back_2.append(a_t)
                para_back_2.append(b_t)
                para_back_2.append(a_step)


            R2 = self.__R2(y_list, self.semi_peak(para_back, x_list))
            return para_back_2, x_list_back, bg_back, peak_gauss, R2
        else:

            p0 = [bg_para_init]
            pl = [0]
            pr = [np.inf]

            for i in range(len(peak_para_init)):
                # E0
                pl.append(0)
                pr.append(np.inf)
                # Amp
                pl.append(0)
                pr.append(np.inf)
                # sigma
                pl.append(0)
                pr.append(np.inf)
                # A l_skew
                pl.append(0)
                pr.append(np.inf)
                # B l_skew
                pl.append(0)
                pr.append(np.inf)
                # # A r_skew
                # pl.append(-2)
                # pr.append(np.inf)
                # # B r_skew
                # pl.append(-2)
                # pr.append(np.inf)
                # A tail
                pl.append(0)
                pr.append(np.inf)
                # B tail
                pl.append(0)
                pr.append(np.inf)
                # A step
                pl.append(0)
                pr.append(np.inf)

                for j in range(len(peak_para_init[i])):
                    p0.append(peak_para_init[i][j])

            para = least_squares(self.error_semi, p0, args=(x_list, y_list), bounds=(pl, pr))

            para_back = para.x
            para_back_2 = []
            bg = para_back[0]
            para_back_2.append(bg)

            bg_back = self.sci_bg(bg, x_list_back)
            peak_gauss = []
            row_n = int((len(para_back) - 1) / 8)

            for i in range(row_n):
                e0,amp, sigma, a_l_sk, b_l_sk, a_t, b_t, a_step = para_back[1 + i * 8], para_back[2 + i * 8], para_back[3 + i * 8], \
                                                                               para_back[4 + i * 8], para_back[5 + i * 8], para_back[6 + i * 8], \
                                                                               para_back[7 + i * 8],para_back[8 + i * 8]

                peak_gauss.append(
                        [self.semi_gauss(x_list_back, amp, e0, sigma),
                         self.semi_left_skew(x_list_back, a_l_sk, sigma, b_l_sk, e0),
                         self.semi_tail(x_list_back, a_t, sigma, b_t, e0),
                         self.semi_step(x_list_back, a_step, sigma, e0)
                         ])

                para_back_2.append(e0)
                para_back_2.append(amp)
                para_back_2.append(sigma)
                para_back_2.append(a_l_sk)
                para_back_2.append(b_l_sk)
                para_back_2.append(a_t)
                para_back_2.append(b_t)
                para_back_2.append(a_step)

            R2 = self.__R2(y_list, self.semi_peak(para_back, x_list))
            return para_back_2, x_list_back, bg_back, peak_gauss, R2

    def semi_peak_ef(self,p,x):
        bg = p[0]
        y = self.sci_bg(bg, x)

        row_n = int((len(p) - 1) / 7)
        for i in range(row_n):
            e0 = self.energy[i]
            amp, sigma, a_l_sk,b_l_sk,a_t,b_t,a_step = p[1 + i * 7], p[2 + i * 7], p[3 + i * 7], p[4 + i * 7], p[5 + i * 7], p[6 + i * 7], p[7 + i * 7]
            y = y + self.semi_gauss(x,amp,e0,sigma) + self.semi_left_skew(x,a_l_sk,sigma,b_l_sk,e0) \
                + self.semi_tail(x,a_t,sigma,b_t,e0)+self.semi_step(x,a_step,sigma,e0)
            # if self.ru:
            #     y = y + self.semi_right_skew(x,a_r_sk,b_r_sk)

        return y

    def semi_peak(self,p,x):
        bg = p[0]
        y = self.sci_bg(bg, x)
        #print("sss ",np.shape(y))
        row_n = int((len(p) - 1) / 8)
        for i in range(row_n):
            e0, amp, sigma, a_l_sk, b_l_sk, a_t, b_t, a_step = p[1 + i * 8], p[2 + i * 8], p[3 + i * 8], p[
                4 + i * 8], p[5 + i * 8], p[6 + i * 8], p[7 + i * 8], p[8 + i * 8]
            y = y + self.semi_gauss(x, amp, e0, sigma) + self.semi_left_skew(x, a_l_sk, sigma, b_l_sk, e0) \
                + self.semi_tail(x, a_t, sigma, b_t, e0) + self.semi_step(x, a_step, sigma, e0)
        #print("sss11 ", np.shape(y))
        return y

    def error_semi(self,p,x,y):
        #print("error semi")
        if self.ef:
            return self.semi_peak_ef(p,x)-y
        else:
            #print("error semi 1")
            return self.semi_peak(p,x)-y


    def __R2(self,y0,yf):
        y0_mean = np.average(y0)
        ssr = np.sum(np.power((yf-y0_mean),2))
        sst = np.sum(np.power((y0-y0_mean),2))
        return ssr/sst



#
# Pos[0]=1071.249Energy[0]=1606.766Amp[0]=2920.87Area[0]=12447DEL=1.393FWHM=2.319AST=1.78BST=0.35ART=0.90BRT=1.50ALT=7.0E-02BLT=28.72SIG=9.3E-04BLN=2133.52
