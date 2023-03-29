from frame import Frame
from mydevice import MyDevice


class RepayAttack(MyDevice):
    def __init__(self):
        super(RepayAttack, self).__init__()

    def transmit(self):
        data = self.receive()
if name__ == "__main__":
    feature = CrackFeature()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    feature.start(baud_rate)

    try:
        print('请输入预计收集数据帧数量:\r\n')
        number_frame = int(input())
        feature.init_feature(number_frame)
        #feature.time_gap(5)
        #feature.new_feature(number_frame)
        #feature.compare_feature()
        #feature.write_data()
        #feature.threat_data()
    #except Exception as result:
      #  print("unknown error %s" % result)

    finally:
        feature.stop()
