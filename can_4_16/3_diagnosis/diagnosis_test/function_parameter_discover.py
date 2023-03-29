from frame import Frame
from mydevice import MyDevice
import time
import csv
import json


class FunctionCrack(MyDevice):
    def __init__(self):
        super(FunctionCrack, self).__init__()

    def function_crack(self, ecu_id=0x7e0, service_id=0x31, sub_function=0x10):
        length = False
        valid_length = 0
        for i in range(3, 8):
            tx_frame = Frame(ecu_id, [i, service_id, sub_function, 0xff, 0xff, 0xff, 0xff, 0xff])
            self.clear_buffer()
            self.transmit(tx_frame)  # 确定数据长度
            while True:
                data = self.receive()
                if 0x7FF >= data.ID >= 0x700:
                    if data.Data[1] == 0x7f and data.Data[3] == 0x13:
                        break
                    else:
                        length = True
                        valid_length = i
                        break
            if length is True:
                break

        if length is False:  # 对应长度的穷举扫描
            print("无法找到该子功能其有效的数据长度", end='')
            print(hex(sub_function))
        else:
            print(hex(sub_function), end="")
            print('子功能详细服务信息：')
            print('###########send################', end="    ")
            print('###########receive#############')
            tx_data = [valid_length, service_id, sub_function, 0x00, 0x00, 0x00, 0x00, 0x00]
            size = "FF" * (valid_length - 2)
            size = int(size, 16)
            for n in range(0, size):
                initial_data = "0" * (10 - len(hex(n).replace('0x', ''))) + hex(n).replace('0x', '')
                tx_data[3] = int(initial_data[8:10], 16)
                tx_data[4] = int(initial_data[6:8], 16)
                tx_data[5] = int(initial_data[4:6], 16)
                tx_data[6] = int(initial_data[2:4], 16)
                tx_data[7] = int(initial_data[0:2], 16)
                # print(tx_data)
                # self.clear_buffer()
                rx_frame = self.receive()
                for i in range(8):
                    print(hex(rx_frame.Data[i]), end=" ")
                self.transmit(tx_data)
                while True:
                    rx_data = self.receive()
                    if 0x7FF >= rx_data.ID >= 0x700:
                        for i in range(8):
                            print(hex(rx_data.Data[i]), end=" ")
                        if rx_data.Data[1] == 0x71:
                            print("破解成功")
                        break


if __name__ == "__main__":
    crack = FunctionCrack()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    crack.start(baud_rate)

    try:
        crack.function_crack()

    except Exception as result:
        print("unknown error %s" % result)

    finally:
        crack.stop()
