import time
import csv
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
import random
import matplotlib

class wave(object):
    def __init__(self):
        self.picture_time = {}
        self.ID_list = []
        self.phy_data = {}
        self.phy_edge = {}
        self.high_phy_data = {}
        self.medium_phy_data = {}
        self.low_phy_data = {}
        self.count = 0


    def get_phy(self, phy_file=''):
        with open('data/{0}.csv'.format(phy_file), 'r', newline="") as csv_file:
            readers = csv.reader(csv_file)
            for read in readers:
                self.ID_list.append(read[0])
                new_list = eval(read[1])
                self.phy_edge.setdefault(read[0], []).extend(new_list)


    def get_data(self, gather_file=''):
        with open('data/{0}.csv'.format(gather_file), 'r', newline="") as csv_file:
            readers = csv.reader(csv_file)

            for read in readers:
                self.picture_time.setdefault(read[0], []).append(float(read[3])) #收集时间

                if read[0] in self.ID_list:
                    temp_list = ''
                    new_list = eval(read[1])
                    temp_dic_phy_all = self.phy_data.setdefault(read[0], {})
                    temp_dic_phy_8 = self.low_phy_data.setdefault(read[0], {})
                    temp_dic_phy_13 = self.medium_phy_data.setdefault(read[0], {})
                    temp_dic_phy_l = self.high_phy_data.setdefault(read[0], {})
                    if len(new_list) == 8:
                        for j in range(8):
                            temp_list += "0" * (8 - len(bin(int(new_list[j], 16)).replace("0b", ""))) + bin(int(new_list[j], 16)).replace("0b", "")
                    else:
                        raise Exception("data length error")    #获取以64位的字符串形式表示的原始数据


                    for n in range(int(len(self.phy_edge[read[0]]) / 2)):
                        temp_2_data = temp_list[self.phy_edge[read[0]][2*n] : self.phy_edge[read[0]][2*n+1] + 1]  #收集总的数据
                        temp_10_data = int(temp_2_data, 2)
                        len_bit_data = self.phy_edge[read[0]][2*n+1] + 1 - self.phy_edge[read[0]][2*n]

                        temp_dic_phy_all.setdefault(
                            (self.phy_edge[read[0]][2*n], self.phy_edge[read[0]][2*n+1]), []).append(temp_10_data)
                        #数据分流
                        if len_bit_data < 8:
                            temp_dic_phy_8.setdefault(
                                (self.phy_edge[read[0]][2*n], self.phy_edge[read[0]][2*n+1]), []).append(
                                temp_10_data)
                        elif len_bit_data < 13:
                            temp_dic_phy_13.setdefault(
                                (self.phy_edge[read[0]][2*n], self.phy_edge[read[0]][2*n+1]), []).append(
                                temp_10_data)
                        else:
                            temp_dic_phy_l.setdefault(
                                (self.phy_edge[read[0]][2*n], self.phy_edge[read[0]][2*n+1]), []).append(
                                temp_10_data)
                else:pass

        self.clear_empty_data(self.high_phy_data)
        self.clear_empty_data(self.medium_phy_data)
        self.clear_empty_data(self.low_phy_data)

    def clear_empty_data(self, clear_dir=None):
        IDs = clear_dir.keys()
        IDs = list(IDs)
        for ID in IDs:
            if len(clear_dir[ID]) == 0:
                del clear_dir[ID]


    def picture_generation(self, ID='', path='', data=None):
        if data is None:
            data = {}

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.xlabel("时间", fontsize=20)
        plt.ylabel("物理信号值", fontsize=20)
        plt.title("车载CAN网络物理信号变化曲线", fontsize=20)
        plt.figure(figsize=(30, 7), dpi=180)
       # plt.figure(figsize=(20, 10), dpi=40)

        for edge in data[ID]:
            lable = '(' + str(edge[0]) + ',' + str(edge[1]) + ')'
            plt.plot(self.picture_time[ID], data[ID][edge], label=lable)
            plt.legend()
            plt.grid()
            plt.savefig("picture/" + path + "/{0}.png".format(ID))
        plt.clf()
        plt.close()
        self.count += 1
        print('Generated:', self.count)


    def picture_start(self):
        #self.add_time()
        self.get_phy('PHY')
        self.get_data('initial_data')

        for IDs in self.high_phy_data:
             self.picture_generation(ID=IDs, path='high', data=self.high_phy_data)
        for IDs in self.medium_phy_data:
             self.picture_generation(ID=IDs, path='medium', data=self.medium_phy_data)
        for IDs in self.low_phy_data:
             self.picture_generation(ID=IDs, path='low', data=self.low_phy_data)


    def add_time(self):
        test_list = []
        with open('data/new_feature.csv', 'r', newline='') as csvin:
            readers = csv.reader(csvin)
            for read in readers:
                test_list.append(read[0])
                test_list.append(read[1])
                test_list.append(random.uniform(0, 20))

        with open('data/initial_data.csv', 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            for n in range(int(len(test_list) / 3)):
                csv_writer.writerow([test_list[3*n], test_list[3*n+1], test_list[3*n+2]])





if __name__ == "__main__":
    show_test = wave()
    #show_test.start(500)
    try:
        show_test.picture_start()

    finally:
        print("Picture Generated")