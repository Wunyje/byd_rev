import csv
import re
import os


class DataFieldDetection:

    def __init__(self):
        super(DataFieldDetection, self).__init__()
        self.data_feature = []
        self.data_dict = {}
        self.data_detect = {}
        self.data_exception = {}

    def receive_data(self, frequency=2000):
        time_slice = 1
        if self.clear_buffer() is not True:
            ex = Exception("clear failure")
            raise ex

        else:
            print("begin")
            with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'origin_data.csv', 'w', newline="") as csv_file:
                data_writer = csv.writer(csv_file)
                while time_slice <= frequency:
                    data = self.receive()
                    p_list = []
                    for i in range(8):
                        p_list.append("0x" + "0" * (2 - len(hex(data.Data[i]).replace("0x", "")))
                                      + hex(data.Data[i]).replace("0x", ""))
                    print(p_list)
                    data_writer.writerow([hex(data.ID), p_list])
                    time_slice += 1
            print("end")

    @staticmethod
    def read_data(data_record, filename):
        ecu_id = []
        with open(filename, 'r', newline="") as file:
            readers = csv.reader(file)
            for read in readers:
                # print(read)
                if read[0] not in ecu_id:
                    ecu_id.append(read[0])
            print(ecu_id)
        for i in range(len(ecu_id)):
            with open(filename, 'r', newline="") as file:
                readers = csv.reader(file)
                data_field = []
                for read in readers:
                    # print(read[0])
                    if read[0] == ecu_id[i]:
                        new_list = eval(read[1])
                        new_list = list(map(eval, new_list))
                        data_field.append(new_list)
                # print(data_field)
                for j in range(len(data_field)):
                    temp_str = ''.join(["{0:b}".format(each).zfill(8) for each in data_field[j]])
                    data_field[j] = temp_str
                data_record[ecu_id[i]] = data_field

    @staticmethod
    def get_constant(index_list, value, ecu_id):
        common_key_data = []
        for index_record in index_list:
            data_key_valid = []
            flag_left = False
            flag_change = False
            while True:
                data_key = []
                for data_item in value:
                    if data_item[index_record[0]:index_record[1]] not in data_key:
                        data_key.append(data_item[index_record[0]:index_record[1]])
                if len(data_key) == 1:
                    flag_left = True
                    data_key_valid = data_key
                    if index_record[0] > 0:
                        flag_change = True
                        index_record[0] -= 1
                    else:
                        break
                else:
                    if flag_change:
                        index_record[0] += 1
                    break

            flag_right = False
            flag_change = False
            while True:
                data_key = []
                for data_item in value:
                    if data_item[index_record[0]:index_record[1]] not in data_key:
                        data_key.append(data_item[index_record[0]:index_record[1]])
                if len(data_key) == 1:
                    flag_right = True
                    data_key_valid = data_key
                    if index_record[1] < len(data_item):
                        flag_change = True
                        index_record[1] += 1
                    else:
                        break
                else:
                    if flag_change:
                        index_record[1] -= 1
                    break
            if flag_left or flag_right:
                index_range = [index_record[0], index_record[1]]

                flag_exist = False
                for common_data_item in common_key_data:
                    if common_data_item['index'] == index_range:
                        flag_exist = True
                        break

                if not flag_exist:
                    common = {'ecu_id': ecu_id, 'index': [index_record[0], index_record[1]], 'data': data_key_valid,
                              'type': 'constant'}
                    common_key_data.append(common)

        return common_key_data

    @staticmethod
    def get_index(data_field, index_number):
        index_temp = [index_item[0:2] for index_item in index_number]
        new_index = []
        data_index = []
        for data_item in data_field:
            data_index.append(data_item['index'])
        for index_item in index_temp:
            if index_item not in data_index:
                new_index.append(index_item)
        index_limit = []
        i = 0
        while i < len(new_index):
            low = new_index[i][0]
            while i < len(new_index) - 1 and new_index[i][1] == new_index[i + 1][0]:
                i += 1
            high = new_index[i][1]
            index_limit.append([low, high])
            i += 1

        i = 0
        for new_index_item in new_index:
            while i < len(index_limit):
                if new_index_item[0] >= index_limit[i][0] and new_index_item[1] <= index_limit[i][1]:
                    new_index_item.extend(index_limit[i])
                    break
                else:
                    i += 1

        return new_index

    @staticmethod
    def get_multiple(data=list, index_list=list, ecu_id=str):
        mul_data = []

        for index_record in index_list:
            data_key_valid = []

            flag_left = False
            flag_change = False
            while True:
                data_key = []

                for data_item in data:
                    if data_item[index_record[0]:index_record[1]] not in data_key:
                        data_key.append(data_item[index_record[0]:index_record[1]])

                if len(data_key) < 2 ** (index_record[1] - index_record[0] + 1) * 1.0 / 3:
                    flag_left = True
                    data_key_valid = data_key
                    if index_record[0] > index_record[2]:
                        flag_change = True
                        index_record[0] -= 1
                    else:
                        break
                else:
                    if flag_change:
                        index_record[0] += 1
                    break

            flag_right = False
            flag_change = False
            while True:
                data_key = []

                for data_item in data:
                    if data_item[index_record[0]:index_record[1]] not in data_key:
                        data_key.append(data_item[index_record[0]:index_record[1]])

                if len(data_key) < 2 ** (index_record[1] - index_record[0] + 1) * 1.0 / 3:
                    flag_right = True
                    data_key_valid = data_key
                    if index_record[1] < index_record[3]:
                        flag_change = True
                        index_record[1] += 1
                    else:
                        break
                else:
                    if flag_change:
                        index_record[1] -= 1
                    break

            if flag_left or flag_right:
                index_range = [index_record[0], index_record[1]]

                flag_exist = False
                for common_data_item in mul_data:
                    if common_data_item['index'] == index_range:
                        flag_exist = True
                        break

                if not flag_exist:
                    common = {'ecu_id': ecu_id, 'index': [index_record[0], index_record[1]], 'data': data_key_valid,
                              'type': 'multi_value'}
                    mul_data.append(common)

        return mul_data

    @staticmethod
    def get_loop(data_field, index_list, tolerate=0, ecu_id=str):
        loop_data = []
        for index_record in index_list:
            data_key_valid = {}

            flag_left = False
            flag_change = False
            while True:
                data_key = {}

                for data_item in data_field:
                    if data_item[index_record[0]:index_record[1]] not in data_key:
                        data_key[data_item[index_record[0]:index_record[1]]] = 1
                    else:
                        data_key[data_item[index_record[0]:index_record[1]]] += 1

                if len(data_key) == 2 ** (index_record[1] - index_record[0]) and max(data_key.values()) - min(
                        data_key.values()) < tolerate:
                    flag_left = True
                    data_key_valid = data_key
                    if index_record[0] > index_record[2]:
                        flag_change = True
                        index_record[0] -= 1
                    else:
                        break
                else:
                    if flag_change:
                        index_record[0] += 1
                    break

            flag_right = False
            flag_change = False
            while True:
                data_key = {}

                for data_item in data_field:
                    if data_item[index_record[0]:index_record[1]] not in data_key:
                        data_key[data_item[index_record[0]:index_record[1]]] = 1
                    else:
                        data_key[data_item[index_record[0]:index_record[1]]] += 1

                if len(data_key) == 2 ** (index_record[1] - index_record[0]) and max(data_key.values()) - min(
                        data_key.values()) < tolerate:
                    flag_right = True
                    data_key_valid = data_key
                    if index_record[1] < index_record[3]:
                        flag_change = True
                        index_record[1] += 1
                    else:
                        break
                else:
                    if flag_change:
                        index_record[1] -= 1
                    break

            if flag_left or flag_right:
                index_range = [index_record[0], index_record[1]]

                flag_exist = False
                for common_data_item in loop_data:
                    if common_data_item['index'] == index_range:
                        flag_exist = True
                        break

                if not flag_exist:
                    common = {'ecu_id': ecu_id, 'index': [index_record[0], index_record[1]], 'data': data_key_valid,
                              'type': 'loop'}
                    loop_data.append(common)

        return loop_data

    @staticmethod
    def get_irregular(index_list, ecu_id=str):
        irregular_data = []
        for index_record in index_list:
            irregular_data.append(
                {'ecu_id': ecu_id, 'index': [index_record[0], index_record[1]], 'type': 'irregular', 'data': ''})
        return irregular_data

    @staticmethod
    def compare_byte_score(index=list, data_correct=str, data_exception=str):
        if data_exception[index[0]: index[1]] == data_correct:
            return 0

        score = 0
        for i in range(index[1] - index[0]):
            if data_correct[i] != data_exception[index[0] + i]:
                score += 1

        return score

    @staticmethod
    def compare_byte(index=list, data_correct=str, data_exception=str, exception_byte=list):
        for i in range(index[1] - index[0]):
            if data_correct[i] != data_exception[index[0] + i]:
                byte_index = (index[0] + i) // 8
                if byte_index not in exception_byte:
                    exception_byte.append(byte_index)
        return exception_byte

    def get_feature(self):
        split_len = 4
        for key, value_list in self.data_dict.items():
            key_data_feature = []
            index = [[i, i + split_len] for i in range(0, 64, split_len)]
            common_data = self.get_constant(index, value_list, key)
            key_data_feature.extend(common_data)
            index = self.get_index(common_data, index)
            loop_data = self.get_loop(value_list, index, 2000, key)
            key_data_feature.extend(loop_data)
            index = self.get_index(loop_data, index)
            mul_data = self.get_multiple(value_list, index, key)
            key_data_feature.extend(mul_data)
            index = self.get_index(mul_data, index)
            irregular_data = self.get_irregular(index, key)
            key_data_feature.extend(irregular_data)
            self.data_feature.extend(key_data_feature)

    def write_feature(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'feature_data.csv', 'w', encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file)
            # csv_writer.writerow(['ecu_id', 'index', 'type', 'data'])
            for record in self.data_feature:
                csv_writer.writerow([record['ecu_id'], record['index'], record['type'], record['data']])

    def read_feature_data(self):
        self.data_feature = []
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'feature_data.csv', 'r', newline='') as file:
            for file_record in file:
                temp = file_record.strip().split(',')
                file_record = [temp[0]]
                list_sub = re.sub('\D', ' ', temp[1] + temp[2])
                list_sub = list_sub.split()
                file_record.append([int(list_sub[0]), int(list_sub[1])])
                file_record.append(temp[3])
                data_record = []
                for i in range(4, len(temp)):
                    list_sub = re.sub('\D', ' ', temp[i])
                    list_sub = list_sub.split()
                    data_record.extend(list_sub)
                file_record.append(data_record)
                self.data_feature.append({'ecu_id': file_record[0], 'index': file_record[1], 'type': file_record[2],
                                          'data': file_record[3]})

    def detect(self, detect_ecu_id, detect_data):
        i = 0

        while self.data_feature[i]['ecu_id'] != detect_ecu_id:
            i += 1

        exception_byte = []

        while i < len(self.data_feature) and self.data_feature[i]['ecu_id'] == detect_ecu_id:
            index = self.data_feature[i]['index']
            data = self.data_feature[i]['data']

            if self.data_feature[i]['type'] == 'constant':
                if data[0] != detect_data[index[0]: index[1]]:
                    self.compare_byte(index, data[0], detect_data, exception_byte)

            elif self.data_feature[i]['type'] == 'multi_value':
                value_comp_id = None
                score = 64
                for multi_value in data:
                    cur_score = self.compare_byte_score(index, multi_value, detect_data)
                    if cur_score < score:
                        score = cur_score
                        value_comp_id = multi_value
                if score > 0:
                    self.compare_byte(index, value_comp_id, detect_data, exception_byte)

            i += 1
        return exception_byte

    def write_exception(self):
        with open(os.path.dirname(os.path.realpath(__file__)) + os.sep +'exception_data.csv', 'w', encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file)
            # csv_writer.writerow(['ecu_id', 'index', 'type', 'data'])
            print(self.data_exception)
            for ecu_id, exp in self.data_exception.items():
                csv_writer.writerow([ecu_id, exp])

    def read_origin_data(self):
        self.read_data(self.data_dict, os.path.dirname(os.path.realpath(__file__)) + os.sep +'origin_data.csv')

    def read_detect_data(self):
        self.read_data(self.data_detect, os.path.dirname(os.path.realpath(__file__)) + os.sep +'detect_data.csv')

    def get_exception(self):
        for ecu_id, data in self.data_detect.items():
            for detect_data in data:
                print(ecu_id, ' ', detect_data)
                exp = data_detection.detect(ecu_id, detect_data)
                self.data_exception[ecu_id] = exp


if __name__ == "__main__":

    data_detection = DataFieldDetection()

    try:
        #get_feature
        data_detection.read_origin_data()
        data_detection.get_feature()
        data_detection.write_feature()

        #detect
        data_detection.read_feature_data()
        data_detection.read_detect_data()
        data_detection.get_exception()
        data_detection.write_exception()

    finally:
        pass
