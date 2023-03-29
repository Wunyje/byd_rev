from ctypes import *
import sys
sys.path.append("..")
import random
from mydevice import MyDevice
from frame import Frame
import csv
import os

class General_Fuzz(MyDevice):
    def __init__(self):
        super(General_Fuzz, self).__init__()


    def int_from_byte_list(self, byte_values, start_index=0, length=None):
        """Parses a range of unsigned-up-to-8-bit-ints (bytes) from a list into a single int
        Example:
        int_from_byte_list([0x11, 0x22, 0x33, 0x44], 1, 2) = 0x2233 = 8755
        """
        if length is None:
            length = len(byte_values)
        value = 0
        for i in (range(start_index, start_index+length)):
            value = value << 8
            value += byte_values[i]
        return value


    def data_split(self, data=[]):    #将收到的数据帧打开为半字节
        hex_data = []
        for item in data:
            #print(hex(item))
            hex_data.append((item & 0xf0) >> 4)
            hex_data.append(item & 0x0f)
            #hex_data = [int(i,16) for i in hex_data]
        return hex_data


    def apply_fuzzed_data(self, initial_data, fuzzed_nibbles, bitmap):
        fuzz_index = 0
        result_bytes = []
        for i in range(0, len(bitmap), 2):
            # Apply fuzzed nibbles on top of initial data
            if bitmap[i]:
                high_nibble = fuzzed_nibbles[fuzz_index]
                fuzz_index += 1
            else:
                high_nibble = initial_data[i]

            if bitmap[i+1]:
                low_nibble = fuzzed_nibbles[fuzz_index]
                fuzz_index += 1
            else:
                low_nibble = initial_data[i + 1]
            current_byte = (high_nibble << 4) + low_nibble
            result_bytes.append(current_byte)
        return result_bytes


    def mutate_fuzz_id(self, arb_id_bitmap,arb_id_recv=[]):    #将3个半字节ID随机组合并变异生成

        arb_id = []
        initial_arb_id = self.data_split(arb_id_recv)
        number_of_nibbles_to_fuzz_arb_id = sum(arb_id_bitmap)

        if number_of_nibbles_to_fuzz_arb_id == 0:
            arb_id = self.int_from_byte_list(self.apply_fuzzed_data(initial_arb_id, [], arb_id_bitmap))

        # Mutate arbitration ID
        if number_of_nibbles_to_fuzz_arb_id > 0:
            fuzzed_nibbles_arb_id = [random.randint(0, 0xF) for i in range(number_of_nibbles_to_fuzz_arb_id)]
            arb_id = self.apply_fuzzed_data(initial_arb_id, fuzzed_nibbles_arb_id, arb_id_bitmap)

        return arb_id


    def mutate_fuzz_data(self, data_bitmap, data_recv=[]):    #将16个半字节DATA随机组合并变异生成
        data = []
        data0 = []
        initial_data = self.data_split(data_recv)
        number_of_nibbles_to_fuzz_data = sum(data_bitmap)

        if number_of_nibbles_to_fuzz_data == 0:
            data0 = self.apply_fuzzed_data(initial_data, [], data_bitmap)

        # Mutate data
        if number_of_nibbles_to_fuzz_data > 0:
            fuzzed_nibbles_data = [random.randint(0, 0xF) for i in range(number_of_nibbles_to_fuzz_data)]
            #print(fuzzed_nibbles_data)
            data0 = self.apply_fuzzed_data(initial_data, fuzzed_nibbles_data, data_bitmap)

        for i in data0:
            #data.append('0x%02x'.upper() % i)
            data.append(i)
        return data


    def Mutate_Record(self,amount=200,mode=1,bit_mode=1):    #将8字节模糊生成的列表数组写进文件
        #file = open("E:/PythonQ/Fuzzing_Car/Three Attack/Car_fuzz/CarFuzzing/Fuzz.txt",'w')
        bitmap = []
        if bit_mode == 1:
            for _ in range(16):
                bitmap.append(random.choice([True,False]))
        elif bit_mode == 2:
            tmp = [[True,False],[False,True]]
            for _ in range(8):
                bitmap.extend(random.choice(tmp))

        print(bitmap)
        if mode == 1:  #每收到一帧就模糊一帧data，将模糊好的data与当前收到的id匹配写入文件
            self.record = [[] for _ in range(amount)]
            j = 0
            print("mode1写入开始")
            self.clear_buffer()
            while j < amount:
                self.data = self.receive()
                mut_data = self.mutate_fuzz_data(bitmap, self.data.Data)
                self.record[j].append(hex(self.data.ID))
                for n in range(8):
                    self.record[j].append(hex(mut_data[n]))

                print(self.record[j])
                j += 1

            with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +"Nor_m1.csv", "w", newline="") as f:
                wf = csv.writer(f)
                wf.writerow(["ECU_ID", "Data0", "Data1", "Data2", "Data3", "Data4", "Data5", "Data6",
                             "Data7", "模糊类型"])
                for line in self.record:
                    wf.writerow(line)


        elif mode==2:    #从已扫描好的ECUid列表里遍历指定id 模糊data，每个id生成50组模糊数据。
            list_id = self.monitor()
            print("mode2写入开始")
            self.record = [[] for _ in range(len(list_id)*amount)]
            j, n = 0, 0
            self.clear_buffer()
            for ECUid in list_id:
                while n*amount <= j < (n+1)*amount:
                    self.data = self.receive()
                    mut_data = self.mutate_fuzz_data(bitmap, self.data.Data)
                    self.record[j].append(hex(ECUid))
                    for index in range(8):
                        self.record[j].append(hex(mut_data[index]))
                    print(self.record[j])
                    j += 1
                n += 1
                j = n*amount
            with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +"Nor_m2.csv", "w", newline="") as f:
                wf = csv.writer(f)
                wf.writerow(["ECU_ID", "Data0", "Data1", "Data2", "Data3", "Data4", "Data5", "Data6", "Data7", "模糊类型"])
                for line in self.record:
                    wf.writerow(line)


    def Nor_Mut_Replay(self):
        print("常规模糊重放开始")
        fnum = len(self.record)
        while fnum>=0:
            for frame in self.record:
                self.frame = Frame(int(frame[0],16),[int(frame[1],16),int(frame[2],16),int(frame[3],16),
                        int(frame[4],16),int(frame[5],16),int(frame[6],16),int(frame[7],16),int(frame[8],16)])
                self.transmit(self.frame)
                print(hex(self.frame.id), end=' ')
                for n in range(8):
                    print(hex(self.frame.data[n]), end=' ')
                print('')
            fnum -= 1


    def monitor(self, i=20):
        ID_collect = []
        while i != 0:
            rx = self.receive()
            if rx.ID in ID_collect:pass
            else:ID_collect.append(rx.ID)
            i -= 1
        return ID_collect

if __name__=="__main__":
    Nor_fuzz = General_Fuzz()
    print("请输入选择的波特率:\r\n"
          "125 or 500\r\n")
    baud_rate = int(input())
    Nor_fuzz.start(baud_rate)
    try:
        print('请输入模糊数据的数量:\r\n')
        number_frame = int(input())
        print('请选择模糊方式:  1 or 2\r\n'
              'mode = 1:  每收到一帧就模糊一帧data，将模糊好的data与当前收到的id匹配写入文件\r\n'
              'mode = 2:  从已扫描好的ECUid列表里遍历指定id 模糊data，每个id生成给定组模糊数据\r\n(default 1)')
        fuzzy_method = int(input())
        print('请选择模糊DLC的方式:  1 or 2\r\n'
              'default 1')
        bit_m = int((input()))
        Nor_fuzz.Mutate_Record(amount=number_frame, mode=fuzzy_method, bit_mode=bit_m)

        Nor_fuzz.Nor_Mut_Replay()

    finally:
        Nor_fuzz.stop()
