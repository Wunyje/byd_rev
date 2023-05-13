import pandas as pd
import os

# read the two CSV files into dataframes
cwd = os.getcwd()
id_a = pd.read_csv(os.path.join(cwd,'CANlog_adb_reboot_bootloader.csv'), usecols=['帧ID'], encoding='GB2312')
id_b = pd.read_csv(os.path.join(cwd,'CANlog_adb_reboot.csv'), usecols=['帧ID'], encoding='GB2312')

# count the unique values in each dataframe
sorts_a = id_a['帧ID'].nunique()
sorts_b = id_b['帧ID'].nunique()

# find the unique values in each dataframe
unique_to_a = id_a[~id_a['帧ID'].isin(id_b['帧ID'])]
unique_to_b = id_b[~id_b['帧ID'].isin(id_a['帧ID'])]

# print the results
print(f"Number of unique values in id_a: {sorts_a}")
print(f"Number of unique values in id_b: {sorts_b}")
print("Values unique to id_a:")
print(unique_to_a)
print("Values unique to id_b:")
print(unique_to_b)
