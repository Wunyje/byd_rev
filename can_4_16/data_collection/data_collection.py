from frame import Frame
from mydevice import MyDevice
import csv
import time
import os

class Collect(MyDevice):
    def __init__(self):
        super(Collect, self).__init__()
        self.init_car_time = 0

    def capture(self, number_time=10):
        if self.clear_buffer() is not True:
            ex = Exception("clear failure")
            raise ex
        else:
            print("begin")
            with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'data.csv', 'w', newline="") as csv_file:
                replay_writer = csv.writer(csv_file)

                init_data = self.receive()
                self.init_car_time = init_data.TimeStamp
                time0 = time.time()
                while time.time() - time0 <= number_time: # collecting time determination
                    data = self.receive() 
                    p_list = []
                    for i in range(8):
                        p_list.append("0x" + "0" * (2 - len(hex(data.Data[i]).replace("0x", "")))
                                      + hex(data.Data[i]).replace("0x", ""))
                    replay_writer.writerow([hex(data.ID), p_list, (data.TimeStamp-self.init_car_time) * 0.0001, data.TimeStamp])
            print("end")

    def time_gap(self, i):
        print("count down")
        time.sleep(i)


if __name__ == "__main__":
    collect_data = Collect()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    collect_data.start(baud_rate)
    try:
        print('请输入预计收集数据帧时间:\r\n')
        number_time = int(input())
        collect_data.capture(number_time)

    except Exception as result:
        print("unknown error :%s" % result)

    finally:
        collect_data.stop()