# -*- coding: utf-8 -*-



import struct
import numpy as np


class geRWIO:
    def __init__(self, file_path, file_type):
        if file_type == "chn":
            self.infile = open(file_path, "rb")
            self.read_chn_binary()
        elif file_type == "mca":
            # self.infile = open(file_path, "rb")
            self.read_mca(file_path)
        elif file_type == "spe":
            # self.infile = open(file_path, "rb")
            self.read_spe(file_path)
        elif file_type == "txt":
            # self.infile = open(file_path, "rb")
            self.read_txt(file_path)
        elif file_type == "tka":
            # self.infile = open(file_path, "rb")
            self.read_tka(file_path)

    def read_chn_binary(self):       # We start by reading the 32 byte header
        self.version            = struct.unpack('h', self.infile.read(2))[0]
        self.mca_detector_id    = struct.unpack('h', self.infile.read(2))[0]
        self.segment_number     = struct.unpack('h', self.infile.read(2))[0]
        self.start_time_ss      = self.infile.read(2)
        self.real_time          = struct.unpack('I', self.infile.read(4))[0]
        self.live_time          = struct.unpack('I', self.infile.read(4))[0]
        self.start_date         = self.infile.read(8) # Ascii type date in
                                # DDMMMYY* where * == 1 means 21th century
        self.start_time_hhmm    = self.infile.read(4)
        self.chan_offset        = struct.unpack('h', self.infile.read(2))[0]
        self.no_channels        = struct.unpack('h', self.infile.read(2))[0]
        self.spec         = np.zeros(self.no_channels) # Init hist_array
        # Read the binary data
        for index in range(len(self.spec)):
            self.spec[index]= struct.unpack('I', self.infile.read(4))[0]
        assert struct.unpack('h', self.infile.read(2))[0] == -102
        self.infile.read(2)
        self.en_zero_inter = struct.unpack('f', self.infile.read(4))[0]
        self.en_slope = struct.unpack('f', self.infile.read(4))[0]
        self.en_quad = struct.unpack('f', self.infile.read(4))[0]
        self.infile.close()

        channels = np.linspace(1,len(self.spec),len(self.spec))

        self.energy_list = self.en_quad*channels*channels+self.en_slope*channels+self.en_zero_inter
        self.spec = np.array(self.spec)
        self.energy_list = np.array(self.energy_list)

    def read_mca(self,file_path):
        self.spec = []
        self.energy_list = []
        with open(file_path,"rb") as f:
            lines = f.read().split(b"\r\n")
            cali_index_l = lines.index(b"<<CALIBRATION>>")+2
            cali_index_r = lines.index(b"<<DATA>>")
            calis = lines[cali_index_l:cali_index_r]
            cali_A = np.zeros((3,3))
            cali_b = np.zeros(3)
            for i in range(len(calis)):
                c,e = str(calis[i],encoding="gbk").split(" ")
                c,e = float(c),float(e)
                cali_A[i,0],cali_A[i,1],cali_A[i,2] = c**2,c,1
                cali_b[i] = e
            a,b,c = np.linalg.solve(cali_A,cali_b)

            spec_index_l = lines.index(b"<<DATA>>") + 1
            spec_index_r = lines.index(b"<<END>>")
            spec_b = lines[spec_index_l:spec_index_r]
            for i in range(len(spec_b)):
                self.spec.append(int(spec_b[i]))
                self.energy_list.append(a*(i+1)*(i+1)+b*(i+1)+c)
        self.spec = np.array(self.spec)
        self.energy_list = np.array(self.energy_list)

    def read_spe(self,file_path):
        self.spec = []
        self.energy_list = []
        with open(file_path, "rb") as f:
            lines = f.read().split(b"\r\n")

            cali_index_l = lines.index(b"$MCA_CAL:") + 2
            cali_index_r = cali_index_l+1
            calis = lines[cali_index_l]
            calis = str(calis,encoding="gbk").split(" ")

            a = float(calis[0])
            b = float(calis[1])
            c = float(calis[2])
            print(a,b,c)
            spec_index_l = lines.index(b"$DATA:") + 2
            spec_index_r = lines.index(b"$ROI:")
            spec_b = lines[spec_index_l:spec_index_r]
            for i in range(len(spec_b)):
                self.spec.append(int(spec_b[i]))
                self.energy_list.append(c * (i + 1) * (i + 1) + b * (i + 1) + a)
        self.spec = np.array(self.spec)
        self.energy_list = np.array(self.energy_list)

    def read_txt(self,file_path):
        self.spec = np.loadtxt(file_path)

    def read_tka(self,file_path):
        self.spec = np.loadtxt(file_path)[2:]
