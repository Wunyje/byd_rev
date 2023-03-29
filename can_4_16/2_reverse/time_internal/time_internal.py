from frame import Frame
from mydevice import MyDevice
import time
from math import log
import csv
import matplotlib.pyplot as plt
import pandas as pd
import os

class TimeGap(MyDevice):
    def __init__(self):
        super(TimeGap, self).__init__()
        self.dic = {}

    def time_write(self, dictionary=None, mode=0, i=10000, j=10):
        temporary = 0
        if dictionary is None:
            ex = Exception("no data")
            raise ex

        if mode == 0:
            while i != 0:
                data = self.receive()
                print(hex(data.ID), end="  ")
                time_point = data.TimeStamp
                time_gap = time_point - temporary
                temporary = time_point
                if time_gap != data.TimeStamp:
                    self.dic.setdefault(hex(data.ID), []).append(time_gap)
                print("TimeStamp is %d" % time_gap)
                i -= 1

        elif mode == 1:
            start_time = time.time()
            while time.time() - start_time <= j:
                data = self.receive()
                print(hex(data.ID), end="  ")
                time_point = data.TimeStamp
                time_gap = time_point - temporary
                temporary = time_point
                if time_gap != data.TimeStamp:
                    self.dic.setdefault(hex(data.ID), []).append(time_gap)
                print("TimeStamp is %d" % time_gap)
        else:
            ex = Exception("mode error")
            raise ex

    def record(self, ):
        print("message time internal record start")
        if self.clear_buffer() is not True:
            ex = Exception("clear failure")
            raise ex

        else:
            self.time_write(dictionary=self.dic, mode=m, i=number_frame, j=number_time)
            print(self.dic)
            print("message time internal record end")

    def time_analysis(self):
        for identity, values in self.dic.items():
            print(identity, end=" ")
            print("max is %d" % (max(values)), end=" ")
            print("min is %d " % (min(values)), end=" ")
            ave = sum(values) / len(values)
            print("average is ", round(ave, 2))

    def write_file(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'time_internal.csv', 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='\t')
            csv_writer.writerow(["ID", "最大时间", "最小时间", "平均时间", "报文时间间隔"])
            for key, values in self.dic.items():
                time_max = max(values)
                time_min = min(values)
                ave = round(sum(values) / len(values), 2)
                csv_writer.writerow([key, time_max, time_min, ave, values])

    def visual_time_interval(self):
        pf = pd.DataFrame.from_dict(self.dic, orient='index')
        # print(pf)
        plt.figure(figsize=(20, 8), dpi=80)
        x_axis = list(pf.columns)
        total = pf.size - sum(list(pf.isnull().sum(axis=1)))+1
        # x_length = list(range(len(x_axis)))
        x = range(1, len(x_axis) + 1)
        # print(x_length)
        id_type = list(pf.index)
        for i in id_type:
            entropy_value = pf.loc[i].values
            # print(entropy_value)
            # print(i)
            plt.plot(x, entropy_value, label="ecu_id = {}".format(i), linestyle=":", marker="o", markersize=2)
        plt.legend(loc="best")
        plt.xlabel("统计次数")
        plt.ylabel("时间间隔")
        plt.title("统计总数:{} CAN总线报文时间间隔统计".format(total))
        # plt.title("CAN总线报文时间间隔统计")
        plt.xticks(rotation=90)
        plt.savefig(os.path.dirname(os.path.realpath(__file__)) + os.sep +"time_interval.png")
        plt.show()


if __name__ == "__main__":
    time_gap = TimeGap()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    time_gap.start(baud_rate)

    try:

        number_frame = 10000
        number_time = 10
        print('请选择收集数据的方式:\r\nnumber or time\r\n')
        while True:
            m = input()
            if m == 'number':
                print('请输入预计收集数据帧数量:\r\n')
                number_frame = int(input())
                m = 0
                break
            elif m == 'time':
                print('请输入收集数据时间:\r\n seconds\r\n')
                number_time = int(input())
                m = 1
                break
            else:
                print("Input type ERROR")

        time_gap.record()
        time_gap.write_file()
        time_gap.visual_time_interval()

    # except Exception as result:
        # print("未知错误%s" % result)

    finally:
        time_gap.stop()