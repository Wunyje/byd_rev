from frame import Frame
from mydevice import MyDevice
import csv
import time


"""根据PID协议 发送服务位为03的请求数据帧，记录汽车对该检验帧的反馈并记录到
    DTCs_stored.csv文件中，再根据协议对响应进行分析，直接得到故障码"""


class DTC(MyDevice):
    def __init__(self):
        super(DTC, self).__init__()

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

    def get_DTC_frame(self):
        DTC.get_ID(self, lis=self.original_ID, receive_time=10)   # 获取原始ID
        temp_ID_list = []
        for num_ID in range(len(self.original_ID)):
            temp_ID_list.append(hex(self.original_ID[num_ID]))

        print(temp_ID_list)
        print("Already got initial id")
        with open("DTC/DTCs_stored.csv", 'w', newline="") as csv_file:
            file_writer = csv.writer(csv_file)
            file_writer.writerow(['Original ID', temp_ID_list])

            tx = Frame(0x7DF, [0x01, 0x03])          # 03服务获取DTC故障码

            init_data = self.receive()
            init_car_time = init_data.TimeStamp
            time_start = time.time()

            print("get DTC start")

            for check_times in range(5):     # 循环5次确保不产生遗漏
                temp_DTC_data = self.DTC_data.setdefault(check_times, [])
                file_writer.writerow(['Number:', check_times])
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
                        print("get")
                        print(hex(data.ID))
                        p_list = []
                        for i in range(8):
                            p_list.append("0x" + "0" * (2 - len(hex(data.Data[i]).replace("0x", "")))
                                          + hex(data.Data[i]).replace("0x", ""))
                        file_writer.writerow([hex(data.ID), p_list, (data.TimeStamp - init_car_time) * 0.0001,
                                              data.DataLen])
                        temp_DTC_data.append(data.Data)    # 收集数据用于获取真实DTC

    def get_real_DTC(self):                     # 获取真实DTC
        with open('DTC/DTCs_stored.csv', 'a', newline='') as csv_file:
            file_writer = csv.writer(csv_file)

            for times in self.DTC_data:
                file_writer.writerow(['Number', times])
                for i in range(len(self.DTC_data[times])):
                    temp_2_list = ''
                    temp_data = self.DTC_data[times][i]
                    for j in range(2, 4):                    # 获取十六位二进制码
                        temp_2_list += ("0" * (8 - len(bin(temp_data[j]).replace("0b", ""))) +
                                        bin(temp_data[j]).replace("0b", ""))

                    target_list = ''
                    target_list += self.get_DTC_character_1(temp_2_list[:2])
                    target_list += self.get_DTC_character_2(temp_2_list[2:4])
                    target_list += self.get_DTC_character_2(temp_2_list[4:8])
                    target_list += self.get_DTC_character_2(temp_2_list[8:12])
                    target_list += self.get_DTC_character_2(temp_2_list[12:16])

                    file_writer.writerow(target_list)

    def get_DTC_character_1(self, temp_string=''):
        if temp_string == '00':
            return 'P'
        elif temp_string == '01':
            return 'C'
        elif temp_string == '10':
            return 'B'
        elif temp_string == '11':
            return 'U'
        else:
            print("ERROR")

    def get_DTC_character_2(self, temp_string=''):
        return hex(int(temp_string, 2)).replace('0x', '')

if __name__ == "__main__":
    DTC_get = DTC()
    DTC_get.start(500)
    try:
        DTC_get.get_DTC_frame()
        DTC_get.get_real_DTC()

    except Exception as result:
        print("unknown error :%s" % result)

    finally:
        DTC_get.stop()

