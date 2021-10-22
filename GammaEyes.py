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

=============== Main ====================
"""

# ======================================================================
# Import the required modules
import sys, os
# PyQt5 modules
from PyQt5.QtWidgets import *
from PyQt5 import sip, QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QMenu, QApplication, QTableWidgetItem)
# geGui modules
from geGui import Ui_MainWindow
# ge modules
from lib.geDenoise import geDenoise
from lib.geFindPeaks import geFindpeaks
from lib.geFwhmCali import geFwhmCali
from lib.geStable import geStabilization
from lib.geBroaden import geBroaden
from lib.geMCReader import geMCReader
from lib.geFit import geFit
from lib.geDatabase import geDatabase
from lib.geRWIO import geRWIO
from lib.geFSA import geFSA
# Else
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar



class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # ==========================================================================================
        # Setting interface conversion
        self.stackedWidget.setCurrentIndex(0)
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.pushButton_5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.pushButton_6.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.pushButton_7.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))

        self.cbx_fsa_wlls_type.currentIndexChanged.connect(lambda: self.slot_cbx_fsa_wlls_change())
        # ==========================================================================================
        # Table Setting
        # ------------------
        # Table 1
        # set customMenu
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.showCustomMenu)
        # self.setLayout(conLayout)
        self.contextMenu = QMenu(self)
        self.ADD = self.contextMenu.addAction('Add')
        self.DELE = self.contextMenu.addAction('Delete')

        self.ADD.triggered.connect(lambda: self.table_add(self.tableWidget))
        self.DELE.triggered.connect(lambda: self.table_delete(self.tableWidget))

        # --------
        # Table 2
        self.table_eva_fwhm_cr.setContextMenuPolicy(Qt.CustomContextMenu)  ######
        self.table_eva_fwhm_cr.customContextMenuRequested.connect(self.showCustomMenu1)  ####

        self.contextMenu1 = QMenu(self)
        self.ADD1 = self.contextMenu1.addAction('Add')
        self.DELE1 = self.contextMenu1.addAction('Delete')

        self.ADD1.triggered.connect(lambda: self.table_add(self.table_eva_fwhm_cr))
        self.DELE1.triggered.connect(lambda: self.table_delete(self.table_eva_fwhm_cr))

        # --------
        # Table 3
        self.table_eva_fwhm_ln.setContextMenuPolicy(Qt.CustomContextMenu)  ######
        self.table_eva_fwhm_ln.customContextMenuRequested.connect(self.showCustomMenu2)  ####
        self.contextMenu2 = QMenu(self)
        self.ADD2 = self.contextMenu2.addAction('Add')
        self.DELE2 = self.contextMenu2.addAction('Delete')
        self.ADD2.triggered.connect(lambda: self.table_add(self.table_eva_fwhm_ln))
        self.DELE2.triggered.connect(lambda: self.table_delete(self.table_eva_fwhm_ln))

        # --------
        # Table 4
        self.table_fit_sci.setContextMenuPolicy(Qt.CustomContextMenu)  ######
        self.table_fit_sci.customContextMenuRequested.connect(self.showCustomMenu3)  ####
        self.contextMenu3 = QMenu(self)
        self.ADD3 = self.contextMenu3.addAction('Add')
        self.DELE3 = self.contextMenu3.addAction('Delete')
        self.ADD3.triggered.connect(lambda: self.table_add(self.table_fit_sci))
        self.DELE3.triggered.connect(lambda: self.table_delete(self.table_fit_sci))

        self.table_fit_semi_p.setContextMenuPolicy(Qt.CustomContextMenu)  ######
        self.table_fit_semi_p.customContextMenuRequested.connect(self.showCustomMenu4)  ####
        self.contextMenu4 = QMenu(self)
        self.ADD4 = self.contextMenu4.addAction('Add')
        self.DELE4 = self.contextMenu4.addAction('Delete')
        self.ADD4.triggered.connect(lambda: self.table_add(self.table_fit_semi_p))
        self.DELE4.triggered.connect(lambda: self.table_delete(self.table_fit_semi_p))


        # --------
        # Table 5
        self.table_data_pgnaa.setContextMenuPolicy(Qt.CustomContextMenu)  ######
        self.table_data_pgnaa.customContextMenuRequested.connect(self.showCustomMenuPgaa)  ####
        self.contextMenuPgaa = QMenu(self)
        self.Show = self.contextMenuPgaa.addAction('Show selected lines')
        self.Show.triggered.connect(lambda: self.table_show(self.table_data_pgnaa))

        # --------
        # Table 6
        self.table_data_decay.setContextMenuPolicy(Qt.CustomContextMenu)  ######
        self.table_data_decay.customContextMenuRequested.connect(self.showCustomMenuDecay)  ####
        self.contextMenuDecay = QMenu(self)
        self.Show1 = self.contextMenuDecay.addAction('Show selected lines')
        self.Show1.triggered.connect(lambda: self.table_show(self.table_data_decay))


        # =======================================================================================
        # slot connect

        # ----- toolbar -----
        self.pushButton_11.clicked.connect(lambda: self.slot_btn_fig_zoom())
        self.pushButton_12.clicked.connect(lambda: self.slot_btn_fig_zoom_back())
        self.pushButton_13.clicked.connect(lambda: self.slot_btn_fig_zoom_home())
        self.pushButton_14.clicked.connect(lambda: self.slot_btn_fig_parameters())
        self.pushButton_18.clicked.connect(lambda: self.slot_btn_fig_save())
        self.pushButton_17.clicked.connect(lambda: self.slot_btn_data_back())
        self.pushButton_16.clicked.connect(lambda: self.slot_btn_data_home())
        self.pushButton_15.clicked.connect(lambda: self.slot_btn_energy_show())

        # ----- start -----
        self.pushButton_8.clicked.connect(lambda: self.slot_btn_open_file())
        self.pushButton_9.clicked.connect(lambda: self.slot_btn_save_file())
        self.pushButton_10.clicked.connect(lambda: self.slot_btn_open_energy_file())

        # ----- evaluation -----
        self.pbt_eva_cali_linear_do.clicked.connect(lambda: self.slot_btn_eva_cali_linear_do())
        self.pbt_eva_cali_linear_save.clicked.connect(lambda: self.slot_btn_eva_cali_linear_save())
        self.pbt_eva_cali_nonlinear_do.clicked.connect(lambda: self.slot_btn_eva_cali_nonlinear_do())
        self.pbt_eva_cali_nonlinear_save.clicked.connect(lambda: self.slot_btn_eva_cali_nonlinear_save())

        self.pbt_eva_fwhm_mc_do.clicked.connect(lambda: self.slot_btn_eva_fwhm_mcnp())
        self.pbt_eva_fwhm_cr_do.clicked.connect(lambda: self.slot_btn_eva_fwhm_cear())
        self.pbt_eva_fwhm_ln_do.clicked.connect(lambda: self.slot_btn_eva_fwhm_linear())

        # ----- process -----
        self.pbt_proc_findp_auto_do.clicked.connect(lambda: self.slot_btn_proc_findp_auto())
        self.pbt_proc_findp_auto_do_2.clicked.connect(lambda: self.slot_btn_proc_findp_auto_cwt())

        self.pbt_proc_denoi_fit_do.clicked.connect(lambda: self.slot_btn_proc_fit())
        self.pbt_proc_denoi_wt_do.clicked.connect(lambda: self.slot_btn_proc_wavelet())
        self.pbt_proc_denoi_lp_do.clicked.connect(lambda: self.slot_btn_proc_lowpass())

        self.pbt_proc_denoi_emd1.clicked.connect(lambda: self.slot_btn_proc_emd_1())
        self.pbt_proc_denoi_emd_do.clicked.connect(lambda: self.slot_btn_proc_emd_do())

        self.pbt_proc_sta_3rp_do.clicked.connect(lambda: self.slot_btn_proc_sta_3rp_do())
        self.pbt_proc_sta_2rp_do.clicked.connect(lambda: self.slot_btn_proc_sta_2rp_do())

        # ----- FSA -----
        self.pbt_fsa_lls_lib.clicked.connect(lambda: self.slot_btn_fsa_lls_lib())
        self.pbt_fsa_lls_compo.clicked.connect(lambda: self.slot_btn_fsa_lls_compos())
        self.pbt_fsa_lls_spe.clicked.connect(lambda: self.slot_btn_fsa_lls_spec())
        self.pbt_fsa_lls_solve.clicked.connect(lambda: self.slot_btn_fsa_lls_solve())

        self.pbt_fsa_wlls_lib.clicked.connect(lambda: self.slot_btn_fsa_wlls_lib())
        self.pbt_fsa_wlls_cont.clicked.connect(lambda: self.slot_btn_fsa_wlls_compos())
        self.pbt_fsa_wlls_spe.clicked.connect(lambda: self.slot_btn_fsa_wlls_spec())
        self.pbt_fsa_wlls_w.clicked.connect(lambda: self.slot_btn_fsa_wlls_weight())
        self.pbt_fsa_wlls_solve.clicked.connect(lambda: self.slot_btn_fsa_wlls_solve())

        self.pbt_fsa_pca_lib.clicked.connect(lambda: self.slot_btn_fsa_pca_lib())
        self.pbt_fsa_pca_cont.clicked.connect(lambda: self.slot_btn_fsa_pca_compos())
        self.pbt_fsa_pca_spe.clicked.connect(lambda: self.slot_btn_fsa_pca_spec())
        self.pbt_fsa_pca_do.clicked.connect(lambda: self.slot_btn_fsa_pca_solve())

        # ----- fitting -----
        self.pbt_fit_sci_do.clicked.connect(lambda: self.slot_btn_fit_sci_do())
        self.pbt_fit_sci_do_2.clicked.connect(lambda: self.slot_btn_fit_semi_do())

        # ----- simulation -----
        self.radioButton.clicked.connect(lambda: self.slot_rbn_simu_edep())
        self.radioButton_2.clicked.connect(lambda: self.slot_rbn_simu_spec())
        self.rbt_simu_broaden_conv.clicked.connect(lambda: self.slot_rbn_simu_spec_conv())

        self.pbt_simu_bro_mc_do.clicked.connect(lambda: self.slot_btn_simu_bro_mc_do())
        self.pbt_simu_bro_mc_draw.clicked.connect(lambda: self.slot_btn_simu_bro_mc_draw())
        self.pbt_simu_bro_cr_do.clicked.connect(lambda: self.slot_btn_simu_bro_cr_do())
        self.pbt_simu_bro_cr_draw.clicked.connect(lambda: self.slot_btn_simu_bro_cr_draw())
        self.pbt_simu_bro_ln_do.clicked.connect(lambda: self.slot_btn_simu_bro_ln_do())
        self.pbt_simu_bro_ln_draw.clicked.connect(lambda: self.slot_btn_simu_bro_ln_draw())

        self.pbt_simu_mcr_open.clicked.connect(lambda: self.slot_btn_simu_mcr_open())
        self.pbt_simu_mcr_save.clicked.connect(lambda: self.slot_btn_simu_mcr_save())

        # ----- database -----
        self.pbt_data_pgaa_do.clicked.connect(lambda: self.slot_btn_data_pgnaa_do())
        self.pbt_data_decay_do.clicked.connect(lambda: self.slot_btn_data_decay_do())
        self.pbt_data_iso_do.clicked.connect(lambda: self.slot_btn_data_iso_do())
        # =======================================================================================
        # setting shadow
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(10)  # 阴影半径
        self.effect_shadow.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.pushButton_8.setGraphicsEffect(self.effect_shadow)
        self.effect_shadow2 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow2.setOffset(0, 0)  # 偏移
        self.effect_shadow2.setBlurRadius(10)  # 阴影半径
        self.effect_shadow2.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.pushButton_9.setGraphicsEffect(self.effect_shadow2)
        self.effect_shadow3 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow3.setOffset(0, 0)  # 偏移
        self.effect_shadow3.setBlurRadius(10)  # 阴影半径
        self.effect_shadow3.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.pushButton_10.setGraphicsEffect(self.effect_shadow3)

        self.effect_shadow4 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow4.setOffset(0, 0)  # 偏移
        self.effect_shadow4.setBlurRadius(10)  # 阴影半径
        self.effect_shadow4.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.label_4.setGraphicsEffect(self.effect_shadow4)

        self.effect_shadow5 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow5.setOffset(0, 0)  # 偏移
        self.effect_shadow5.setBlurRadius(10)  # 阴影半径
        self.effect_shadow5.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.label_17.setGraphicsEffect(self.effect_shadow5)

        self.effect_shadow6 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow6.setOffset(0, 0)  # 偏移
        self.effect_shadow6.setBlurRadius(10)  # 阴影半径
        self.effect_shadow6.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.textEdit_8.setGraphicsEffect(self.effect_shadow6)

        self.effect_shadow7 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow7.setOffset(0, 0)  # 偏移
        self.effect_shadow7.setBlurRadius(10)  # 阴影半径
        self.effect_shadow7.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.tabWidget_2.setGraphicsEffect(self.effect_shadow7)

        self.effect_shadow8 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow8.setOffset(0, 0)  # 偏移
        self.effect_shadow8.setBlurRadius(10)  # 阴影半径
        self.effect_shadow8.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.tabWidget_3.setGraphicsEffect(self.effect_shadow8)

        self.effect_shadow9 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow9.setOffset(0, 0)  # 偏移
        self.effect_shadow9.setBlurRadius(10)  # 阴影半径
        self.effect_shadow9.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.tabWidget_4.setGraphicsEffect(self.effect_shadow9)

        self.effect_shadow10 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow10.setOffset(0, 0)  # 偏移
        self.effect_shadow10.setBlurRadius(10)  # 阴影半径
        self.effect_shadow10.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.tabWidget_5.setGraphicsEffect(self.effect_shadow10)

        self.effect_shadow11 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow11.setOffset(0, 0)  # 偏移
        self.effect_shadow11.setBlurRadius(10)  # 阴影半径
        self.effect_shadow11.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.tabWidget_6.setGraphicsEffect(self.effect_shadow11)

        self.effect_shadow12 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow12.setOffset(0, 0)  # 偏移
        self.effect_shadow12.setBlurRadius(10)  # 阴影半径
        self.effect_shadow12.setColor(QtCore.Qt.gray)  # 阴影颜色
        self.tabWidget.setGraphicsEffect(self.effect_shadow12)

        # =======================================================================================
        # canvas config
        self.fig = plt.figure(figsize=(5, 10))
        self.canvas = FC(self.fig)
        # self.ax = self.fig.add_subplot(111)
        self.ax = self.fig.subplots()
        self.fig.subplots_adjust(top=0.93,bottom=0.08,left=0.05,right=0.98,hspace=0,wspace=0)
        self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        self.gridlayout = QGridLayout(self.label_4)  # 继承容器groupBox
        self.gridlayout.addWidget(self.canvas, 0, 1)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.hide()
        self.canvas.mpl_connect("motion_notify_event",self.slot_show_data)

        # =======================================================================================
        # global parameters
        self.spec_now = np.zeros(0)
        self.spec_last = np.zeros(0)
        self.spec_ori = np.zeros(0)

        self.energy = np.zeros(0)

        self.energy_curve_nonlinear = np.zeros(0)
        self.energy_curve_linear = np.zeros(0)

        self.fwhm_curve = np.zeros(0)

        self.flag_energy = False
        self.flag_open_file = False
        self.flas_simu_broaden = 0          # broaden algorithm type 0: sampling 1: conv

        self.simu_bro_edep_fp = ""

    # ===================================================================================
    # 1  SLOT  table operate
    def showCustomMenu(self):
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示
    def showCustomMenu1(self):
        self.contextMenu1.exec_(QCursor.pos())  # 在鼠标位置显示
    def showCustomMenu2(self):
        self.contextMenu2.exec_(QCursor.pos())  # 在鼠标位置显示
    def showCustomMenu3(self):
        self.contextMenu3.exec_(QCursor.pos())  # 在鼠标位置显示
    def showCustomMenu4(self):
        self.contextMenu4.exec_(QCursor.pos())  # 在鼠标位置显示
    def showCustomMenuPgaa(self):
        self.contextMenuPgaa.exec_(QCursor.pos())  # 在鼠标位置显示
    def showCustomMenuDecay(self):
        self.contextMenuDecay.exec_(QCursor.pos())  # 在鼠标位置显示

    def slot_cbx_fsa_wlls_change(self):
        try:
            if self.cbx_fsa_wlls_type.currentText()=="std":
                self.pbt_fsa_wlls_w.setEnabled(False)
                self.let_fsa_wlls_weight.setEnabled(False)
            else:
                self.pbt_fsa_wlls_w.setEnabled(True)
                self.let_fsa_wlls_weight.setEnabled(True)

            if len(self.let_fsa_wlls_lib.text())!=0 and len(self.let_fsa_wlls_cont.text())!=0 and len(self.let_fsa_wlls_spe.text())!=0:
                if self.cbx_fsa_wlls_type.currentText() == "std":
                    self.pbt_fsa_wlls_solve.setEnabled(True)
                elif len(self.let_fsa_wlls_weight.text()) != 0 and self.cbx_fsa_wlls_type.currentText() == "else":
                    self.pbt_fsa_wlls_solve.setEnabled(True)
                else:
                    self.pbt_fsa_wlls_solve.setEnabled(False)
        except BaseException as e:
            QMessageBox.warning(self,
                            "Error!",
                            e.__str__())

    def table_add(self, table):
        try:
            cur_total_row = table.rowCount()
            table.setRowCount(cur_total_row+1)
        except BaseException as e:
            QMessageBox.warning(self,
                            "Error!",
                            e.__str__())

    def table_delete(self, table):
        try:
            selected_indexs = table.selectedIndexes()
            if len(selected_indexs) == 0:
                return
            indexs = []
            for i in range(len(selected_indexs)):
                index_now = selected_indexs[len(selected_indexs)-i-1].row()
                if index_now not in indexs:
                    indexs.append(index_now)
                    table.removeRow(index_now)
        except BaseException as e:
            QMessageBox.warning(self,
                            "Error!",
                            e.__str__())

    def table_show(self, table):
        try:
            selected_indexs = table.selectedIndexes()
            if len(selected_indexs) == 0:
                return
            indexs = []
            Egamma = []
            sigma = []
            for i in range(len(selected_indexs)):
                index_now = selected_indexs[len(selected_indexs) - i - 1].row()
                if index_now not in indexs:
                    indexs.append(index_now)
                    Egamma.append(self.dataBase[index_now,5])
                    sigma.append(self.dataBase[index_now,7])
            self.canvas_update_database(Egamma, sigma)

        except BaseException as e:
            QMessageBox.warning(self,
                            "Error!",
                            e.__str__())

    # ===================================================================================
    # 2  SLOT  canvas

    # ----- canvas -----
    def canvas_update(self):
        self.ax.cla()
        # self.fig.clf()
        self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        # print(len(self.spec_now))
        # print(len(self.spec_last))
        if self.pushButton_15.isChecked():
            if len(self.spec_last) == 0:  # when there is no spec_last
                self.ax.plot(self.energy,self.spec_now, color="red", label="Now")
                self.ax.legend()
                self.canvas.draw()
            else:
                self.ax.plot(self.energy,self.spec_last, color="blue", label="Last")
                self.ax.plot(self.energy,self.spec_now, color="red", label="Now")
                self.ax.legend()
                self.canvas.draw()
        else:
            if len(self.spec_last) == 0:  # when there is no spec_last
                self.ax.plot(self.spec_now, color="red", label="Now")
                self.ax.legend()
                self.canvas.draw()
            else:
                self.ax.plot(self.spec_last, color="blue", label="Last")
                self.ax.plot(self.spec_now, color="red", label="Now")
                self.ax.legend()
                self.canvas.draw()

    def canvas_update_fsa_lib(self,lib):
        m,n = np.shape(lib)
        self.ax.cla()
        self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        if self.pushButton_15.isChecked():
            for i in range(n):
                self.ax.plot(self.energy, lib[:,i])
            self.ax.legend()
            self.canvas.draw()

        else:
            for i in range(n):
                self.ax.plot(lib[:, i])
            self.ax.legend()
            self.canvas.draw()

    def canvas_update_fsa_spec(self,spec):

        self.ax.cla()
        self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        if self.pushButton_15.isChecked():

            self.ax.plot(self.energy, spec)
            self.ax.legend()
            self.canvas.draw()

        else:
            self.ax.plot(spec)
            self.ax.legend()
            self.canvas.draw()

    def canvas_update_findp(self,peaks):
        self.ax.cla()
        # self.fig.clf()
        self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        # print(len(self.spec_now))
        # print(len(self.spec_last))
        if self.pushButton_15.isChecked():
            self.ax.plot(self.energy, self.spec_now, color="red", label="Now")
            for i in range(len(peaks)):
                self.ax.axvline(x=self.energy[peaks[i]],color="green")
            self.ax.legend()
            self.canvas.draw()
        else:
            self.ax.plot(self.spec_now, color="red", label="Now")
            for i in range(len(peaks)):
                self.ax.axvline(x=peaks[i],color="green")
            self.ax.legend()
            self.canvas.draw()

    def canvas_update_energy_curve(self,energy_curve):
        self.ax.cla()
        # self.fig.clf()
        self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

        self.ax.plot(energy_curve,color="red",label="Energy Curve")
        self.ax.legend()
        self.canvas.draw()

    def canvas_update_fit_result(self,points_x,points_y,curve_x,curve_y):
        self.ax.cla()
        # self.fig.clf()
        self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        self.ax.scatter(points_x,points_y,color="red",label="Points")
        self.ax.plot(curve_x,curve_y,color="green",label="Curve")
        self.ax.legend()
        self.canvas.draw()

    def canvas_update_database(self,egamma,sigma):
        if len(self.spec_now)==0:
            self.ax.cla()
            self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

            for i in range(len(egamma)):
                self.ax.plot([egamma[i],egamma[i]],[0,sigma[i]],color="red")
            self.canvas.draw()

        else:
            if len(self.energy)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please choose the energy list")

            max_in_plot = np.max(self.spec_now)

            sigma = sigma/np.max(sigma)*max_in_plot

            self.ax.cla()
            self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

            self.ax.plot(self.energy,self.spec_now,color="blue")

            for i in range(len(egamma)):
                self.ax.plot([egamma[i],egamma[i]],[0,sigma[i]],color="red")
            self.canvas.draw()

    # ===================================================================================
    # 3  SLOT  information out
    # ----- Do -----
    def cmd_out(self,strings):
        self.label_17.setText(strings)

    # ----- Do -----
    def info_out(self, strings):
        self.textEdit_8.setText(strings)

    # =======================================================
    # 4 SLOT  toolbar setting
    def slot_btn_fig_zoom(self):
        try:
            self.toolbar.zoom()
        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fig_zoom_back(self):
        try:
            self.toolbar.back()
        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fig_zoom_home(self):
        try:
            self.toolbar.home()
        except BaseException as e:
            print(e.__str__())

        # self.ax.plot([1, 2, 3, 4], [5, 5, 5, 5])
        # self.canvas.draw()

    def slot_btn_fig_parameters(self):
        try:
            self.toolbar.edit_parameters()
        except BaseException as e:
            print(e.__str__())

    def slot_btn_fig_save(self):
        try:
            self.toolbar.save_figure()
        except BaseException as e:
            print(e.__str__())

    def slot_btn_data_back(self):
        try:
            if len(self.spec_last) != 0:
                self.spec_now = self.spec_last + 0
                self.spec_last = np.zeros(0)

            self.canvas_update()
            self.cmd_out("DO: 已清除上一步操作")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_data_home(self):
        try:
            self.spec_now = self.spec_ori + 0
            self.spec_last = np.zeros(0)

            self.canvas_update()
            self.cmd_out("DO: 已返回原始能谱")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_energy_show(self):
        try:
            if len(self.energy) == 0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please choose the Energy file")
                self.pushButton_15.setChecked(False)
            else:
                self.canvas_update()
                self.cmd_out("DO: Show the Energy")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_show_data(self, event):
        try:
            info = "  " + str(int(event.xdata * 10000) / 10000) + "  " + str(int(event.ydata * 10000) / 10000)
            self.lbl_canvas_data.setText(info)
        except BaseException as e:
            pass
    # ===================================================================================
    # 5  SLOT  Start

    # ----- open the spectrum file -----
    def slot_btn_open_file(self):
        try:
            self.spec_now = np.zeros(0)
            self.spec_last = np.zeros(0)

            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "Open the spectrum",
                                                                "./",  # original path
                                                                "txt (*.txt);;chn (*.Chn);;spe (*.Spe);;mca (*.mca);;tka (*.TKA);;All Files (*)"
                                                                )  # filetype filter

            if fileName_choose == "":
                return
            gr = geRWIO(fileName_choose,filetype.split(" ")[0])

            self.spec_now = gr.spec
            self.spec_ori = self.spec_now+0
            self.flag_open_file = True

            if filetype.split(" ")[0]!="txt" and filetype.split(" ")[0]!="tka":
                self.energy = gr.energy_list

            self.canvas_update()
            self.cmd_out("DO: Open the spectrum: "+fileName_choose)

        except BaseException as e:
            QMessageBox.warning(self,
                            "Error!",
                            e.__str__())

    # ----- open the spectrum file -----
    def slot_btn_save_file(self):
        try:
            if len(self.spec_now)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "There is no spectrum")
                return

            file_path,file_type = QFileDialog.getSaveFileName(self, "Save the spectrum",
                                                    "./spectrum",
                                                    "Text Files (*.txt);;all files(*.*)")

            if file_path == "":
                # print("\n取消选择")
                return
            np.savetxt(file_path, self.spec_now)
            self.cmd_out("DO: Save spectrum at " + file_path)

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    # ----- open the energy file -----
    def slot_btn_open_energy_file(self):
        try:
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "Choose energy file",
                                                                "./",  # 起始路径
                                                                "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

            if fileName_choose == "":
                # print("\n取消选择")
                return
            # label show
            self.energy = np.loadtxt(fileName_choose)
            self.flag_energy = True

            # self.canvas_update()
            self.cmd_out("DO: Open the energy file "+fileName_choose)

        except BaseException as e:
            QMessageBox.warning(self,
                            "Error!",
                            e.__str__())

    # ===================================================================================
    # 6  SLOT  Evaluation
    # 1.calibration
    def slot_btn_eva_cali_linear_do(self):
        try:
            if len(self.spec_now)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please choose spectrum")
                return
            peak1 = [int(self.let_eva_cali_linear_p1.text()),float(self.let_eva_cali_linear_e1.text())]
            peak2 = [int(self.let_eva_cali_linear_p2.text()), float(self.let_eva_cali_linear_e2.text())]

            k = (peak2[1]-peak1[1])/(peak2[0]-peak1[0])
            b = peak1[1]-k*peak1[0]

            self.energy_curve_linear = np.zeros(len(self.spec_now))
            for i in range(len(self.spec_now)):
                self.energy_curve_linear[i] = k*i+b

            info = "Finish the FWHM calibration\n"
            info = info + "=============\n"
            info = info + "The curve is: E = k*Chan+b\n"
            info = info + "=============\n"
            info = info+"k: "+str(k)+"\n" + "b: "+str(b)+"\n" + "=============\n"
            self.info_out(info)

            self.canvas_update_energy_curve(self.energy_curve_linear)
            self.cmd_out("DO: Finish the linear energy curve's calibration")

            pass
        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_eva_cali_linear_save(self):
        try:
            if len(self.energy_curve_linear)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please calibration first")
                return
            file_path,filetype = QFileDialog.getSaveFileName(self, "Save the energy curve","C:/Users/Administrator/Desktop/energy_linear",
                                                    "Text Files (*.txt);;all files(*.*)")
            print(file_path)
            if file_path=="":
                # print("\n取消选择")
                return
            np.savetxt(file_path,self.energy_curve_linear)
            self.cmd_out("DO: Save the linear energy curve at "+file_path)

            pass
        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_eva_cali_nonlinear_do(self):
        try:
            if len(self.spec_now)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please choose spectrum")
                return

            p1, e1 = int(self.let_eva_cali_nonlinear_p1.text()), float(self.let_eva_cali_nonlinear_e1.text())
            p2, e2 = int(self.let_eva_cali_nonlinear_p2.text()), float(self.let_eva_cali_nonlinear_e2.text())
            p3, e3 = int(self.let_eva_cali_nonlinear_p4.text()), float(self.let_eva_cali_nonlinear_e3.text())

            arr1 = np.array([p1**2,p2**2,p3**2])
            arr2 = np.array([p1,p2,p3])
            arr3 = np.array([1, 1, 1])

            b = np.array([e1,e2,e3])

            arr = np.vstack((arr1,arr2,arr3)).T

            para = np.linalg.solve(arr,b)

            self.energy_curve_nonlinear = np.zeros(len(self.spec_now))
            for i in range(len(self.spec_now)):
                self.energy_curve_nonlinear[i] = para[0]*i*i+para[1]*i+para[2]

            info = "Finish the FWHM calibration\n"
            info = info + "=============\n"
            info = info + "The curve is: E = a*Chan^2+b*Chan+c\n"
            info = info + "=============\n"
            info = info + "a: " + str(para[0]) + "\n" + "b: " + str(para[1]) + "\n" + "c: " + str(para[2]) + "\n" + "=============\n"

            info = info + "=========\n"


            self.info_out(info)
            self.canvas_update_energy_curve(self.energy_curve_nonlinear)
            self.cmd_out("DO: Finish the non-linear energy curve's calibration")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_eva_cali_nonlinear_save(self):
        try:
            if len(self.energy_curve_nonlinear)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please calibration first")
                return
            file_path,filetype = QFileDialog.getSaveFileName(self, "Save the energy curve","C:/Users/Administrator/Desktop/energy_nonlinear",
                                                    "Text Files (*.txt);;all files(*.*)")
            if file_path=="":
                # print("\n取消选择")
                return
            np.savetxt(file_path,self.energy_curve_nonlinear)
            self.cmd_out("DO: Save the non-linear energy curve at "+file_path)

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_eva_fwhm_mcnp(self):
        try:
            row_c = self.tableWidget.rowCount()
            # col_c = self.tableWidget.columnCount()

            energy = []
            fwhm = []

            for i in range(row_c):
                if self.tableWidget.item(i,0)==None and self.tableWidget.item(i,1)==None:
                    pass
                elif self.tableWidget.item(i,0)!=None and self.tableWidget.item(i,1)!=None:
                    energy.append(float(self.tableWidget.item(i, 0).text()))
                    fwhm.append(float(self.tableWidget.item(i, 1).text()))
                else:
                    QMessageBox.warning(self,
                                        "Error!",
                                        "data error, row: "+str(i+1))
            if len(energy)==0 or (len(energy)!=len(fwhm)):
                QMessageBox.warning(self,
                                    "Error!",
                                    "There is no data")
            else:
                if len(self.energy)==0:
                    QMessageBox.warning(self,
                                        "Error!",
                                        "There is no energy list")
                else:
                    print(type(energy[0]))
                    fwhm_list,para = geFwhmCali().MCNP_cali(energy,fwhm,self.energy)


                    self.canvas_update_fit_result(energy,fwhm,self.energy,fwhm_list)
                    info = "Finish the FWHM calibration\n"
                    info = info + "=========\n"
                    info = info + "The curve is: FWHM = a + sqrt(b*(Energy)+c*(Energy^2))\n"
                    info = info + "=========\n"
                    info = info + "The parameters are:\n"+"a: "+str(para[0])+"\n"+"b: "+str(para[1])+"\n"+"c: "+str(para[2])+"\n"
                    self.info_out(info)
                    self.cmd_out("DO: Finish the FWHM calibration: MCNP model")




        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_eva_fwhm_cear(self):
        try:
            row_c = self.table_eva_fwhm_cr.rowCount()
            # col_c = self.tableWidget.columnCount()
            print("1")
            energy = []
            fwhm = []

            for i in range(row_c):
                if self.table_eva_fwhm_cr.item(i, 0) == None and self.table_eva_fwhm_cr.item(i, 1) == None:
                    pass
                elif self.table_eva_fwhm_cr.item(i, 0) != None and self.table_eva_fwhm_cr.item(i, 1) != None:
                    energy.append(float(self.table_eva_fwhm_cr.item(i, 0).text()))
                    fwhm.append(float(self.table_eva_fwhm_cr.item(i, 1).text()))
                else:
                    QMessageBox.warning(self,
                                        "Error!",
                                        "data error, row: " + str(i + 1))
            if len(energy) == 0 or (len(energy) != len(fwhm)):
                QMessageBox.warning(self,
                                    "Error!",
                                    "There is no data")
            else:
                if len(self.energy) == 0:
                    QMessageBox.warning(self,
                                        "Error!",
                                        "There is no energy list")
                else:
                    print("2")
                    fwhm_list, para = geFwhmCali().CEAR_cali(energy, fwhm, self.energy)
                    print("3")
                    self.canvas_update_fit_result(energy, fwhm, self.energy, fwhm_list)
                    info = "Finish the FWHM calibration\n"
                    info = info + "=========\n"
                    info = info + "The curve is: FWHM = d*(Energy^e)\n"
                    info = info + "=========\n"
                    info = info + "The parameters are:\n" + "d: " + str(para[0]) + "\n" + "e: " + str(
                        para[1])
                    self.info_out(info)
                    self.cmd_out("DO: Finish the FWHM calibration: CEAR model")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_eva_fwhm_linear(self):
        try:
            row_c = self.table_eva_fwhm_ln.rowCount()

            energy = []
            fwhm = []

            for i in range(row_c):
                if self.table_eva_fwhm_ln.item(i, 0) == None and self.table_eva_fwhm_ln.item(i, 1) == None:
                    pass
                elif self.table_eva_fwhm_ln.item(i, 0) != None and self.table_eva_fwhm_ln.item(i, 1) != None:
                    energy.append(float(self.table_eva_fwhm_ln.item(i, 0).text()))
                    fwhm.append(float(self.table_eva_fwhm_ln.item(i, 1).text()))
                else:
                    QMessageBox.warning(self,
                                        "Error!",
                                        "data error, row: " + str(i + 1))
            if len(energy) == 0 or (len(energy) != len(fwhm)):
                QMessageBox.warning(self,
                                    "Error!",
                                    "There is no data")
            else:
                if len(self.energy) == 0:
                    QMessageBox.warning(self,
                                        "Error!",
                                        "There is no energy list")
                else:
                    print("2")
                    fwhm_list, para = geFwhmCali().LINEAR_cali(energy, fwhm, self.energy)
                    print("3")
                    self.canvas_update_fit_result(energy, fwhm, self.energy, fwhm_list)
                    info = "Finish the FWHM calibration\n"
                    info = info + "=========\n"
                    info = info + "The curve is: FWHM = k*Energy+b\n"
                    info = info + "=========\n"
                    info = info + "The parameters are:\n" + "k: " + str(para[0]) + "\n" + "b: " + str(
                        para[1])
                    self.info_out(info)
                    self.cmd_out("DO: Finish the FWHM calibration: LINEAR model")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    # ===================================================================================
    # 7  SLOT  Process
    # 1. fit
    def slot_btn_proc_fit(self):
        try:
            # 获取拟合点数
            point_num = self.cbx_proc_denosi_fit.currentText()
            # spec_smooth = self.spec_now+0
            self.spec_last = self.spec_now+0

            # print(id(spec_smooth),id(self.spec_last),id(self.spec_now))
            spec_smooth = geDenoise().fit_denoise(self.spec_now,point_num)+0

            self.spec_now = spec_smooth+0

            self.canvas_update()
            self.cmd_out("DO: Finish the denoise: Fit")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    # 2. wavelet
    def slot_btn_proc_wavelet(self):
        try:
            # 小波降噪的参数：母小波 模式 阶次
            wavelet = self.cbx_proc_denosi_wt_wave.currentText()
            mode = self.cbx_proc_denosi_wt_mode.currentText()
            level = int(self.cbx_proc_denosi_wt_pow.currentText())

            # spec_smooth = self.spec_now+0
            self.spec_last = self.spec_now+0

            # print(id(spec_smooth),id(self.spec_last),id(self.spec_now))
            spec_smooth = geDenoise().wavelet_denoise(self.spec_now,wavelet,mode,level)+0

            self.spec_now = spec_smooth+0

            self.canvas_update()
            self.cmd_out("DO: Finish the denoise: Wavelet transform")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    # 3. lowpass
    def slot_btn_proc_lowpass(self):
        try:
            b = int(self.let_proc_denosi_lp_b.text())
            a = float(self.let_proc_denosi_lp_a.text())

            # spec_smooth = self.spec_now+0
            self.spec_last = self.spec_now+0

            # print(id(spec_smooth),id(self.spec_last),id(self.spec_now))
            spec_smooth = geDenoise().lowpass_denoise(self.spec_now,b,a)+0

            self.spec_now = spec_smooth+0

            self.canvas_update()
            self.cmd_out("DO: Finish the denoise: Low Pass")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_proc_emd_1(self):
        try:
            self.imf = geDenoise().emd(self.spec_now)
            self.cbx_proc_denosi_emd_imf.clear()
            for i in range(len(self.imf)):
                self.cbx_proc_denosi_emd_imf.addItem(str(i+1))
            self.cmd_out("DO: Finish the EMD transform")
            # print(np.shape(self.imf))
        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_proc_emd_do(self):
        try:
            imf_thr = int(self.cbx_proc_denosi_emd_imf.currentText())

            temp = np.array(self.imf)+0
            temp = temp[imf_thr-1:,:]
            self.spec_last = self.spec_now+0
            self.spec_now = np.sum(temp,axis=0)+0

            self.canvas_update()
            self.cmd_out("DO: Finish the denoise: EMD")
        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    # find peaks slot
    #
    # 1. auto
    def slot_btn_proc_findp_auto(self):
        try:
            para = [-1,-1,-1,-1]
            para[0] = float(self.let_proc_findp_auto_t.text())
            para[1] = int(self.let_proc_findp_auto_d.text())
            para[2] = float(self.let_proc_findp_auto_p.text())
            para[3] = int(self.let_proc_findp_auto_w.text())

            peaks = geFindpeaks().auto_find(self.spec_now,para)[0]

            self.canvas_update_findp(peaks)
            self.cmd_out("DO: auto find peaks finished")

            info = "Find "+str(len(peaks))+" peaks\n"+"They are:\n"
            if len(self.energy)==0:
                for i in range(len(peaks)):
                    info = info+str(peaks[i])+" chan\n"
            else:
                for i in range(len(peaks)):
                    info = info+str(peaks[i])+" chan, "+str(int(self.energy[peaks[i]]*100)/100)+" ener\n"
            self.info_out(info)

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_proc_findp_auto_cwt(self):
        try:
            para = [-1,-1,-1]
            para[0] = np.arange(1,int(self.let_proc_findp_autow_w.text()))
            para[1] = para[0]/float(self.let_proc_findp_autow_d.text())
            para[2] = float(self.let_proc_findp_autow_snr.text())

            peaks = geFindpeaks().auto_find_cwt(self.spec_now,para)

            self.canvas_update_findp(peaks)
            self.cmd_out("DO: auto find peaks finished")

            info = "Find "+str(len(peaks))+" peaks\n"+"They are:\n"
            if len(self.energy)==0:
                for i in range(len(peaks)):
                    info = info+str(peaks[i])+" chan\n"
            else:
                for i in range(len(peaks)):
                    info = info+str(peaks[i])+" chan, "+str(int(self.energy[peaks[i]]*100)/100)+" ener\n"
            self.info_out(info)

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    # 2. stabilization
    def slot_btn_proc_sta_3rp_do(self):
        try:
            if len(self.spec_now)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please choose a spectrum")
                return

            spline_point = int(self.cbx_proc_sta_3rp_pn.currentText())
            ener_1 = float(self.let_proc_sta_3rp_e.text())
            cur_chan_1 = int(self.let_proc_sta_3rp_cc.text())
            stan_chan_1 = int(self.let_proc_sta_3rp_sc.text())

            ener_2 = float(self.let_proc_sta_3rp_e_2.text())
            cur_chan_2 = int(self.let_proc_sta_3rp_cc_2.text())
            stan_chan_2 = int(self.let_proc_sta_3rp_sc_2.text())

            ener_3 = float(self.let_proc_sta_3rp_e_3.text())
            cur_chan_3 = int(self.let_proc_sta_3rp_cc_3.text())
            stan_chan_3 = int(self.let_proc_sta_3rp_sc_3.text())

            sta = geStabilization(self.spec_now)
            sta.channelIndex_3rp([cur_chan_1,cur_chan_2,cur_chan_3],
                                 [stan_chan_1,stan_chan_2,stan_chan_3],
                                 [ener_1,ener_2,ener_3])
            spec_staled = sta.stable(spline_point) + 0

            self.spec_last = self.spec_now+0
            self.spec_now = spec_staled+0

            self.canvas_update()
            self.cmd_out("DO: Finish the stabilization: 3 reference peaks")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_proc_sta_2rp_do(self):
        try:
            if len(self.spec_now)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please choose a spectrum")
                return

            spline_point = int(self.cbx_proc_sta_2rp_pn.currentText())
            ener_1 = float(self.let_proc_sta_2rp_e_1.text())
            cur_chan_1 = int(self.let_proc_sta_2rp_cc_1.text())
            stan_chan_1 = int(self.let_proc_sta_2rp_sc_1.text())

            ener_2 = float(self.let_proc_sta_2rp_e_2.text())
            cur_chan_2 = int(self.let_proc_sta_2rp_cc_2.text())
            stan_chan_2 = int(self.let_proc_sta_2rp_sc_2.text())

            sta = geStabilization(self.spec_now)
            sta.channelIndex_3rp([cur_chan_1,cur_chan_2],
                                 [stan_chan_1,stan_chan_2],
                                 [ener_1,ener_2],
                                 mode="linear")
            spec_staled = sta.stable(spline_point) + 0

            self.spec_last = self.spec_now+0
            self.spec_now = spec_staled+0

            self.canvas_update()
            self.cmd_out("DO: Finish the stabilization: 2 reference peaks")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    # ===================================================================================
    # 8  SLOT  FSA
    # FSA - LLS
    def slot_btn_fsa_lls_lib(self):
        try:
            # pass
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the lib",
                                                                    os.getcwd(),  # 起始路径
                                                                    "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

            if fileName_choose == "":
                # print("\n取消选择")
                return

            self.lls_lib = np.loadtxt(fileName_choose)

            self.let_fsa_lls_lib.setText(fileName_choose)

            self.canvas_update_fsa_lib(self.lls_lib)
            self.cmd_out("DO: Choose the library")

            if len(self.let_fsa_lls_lib.text())!=0 and len(self.let_fsa_lls_cont.text())!=0 and len(self.let_fsa_lls_spe.text())!=0:
                self.pbt_fsa_lls_solve.setEnabled(True)
        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fsa_lls_compos(self):
        try:
            # pass
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the composition",
                                                                    os.getcwd(),  # 起始路径
                                                                    "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

            if fileName_choose == "":
                # print("\n取消选择")
                return
            self.lls_cont = np.loadtxt(fileName_choose)

            self.let_fsa_lls_cont.setText(fileName_choose)
            self.cmd_out("DO: Choose the composition")

            if len(self.let_fsa_lls_lib.text())!=0 and len(self.let_fsa_lls_cont.text())!=0 and len(self.let_fsa_lls_spe.text())!=0:
                self.pbt_fsa_lls_solve.setEnabled(True)

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fsa_lls_spec(self):
        try:
            # pass
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the spectrum",
                                                                    os.getcwd(),  # 起始路径
                                                                    "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

            if fileName_choose == "":
                # print("\n取消选择")
                return
            self.lls_spec = np.loadtxt(fileName_choose)

            self.canvas_update_fsa_spec(self.lls_spec)
            self.let_fsa_lls_spe.setText(fileName_choose)
            self.cmd_out("DO: Choose the spectrum")

            if len(self.let_fsa_lls_lib.text())!=0 and len(self.let_fsa_lls_cont.text())!=0 and len(self.let_fsa_lls_spe.text())!=0:
                self.pbt_fsa_lls_solve.setEnabled(True)

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fsa_lls_solve(self):
        try:
            # pass
            solve = np.linalg.lstsq(self.lls_lib,self.lls_spec)[0]
            result = np.dot(self.lls_cont.T,solve)

            spec_solve = np.dot(self.lls_lib,solve)
            spec_ori_mean = np.average(self.lls_spec)
            ssr = np.sum(np.power((spec_solve-spec_ori_mean),2))
            sst = np.sum(np.power((self.lls_spec - spec_ori_mean), 2))
            R2 = ssr/sst

            self.ax.cla()
            self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
            if self.pushButton_15.isChecked():
                self.ax.plot(self.energy, self.lls_spec,label="experiment")
                self.ax.plot(self.energy, spec_solve, label="solve")
                self.ax.legend()
                self.canvas.draw()

            else:
                self.ax.plot(self.lls_spec, label="experiment")
                self.ax.plot(spec_solve, label="solve")
                self.ax.legend()
                self.canvas.draw()

            info = "============\n"
            info = info + "the results are:\n"
            for i in range(len(result)):
                info = info + str(result[i]) + "\n"
            info = info + "============\n"
            info = info + "R2: "+str(R2)

            self.info_out(info)
            self.cmd_out("DO: Finish the LLS analysis")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fsa_wlls_lib(self):
        try:
            # pass
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the lib",
                                                                    os.getcwd(),  # 起始路径
                                                                    "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

            if fileName_choose == "":
                # print("\n取消选择")
                return

            self.wlls_lib = np.loadtxt(fileName_choose)

            self.let_fsa_wlls_lib.setText(fileName_choose)

            self.canvas_update_fsa_lib(self.wlls_lib)
            self.cmd_out("DO: Choose the library")

            if len(self.let_fsa_wlls_lib.text())!=0 and len(self.let_fsa_wlls_cont.text())!=0 and len(self.let_fsa_wlls_spe.text())!=0:
                if self.cbx_fsa_wlls_type.currentText()=="std":
                    self.pbt_fsa_wlls_solve.setEnabled(True)
                else:
                    if len(self.let_fsa_wlls_weight.text())!=0:
                        self.pbt_fsa_wlls_solve.setEnabled(True)
        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fsa_wlls_compos(self):
        try:
            # pass
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the composition",
                                                                    os.getcwd(),  # 起始路径
                                                                    "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

            if fileName_choose == "":
                # print("\n取消选择")
                return
            self.wlls_cont = np.loadtxt(fileName_choose)

            self.let_fsa_wlls_cont.setText(fileName_choose)
            self.cmd_out("DO: Choose the composition")

            if len(self.let_fsa_wlls_lib.text())!=0 and len(self.let_fsa_wlls_cont.text())!=0 and len(self.let_fsa_wlls_spe.text())!=0:
                if self.cbx_fsa_wlls_type.currentText() == "std":
                    self.pbt_fsa_wlls_solve.setEnabled(True)
                else:
                    if len(self.let_fsa_wlls_weight.text()) != 0:
                        self.pbt_fsa_wlls_solve.setEnabled(True)

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fsa_wlls_spec(self):
        try:
            # pass
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the spectrum",
                                                                    os.getcwd(),  # 起始路径
                                                                    "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

            if fileName_choose == "":
                # print("\n取消选择")
                return
            self.wlls_spec = np.loadtxt(fileName_choose)

            self.canvas_update_fsa_spec(self.wlls_spec)
            self.let_fsa_wlls_spe.setText(fileName_choose)
            self.cmd_out("DO: Choose the spectrum")

            if len(self.let_fsa_wlls_lib.text())!=0 and len(self.let_fsa_wlls_cont.text())!=0 and len(self.let_fsa_wlls_spe.text())!=0:
                if self.cbx_fsa_wlls_type.currentText() == "std":
                    self.pbt_fsa_wlls_solve.setEnabled(True)
                else:
                    if len(self.let_fsa_wlls_weight.text()) != 0:
                        self.pbt_fsa_wlls_solve.setEnabled(True)

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fsa_wlls_weight(self):
        try:
            # pass
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the weight file",
                                                                    os.getcwd(),  # 起始路径
                                                                    "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

            if fileName_choose == "":
                # print("\n取消选择")
                return
            self.wlls_weight = np.loadtxt(fileName_choose)

            self.let_fsa_wlls_weight.setText(fileName_choose)
            self.cmd_out("DO: Choose the weight file")

            if len(self.let_fsa_wlls_lib.text())!=0 and len(self.let_fsa_wlls_cont.text())!=0 and len(self.let_fsa_wlls_spe.text())!=0:
                if self.cbx_fsa_wlls_type.currentText() == "std":
                    self.pbt_fsa_wlls_solve.setEnabled(True)
                else:
                    if len(self.let_fsa_wlls_weight.text()) != 0:
                        self.pbt_fsa_wlls_solve.setEnabled(True)

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fsa_wlls_solve(self):
        try:
            # pass
            if self.cbx_fsa_wlls_type.currentText()=="std":
                self.wlls_weight = np.sqrt(self.wlls_spec)+0

            w_mat = np.zeros((len(self.wlls_spec), len(self.wlls_spec)))
            for i in range(len(self.wlls_spec)):
                if self.wlls_weight[i] != 0:
                    w_mat[i,i] = 1/self.wlls_weight[i]

            WA = np.dot(w_mat,self.wlls_lib)
            Wb = np.dot(self.wlls_spec,w_mat)

            solve = np.linalg.lstsq(WA,Wb)[0]
            result = np.dot(self.wlls_cont.T,solve)

            spec_solve = np.dot(self.wlls_lib,solve)
            spec_ori_mean = np.average(self.wlls_spec)
            ssr = np.sum(np.power((spec_solve-spec_ori_mean),2))
            sst = np.sum(np.power((self.wlls_spec - spec_ori_mean), 2))
            R2 = ssr/sst

            self.ax.cla()
            self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
            if self.pushButton_15.isChecked():
                self.ax.plot(self.energy, self.wlls_spec,label="experiment")
                self.ax.plot(self.energy, spec_solve, label="solve")
                self.ax.legend()
                self.canvas.draw()

            else:
                self.ax.plot(self.wlls_spec, label="experiment")
                self.ax.plot(spec_solve, label="solve")
                self.ax.legend()
                self.canvas.draw()

            info = "============\n"
            info = info + "the results are:\n"
            for i in range(len(result)):
                info = info + str(result[i]) + "\n"
            info = info + "============\n"
            info = info + "R2: "+str(R2)

            self.info_out(info)
            self.cmd_out("DO: Finish the WLLS analysis")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fsa_pca_lib(self):
        try:
            # pass
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the lib",
                                                                    os.getcwd(),  # 起始路径
                                                                    "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

            if fileName_choose == "":
                # print("\n取消选择")
                return

            self.pca_lib = np.loadtxt(fileName_choose)

            self.let_fsa_pca_fp_lib.setText(fileName_choose)

            self.canvas_update_fsa_lib(self.pca_lib)
            self.cmd_out("DO: Choose the library")

            if len(self.let_fsa_pca_fp_lib.text())!=0 and len(self.let_fsa_pca_fp_cont.text())!=0 and len(self.let_fsa_pca_fp_spe.text())!=0:
                self.pbt_fsa_pca_do.setEnabled(True)

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fsa_pca_compos(self):
        try:
            # pass
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the composition",
                                                                    os.getcwd(),  # 起始路径
                                                                    "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

            if fileName_choose == "":
                # print("\n取消选择")
                return
            self.pca_cont = np.loadtxt(fileName_choose)

            self.let_fsa_pca_fp_cont.setText(fileName_choose)
            self.cmd_out("DO: Choose the composition")

            if len(self.let_fsa_pca_fp_lib.text()) != 0 and len(self.let_fsa_pca_fp_cont.text()) != 0 and len(
                    self.let_fsa_pca_fp_spe.text()) != 0:
                self.pbt_fsa_pca_do.setEnabled(True)

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fsa_pca_spec(self):
        try:
            # pass
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the spectrum",
                                                                    os.getcwd(),  # 起始路径
                                                                    "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

            if fileName_choose == "":
                # print("\n取消选择")
                return
            self.pca_spec = np.loadtxt(fileName_choose)

            self.canvas_update_fsa_spec(self.pca_spec)
            self.let_fsa_pca_fp_spe.setText(fileName_choose)
            self.cmd_out("DO: Choose the spectrum")

            if len(self.let_fsa_pca_fp_lib.text()) != 0 and len(self.let_fsa_pca_fp_cont.text()) != 0 and len(
                    self.let_fsa_pca_fp_spe.text()) != 0:
                self.pbt_fsa_pca_do.setEnabled(True)

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fsa_pca_solve(self):
        try:
            # print(self.pca_lib.shape,self.pca_spec.shape,self.pca_cont.shape)
            # m,n = np.shape(self.pca_lib)
            # matrix = np.zeros((m,n+1))
            # matrix[:,:n] = self.pca_lib
            # matrix[:,n] = self.pca_spec
            dimension = int(self.let_fsa_pca_dim.text())

            result,solve,spec_solve,spec_pca,R2 = geFSA().pls(self.pca_lib,self.pca_cont,self.pca_spec,dimension)
            # print("here")
            # spec_solve = np.dot(self.pca_cont.T, solve)
            # spec_ori_mean = np.average(self.pca_spec)
            # ssr = np.sum(np.power((spec_solve-spec_ori_mean),2))
            # sst = np.sum(np.power((self.pca_spec - spec_ori_mean), 2))
            # R2 = ssr/sst

            self.ax.cla()
            self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

            self.ax.plot(spec_pca, label="experiment")
            self.ax.plot(spec_solve, label="solve")
            self.ax.legend()
            self.canvas.draw()

            info = "============\n"
            info = info + "the results are:\n"
            for i in range(len(result)):
                info = info + str(result[i]) + "\n"
            info = info + "============\n"
            info = info + "R2: "+str(R2)

            self.info_out(info)
            self.cmd_out("DO: Finish the LLS analysis")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())
    # ===================================================================================
    # 9  SLOT  Fitting
    # fitting - scintillator
    def slot_btn_fit_sci_do(self):
        try:
            if len(self.let_fit_sci_left.text())==0 or len(self.let_fit_sci_right.text())==0 or len(self.let_fit_sci_bg.text())==0:
                #print(len(self.let_fit_sci_left.text()),len(self.let_fit_sci_right.text()),len(self.let_fit_sci_bg.text()))
                QMessageBox.warning(self,
                                    "Error!",
                                    "Missing parameters 1")
                return

            # roi parameters
            left = int(self.let_fit_sci_left.text())
            right = int(self.let_fit_sci_right.text())

            # bg parameters
            bg = float(self.let_fit_sci_bg.text())

            # peak parameters
            if self.table_fit_sci.rowCount()==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Missing parameters")
                return

            peak_paras = []

            for i in range(self.table_fit_sci.rowCount()):
                if self.table_fit_sci.item(i, 0) == None and self.table_fit_sci.item(i, 1) == None and self.table_fit_sci.item(i, 2) == None and self.table_fit_sci.item(i, 3) == None :
                    pass
                elif self.table_fit_sci.item(i, 0) != None and self.table_fit_sci.item(i, 1) != None and self.table_fit_sci.item(i, 2) != None and self.table_fit_sci.item(i, 3) != None:
                    peak_paras.append([float(self.table_fit_sci.item(i, 0).text()),
                                       float(self.table_fit_sci.item(i, 1).text()),
                                       float(self.table_fit_sci.item(i, 2).text()),
                                       float(self.table_fit_sci.item(i, 3).text())])
                else:
                    QMessageBox.warning(self,
                                        "Error!",
                                        "data error, row: " + str(i + 1))
            if len(peak_paras)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Missing parameters 2")
                return

            x_list = self.energy[left:right+1]
            y_list = self.spec_now[left:right+1]

            para_back,x_list_back,bg_back,peak_gauss,R2 = geFit().sci_peak_fit(x_list,y_list,bg,peak_paras,self.cbx_fit_sci_ef.isChecked())

            bg_for_pic = bg_back
            line_all = np.array(bg_back)
            self.ax.cla()
            self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

            self.ax.scatter(x_list,y_list,color="black",label="points")


            for i in range(len(peak_gauss)):
                # self.ax.plot(x_list_back, peak_gauss[i][0],label="peak "+str(i+1))

                self.ax.fill_between(x_list_back, 0, peak_gauss[i][0], label="peak " + str(i + 1), alpha=0.5)

                bg_for_pic = bg_for_pic + peak_gauss[i][1]
                line_all = line_all + peak_gauss[i][0] + peak_gauss[i][1]
                # self.ax.plot(x_list_back, peak_gauss[i][1], label="step " + str(i + 1))
            #line_all = line_all
            self.ax.plot(x_list_back, bg_for_pic, color="darkblue", label="background+steps")
            self.ax.plot(x_list_back, line_all, color="darkgreen", label="fit")
            self.ax.legend()
            self.canvas.draw()


            info = "============\n"
            info = info + "the parameters are:\n"
            info = info + "Bg: "+str(para_back[0])+"\n"

            info_area = ""
            for i in range((int((len(para_back)-1)/4))):
                info = info + "------------\n"
                info = info + "E "+str(i+1)+": "+str(para_back[1+i*4])+"\n"
                info = info + "Amp " + str(i + 1) + ": " + str(para_back[2 + i * 4])+"\n"
                info = info + "Sigma " + str(i + 1) + ": " + str(para_back[3 + i * 4])+"\n"
                info = info + "Step " + str(i + 1) + ": " + str(para_back[4 + i * 4])+"\n"

                info_area = info_area + "Area " + str(i + 1) + ": " + str(np.sum(peak_gauss[i][0]))+"\n"

            info = info + "============\n"
            info = info + info_area
            info = info + "R2: "+str(R2)+"\n"


            self.info_out(info)
            self.cmd_out("DO: Finish peak fitting")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_fit_semi_do(self):
        try:

            if len(self.let_fit_sci_left_2.text())==0 or len(self.let_fit_sci_right_2.text())==0 or len(self.let_fit_sci_bg_2.text())==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Missing parameters!")
                return

            # roi parameters
            left = int(self.let_fit_sci_left_2.text())
            right = int(self.let_fit_sci_right_2.text())
            # bg parameters
            bg = float(self.let_fit_sci_bg_2.text())

            if self.table_fit_semi_p.rowCount() == 0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Missing parameters")
                return

            peak_paras = []

            for i in range(self.table_fit_semi_p.rowCount()):
                if self.table_fit_semi_p.item(i, 0) == None and self.table_fit_semi_p.item(i, 1) == None and \
                        self.table_fit_semi_p.item(i, 2) == None and self.table_fit_semi_p.item(i, 3) == None \
                        and self.table_fit_semi_p.item(i, 4) == None and self.table_fit_semi_p.item(i, 5) == None \
                        and self.table_fit_semi_p.item(i, 6) == None and self.table_fit_semi_p.item(i, 7) == None:
                    pass
                elif self.table_fit_semi_p.item(i, 0) != None and self.table_fit_semi_p.item(i, 1) != None and \
                        self.table_fit_semi_p.item(i, 2) != None and self.table_fit_semi_p.item(i, 3) != None \
                        and self.table_fit_semi_p.item(i, 4) != None and self.table_fit_semi_p.item(i, 5) != None \
                        and self.table_fit_semi_p.item(i, 6) != None and self.table_fit_semi_p.item(i, 7) != None:
                    peak_paras.append([float(self.table_fit_semi_p.item(i, 0).text()),
                                       float(self.table_fit_semi_p.item(i, 1).text()),
                                       float(self.table_fit_semi_p.item(i, 2).text()),
                                       float(self.table_fit_semi_p.item(i, 3).text()),
                                       float(self.table_fit_semi_p.item(i, 4).text()),
                                       float(self.table_fit_semi_p.item(i, 5).text()),
                                       float(self.table_fit_semi_p.item(i, 6).text()),
                                       float(self.table_fit_semi_p.item(i, 7).text())])
                else:
                    QMessageBox.warning(self,
                                        "Error!",
                                        "data error, row: " + str(i + 1))


            if len(peak_paras)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Missing parameters 2")
                return

            x_list = self.energy[left:right + 1]
            y_list = self.spec_now[left:right + 1]
            # print("???????",len(peak_paras))
            para_back, x_list_back, bg_back, peak_gauss, R2 = geFit().semi_peak_fit(x_list, y_list, bg, peak_paras,
                                                                                    self.cbx_fit_sci_ef_2.isChecked(),False)
            # print("!!!!!!!", len(para_back), len(peak_gauss))
            # print("here2")
            bg_for_pic = bg_back
            self.ax.cla()
            self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

            self.ax.scatter(x_list, y_list, color="black", label="points")
            peaks = []
            all = np.zeros_like(x_list_back)
            if True:
                for i in range(len(peak_gauss)):
                    self.ax.fill_between(x_list_back, 0, peak_gauss[i][0]+peak_gauss[i][1], label="peak " + str(i + 1), alpha=0.5)
                    bg_for_pic = bg_for_pic + peak_gauss[i][2] + peak_gauss[i][3]
                    peaks = peak_gauss[i][0]+peak_gauss[i][1]
                    all = all + peak_gauss[i][0] + peak_gauss[i][1]

            # print("here3")
            self.ax.plot(x_list_back, bg_for_pic, color="darkblue", label="background+steps+tails")
            self.ax.plot(x_list_back, bg_for_pic+all, color="darkgreen", label="fit")
            self.ax.legend()
            self.canvas.draw()

            info = "============\n"
            info = info + "the parameters are:\n"
            info = info + "Bg: " + str(para_back[0]) + "\n"
            # print(2)
            info_area = ""
            if True:
                for i in range((int((len(para_back) - 1) / 8))):
                    info = info + "------------\n"
                    info = info + "E " + str(i + 1) + ": " + str(para_back[1 + i * 8]) + "\n"
                    info = info + "Amp " + str(i + 1) + ": " + str(para_back[2 + i * 8]) + "\n"
                    info = info + "Sigma " + str(i + 1) + ": " + str(para_back[3 + i * 8]) + "\n"
                    info = info + "A l-skew " + str(i + 1) + ": " + str(para_back[4 + i * 8]) + "\n"
                    info = info + "B l-skew " + str(i + 1) + ": " + str(para_back[5 + i * 8]) + "\n"
                    info = info + "A tail " + str(i + 1) + ": " + str(para_back[6 + i * 8]) + "\n"
                    info = info + "B tail " + str(i + 1) + ": " + str(para_back[7 + i * 8]) + "\n"
                    info = info + "A step " + str(i + 1) + ": " + str(para_back[8 + i * 8]) + "\n"

                    info_area = info_area + "Area " + str(i + 1) + ": " + str(np.sum(peak_gauss[i][0]+peak_gauss[i][1])) + "\n"

            # print(3)
            info = info + "============\n"
            info = info + info_area
            info = info + "R2: " + str(R2) + "\n"
            # print(4)

            self.info_out(info)
            self.cmd_out("DO: Finish peak fitting")
        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    # ===================================================================================
    # 10  SLOT  Simulation
    # simulation-broaden

    def slot_rbn_simu_edep(self):
        try:
            print("excu slot_rbn_simu_edep")
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the energy deposition file",
                                                                    "./",  # 起始路径
                                                                    "Text Files (*.txt);;All Files (*)")  # 设置文件扩展名过滤,用双分号间隔
            if fileName_choose == "":
                return
            self.simu_bro_edep_fp = fileName_choose
            self.flas_simu_broaden = 0
        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_rbn_simu_spec(self):
        try:
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the energy deposition file",
                                                                    "./",  # 起始路径
                                                                    "Text Files (*.txt);;All Files (*)")  # 设置文件扩展名过滤,用双分号间隔
            if fileName_choose == "":
                self.radioButton_2.setChecked(False)
                return
            self.spec_now = np.loadtxt(fileName_choose)
            self.flas_simu_broaden = 0

            self.canvas_update()
            self.cmd_out("DO: Read the energy deposition spectrum")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_rbn_simu_spec_conv(self):
        try:
            print("excu slot_rbn_simu_spec")
            fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                    "Open the energy deposition file",
                                                                    "./",  # 起始路径
                                                                    "Text Files (*.txt);;All Files (*)")  # 设置文件扩展名过滤,用双分号间隔
            if fileName_choose == "":
                self.rbt_simu_broaden_conv.setChecked(False)
                return
            self.spec_now = np.loadtxt(fileName_choose)
            self.flas_simu_broaden = 1

            self.canvas_update()
            self.cmd_out("DO: Read the energy deposition spectrum")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_simu_bro_mc_draw(self):
        try:
            if len(self.energy)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please choose the energy list")
                return
            a = float(self.let_simu_bro_mc_a.text())
            b = float(self.let_simu_bro_mc_b.text())
            c = float(self.let_simu_bro_mc_c.text())
            self.fwhm_curve = a + np.sqrt(b * (self.energy + c * np.power(self.energy, 2)))

            self.ax.cla()
            self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
            self.ax.plot(self.energy, self.fwhm_curve, color="red", label="FWHM")
            self.ax.legend()
            self.canvas.draw()

            self.cmd_out("DO: Draw the FWHM curve: MCNP model")


        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_simu_bro_mc_do(self):
        try:
            if len(self.energy)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please choose the energy list")
                return

            a = float(self.let_simu_bro_mc_a.text())
            b = float(self.let_simu_bro_mc_b.text())
            c = float(self.let_simu_bro_mc_c.text())
            self.fwhm_curve = a + np.sqrt(b * (self.energy + c * np.power(self.energy, 2)))

            if self.radioButton.isChecked():                    # edep
                self.cmd_out("DO: Broaden...")
                spec_broaden = geBroaden().broaden_sampling(self.simu_bro_edep_fp, self.energy, self.fwhm_curve)
                self.spec_last = self.spec_now + 0
                self.spec_now = spec_broaden

                self.canvas_update()
                self.cmd_out("DO: Finish the spectrum broaden")

            elif self.radioButton_2.isChecked():                # spec
                if len(self.spec_now)==0:
                    QMessageBox.warning(self,
                                        "Error!",
                                        "Please choose the spectrum")
                    return

                self.cmd_out("DO: Broaden...")
                spec_broaden = geBroaden().broaden_sampling_spec(self.spec_now,self.energy,self.fwhm_curve)
                self.spec_last = self.spec_now + 0
                self.spec_now = spec_broaden

                self.canvas_update()
                self.cmd_out("DO: Finish the spectrum broaden")






        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_simu_bro_cr_draw(self):
        try:
            if len(self.energy)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please choose the energy list")
                return
            d = float(self.let_simu_bro_cr_a.text())
            e = float(self.let_simu_bro_cr_e.text())
            self.fwhm_curve = np.dot(d,np.power(self.energy,e))+0

            self.ax.cla()
            self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
            self.ax.plot(self.energy, self.fwhm_curve, color="red", label="FWHM")
            self.ax.legend()
            self.canvas.draw()

            self.cmd_out("DO: Draw the FWHM curve: CEAR model")


        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_simu_bro_cr_do(self):
        try:
            if len(self.energy)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please choose the energy list")
                return

            d = float(self.let_simu_bro_cr_a.text())
            e = float(self.let_simu_bro_cr_e.text())
            self.fwhm_curve = np.dot(d,np.power(self.energy,e))+0

            if self.radioButton.isChecked():                    # edep
                self.cmd_out("DO: Broaden...")
                spec_broaden = geBroaden().broaden_sampling(self.simu_bro_edep_fp, self.energy, self.fwhm_curve)
                self.spec_last = self.spec_now + 0
                self.spec_now = spec_broaden

                self.canvas_update()
                self.cmd_out("DO: Finish the spectrum broaden")

            elif self.radioButton_2.isChecked():                # spec
                if len(self.spec_now)==0:
                    QMessageBox.warning(self,
                                        "Error!",
                                        "Please choose the spectrum")
                    return

                self.cmd_out("DO: Broaden...")
                spec_broaden = geBroaden().broaden_sampling_spec(self.spec_now,self.energy,self.fwhm_curve)
                self.spec_last = self.spec_now + 0
                self.spec_now = spec_broaden

                self.canvas_update()
                self.cmd_out("DO: Finish the spectrum broaden")






        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_simu_bro_ln_draw(self):
        try:
            if len(self.energy)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please choose the energy list")
                return
            k = float(self.let_simu_bro_ln_k.text())
            b = float(self.let_simu_bro_ln_b.text())
            self.fwhm_curve = np.dot(k, self.energy) + b

            self.ax.cla()
            self.ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
            self.ax.plot(self.energy, self.fwhm_curve, color="red", label="FWHM")
            self.ax.legend()
            self.canvas.draw()

            self.cmd_out("DO: Draw the FWHM curve: LINEAR model")


        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_simu_bro_ln_do(self):
        try:
            if len(self.energy)==0:
                QMessageBox.warning(self,
                                    "Error!",
                                    "Please choose the energy list")
                return

            k = float(self.let_simu_bro_ln_k.text())
            b = float(self.let_simu_bro_ln_b.text())
            self.fwhm_curve = np.dot(k, self.energy) + b
            if self.flas_simu_broaden==0:
                if self.radioButton.isChecked():                    # edep
                    self.cmd_out("DO: Broaden...")
                    spec_broaden = geBroaden().broaden_sampling(self.simu_bro_edep_fp, self.energy, self.fwhm_curve)
                    self.spec_last = self.spec_now + 0
                    self.spec_now = spec_broaden

                    self.canvas_update()
                    self.cmd_out("DO: Finish the spectrum broaden")

                elif self.radioButton_2.isChecked():                # spec
                    if len(self.spec_now)==0:
                        QMessageBox.warning(self,
                                            "Error!",
                                            "Please choose the spectrum")
                        return

                    self.cmd_out("DO: Broaden...")
                    spec_broaden = geBroaden().broaden_sampling_spec(self.spec_now,self.energy,self.fwhm_curve)
                    self.spec_last = self.spec_now + 0
                    self.spec_now = spec_broaden

                    self.canvas_update()
                    self.cmd_out("DO: Finish the spectrum broaden")
            else:
                if len(self.spec_now) == 0:
                    QMessageBox.warning(self,
                                        "Error!",
                                        "Please choose the spectrum")
                    return

                self.cmd_out("DO: Broaden...")
                spec_broaden = geBroaden().broaden_conv_spec(self.spec_now, self.energy, self.fwhm_curve)
                self.spec_last = self.spec_now + 0
                self.spec_now = spec_broaden

                self.canvas_update()
                self.cmd_out("DO: Finish the spectrum broaden")






        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_simu_mcr_open(self):
        try:
            txtNames, filetype = QFileDialog.getOpenFileNames(self,
                                                                "Open the MCNP output file",
                                                                "./",  # 起始路径
                                                                "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,用双分号间隔

            if len(txtNames)==0:
                # print("\n取消选择")
                return
            self.geMCR = geMCReader()
            self.geMCR.open(txtNames,self.procB_simu_mcr)

            self.pbt_simu_mcr_save.setEnabled(True)
            self.cmd_out("DO: Finish read "+str(len(txtNames))+" MCNP output files.")

        except BaseException as e:
            QMessageBox.warning(self,
                            "Error!",
                            e.__str__())

    def slot_btn_simu_mcr_save(self):
        try:

            file_path,file_type = QFileDialog.getSaveFileName(self, "Save the spectrum",
                                                    "./output",
                                                    "Excel File (*.xlsx)")

            self.geMCR.save(file_path)
            self.cmd_out("DO: Save the MCNP output file: " + file_path)

        except BaseException as e:
            QMessageBox.warning(self,
                            "Error!",
                            e.__str__())

    # ===================================================================================
    # 11  SLOT  Database
    # database - pgnaa
    def slot_btn_data_pgnaa_do(self):
        try:
            self.table_data_pgnaa.setRowCount(0)
            # self.table_data_pgnaa.clearContents()

            Z = int(self.let_data_pgnaa_Z.text())
            data = geDatabase().PGAA_Z(Z)
            self.dataBase = data

            for i in range(np.shape(data)[0]):
                cur_total_row = self.table_data_pgnaa.rowCount()
                self.table_data_pgnaa.setRowCount(cur_total_row + 1)

                newItem = QTableWidgetItem(data[i, 1].strip())
                self.table_data_pgnaa.setItem(i,0,newItem)

                newItem = QTableWidgetItem(data[i, 4].strip())
                self.table_data_pgnaa.setItem(i, 1, newItem)

                newItem = QTableWidgetItem(data[i, 6].strip())
                self.table_data_pgnaa.setItem(i, 2, newItem)

                newItem = QTableWidgetItem(data[i, 9].strip())
                self.table_data_pgnaa.setItem(i, 3, newItem)

            Egamma,sigma = data[:,5],data[:,7]

            self.canvas_update_database(Egamma,sigma)
            self.cmd_out("DO: Search the PGNAA database")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_data_decay_do(self):
        try:
            self.table_data_decay.setRowCount(0)
            # self.table_data_pgnaa.clearContents()

            Z = int(self.let_data_decay_Z.text())
            data = geDatabase().decay_Z(Z)
            self.dataBase = data
            for i in range(np.shape(data)[0]):
                cur_total_row = self.table_data_decay.rowCount()
                self.table_data_decay.setRowCount(cur_total_row + 1)

                newItem = QTableWidgetItem(data[i, 1].strip())
                self.table_data_decay.setItem(i,0,newItem)

                newItem = QTableWidgetItem(data[i, 4].strip())
                self.table_data_decay.setItem(i, 1, newItem)

                newItem = QTableWidgetItem(data[i, 6].strip())
                self.table_data_decay.setItem(i, 2, newItem)

                newItem = QTableWidgetItem(str(data[i, 10]))
                self.table_data_decay.setItem(i, 3, newItem)

                newItem = QTableWidgetItem(data[i, 11].strip())
                self.table_data_decay.setItem(i, 4, newItem)

            Egamma,sigma = data[:,5],data[:,7]

            self.canvas_update_database(Egamma,sigma)
            self.cmd_out("DO: Search the Decay database")

        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())

    def slot_btn_data_iso_do(self):
        try:
            self.table_data_iso.setRowCount(0)
            # self.table_data_pgnaa.clearContents()

            Z = int(self.let_data_iso_Z.text())
            data = geDatabase().isotope_Z(Z)

            for i in range(np.shape(data)[0]):
                cur_total_row = self.table_data_iso.rowCount()
                self.table_data_iso.setRowCount(cur_total_row + 1)

                newItem = QTableWidgetItem(data[i, 1].strip())
                self.table_data_iso.setItem(i,0,newItem)

                newItem = QTableWidgetItem(data[i, 4].strip())
                self.table_data_iso.setItem(i, 1, newItem)

                newItem = QTableWidgetItem(data[i, 7].strip())
                self.table_data_iso.setItem(i, 2, newItem)

                newItem = QTableWidgetItem(str(data[i, 10]))
                self.table_data_iso.setItem(i, 3, newItem)

                newItem = QTableWidgetItem(str(data[i, 11]))
                self.table_data_iso.setItem(i, 4, newItem)

            # Egamma,sigma = data[:,5]/1000,data[:,7]
            #
            # self.canvas_update_database(Egamma,sigma)
            self.cmd_out("DO: Search the ISOTOPE database")
        except BaseException as e:
            QMessageBox.warning(self,
                                "Error!",
                                e.__str__())


if __name__ == "__main__":
    #
    app = QApplication(sys.argv)
    #
    window = MainWindow()
    #
    window.show()
    #
    sys.exit(app.exec_())