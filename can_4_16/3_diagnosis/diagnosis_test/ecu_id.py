from frame import Frame
from mydevice import MyDevice
import time
import csv
import json
import os


class EcuScan(MyDevice):
    def __init__(self):
        super(EcuScan, self).__init__()
        self.diagnosis_id = []

    def ecu_id(self, id_start=0x700, id_end=0x7ff):
        """根据UDS协议、扫描出所有诊断ID 通常情况下，可以向CAN ID发送诊断会话控制服务
        (0x10)的默认会话请求(也可以选取其它的诊断服务)、这是因为支持诊断的ECU通常是支持
        诊断会话控制服务的默认会话，即使某个支持诊断的ECU不支持诊断会话服务，该ECU也会回复
        UDS协议的格式的否定消息,这样也可以认为该ECU支持诊断服务"""
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'ecu_id.csv', 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='\t')
            csv_writer.writerow(["Challenge_Id", "Response_Id", "Data Domain", "Response_Type"])
            print("Ecu Scan Start")
            while id_start <= id_end:
                tx = Frame(id_start, [0x02, 0x10, 0x01])
                if self.clear_buffer() is not True:
                    ex = Exception("clear failure")
                    raise ex
                else:
                    self.transmit(tx)
                    print(hex(id_start))
                    time_start = time.time()

                    while time.time() - time_start < 1:
                        data = self.receive()
                        if 0x700 <= data.ID <= 0x7ff and data.Data[1] == 0x50:
                            self.diagnosis_id.append(hex(id_start))
                            p_list = []
                            for i in range(8):
                                p_list.append("0x" + "0" * (2 - len(hex(data.Data[i]).replace("0x", "")))
                                              + hex(data.Data[i]).replace("0x", ""))
                            csv_writer.writerow([hex(id_start), hex(data.ID), p_list, "Positive Response"])
                            break

                        if 0x700 <= data.ID <= 0x7ff and data.Data[1] == 0x7f and data.Data[2] == 0x10:
                            self.diagnosis_id.append(hex(id_start))
                            n_list = []
                            for i in range(8):
                                n_list.append("0x" + "0" * (2 - len(hex(data.Data[i]).replace("0x", "")))
                                              + hex(data.Data[i]).replace("0x", ""))
                            csv_writer.writerow([hex(id_start), hex(data.ID), n_list, "Negative Response"])
                            break

                        if 0x700 <= data.ID <= 0x7ff and data.Data[1] != 0x7f and data.Data[1] != 0x50:
                            a_list = []
                            for i in range(8):
                                a_list.append("0x" + "0" * (2 - len(hex(data.Data[i]).replace("0x", "")))
                                              + hex(data.Data[i]).replace("0x", ""))
                            csv_writer.writerow([hex(id_start), hex(data.ID), a_list, "Abnormal Response"])
                            break
                    id_start += 1
            print("Ecu Scan End")

    def id_write(self):
        f = open(os.path.dirname(os.path.realpath(__file__)) + os.sep +"id.json", "w")
        json.dump(self.diagnosis_id, f)


if __name__ == "__main__":
    ecu_scan = EcuScan()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    ecu_scan.start(baud_rate)
    try:
        ecu_scan.ecu_id()
        ecu_scan.id_write()
    except Exception as result:
        print("未知异常:%s" % result)
    finally:
        ecu_scan.stop()