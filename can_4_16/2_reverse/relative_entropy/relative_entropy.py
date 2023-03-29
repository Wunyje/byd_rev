from frame import Frame
from mydevice import MyDevice
from math import log
import json
from collections import OrderedDict
import matplotlib.pyplot as plt
import pandas as pd
import ast
import os

# 标定阶段 检测阶段 采集数据 数据预处理 熵值计算 阈值范围的确定



class Relative_Entropy_Dectection(MyDevice):
    def __init__(self):
        """ 信息熵(全部设置一个阈值)超过阈值就报警 """
        super(Relative_Entropy_Dectection, self).__init__()
        self.capture = {}
        self.relative_entropy = {}
        self.center = {}

    def traffic_write(self, arg):
        if self.capture is None:
            ex = Exception("no data")
            raise ex

        for time_point in arg:
            first = self.capture.setdefault(time_point, {})
            self.record(point=time_point)
            for k, v in self.center.items():
                first.setdefault(k, v)

    def record(self, point):
        self.center.clear()
        print("first traffic record")
        if self.clear_buffer() is not True:
            ex = Exception("clear failure")
            raise ex

        else:
            while point != 0:
                rx = self.receive()
                if hex(rx.ID) in self.center:
                    self.center[hex(rx.ID)] += 1
                else:
                    self.center[hex(rx.ID)] = 1
                point -= 1

    def data_write(self):
        f = open(os.path.dirname(os.path.realpath(__file__)) + os.sep +"normal_data_set.json", "w")
        json.dump(self.capture, f)


    def get_relative_entropy(self,):
        f = open(os.path.dirname(os.path.realpath(__file__)) + os.sep +"normal_data_set.json", "r")
        store_data = json.load(f)
        capture_sort = sorted(self.capture.items(), key=lambda x: x[0])
        store_sort = sorted(store_data.items(), key=lambda x: x[0])
        for (capture_key, capture_value), (store_key, store_value) in zip(capture_sort, store_sort):
            a = sorted(capture_value.items(), key=lambda x: x[0])
            b = sorted(store_value.items(), key=lambda x: x[0])
            first = self.relative_entropy.setdefault(capture_key, {})
            for (k, k1), (k2, k3) in zip(a, b):
                value = k1 / capture_key * log(k1 / k3, 2)
                first.setdefault(k, value)

    def entropy_visual(self):
        pf = pd.DataFrame(self.relative_entropy)
        # print(pf)
        plt.figure(figsize=(20, 10), dpi=100)
        x_axis = list(pf.index)
        # print(x_axis)
        x_length = list(range(len(x_axis)))
        bar_width = 0.2
        for j in list(pf.columns):
            t1 = pf.loc[:, j].values
            print(t1)
            plt.bar(x_length, t1, width=bar_width, label="滑动窗口%d" % j)
            x_length = [k + bar_width for k in x_length]
        plt.legend(loc="best", fontsize=20)
        plt.xlabel("车载CAN网络 ID", fontsize=20)
        plt.ylabel("relative_entropy", fontsize=20)
        plt.title("车载CAN网络数据包ID的相对熵", fontsize=20)
        a_length = [i - 2 * bar_width for i in x_length]
        plt.xticks(a_length, x_axis, fontsize=20,rotation=45)
        plt.savefig(os.path.dirname(os.path.realpath(__file__)) + os.sep +"relative_entropy_detection.png")
        plt.show()


if __name__ == "__main__":
    usual = Relative_Entropy_Dectection()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    usual.start(baud_rate)
    try:
        print('请输入数个数量不同的滑动窗口:\r\n(使用逗号隔开,默认 1000,2000,3000)\r\n')
        lists = ast.literal_eval(input())

        usual.traffic_write(arg=lists)
        usual.data_write()

        usual.get_relative_entropy()
        usual.entropy_visual()
    # except Exception as result:
        # print("异常错误:%s" % result)
    finally:
        usual.stop()



