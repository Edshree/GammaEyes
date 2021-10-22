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
import statsmodels.api as sm
class geFSA:

    def LLS(self, spec_lib, cont_lib, spec):
        pass

    def pls(self,spec_lib, cont_lib, spec,k):
        '''
        function:
            - 该函数为主元分析降维函数
        input:
            - inputMat:  传入的是一个numpy的矩阵格式，行表示样本数，列表示特征
            - k:  表示取前k个特征值相应的特征向量
        return:
            - finalData：參数一指的是返回的低维矩阵，相应于输入參数二
            - reconData：參数二相应的是移动坐标轴后的矩阵

        '''
        m11, n11 = np.shape(spec_lib)
        matrix = np.zeros((m11, n11 + 1))
        matrix[:, :n11] = spec_lib
        matrix[:, n11] = spec


        # pca = sm.PCA(matrix, ncomp=2)
        # X_reconst = pca.projection
        # print(np.shape(matrix), np.shape(X_reconst))
        inputMat = matrix.T
        average = np.mean(inputMat,axis=0)      # 求每一行数据的均值
        m, n = np.shape(inputMat)               # m，n 为数据的维数
        #print("m,n",m,n)
        avgs = np.tile(average, (m, 1))
        data_adjust = inputMat - avgs
        covX = np.cov(data_adjust.T)  # 计算协方差矩阵
        featValue, featVec = np.linalg.eig(covX)  # 求解协方差矩阵的特征值和特征向量
        index = np.argsort(-featValue)  # 依照featValue进行从大到小排序

        if k > n:
            print("k must lower than feature number")
            return
        else:
            # 注意特征向量时列向量。而numpy的二维矩阵(数组)a[m][n]中，a[1]表示第1行值
            selectVec = np.matrix(featVec.T[index[:k]])  # 所以这里须要进行转置
            finalData = data_adjust * selectVec.T
            reconData = (finalData * selectVec) + average
            #print("finalData shape ",finalData.shape)
            lib_pca,spec_pca = finalData[:m-1,:],finalData[m-1,:]
            #print("lib_pca shape ", lib_pca.shape,spec_pca.shape)
            solve = np.linalg.lstsq(lib_pca.T, spec_pca.T)[0]
            # print(solve[0,0])

            result = np.dot(cont_lib.T, solve)

            spec_solve = np.dot(lib_pca.T, solve)
            spec_ori_mean = np.average(spec_pca)
            ssr = np.sum(np.power((spec_solve - spec_ori_mean), 2))
            sst = np.sum(np.power((spec_pca - spec_ori_mean), 2))
            R2 = ssr / sst


            result = np.real(result)
            R2 = np.real(R2)
            spec_solve = np.real(spec_solve)
            spec_pca = np.real(spec_pca).T
            # print("solve shape ", solve.shape)
            # print("result shape ", result.shape)
            # print("spec_solve ", spec_solve.shape)
            # print("spec_pca ", spec_pca.shape)
            # print("R2 ", R2.shape)
            result_list = []
            for i in range(np.shape(result)[0]):
                result_list.append(result[i,0])
            #print(np.shape(cont_lib),np.shape(solve),np.shape(result))

            #print(finalData.shape,reconData.shape)

        return result_list,solve,spec_solve,spec_pca,R2






