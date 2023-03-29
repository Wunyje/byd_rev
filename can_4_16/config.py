import os

ROOT_DIR = os.path.dirname(os.path.realpath(__file__)) #  The path of the current file

CODE_DIR = ROOT_DIR
ATTACK_DIR = ROOT_DIR+ os.sep + "1_attack"                  #  The root path of All the binary file
REVERSE_DIR = ROOT_DIR+ os.sep + "2_reverse"                #  The root path of All the idb file
DIAGNOSIS_DIR = ROOT_DIR+ os.sep + "3_diagnosis"            #  The root path of  the feature file