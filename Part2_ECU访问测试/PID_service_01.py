from frame import Frame
from mydevice import MyDevice
import csv
import time


"""根据PID协议 发送PID码为0x00 0x20 0x40等校验位的数据帧，记录汽车对改检验帧的反馈并记录到
    PIDs_response。csv文件中，再根据协议对响应进行分析，获取检测汽车所支持的所有PID码，并构造
    相应的PID检测数据帧，发送至汽车并记录其对应反馈数据流"""


class PID(MyDevice):
    def __init__(self):
        super(PID, self).__init__()

        self.supportPID = 0x00
        self.original_ID = []    # 以十进制数字存放初始ID
        self.new_ID = []         # 以十进制数字存放新出现ID
        self.PIDs = []            # 存放所有支持的PID

    def get_ID(self, lis=[], receive_time=20):

        start_time = time.time()
        while time.time() - start_time < receive_time:
            data_frame = self.receive()
            if data_frame.ID in lis:
                pass
            else:
                lis.append(data_frame.ID)
                print(data_frame.ID)

    def get_PID_frame(self):
        PID.get_ID(self, lis=self.original_ID, receive_time=10)   # 获取原始ID
        temp_ID_list = []
        print('test')
        for num_ID in range(len(self.original_ID)):
            temp_ID_list.append(hex(self.original_ID[num_ID]))

        print(temp_ID_list)
        print("Already got initial id")
        with open("data/PIDs_response.csv", 'w', newline="") as csv_file:
            file_writer = csv.writer(csv_file)
            file_writer.writerow(['Original ID', temp_ID_list])

            while True:
           # for pid_title in self.supportPID:
                tx = Frame(0x7DF, [0x02, 0x01, self.supportPID])

                file_writer.writerow([hex(self.supportPID), 'PID phase'])  # 区分每一段（32PID）的具体支持情况

                init_data = self.receive()
                init_car_time = init_data.TimeStamp
                time_start = time.time()

                print("get new ID start")

                for check_times in range(5):     # 循环5次确保不产生遗漏
                    if self.clear_buffer() is not True:
                        ex = Exception("clear failure")
                        raise ex
                    else:
                        self.transmit(tx)

                    while time.time() - time_start < 0.2:     # 记录所有新出现ID的数据帧
                        data = self.receive()
                        if data.ID in self.original_ID:
                            pass
                        else:
                            print("get")
                            self.new_ID.append(hex(data.ID))
                            print(self.new_ID)
                            p_list = []
                            for i in range(8):
                                p_list.append("0x" + "0" * (2 - len(hex(data.Data[i]).replace("0x", "")))
                                              + hex(data.Data[i]).replace("0x", ""))
                            file_writer.writerow([hex(data.ID), p_list, (data.TimeStamp - init_car_time) * 0.0001,
                                                  data.DataLen])

                            if data.Data[0] >= 3:                   # 确定具体支持的PID数值
                                data_start = data.Data[0] - 3
                                temp_10_list = []
                                temp_2_list = ''
                                for j in range(4):
                                    temp_2_list += ("0" * (8 - len(bin(data.Data[data_start+j]).replace("0b", "")))
                                           + bin(data.Data[data_start+j]).replace("0b", ""))
                                for n in range(len(temp_2_list)):            # 收集功能PID的十进制数 1-31,32位则表示该车是否支持下一阶段的支持PID
                                    if temp_2_list[n] == '1':
                                        temp_10_list.append(n+1+self.supportPID)
                                file_writer.writerow([hex(data.ID), temp_10_list])
                                self.PIDs = self.get_max_list(list_1=temp_10_list, list_2=self.PIDs)

                if self.PIDs[-1] % 32 == 0:      # 在supportPID显示不支持下一段时，及时停止继续发送接收数据帧
                    self.supportPID += 0x20
                else:
                    break

    def get_max_list(self, list_1=[1, 2, 3], list_2=[1]):  # 得到两列表包含的所有元素
        temp_list = list_1 + list_2
        temp_list.sort()
        max_list = []
        for i in range(len(temp_list)):
            if temp_list[i] in max_list:
                pass
            else:
                max_list.append(temp_list[i])
        return max_list

    def PID_pipeline(self, collect_time=10):
        for value in range(len(self.PIDs)):
            pid = self.PIDs[value]
            print('Already finished:', pid)
            send_frame = Frame(0x7DF, [0x02, 0x01, pid])

            with open('data/{0}.csv'.format(pid), 'w', newline="") as csv_file:
                file_writer = csv.writer(csv_file)

                time_start = time.time()
                init_data = self.receive()
                init_car_time = init_data.TimeStamp

                while time.time() - time_start <= collect_time:

                    start_time_1 = time.time()
                    self.transmit(tx_frame=send_frame)

                    while time.time() - start_time_1 < 0.10:        # 该处实际响应有可能会有多值
                        data = self.receive()
                        if data.ID not in self.original_ID:
                            p_list = []
                            for i in range(8):
                                p_list.append("0x" + "0" * (2 - len(hex(data.Data[i]).replace("0x", "")))
                                              + hex(data.Data[i]).replace("0x", ""))
                            file_writer.writerow([hex(data.ID), p_list, (data.TimeStamp - init_car_time) * 0.0001,
                                                  data.DataLen])
                        else:
                            continue


if __name__ == "__main__":
    PID_get = PID()
    PID_get.start(500)
    try:
        PID_get.get_PID_frame()
        PID_get.PID_pipeline(collect_time=20)    # 确定每个PID接收数据时间

    except Exception as result:
        print("unknown error :%s" % result)

    finally:
        PID_get.stop()

