# -*- coding: utf-8 -*-

# GammaEyes
#
# Created at: 2021.07.19
#
# A class for gamma spectrum
import numpy as np
import pywt
from statsmodels.robust import mad
from scipy import signal

class geBroaden:

    def broaden_sampling_spec(self, spec_edep, energy_list, fwhm_list):
        #   ?????
        sigma_list = fwhm_list/2.355
        edep_now = []
        sums = np.sum(spec_edep)
        now = 0
        per_10 = 0.1
        print(sums)
        for i in range(len(energy_list)):

            temp = np.random.normal(energy_list[i],sigma_list[i],int(spec_edep[i]))
            now += int(spec_edep[i])

            for j in range(len(temp)):
                edep_now.append(temp[j])

            if now/sums>=per_10:
                print(per_10)
                per_10+=0.1
        #print("edep_now")
        per_10 = 0.1
        spec_broaden = np.zeros_like(energy_list)

        for i in range(len(edep_now)):
            for j in range(len(energy_list) - 1):
                if edep_now[i] >= energy_list[j] and edep_now[i] < energy_list[j + 1]:
                    spec_broaden[j] += 1
                    break
            if i>per_10*sums:
                print(per_10)
                per_10 += 0.1
            print(i)
        #print("finish")
        return spec_broaden

    def broaden_sampling(self, edep_fp, energy_list, fwhm_list):
        sigma_list = fwhm_list/2.355
        edep_now = []
        for text in self.open_txt(edep_fp):
            try:
                # strs = text.split(" ")
                edep_ori = float(text)

                for i in range(len(energy_list)-1):
                    if edep_ori>=energy_list[i] and edep_ori<energy_list[i+1]:

                        edep_now.append(np.random.normal(edep_ori,sigma_list[i]))
                        # np.random.normal(edep_now, sigma_list[i])
                        break
            except:
                pass

        spec_broaden = np.zeros_like(energy_list)
        for i in range(len(edep_now)):
            for j in range(len(energy_list)-1):
                if edep_now[i] >= energy_list[j] and edep_now[i] < energy_list[j + 1]:
                    spec_broaden[j]+=1
                    break

        return spec_broaden

    def broaden_conv_spec(self, spec_edep, energy_list, fwhm_list):
        sigma_list = fwhm_list/2.355
        resopnse_mat = np.zeros((len(energy_list),len(energy_list)))
        for i in range(len(energy_list)):
            resopnse_mat[:,i] = (1/sigma_list[i]/np.sqrt(2*np.pi)*np.exp(-np.power(energy_list-energy_list[i],2)/2/sigma_list[i]/sigma_list[i]))

        spec_broaden = np.dot(resopnse_mat,np.array(spec_edep).T)
        zoom_k = np.sum(spec_broaden)/np.sum(spec_edep)
        spec_broaden = spec_broaden/zoom_k
        print(np.sum(spec_edep),np.sum(spec_broaden))

        return spec_broaden

    def open_txt(self, file_name):
        with open(file_name, 'r+') as f:
            while True:

                line = f.readline()
                if not line:
                    return

                yield line.strip()





