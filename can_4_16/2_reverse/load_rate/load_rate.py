from frame import Frame
from mydevice import MyDevice
import time


class LoadAbnormal(MyDevice):
    def __init__(self):
        super(LoadAbnormal, self).__init__()
        self.hunt = {}
        self.total_value = 0

    def traffic_write(self, queue=None, mode=1, i=20, j=20):
        if queue is None:
            ex = Exception("no data")
            raise ex

        if mode == 0:
            while i != 0:
                data = self.receive()
                if hex(data.ID) in queue:
                    queue[hex(data.ID)] += 1
                else:
                    queue[hex(data.ID)] = 1
                i -= 1

        elif mode == 1:
            start_time = time.time()
            while time.time() - start_time <= j:
                data = self.receive()
                if hex(data.ID) in queue:
                    queue[hex(data.ID)] += 1
                else:
                    queue[hex(data.ID)] = 1
        else:
            ex = Exception("mode error")
            raise ex

    def record(self,):
        print("traffic record")
        if self.clear_buffer() is not True:
            ex = Exception("clear failure")
            raise ex

        else:
            self.traffic_write(queue=self.hunt, j=number_time)
            print(self.hunt)
            print("traffic record end")

    def load_rate_analysis(self, t=20, baud=500):
        total = 0
        for i, j in self.hunt.items():
            value = j * (44+8*8+(34+8*8)/5+3)/(t*baud*1000)
            total += j
            print("id为 0x%x 的负载率为%f" % (int(i, 16), value))
        self.total_value = total*(44+8*8+(34+8*8)/5+3)/(t*baud*1000)
        print("总线负载率为%.5f" % self.total_value)

    def normal(self, low, high):
        if low < self.total_value < high:
            print("load rate normal")

        else:
            print("load rate abnormal")


if __name__ == "__main__":
    load = LoadAbnormal()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    load.start(baud_rate)
    try:
        print('请输入收集数据时间:\r\n seconds\r\n')
        number_time = int(input())

        load.record()
        load.load_rate_analysis(t=number_time, baud=baud_rate)
        # load.normal()
    except Exception as result:
        print("unknown error:%s" % result)
    finally:
        load.stop()