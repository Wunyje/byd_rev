from READ import read
from copy import deepcopy
import numpy as np
import csv
from PHY_wave import wave


class LibreCAN(read, wave):
    def __init__(self, unused_len_00, append_len_01,
                 flip_th_02, multi_th_03, relation_th_1,
                 average_flip_th_20, body_th_23):
        super(LibreCAN, self).__init__()
        # [parameter predefined]
        # phase 0
        self.unused_len_00 = unused_len_00
        self.append_len_01 = append_len_01
        self.flip_th_02 = flip_th_02
        self.multi_th_03 = multi_th_03
        # phase 1
        self.relation_th_1 = relation_th_1
        # phase 2
        self.average_flip_th_20 = average_flip_th_20
        self.body_th_23 = body_th_23

        # [data]
        # phase 0
        self.bit_change = {}
        self.bit_dont_change = {}
        self.can_id = []
        self.data_sample_64 = {}
        self.data_64 = {}
        self.characteristic_num = {}
        # phase 2
        self.ref_data_64 = {}
        self.ref_flip_rate = {}

        # [label]
        # phase 0
        self.POSS = {}
        self.UNUSED = {}
        self.CONST = {}
        self.MULTI = {}
        self.Counter = {}
        self.PHY = {}
        self.CRC = {}
        # phase 2
        self.reference = {}
        self.event_data_64 = {}

    def pre_label(self):
        """

        :return:
        """
        """
        1.first, we copy the bit_flip_rate dic into 2 dics: 
        bit_change and bit_dont_change, which has the same 
        keys but none value. they re used to take the change/
        dont_change label and regions.
        """
        self.can_id = self.bit_flip.keys()
        self.bit_change = self.bit_change.fromkeys(self.can_id)
        self.bit_dont_change = self.bit_dont_change.fromkeys(self.can_id)
        # test print(self.bit_change)
        """
        2.sort into 2 dics: change and dont_change
        """
        for k, v in self.bit_flip.items():
            self.bit_change[k] = []
            self.bit_dont_change[k] = []
            signal_start = 0
            prev_v = v[0]
            for signal_end in range(1, 64):
                if v[signal_end] != 0 and prev_v == 0:
                    self.bit_dont_change[k].append(['dont_change', signal_start, signal_end - 1])
                    prev_v = v[signal_end]
                    signal_start = signal_end
                elif v[signal_end] == 0 and prev_v != 0:
                    self.bit_change[k].append(['POSS', signal_start, signal_end - 1])
                    prev_v = v[signal_end]
                    signal_start = signal_end
                else:
                    prev_v = v[signal_end]
            if v[63] == 0:
                self.bit_dont_change[k].append(['dont_change', signal_start, 63])
            else:
                self.bit_change[k].append(['POSS', signal_start, 63])
        # print(self.bit_dont_change)

        """
        3.get one sample data filed(64*1) for each id
        """
        for k, v in self.initial_data.items():
            self.data_sample_64[k] = []
            for datax in range(8):
                for bitx in range(8):
                    self.data_sample_64[k].append(int(self.initial_data[k][datax][0][bitx]))
        # print(self.data_sample_64)
        # print(len(self.data_sample_64))

        """
        4.label UNUSED and CONST(still need to find msb of POSS in 'UNUSED')
        """
        for k, v in self.bit_dont_change.items():
            self.CONST[k] = []
            self.UNUSED[k] = []
            # print(len(v))
            # print(v)
            for dont_change_seg in range(len(v)):
                bit_start = v[dont_change_seg][1]
                bit_end = v[dont_change_seg][2]
                # print(bit_start)    # issues
                # print(bit_end)
                for bit_check in range(bit_start, bit_end + 1):
                    if self.data_sample_64[k][bit_check] == 0 and bit_check != bit_end:
                        pass
                    elif self.data_sample_64[k][bit_check] == 0 and bit_check == bit_end:
                        self.UNUSED[k].append(['UNUSED', bit_start, bit_end])
                    else:
                        self.CONST[k].append(['CONST', bit_start, bit_end])
                        break
        self.POSS = self.bit_change
        # print(self.data_sample_64['0x10d'])
        # print(self.UNUSED)
        # print(self.CONST)
        # print(self.POSS)
        # print(self.bit_change)
        # print(self.bit_dont_change)
        """
        5.find POSS's MSB in UNUSED
        """
        for k, v in self.UNUSED.items():
            # print(k)
            for unused_seg in range((len(v)-1), 0, -1):
                if v[unused_seg][2] - v[unused_seg][1] < self.unused_len_00:
                    # print(self.POSS[k])
                    # print(v)
                    for poss_seg in range(len(self.POSS[k])):
                        # print(self.POSS[k][poss_seg])
                        # print(print(v[unused_seg]))
                        if self.POSS[k][poss_seg][1] == v[unused_seg][2] + 1 and self.POSS[k][poss_seg][2] - \
                                self.POSS[k][poss_seg][1] > self.append_len_01:
                            self.POSS[k][poss_seg][1] = v[unused_seg][2]
                            del v[unused_seg]
                            break
        # print(self.POSS)
        # print(self.UNUSED)

    def boundary_by_flip_rate(self):
        # print(self.bit_flip)
        POSS_temp = {}
        for k, v in self.POSS.items():
            POSS_temp[k] = []
            for poss_seg in range(len(v)):
                prev_bitx = v[poss_seg][1]
                for bitx in range(v[poss_seg][1]+1, v[poss_seg][2]+1):
                    if self.bit_flip[k][bitx-1] - self.bit_flip[k][bitx] > self.flip_th_02:
                        POSS_temp[k].append(['POSS', prev_bitx, bitx-1])
                        prev_bitx = bitx
                    else:
                        pass
                POSS_temp[k].append(['POSS', prev_bitx, v[poss_seg][2]])
        # print(POSS_temp)
        self.POSS = POSS_temp
        # print(self.POSS)

    def select_MULTI(self):
        for k, v in self.initial_data.items():
            self.data_64[k] = []

            for payloadx in range(len(self.initial_data[k][0])):
                data_64_1_line = []
                for datax in range(8):
                    for bitx in range(8):
                        data_64_1_line.append(int(self.initial_data[k][datax][payloadx][bitx]))
                self.data_64[k].append(data_64_1_line)
        # print(self.data_64['0x121'][0])

        for k, v in self.POSS.items():
            seg_length = len(v)
            payload_length = len(self.data_64[k])
            self.characteristic_num[k] = [payload_length]*seg_length
            seg_times = -1
            for poss_seg in v:
                seg_times = seg_times + 1
                for payloadx in range(len(self.data_64[k])):
                    if len(v) == 0:
                        pass
                    else:
                        for payloadxx in range(payloadx+1,len(self.data_64[k])):
                            if self.data_64[k][payloadx][poss_seg[1]:poss_seg[2]+1] == self.data_64[k][payloadxx][poss_seg[1]:poss_seg[2]+1]:
                                self.characteristic_num[k][seg_times] = self.characteristic_num[k][seg_times] - 1
                                break
                            else:
                                pass

        self.MULTI = deepcopy(self.POSS)    # deepcopy!
        # print(self.MULTI)
        # print(self.characteristic_num)
        for k, v in self.POSS.items():
            seg_times = -1
            for poss_seg in v:
                seg_times = seg_times + 1
                if self.characteristic_num[k][seg_times] < self.multi_th_03:
                    self.MULTI[k].remove(poss_seg)
        # print(self.characteristic_num)
        # print(self.MULTI)


    def select_Counter_PHY(self):
        self.Counter = deepcopy(self.MULTI)
        # print(self.Counter)
        multi_temp = deepcopy(self.MULTI)
        for k, v in multi_temp.items():
            self.PHY[k] = []
            for multi_seg in v:
                if multi_seg[1] == multi_seg[2]:
                    self.PHY[k].append(multi_seg)
                    self.Counter[k].remove(multi_seg)
                else:
                    for bitx in range(multi_seg[1], multi_seg[2]):
                        if 0.9 * self.bit_flip[k][bitx+1] < self.bit_flip[k][bitx]*2 < 1.1 * self.bit_flip[k][bitx+1]:
                            pass
                        else:
                            self.PHY[k].append(multi_seg)
                            self.Counter[k].remove(multi_seg)
                            break
        # print(self.MULTI)
        # print(self.Counter)
        # print(self.PHY)
        for k, v in self.MULTI.items():
            for poss_seg in v:
                poss_seg[0] = 'MULTI'
        for k, v in self.PHY.items():
            for multi_seg in v:
                multi_seg[0] = 'PHY'
        for k, v in self.Counter.items():
            for multi_seg in v:
                multi_seg[0] = 'Counter'

    def select_CRC(self):
        """
        actually no crc found for present data
        :return:
        """
        self.phase_1()
        phy_temp = deepcopy(self.PHY)
        for k, v in phy_temp.items():
            self.CRC[k] = []
            for seg in v:
                ixs, ixe = seg[1], seg[2]
                a = self.bit_flip[k][ixs:ixe+1]
                mv_crc = np.mean(self.bit_flip[k][ixs:ixe+1])
                std_crc = np.std(self.bit_flip[k][ixs:ixe+1])
                if self.bit_mag[k][ixs:ixe+1] == [0] * len(self.bit_mag[k][ixs:ixe+1]) and (0.5 - std_crc) <= mv_crc <= (0.5 + std_crc):
                    self.CRC[k].append(seg)
                    self.PHY[k].remove(seg)
                else:
                    pass
        for k, v in self.CRC.items():
            for crc_seg in v:
                crc_seg[0] = 'CRC'
        # print(self.PHY)

    def change_result_form(self):

        # print(self.CONST)
        # print(self.PHY)
        # print(self.Counter)
        # print(self.CRC)
        temp_unused = deepcopy(self.UNUSED)
        for k, v in temp_unused.items():
            temp_dic = []
            if not v:
                del self.UNUSED[k]
            else:
                for seg in v:
                    temp_dic.append(seg[1])
                    temp_dic.append(seg[2])
                self.UNUSED[k] = temp_dic
        # print(self.UNUSED)

        temp_const = deepcopy(self.CONST)
        for k, v in temp_const.items():
            temp_dic = []
            if not v:
                del self.CONST[k]
            else:
                for seg in v:
                    temp_dic.append(seg[1])
                    temp_dic.append(seg[2])
                self.CONST[k] = temp_dic

        temp_phy = deepcopy(self.PHY)
        for k, v in temp_phy.items():
            temp_dic = []
            if not v:
                del self.PHY[k]
            else:
                for seg in v:
                    temp_dic.append(seg[1])
                    temp_dic.append(seg[2])
                self.PHY[k] = temp_dic

        temp_cnt = deepcopy(self.Counter)
        for k, v in temp_cnt.items():
            temp_dic = []
            if not v:
                del self.Counter[k]
            else:
                for seg in v:
                    temp_dic.append(seg[1])
                    temp_dic.append(seg[2])
                self.Counter[k] = temp_dic

        temp_crc = deepcopy(self.CRC)
        for k, v in temp_crc.items():
            temp_dic = []
            if not v:
                del self.CRC[k]
            else:
                for seg in v:
                    temp_dic.append(seg[1])
                    temp_dic.append(seg[2])
                self.CRC[k] = temp_dic

    def file_phase0(self):

        """
        remove label name
        """
        with open('data/UNUSED.csv', 'w', newline="") as csv_file:
            unused_writer = csv.writer(csv_file)
            for k, v in self.UNUSED.items():
                unused_writer.writerow([k, v])

        with open('data/CONST.csv', 'w', newline="") as csv_file:
            const_writer = csv.writer(csv_file)
            for k, v in self.CONST.items():
                const_writer.writerow([k, v])

        with open('data/PHY.csv', 'w', newline="") as csv_file:
            phy_writer = csv.writer(csv_file)
            for k, v in self.PHY.items():
                phy_writer.writerow([k, v])

        with open('data/Counter.csv', 'w', newline="") as csv_file:
            cnt_writer = csv.writer(csv_file)
            for k, v in self.Counter.items():
                cnt_writer.writerow([k, v])

        with open('data/CRC.csv', 'w', newline="") as csv_file:
            crc_writer = csv.writer(csv_file)
            for k, v in self.CRC.items():
                crc_writer.writerow([k, v])

    def generate_reference(self):
        # generate reference data list
        for k, v in self.reference_data.items():
            self.ref_data_64[k] = []

            for payloadx in range(len(self.reference_data[k][0])):
                data_64_1_line = []
                for datax in range(8):
                    for bitx in range(8):
                        data_64_1_line.append(int(self.reference_data[k][datax][payloadx][bitx]))
                self.ref_data_64[k].append(data_64_1_line)
        # compute bit flip rate
        for k, v in self.ref_data_64.items():
            flip_times = 64 * [0]
            self.ref_flip_rate[k] = []
            for bitx in range(0, 64):
                for payloadx in range (0,len(v)-1):
                    if v[payloadx+1][bitx] != v[payloadx][bitx]:
                        flip_times[bitx] = flip_times[bitx] + 1
                self.ref_flip_rate[k].append(flip_times[bitx]/len(v))
        # compute average bit flip rate
        average_flip_rate = {}
        for k, v in self.ref_flip_rate.items():
            average_flip_rate[k] = 0
            for bitx in v:
                average_flip_rate[k] = average_flip_rate[k] + bitx
            average_flip_rate[k] = average_flip_rate[k]/64
        # print(average_flip_rate)
        # delete id with high average bit flip rate(more than tp2,0)
        temp_average = deepcopy(average_flip_rate)
        for k, v in temp_average.items():
            if v > self.average_flip_th_20:
                average_flip_rate.pop(k)
        # print(average_flip_rate)
        # generate the reference data:1.make a list of chosen id mapping to all frames(64*1);2. delete repetitive frames
        # print(self.data_64)
        for k, v in average_flip_rate.items():
            self.reference[k] = []
            if v == 0:
                self.reference[k].append(self.data_64[k][0])
            else:
                for data in self.data_64[k]:
                    self.reference[k].append(data)
        # print(self.reference)
        for k, v in self.reference.items():
            if len(v) == 1:
                pass
            else:
                for seg_num in range(len(v)-1, -1, -1):
                    for count_num in range(seg_num-1, -1, -1):
                        if v[seg_num] == v[count_num]:
                            v.remove(v[seg_num])
                            break

    def filter_unchanged_id(self):
        average_flip_rate = {}
        for k, v in self.bit_flip.items():
            average_flip_rate[k] = 0
            for bitx in v:
                average_flip_rate[k] = average_flip_rate[k] + bitx
            average_flip_rate[k] = average_flip_rate[k] / 64

        for k, v in average_flip_rate.items():
            if v == 0:
                pass
            else:
                self.event_data_64[k] = self.data_64[k]

    def filter_reference(self):
        temp_event_data_64 = deepcopy(self.event_data_64)
        for k_r, v_r in self.reference.items():
            for k_e, v_e in temp_event_data_64.items():
                if k_e != k_r:
                    pass
                else:
                    for seg_r in v_r:
                        for seg_e in v_e:
                            if seg_r != seg_e:
                                pass
                            else:
                                self.event_data_64[k_e].remove(seg_e)
        temp_event_data_64 = deepcopy(self.event_data_64)
        for k, v in temp_event_data_64.items():
            if not v:
                self.event_data_64.pop(k)
        # print(len(self.event_data_64))


if __name__ == "__main__":
    analysis = LibreCAN(2, 3, 0.01, 2, 0.07, 0.03, 0.7)

    try:
        """
        phase0 label
        """
        print('请输入预计收集数据时间长度:\r\n')
        number_frame = int(input())
        analysis.initial_frame(number_frame)
        analysis.pre_processing()
        analysis.write_data()
        analysis.phase_1()

        analysis.pre_label()
        analysis.boundary_by_flip_rate()
        analysis.select_MULTI()
        analysis.select_Counter_PHY()
        analysis.select_CRC()
        analysis.change_result_form()
        analysis.file_phase0()
        # analysis.picture_start()

        """
        phase1 xcorr liner regression figure out power-related id
        """
        """
        phase2 figure out body-related id 
        """
        # analysis.generate_reference()    # need data collected when no body and power related event happen
        # analysis.filter_unchanged_id()
        # analysis.filter_reference()

        # analysis.test()

    finally:
        analysis.stop()
