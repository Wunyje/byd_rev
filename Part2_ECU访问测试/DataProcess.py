import time
import csv
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
import random
import matplotlib

class DataProcess():
    def __init__(self):
        super(DataProcess, self).__init__()

        self.supportPID = 0x00
        self.original_ID = []    # 以十进制数字存放初始ID
        self.new_ID = []         # 以十进制数字存放新出现ID
        self.PIDs = []            # 存放所有支持的PID

        self.final_result = {}   # 存放物理值及其对应的时间
        self.target_PIDs = [4, 5, 12, 13, 15]

        self.Service01_PIDs = {
            # 1: self.Service01_PID_1,
            # 2: self.Service01_PID_2,
            # 3: self.Service01_PID_3,
            4: self.Service01_PID_4,
            5: self.Service01_PID_5,
            # 6: self.Service01_PID_6,
            # 7: self.Service01_PID_7,
            # 8: self.Service01_PID_8,
            # 9: self.Service01_PID_9,
            # 10: self.Service01_PID_10,
            # 11: self.Service01_PID_11,
            12: self.Service01_PID_12,
            13: self.Service01_PID_13,
            # 14: self.Service01_PID_14,
            15: self.Service01_PID_15,
            # 16: self.Service01_PID_16,
            # 17: self.Service01_PID_17,
            # 18: self.Service01_PID_18,
            # 19: self.Service01_PID_19,
            21: self.Service01_PID_21,
            31: self.Service01_PID_31,
            49: self.Service01_PID_49,
        }

    def Get_PID_Response(self):
        for target_PID in self.target_PIDs:
            Data_All = self.final_result.setdefault(target_PID, {})
            Data = Data_All.setdefault('data', [])
            Time = Data_All.setdefault('time', [])
            with open('./data/{}.csv'.format(target_PID), 'r', newline="") as csv_file:
                reader = csv.reader(csv_file)
                for read in reader:
                    ID = int(read[0], 16)
                    frame = []
                    for data in eval(read[1]):
                        frame.append(int(data, 16))
                    if frame[1] == 65 and frame[2] == target_PID:
                        target_list = []
                        target_list.extend(frame[3:frame[0]+1])
                        if len(target_list) == 0:
                            continue
                        else:
                            temp_data = self.Service01_PIDs.get(target_PID)(target_list)
                            Data.append(temp_data)
                            Time.append(float(read[2]))

    def picture_generation(self, PID=1, label=''):

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        plt.figure(figsize=(21, 12), dpi=240)
       # plt.figure(figsize=(20, 10), dpi=40)
        plt.xlabel("时间", fontsize=35)
        plt.ylabel("物理信号值", fontsize=35)
        plt.title("车载CAN网络物理信号变化曲线", fontsize=35)
        plt.xticks(fontsize=35)
        plt.yticks(fontsize=35)
        plt.plot(self.final_result[PID]['time'], self.final_result[PID]['data'], label=label, linewidth=3)
        plt.legend(fontsize=35)
        plt.grid()
        plt.savefig("./phy/{0}.png".format(PID))

        plt.clf()
        plt.close()
#    -------------------------------图像数据处理部分 - ---------------------------------------------
# -----------------------------Test------------------------

    def Service01_PID_4(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = round(Data_List[0] * 100 / 255, 2)
            return target_data

    def Service01_PID_5(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = Data_List[0] - 40
            return target_data

    def Service01_PID_12(self, Data_List=[]):
        if len(Data_List) == 2:
            target_data = int(((Data_List[0] * 256) + Data_List[1]) / 4)
            return target_data

    def Service01_PID_13(self, Data_List=[]):
        if len(Data_List) == 1:
            return Data_List[0]

    def Service01_PID_15(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = Data_List[0] - 40
            return target_data

    def Service01_PID_31(self, Data_List=[]):
        if len(Data_List) == 2:
            target_data = (Data_List[0] * 256) + Data_List[1]
            return target_data

    def Service01_PID_49(self, Data_List=[]):
        if len(Data_List) == 2:
            target_data = (Data_List[0] * 256) + Data_List[1]
            return target_data

    # --------------------------------表格数据处理部分----------------------------------------------
    def Service01_PID_21(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = Data_List[0] - 40
            return(target_data)

    def Service01_PID_22(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = Data_List[1]
            return(target_data)

    def Service01_PID_23(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = Data_List[0] * Data_List[1]
            return(target_data)

    def Service01_PID_21(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = Data_List[0] - 40
            return(target_data)

    def Service01_PID_22(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = Data_List[1]
            return(target_data)

    def Service01_PID_23(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = Data_List[0] * Data_List[1]
            return(target_data)

    def Service01_PID_21(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = Data_List[0] - 40
            return(target_data)

    def Service01_PID_22(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = Data_List[1]
            return(target_data)

    def Service01_PID_23(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = Data_List[0] * Data_List[1]
            return(target_data)

    def Service01_PID_23(self, Data_List=[]):
        if len(Data_List) == 1:
            target_data = Data_List[0] * Data_List[1]
            return(target_data)

if __name__ == "__main__":
    show_test = DataProcess()
    #show_test.start(500)
    try:
        show_test.Get_PID_Response()
        print("Response has Generated")
        i = 0
        namelist = ['发动机负载(%)', '发动机冷媒温度(℃)', '发动机转速(RPM)', '车辆速度(km/s)', '进气温度(℃)', '油门位置(%)',
                    '发动机启动后的运行时间(s)', '错误码清除后的行驶距离(km)']
        for key in show_test.final_result:
            show_test.picture_generation(PID=key, label=namelist[i])
            i += 1
    finally:
        print("Picture Generated")