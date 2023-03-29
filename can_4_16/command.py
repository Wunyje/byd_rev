import os
import config

def guide_type():
    print("请选择操作的类型:\r\n1: attack \r\n2: reverse \r\n3: diagnosis")
    while True:
        mode = int(input())
        if mode == 1 or 2 or 3:
            break
        else:
            print('Input type error, pls input again:\r\n')
    return mode


def attack_guide():
    print("请选择攻击类型:\r\n")
    print("1: featurecrack\r\n2: IDcrack\r\n"
          "3: dropattack\r\n4: replayattack\r\n"
          "5: scancrack\r\n6: fuzzyattack\r\n")
    while True:
        attack_type = input()
        if attack_type == '1':
            os.system('python '+ config.ATTACK_DIR +os.sep+'featurecrack/featurecrack.py')
            break
        elif attack_type == '2':
            os.system('python '+ config.ATTACK_DIR +os.sep+'featurecrack/crack.py')
            break
        elif attack_type == '3':
            os.system('python '+ config.ATTACK_DIR +os.sep+'dropattack/entropy.py')
            break
        elif attack_type == '4':
            os.system('python '+ config.ATTACK_DIR +os.sep+'replayattack/replayattack.py')
            break
        elif attack_type == '5':
            os.system('python '+ config.ATTACK_DIR +os.sep+'scan_attack/scancrack.py')
            break
        elif attack_type == '6':
            os.system('python '+ config.ATTACK_DIR +os.sep+'entropy/normal_fuzzy.py')
            break
        else: print('Input type error, pls input again:\r\n')


def reverse_guide():
    print("请选择逆向诊断类型:\r\n")
    print("1: entropy\r\n2: relative_entropy\r\n"
          "3: load_rate\r\n4: time_internal\r\n"
          "\r\n")
    while True:
        attack_type = input()
        if attack_type == '1':
            os.system('python '+ config.REVERSE_DIR +os.sep+'entropy/entropy.py')
            break
        elif attack_type == '2':
         #   os.system('python relative_entropy/information_collection.py')
            os.system('python '+ config.REVERSE_DIR +os.sep+'relative_entropy/relative_entropy.py')
            break
        elif attack_type == '3':
            os.system('python '+ config.REVERSE_DIR +os.sep+'load_rate/load_rate.py')
            break
        elif attack_type == '4':
            os.system('python '+ config.REVERSE_DIR +os.sep+'time_internal/time_internal.py')
            break
        else:
            print('Input type error, pls input again:\r\n')


def diagnosis_guide():
    print("请选择诊断类型:\r\n")
    print("1: ID\r\n2: function_parameter\r\n"
          "3: service_function\r\n4: data_field_detection\r\n"
          "\r\n")
    while True:
        attack_type = input()
        if attack_type == '1':
            os.system('python '+ config.DIAGNOSIS_DIR +os.sep+'diagnosis_test/ecu_id.py')
            break
        elif attack_type == '2':
            os.system('python '+ config.DIAGNOSIS_DIR +os.sep+'diagnosis_test/function_parameter_discover.py')
            break
        elif attack_type == '3':
            os.system('python '+ config.DIAGNOSIS_DIR +os.sep+'diagnosis_test/service_subfunction.py')
            break
        elif attack_type == '4':
            os.system('python '+ config.DIAGNOSIS_DIR +os.sep+'data_field_detection/data_field_abnormal_detection.py')
            break
        else:
            print('Input type error, pls input again:\r\n')


if __name__ == "__main__":
    mode_guide = guide_type()
    if mode_guide == 1:
        attack_guide()
    elif mode_guide == 3:
        diagnosis_guide()
    elif mode_guide == 2:
        reverse_guide()