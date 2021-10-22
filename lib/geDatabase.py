# -*- coding: utf-8 -*-

# GammaEyes
#
# Created at: 2021.07.19
#
# A class for gamma spectrum
import os
import pandas as pd
import numpy as np

# fp = os.path.abspath(os.path.join(os.getcwd(), ".."))+"\\database\\t.txt"

class geDatabase:

    def __init__(self):
        self.current_path = os.path.dirname(__file__)

    def isotope_Z(self,z):
        data = pd.read_table(self.current_path + "\\database\\isotope.dat",
                             names=["Ele", 'Iso', 'Z', "A", 'Abun_tt', 'Abun_v','DAbun', 'Sigma_tt', 'Sigma_v', 'DSigma',
                                    'g_factor', 'N_gammas'], sep='\t',
                             encoding='utf-8'
                             )
        data_z = data[data["Z"] == z]
        data_z = np.array(data_z)
        return data_z

    def PGAA_Z(self,z):
        # self.path + "//promptgammas.dat"
        data = pd.read_table(self.current_path+"\\database\\promptgammas.dat",
                             names=["A",'Iso','Z',"T",'E(gamma)_tt','E(gamma)_v','Sigma_tt','Sigma_v','DSigma','k0_tt','k0_v','Dk0'], sep='\t',
                             encoding='utf-8'
                             )
        data_z = data[data["Z"]==z]
        data_z = np.array(data_z)
        return data_z

    def decay_Z(self,z):
        # self.path + "//promptgammas.dat"
        data = pd.read_table(self.current_path+"\\database\\dacay.dat",
                             names=["A",'Iso','Z',"T",'E(gamma)_tt','E(gamma)_v','Sigma_tt','Sigma_v','DSigma','half_life_tt','half_life_s','k0_tt','k0_v','Dk0'], sep='\t',
                             encoding='utf-8'
                             )
        data_z = data[data["Z"]==z]
        data_z = np.array(data_z)
        return data_z


