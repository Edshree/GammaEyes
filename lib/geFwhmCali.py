# -*- coding: utf-8 -*-

# GammaEyes
#
# Created at: 2021.07.19
#
# A class for gamma spectrum
import numpy as np
from scipy.optimize import least_squares

class geFwhmCali:
    # ====================================================================================
    def MCNP_cali(self, x_list, y_list,x_out_list):
        p0 = [0.001,0.008,0.08]
        para = least_squares(self.error_mcnp,p0,args=(x_list,y_list))

        return self.mcnp_model(para.x,x_out_list),para.x

    def mcnp_model(self,p,x):
        a, b, c = p
        return a + np.sqrt(b * (x + c * np.power(x,2)))

    def error_mcnp(self,p,x,y):
        return self.mcnp_model(p,x)-y

    # ====================================================================================
    def CEAR_cali(self, x_list, y_list,x_out_list):
        p0=[1,1]
        para = least_squares(self.error_cear, p0, args=(x_list, y_list))

        return self.cear_model(para.x, x_out_list), para.x

    def cear_model(self,p,x):
        d,e = p
        return d*np.power(x,e)

    def error_cear(self,p,x,y):
        return self.cear_model(p,x)-y

    # ====================================================================================
    def LINEAR_cali(self, x_list, y_list, x_out_list):
        p0 = [1, 1]
        para = least_squares(self.error_linear, p0, args=(x_list, y_list))
        return self.linear_model(para.x, x_out_list), para.x

    def linear_model(self, p, x):
        k, b = p
        return np.dot(k,x)+ b

    def error_linear(self,p,x,y):
        return self.linear_model(p, x)-y



