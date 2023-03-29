from frame import Frame
from mydevice import MyDevice
import time
from math import log
import csv
import matplotlib.pyplot as plt
import pandas as pd
import ast
import os
# 标定阶段 检测阶段 采集数据 数据预处理 熵值计算 阈值范围的确定


class TrafficAbnormal(MyDevice):
    def __init__(self):
        """ 信息熵(全部设置一个阈值)超过阈值就报警 """
        super(TrafficAbnormal, self).__init__()
        self.capture = {}

    def traffic_write(self, slice_time, arg):
        """ 不同的检测时间间隔对系统的信息熵的影响"""
        if self.capture is None:
            ex = Exception("no data")
            raise ex
        for time_point in arg:
            for i in range(slice_time):
                entropy = self.record(point=time_point)
                self.capture.setdefault(time_point, []).append(entropy)
            print("开始攻击")
        print(self.capture)

    def record(self, point):
        queue = {}
        print("first traffic record")
        if self.clear_buffer() is not True:
            ex = Exception("clear failure")
            raise ex

        else:
            start_time = time.time()
            while time.time() - start_time <= point:
                data = self.receive()
                if hex(data.ID) in queue:
                    queue[hex(data.ID)] += 1
                else:
                    queue[hex(data.ID)] = 1
            base = self.calculate_entropy(**queue)
            # print("traffic record end")
            return base

    def calculate_entropy(self, **dic):
        base_entropy = 0.0
        total = 0
        for value in dic.values():
            total += value
        for key in dic.keys():
            prob = dic[key] / total
            base_entropy -= prob * log(prob, 2)
        print(base_entropy)
        return base_entropy

    # def time_analysis(self):
    #     for slice_time, values in self.dic.items():
    #         max_num = round(max(values, 6))
    #         min_num = round(min(values, 6))
    #         print("max is %d" % max_num, end=" ")
    #         print("min is %d " % min_num, end=" ")
    #         ave = sum(values) / len(values)
    #         print("average is ", round(ave, 6))

    def write_in_txt(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'entropy.csv', 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='\t')
            csv_writer.writerow(["时间片", "最大信息熵", "最小信息熵", "平均信息熵", "时间片信息熵的统计"])
            for key, values in self.capture.items():
                max_num = round(max(values), 6)
                min_num = round(min(values), 6)
                print("max is %d" % max_num, end=" ")
                print("min is %d " % min_num, end=" ")
                ave = round(sum(values) / len(values), 6)
                csv_writer.writerow([key, max_num, min_num, ave, values])

    def visual_entropy(self):
        pf = pd.DataFrame(self.capture)
        # print(pf)
        plt.figure(figsize=(10, 8), dpi=80)
        x_axis = list(pf.index)
        # x_length = list(range(len(x_axis)))
        x = range(1, len(x_axis) + 1)
        # print(x_length)
        time_slice = list(pf.columns)
        for i in time_slice:
            entropy_value = pf.loc[:, i].values
            print(entropy_value)
            print(i)
            plt.plot(x, entropy_value, label="滑动时间窗口= {}".format(i), linestyle=":", marker="o", markersize=3)
        plt.legend(loc="best")
        plt.xlabel("时间片", fontsize=20)
        plt.ylabel("滑动时间窗口内车载CAN网络的信息熵", fontsize=20)
        plt.title("滑动时间窗口内信息熵的值", fontsize=20)
        plt.savefig("entropy/entropy.png")
        plt.xticks(x, fontsize=10)
        plt.savefig("entropy/entropy.png")
        plt.show()


if __name__ == "__main__":
    unusual = TrafficAbnormal()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    unusual.start(baud_rate)
    try:
        print('请输入数个数量不同的滑动时间窗口:\r\n(使用逗号隔开,默认 1,3,5,7,10,20)\r\n')
        lists = ast.literal_eval(input())
        print('请输入时间片:\r\n(默认 20)')
        slice_t = int(input())
        unusual.traffic_write(slice_time=slice_t, arg=lists)
        unusual.write_in_txt()
        unusual.visual_entropy()
    except Exception as result:
        print("异常错误:%s" % result)
    finally:
        unusual.stop()




















































