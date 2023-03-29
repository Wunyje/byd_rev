from frame import Frame
from mydevice import MyDevice
import csv
import time

"""根据PID协议 发送服务位为03的请求数据帧,清除该车辆中的故障码,并关闭故障指示灯"""


class clear_DTC(MyDevice):
    def __init__(self):
        super(clear_DTC, self).__init__()

        self.original_ID = []    # 以十进制数字存放初始ID
        self.DTC_data = {}

    def get_ID(self, lis=None, receive_time=20):
        if lis is None:
            lis = []
        start_time = time.time()
        while time.time() - start_time < receive_time:
            data_frame = self.receive()
            if data_frame.ID in lis:
                pass
            else:
                lis.append(data_frame.ID)

    def clear_DTC(self):
        clear_DTC.get_ID(self, lis=self.original_ID, receive_time=10)   # 获取原始ID
        temp_ID_list = []
        for num_ID in range(len(self.original_ID)):
            temp_ID_list.append(hex(self.original_ID[num_ID]))

        print(temp_ID_list)
        print("Already got initial id")

        tx = Frame(0x7DF, [0x01, 0x04])          # 03服务获取DTC故障码

        init_data = self.receive()
        init_car_time = init_data.TimeStamp
        time_start = time.time()

        for check_times in range(5):     # 循环5次确保不产生遗漏
            if self.clear_buffer() is not True:
                ex = Exception("clear failure")
                raise ex
            else:
                self.transmit(tx)

            while time.time() - time_start < 2:     # 记录所有新出现ID的数据帧
                data = self.receive()
                if data.ID in self.original_ID:
                    pass
                else:
                    print("get CLEAR CODE")
                    p_list = []
                    for i in range(8):
                        p_list.append("0x" + "0" * (2 - len(hex(data.Data[i]).replace("0x", "")))
                                      + hex(data.Data[i]).replace("0x", ""))
                    print(hex(data.ID), p_list, (data.TimeStamp - init_car_time) * 0.0001, data.DataLen)

    def check_DTC(self):
        print("check start")
        tx = Frame(0x7DF, [0x01, 0x03])  # 03服务获取DTC故障码

        init_data = self.receive()
        init_car_time = init_data.TimeStamp
        time_start = time.time()

        for check_times in range(5):  # 循环5次确保不产生遗漏
            if self.clear_buffer() is not True:
                ex = Exception("clear failure")
                raise ex
            else:
                self.transmit(tx)

            while time.time() - time_start < 2:  # 记录所有新出现ID的数据帧
                data = self.receive()
                if data.ID in self.original_ID:
                    pass
                else:
                    print("get DTC CODE")
                    p_list = []
                    for i in range(8):
                        p_list.append("0x" + "0" * (2 - len(hex(data.Data[i]).replace("0x", "")))
                                      + hex(data.Data[i]).replace("0x", ""))
                    print(hex(data.ID), p_list, (data.TimeStamp - init_car_time) * 0.0001, data.DataLen)


if __name__ == "__main__":
    clear_DTC_get = clear_DTC()
    clear_DTC_get.start(500)
    try:
        clear_DTC_get.clear_DTC()
        clear_DTC_get.check_DTC()

    except Exception as result:
        print("unknown error :%s" % result)

    finally:
        clear_DTC_get.stop()

