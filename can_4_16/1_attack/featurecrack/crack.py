from frame import Frame
from mydevice import MyDevice
import time
import csv
import matplotlib.pyplot as plt
import pandas as pd
import os

class TrafficRecord(MyDevice):
    def __init__(self):
        super(TrafficRecord, self).__init__()
        self.record_first = {}
        self.record_second = {}

    def monitor(self, mode=0, i=10000, j=10, dic=None):
        if mode == 0:
            while i != 0:
                rx = self.receive()
                if hex(rx.ID) in dic:
                    dic[hex(rx.ID)] += 1
                else:
                    dic[hex(rx.ID)] = 1
                i -= 1

        elif mode == 1:
            time0 = time.time()
            while time.time() - time0 <= j:
                rx = self.receive()
                if hex(rx.ID) in dic:
                    dic[hex(rx.ID)] += 1
                else:
                    dic[hex(rx.ID)] = 1

        if dic is None:
            ex = Exception("not receive data")
            raise ex

    def operation_first(self, ):
        print("The first traffic recording beginning, please do not perform any operation")
        if self.clear_buffer() is not True:
            ex = Exception("clear failure first")
            raise ex
        else:
            self.monitor(mode=m, i=number_frame, j=number_time, dic=self.record_first)
            print(self.record_first)
            print("the first recording ending")

    def operation_second(self, ):
        print("the second traffic recording beginning,please repeatedly perform a operation")
        if self.clear_buffer() is not True:
            ex = Exception("clear failure second")
            raise ex
        else:
            self.record_second = dict.fromkeys(self.record_first.keys(), 0)
            self.monitor(mode=m, i=number_frame, j=number_time, dic=self.record_second)
            print(self.record_second)
            print("the second traffic recording ending")

    def write_file(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'data_crack/flow.csv', 'w', newline="")as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(["ID", "Flow"])
            for k, v in self.record_first.items():
                writer.writerow([hex(int(k, 16)), v])
            writer.writerow(["second detection"])
            for k, v in self.record_second.items():
                writer.writerow([hex(int(k, 16)), v])
        print("successfully write")

    def timer(self):
        print("count down")
        time.sleep(5)

    def threat_data(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        pf = pd.DataFrame({"first": self.record_first, "second": self.record_second})
        # print(pf)
        # 设置图形的大小
        plt.figure(figsize=(30, 8), dpi=160)
        x_axis = list(pf.index)
        x_length = list(range(len(x_axis)))
        bar_width = 0.1
        c_list = list(pf.columns)
        total = 0
        for i in c_list:
            t1 = pf.loc[:,i].values
            total = pf.loc[:, i].sum()
            plt.bar(x_length, t1, width=bar_width, label="统计:{}".format(i))
            x_length = [k + bar_width for k in x_length]
        plt.legend(loc="best")
        plt.xlabel("车载CAN网络ID", fontsize=20)
        plt.ylabel("车载CAN网络数据包出现的次数", fontsize=20)
        plt.title("统计{}数据包:数据包ID的变化情况".format(total), fontsize=20)
        a_length = [i - bar_width for i in x_length]
        plt.xticks(a_length, x_axis, rotation=45, fontsize=15)
        plt.grid()
        plt.savefig(os.path.dirname(os.path.realpath(__file__)) + os.sep +"data_crack/id.png")
        plt.show()


if __name__ == "__main__":
    crack = TrafficRecord()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    crack.start(baud_rate)

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
        crack.operation_first()
        crack.timer()     #stop 5s and start action
        crack.operation_second()
        crack.write_file()
        crack.threat_data()

    except Exception as result:
        print("unknown error %s" % result)

    finally:
        crack.stop()




