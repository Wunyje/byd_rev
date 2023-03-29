from frame import Frame
from mydevice import MyDevice
import time
import csv
import json
import os

class ScanServiceId(MyDevice):
    def __init__(self):
        super(ScanServiceId, self).__init__()
        self.service_id = {}
        self.sub_function = {}

    def scan_service(self, service_id_start=0x00, service_id_end=0xff):
        """ 将扫描出来的诊断ID 依次扫描 找出各诊断ID的服务的支持情况 """
        f = open(os.path.dirname(os.path.realpath(__file__)) + os.sep +"id.json", "r")
        store_data = json.load(f)
        for column in store_data:
            diagnosis_id = int(column, 16)
            print("Service Id Scan Start")
            # print(hex(ecu_id))
            service_id_start = 0x00
            while service_id_start <= service_id_end:
                if self.clear_buffer() is not True:
                    ex = Exception("clear failure")
                    raise ex
                else:
                    send_frame = Frame(diagnosis_id, [0x02, service_id_start, 0x01])
                    self.transmit(send_frame)
                    print(hex(service_id_start))
                    time_start = time.time()
                    while time.time() - time_start < 1:
                        data = self.receive()
                        if 0x700 <= data.ID <= 0x7ff:
                            a = self.service_id.setdefault(hex(diagnosis_id), [])
                            if data.Data[1] == service_id_start + 0x40:
                                a.append(hex(service_id_start))
                            elif data.Data[1] == 0x7f:
                                if data.Data[3] != 0x11:
                                    a.append(hex(service_id_start))

                            else:
                                print("Abnormal Response")
                            break
                    service_id_start += 1
        print(self.service_id)
        print("Service Id Scan End")

    def service_id_write(self):
        f = open(os.path.dirname(os.path.realpath(__file__)) + os.sep +"id.json", "w")
        json.dump(self.service_id, f)

    def scan_sub_function(self):
        """ 单个诊断CAN ID 支持的服务下的子功能情况"""
        sub_function = 0x00
        f = open(os.path.dirname(os.path.realpath(__file__)) + os.sep +"service_id.json", "r")
        store_data = json.load(f)
        print("Sub Function Scan Start")
        while sub_function <= 0xff:
            if self.clear_buffer() is not True:
                ex = Exception("clear failure")
                raise ex
            else:
                for i, j in store_data.items():
                    ecu_id = int(i, 16)
                    for service in j:
                        ser_id = int(service, 16)
                        send_frame = Frame(ecu_id, [0x02, ser_id, sub_function])
                        self.transmit(tx_frame=send_frame)
                        print(hex(sub_function), end=" ")
                        time_start = time.time()
                        while time.time() - time_start < 2:
                            data = self.receive()
                            if 0x700 <= data.ID <= 0x7ff:
                                first = self.sub_function.setdefault(hex(ecu_id), {})
                                if data.Data[1] == ser_id + 0x40:
                                    first.setdefault(ser_id, []).append(hex(sub_function))
                                    print(hex(data.ID), end=" ")
                                    print(hex(data.Data[0]), hex(data.Data[1]), hex(data.Data[2]),
                                          hex(data.Data[3]), hex(data.Data[4]), hex(data.Data[5]), hex(data.Data[6]),
                                          hex(data.Data[7]), end=" ")
                                    print("positive Response")
                                # 0x12 表示不支持子功能      0x11表示不支持服务  0x12 表示数据的实际长度不够
                                elif data.Data[1] == 0x7f and data.Data[2] == ser_id and data.Data[3] != 0x12:
                                    first.setdefault(ser_id, []).append(hex(sub_function))
                                    print(hex(data.ID), end=" ")
                                    print(hex(data.Data[0]), hex(data.Data[1]), hex(data.Data[2]),
                                          hex(data.Data[3]), hex(data.Data[4]), hex(data.Data[5]), hex(data.Data[6]),
                                          hex(data.Data[7]), end=" ")
                                    print("negative Response")
                                elif data.Data[1] == 0x7f and data.Data[2] == ser_id and data.Data[3] == 0x12:
                                    print(hex(data.ID), end=" ")
                                    print(hex(data.Data[0]), hex(data.Data[1]), hex(data.Data[2]),
                                          hex(data.Data[3]), hex(data.Data[4]), hex(data.Data[5]), hex(data.Data[6]),
                                          hex(data.Data[7]), end=" ")
                                    print("sub_function not ")

                                else:
                                    print(hex(data.ID), end=" ")
                                    print(hex(data.Data[0]), hex(data.Data[1]), hex(data.Data[2]),
                                          hex(data.Data[3]), hex(data.Data[4]), hex(data.Data[5]), hex(data.Data[6]),
                                          hex(data.Data[7]), end=" ")
                                    print("Abnormal Response")
                                break
                sub_function += 1
        print("Sub Function:", self.sub_function)
        print("Sub Function Scan End")

    def file_data_service(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'service_id.csv', 'w', newline="") as service_file:
            service_write = csv.writer(service_file, delimiter='\t')
            service_write.writerow(["diagnosis id", "service id"])
            for key, value in self.service_id.items():
                service_write.writerow([key, value])

    def file_data_sub_function(self):
        """file write"""
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'sub_function.csv', 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='\t')
            csv_writer.writerow(["diagnosis id", "service id", "sub function"])
            for session in self.sub_function:
                for item in self.sub_function[session]:
                    csv_writer.writerow([session, hex(item), self.sub_function[session][item]])


if __name__ == "__main__":
    service_scan_id = ScanServiceId()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    service_scan_id.start(baud_rate)
    try:
        # service_scan_id.scan_service()
        # service_scan_id.service_id_write()
        # service_scan_id.file_data_service()
        service_scan_id.scan_sub_function()
        service_scan_id.file_data_sub_function()

    except Exception as result:
        print("unknown error :%s" % result)
    finally:
        service_scan_id.stop()
