from frame import Frame
from mydevice import MyDevice
import json
import ast

# 标定阶段 检测阶段 采集数据 数据预处理 熵值计算 阈值范围的确定


class Relative_Entropy_Dectection(MyDevice):
    def __init__(self):
        super(Relative_Entropy_Dectection, self).__init__()
        self.capture = {}
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
        f = open("relative_entropy/normal_data_set.json", "w")
        json.dump(self.capture, f)


if __name__ == "__main__":
    usual = Relative_Entropy_Dectection()
    print("请输入波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    usual.start(baud_rate)
    try:
        print('请输入数个数量不同的滑动窗口:\r\n(使用逗号隔开,默认 1000,2000,3000)\r\n')
        lists = ast.literal_eval(input())

        usual.traffic_write(arg=lists)
        usual.data_write()
    except Exception as result:
        print("异常错误:%s" % result)
    finally:
        usual.stop()
