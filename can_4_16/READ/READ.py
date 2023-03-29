from frame import Frame
from mydevice import MyDevice
import time
import csv
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
import os


class read(MyDevice):
    def __init__(self):
        super(read, self).__init__()
        self.bit_flip = {}
        self.bit_data = {}
        self.bit_64 = {}
        self.initial_data = {}
        self.ID_num = {}
        self.bit_mag = {}
        self.ref = {}
        self.ref_phase2 = {}

        self.reference_data = {}

    def initial_frame(self, number_time):
        """ pre processing function """
        print("initial data gather start")
       # if self.clear_buffer() is not True:
        #    ex = Exception("clear failure")
       #     raise ex
      #  else:
            #self.gather_feature_real(i=j, dic=self.initial_data, gather_mode="initial_data")
        self.gather_feature_real(dic_temp=self.initial_data, gather_mode="initial_data", gather_time=number_time)
        self.gather_feature_real(dic_temp=self.reference_data, gather_mode="new_feature", gather_time=number_time)

        print(self.initial_data)
        print("initial feature end")


    def gather_feature_fake(self, dic_temp=None, gather_mode="", gather_time=0):
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'data/{0}.csv'.format(gather_mode), 'r', newline="") as csv_file:
            readers = csv.reader(csv_file)
            for read in readers:
                new_list = eval(read[1])

                if read[0] in self.ID_num:
                    self.ID_num[read[0]] += 1
                else:
                    self.ID_num[read[0]] = 1

                temp_dic = dic_temp.setdefault(read[0], {})
                print(read[0])
                if len(new_list) == 8:
                    for j in range(8):
                        temp_dic.setdefault(j, []).append("0" * (8 - len(bin(int(new_list[j], 16)).replace("0b", "")))
                                                          + bin(int(new_list[j], 16)).replace("0b", ""))
                else:
                    raise Exception("data length error")


    def gather_feature_real(self, dic_temp=None, gather_mode="", gather_time = 20):
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'data/{0}.csv'.format(gather_mode), 'w', newline="") as csv_file:
            temp_writer = csv.writer(csv_file)

            ref_car = self.receive()
            ref_car_time = ref_car.TimeStamp
            time0 = time.time()

            while time.time() - time0 <= gather_time:
                data = self.receive()
                p_list = []
                if hex(data.ID) in self.ID_num:
                    self.ID_num[hex(data.ID)] += 1
                else:
                    self.ID_num[hex(data.ID)] = 1

                for n in range(8):
                    p_list.append("0x" + "0" * (2 - len(hex(data.Data[n]).replace("0x", "")))
                                  + hex(data.Data[n]).replace("0x", ""))

                temp_writer.writerow(
                    [hex(data.ID), p_list, data.DataLen, (data.TimeStamp - ref_car_time) * 0.0001, data.TimeStamp])
                # collect frame           # ID        特征数据     DLC               汽车定义时刻               汽车时间戳

                temp_dic = dic_temp.setdefault(hex(data.ID), {})
                print(hex(data.ID))
                if len(data.Data) == 8:
                    for j in range(8):
                        temp_dic.setdefault(j, []).append("0" * (8 - len(bin(data.Data[j]).replace("0b", "")))
                                                          + bin(data.Data[j]).replace("0b", ""))
                else:
                    raise Exception("data length error")


    def pre_processing(self):
        temp_dic = sorted(self.initial_data)
        for key in temp_dic:
            temp_list = self.bit_data.setdefault(key, {})
            for index in range(8):
                calculate_temp = self.initial_data[key][index]
                temp_list_index = [0, 0, 0, 0, 0, 0, 0, 0]
                for a in range(len(calculate_temp)-1):
                    cal_1 = calculate_temp[a]
                    cal_2 = calculate_temp[a+1]
                    for b in range(8):
                        if cal_1[b] != cal_2[b]:
                            temp_list_index[b] += 1
                temp_list.setdefault(index, []).extend(temp_list_index)

        for key in self.bit_data:
            for index in range(8):
                self.bit_64.setdefault(key, []).extend(self.bit_data[key][index])
        for key in self.bit_64:
            temp_list_1 = self.bit_flip.setdefault(key, [])
            temp_list_3 = self.bit_mag.setdefault(key, [])
            temp_list_2 = self.bit_64[key]
            for c in range(len(self.bit_64[key])):
                temp_list_1.append(temp_list_2[c] / self.ID_num[key])
                if temp_list_2[c] == 0:
                    temp_list_3.append(-20)
                else:
                    temp_list_3.append(math.log(temp_list_2[c], 10))

        self.write_bit_64(filename='bite_64', dictname=self.bit_64)
        self.write_bit_64(filename='bit_flip', dictname=self.bit_flip)
        self.write_bit_64(filename='bit_mag', dictname=self.bit_mag)

    def write_data(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'data/bit_data.csv', 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='\t')
            csv_writer.writerow(["ID", "数据域位置", "数据变化值"])
            for key in self.bit_data:
                for index in self.bit_data[key]:
                    csv_writer.writerow([key, index, self.bit_data[key][index]])


    def write_bit_64(self, filename = '', dictname = None):
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'data/{0}.csv'.format(filename), 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='\t')
            csv_writer.writerow(["ID", "数据域"])
            for key in dictname:
                csv_writer.writerow([key, dictname[key]])

    def phase_1(self):
        for key in self.bit_flip:
            pre_mag = self.bit_mag[key][0]
            xs = 0
            temp_ref = self.ref.setdefault(key, [])
            for x in range(1, 64):
                if self.bit_mag[key][x] < pre_mag:
                    temp_ref.append((xs, x-1))
                    xs = x
                pre_mag = self.bit_mag[key][x]
            temp_ref.append((xs, 63))
        self.write_bit_64(filename='bit_phy', dictname=self.ref)

    def phase_2(self):
        for key in self.ref:
            temp_ref2 = self.ref_phase2.setdefault(key, [])
            for sign in self.ref[key]:
                sign_s, sign_e = sign
                mu = np.mean(self.bit_flip[sign_s:sign_e])
                std = np.std(self.bit_flip[sign_s:sign_e])

                if self.bit_mag[key][sign_e] == 0:
                    for a in range(sign_e - sign_s + 1):
                        b = sign_e - a
                        if self.bit_flip[key][b] == self.bit_flip[key][b-1] * 2:
                            s_ctr = b-1
                        else:
                            temp_ref2.append((sign_s, s_ctr, "PHYSICAL"))
                            temp_ref2.append((s_ctr, sign_e, "COUNTER"))

                if self.bit_mag[key][sign_e] != 0:
                    for s_crc in range(sign_s, sign_e):
                        if all(self.bit_mag[key][s_crc:sign_e]) == 0 and 0.5 <= mu <= 0.5 + std:
                            temp_ref2.append(s_crc, sign_e, "CRC")
                            temp_ref2.append((sign_s, s_crc, "PHYSICAL"))
                else:temp_ref2.append((sign_s, sign_e, "PHYSICAL"))

if __name__ == "__main__":
    bit_test = read()
    bit_test.start(500)

    try:
        print('请输入预计收集数据时间长度:\r\n')
        number_frame = int(input())
        bit_test.initial_frame(number_time=number_frame)
        bit_test.pre_processing()
        bit_test.write_data()
        bit_test.phase_1()
      #  bit_test.phase_2()
    finally:
        bit_test.stop()
