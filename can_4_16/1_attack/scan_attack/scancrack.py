from frame import Frame
from mydevice import MyDevice
import time
import random


class CrackScan(MyDevice):
    def __init__(self):
        super(CrackScan, self).__init__()
        self.ecu_id = []
        self.send_data = []

    def ecu_scan(self):
        time0 = time.time()
        while time.time()-time0 < 10:
            data = self.receive()
            if data.ID in self.ecu_id:
                pass
            else:
                self.ecu_id.append(data.ID)
        if self.ecu_id is None:
            ex = Exception("没有搜索到id")
            raise ex

    def mode_control(self, mode):
        if mode == 0:
            self.send_data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        if mode == 1:
            self.send_data = [0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff]
        if mode == 2:
            self.send_data = self.get_random_data()

    def get_random_data(self, min_length=0, max_length=8):
        """
        Generates a list of random data bytes, whose length lies in the interval 'min_length' to 'max_length'

        :param min_length: int minimum length
        :param max_length: int maximum length
        :return: list of randomized bytes
        """
        # Decide number of bytes to generate
        data_length = random.randint(min_length, max_length)
        # Generate random bytes
        data = []
        for i in range(data_length):
            data_byte = random.randint(0, 255)
            data.append(data_byte)
        for i in range(0, 8 - data_length):
            data.append(0)
        return data

    def scan_crack(self, ):
        for id in self.ecu_id:
            print("测试id:%x" % id)
            if self.clear_buffer() is not True:
                ex = Exception("清空失败")
                raise ex
            else:
                time0 = time.time()
                while time.time() - time0 < 10:
                    self.mode_control(mode=test_mode)
                    tx_data = Frame(id, self.send_data)
                    self.transmit(tx_frame=tx_data)

    def fuzzy_test(self, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]):
        for i in range(0, 8):
            seed = random.randint(0, 255)
            data[i] = seed
        return data


if __name__ == "__main__":
    crack = CrackScan()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    crack.start(baud_rate)
    try:
        print("请选择模拟数据的类型:\r\n"
              "mode = 0:   data = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]\r\n"
              "mode = 1:   data = [0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff]\r\n"
              "mode = 2:   data = random with the limit of DLC\r\n")
        test_mode = int(input())
        crack.ecu_scan()
        crack.scan_crack()
    except Exception as result:
        print("未知异常:%s" % result)
    finally:
        crack.stop()


