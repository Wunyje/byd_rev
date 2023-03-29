from frame import Frame
from mydevice import MyDevice
import csv
import time


"""根据PID协议中service09规定的PID类型，向汽车发送请求数据帧，记录汽车对改检验帧的反馈并记录到
    car_information文件夹中，再根据协议对响应进行分析，获取检测汽车VIN、校验ID、根据汽车类型（压缩点火或火花点火）所显示的不同
    使用表现跟踪数据以及ECU名称等信息"""


class PID(MyDevice):
    def __init__(self):
        super(PID, self).__init__()
        self.test_PID = [1, 2, 3]
        self.supportPID = 0x00
        self.original_ID = []    # 以十进制数字存放初始ID
        self.PIDs = []            # 存放所有支持的PID

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

    def get_PID_frame(self):
        PID.get_ID(self, lis=self.original_ID, receive_time=10)   # 获取原始ID
        temp_ID_list = []
        for num_ID in range(len(self.original_ID)):
            temp_ID_list.append(hex(self.original_ID[num_ID]))

        print(temp_ID_list)
        print("Already got initial id")
        with open("car_information/PIDs_response.csv", 'w', newline="") as csv_file:
            file_writer = csv.writer(csv_file)
            file_writer.writerow(['Original ID', temp_ID_list])

            tx = Frame(0x7DF, [0x02, 0x09, self.supportPID])

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

                while time.time() - time_start < 0.5:     # 记录所有新出现ID的数据帧
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

    def PID_pipeline(self, collect_time=12):
        for value in range(len(self.PIDs)):
            pid = self.PIDs[value]
            send_frame = Frame(0x7DF, [0x02, 0x09, pid])

            with open('car_information/{0}.csv'.format(pid), 'w', newline="") as csv_file:
                file_writer = csv.writer(csv_file)

                time_start = time.time()
                init_data = self.receive()
                init_car_time = init_data.TimeStamp

                while time.time() - time_start <= collect_time:

                    start_time_1 = time.time()
                    self.transmit(tx_frame=send_frame)

                    while time.time() - start_time_1 < 3:  # 该处实际响应有可能会有多值
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
       # PID_get.get_PID_frame()
        PID_get.PID_pipeline(collect_time=10)    # 确定每个PID接收数据时间

    except Exception as result:
        print("unknown error :%s" % result)

    finally:
        PID_get.stop()

