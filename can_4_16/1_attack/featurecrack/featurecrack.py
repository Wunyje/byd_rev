from frame import Frame
from mydevice import MyDevice
import time
import csv
import matplotlib.pyplot as plt
import pandas as pd
import os

class CrackFeature(MyDevice): # class created 
    def __init__(self):
        super(CrackFeature, self).__init__()
        self.init_data_feature = {}
        self.new_data_feature = {}
        self.compare_data_feature = {}

    def init_feature(self, j=10000): # 
        """ initial feature function """
        print("initial feature start")
        if self.clear_buffer() is not True:
            ex = Exception("clear failure")
            raise ex
        else:
            self.gather_feature(i=j, dic=self.init_data_feature, gather_mode="init_feature")
            print(self.init_data_feature)
            print("initial feature end")

    def new_feature(self, j=10000):
        """new feature function"""
        print("new feature start")
        if self.clear_buffer() is not True:
            ex = Exception("clear failure")
            raise ex
        else:
            self.gather_feature(i=j, dic=self.new_data_feature, gather_mode="new_feature")
            print(self.new_data_feature)
            print("new feature end")

    def gather_feature(self, i, dic=None, gather_mode=""):
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'data_feature/{0}.csv'.format(gather_mode), 'w', newline="") as csv_file:
            temp_writer = csv.writer(csv_file)
            while i != 0:
                data = self.receive()
                p_list = []
                for n in range(8):
                    p_list.append("0x" + "0" * (2 - len(hex(data.Data[n]).replace("0x", "")))
                                  + hex(data.Data[n]).replace("0x", ""))
                temp_writer.writerow([hex(data.ID), p_list])    #collect frame

                first = dic.setdefault(hex(data.ID), {})
                print(hex(data.ID))
                if len(data.Data) == 8:
                    # print(type(data.Data)
                    for j in range(8):
                        first.setdefault(j, [])
                        # print('2',self.init_data_feature)
                        # print('3',self.init_data_feature[hex(data.ID)][j])
                        if hex(data.Data[j]) not in dic[hex(data.ID)][j]:
                            first.setdefault(j, []).append(hex(data.Data[j]))
                else:
                    raise Exception("data length error")
                i -= 1
            print(dic)


    def compare_feature(self):
        """compare feature"""
        a = sorted(self.init_data_feature)
        # print(a)
        b = sorted(self.new_data_feature)
        # print(b)
        if len(a) != len(b):
            ex = Exception("new id appear") # Exception: new ID appear
            raise ex
        else:
            for key in a:
                first = self.compare_data_feature.setdefault(hex(int(key, 16)), {})
                for index in range(8):
                    list_first = self.init_data_feature[key][index]
                    list_second = self.new_data_feature[key][index]
                    # 在list_second列表中而不在list_first列表中
                    a = [x for x in list_second if x not in list_first]
                    second = first.setdefault(index, a)
                    print(second)

            print(self.compare_data_feature)
        print("compare feature end")

    def write_data(self):
        """file write"""
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'data_feature/feature_crack.csv', 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='\t')
            csv_writer.writerow(["ID", "数据域位置", "数据变化值"])
            for session in self.compare_data_feature:
                for item in self.compare_data_feature[session]:
                    csv_writer.writerow([session, item, self.compare_data_feature[session][item]])

    def time_gap(self, i):
        print("count down")
        time.sleep(i)

    def threat_data(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        for session in self.compare_data_feature:
            for item in self.compare_data_feature[session]:
                # print(len(self.compare_data_feature[session][item]))
                self.compare_data_feature[session][item] = len(self.compare_data_feature[session][item])

        # my_font = font_manager.FontProperties(fname="/System/Library/Fonts/PingFang.ttc")
        # plt.rcParams["font.sans-serif"] = ["SimHei"]  # 如何解决乱码的问题
        # plt.rcParams['font.family'] = 'sans-serif'
        # plt.rcParams["axes.unicode_minus"] = False
        pf = pd.DataFrame(self.compare_data_feature)
        # print(pf)
        # 设置图形的大小
        plt.figure(figsize=(36, 10), dpi=180)
        x_axis = list(pf.columns)
        x_length = list(range(len(x_axis)))
        bar_width = 0.1
        for j in list(pf.index):
            t1 = pf.loc[j].values
            plt.bar(x_length, t1, width=bar_width, label="特征位置%d" % (int(j)+1))

            x_length = [k + bar_width for k in x_length]
        plt.legend(loc="best")
        plt.xlabel("车载CAN网络ID", fontsize=20)
        plt.ylabel("数据域特征变化次数", fontsize=20)
        plt.title("车载CAN网络数据域特征变化", fontsize=20)
        a_length = [i - bar_width * 4 for i in x_length]
        plt.xticks(a_length, x_axis, rotation=45, fontsize=20)
        plt.grid()
        plt.savefig(os.path.dirname(os.path.realpath(__file__)) + os.sep + "data_feature/ecu_id.png")
        plt.show()


if __name__ == "__main__":
    feature = CrackFeature()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    feature.start(baud_rate)

    try:
        print('请输入预计收集数据帧数量:\r\n')
        number_frame = int(input())
        feature.init_feature(number_frame) # initial frame(what is feature?)
        feature.time_gap(5)
        feature.new_feature(number_frame) # added frame
        feature.compare_feature()
        feature.write_data()
        feature.threat_data()
    except Exception as result:
        print("unknown error %s" % result)

    finally:
        feature.stop()
