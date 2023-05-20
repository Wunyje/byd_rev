import pandas as pd
import re
import os
import glob

def can_data_convert_bin(can_data_path):
    # Extract hexa-bytes from data column in df and output to binary csv_file
    files_filter = glob.glob(can_data_path + os.sep + '*.csv')
    csv_file = ''
    for csv_file in files_filter:
        df = pd.read_csv(csv_file, encoding='GB2312')
        df = df.iloc[:, 1:]
        df.columns = columns
        bin_file_path = os.path.join(can_data_path, csv_file.split('os.sep')[-1].split('.')[0]+'.bin')
        with open(bin_file_path, "wb") as bin_file:
            for data in df["data"]:
                hex_bytes = re.findall(r"[0-9a-fA-F]{2}", data)
                bytes_array = bytearray.fromhex("".join(hex_bytes))
                bin_file.write(bytes_array)

def can_id_compare(df1, df2):
    # Count the unique values in each dataframe
    sorts_a = df1['frame-ID'].nunique()
    sorts_b = df2['frame-ID'].nunique()

    # Find the unique values in each dataframe
    unique_to_a = df1[~df1['frame-ID'].isin(df2['frame-ID'])]
    unique_to_b = df2[~df2['frame-ID'].isin(df1['frame-ID'])]

    # Print the results
    print(f"Number of unique values in df1: {sorts_a}")
    print(f"Number of unique values in df2: {sorts_b}")
    print("Values unique to df1:")
    print(unique_to_a['frame-ID'])
    print("Values unique to df2:")
    print(unique_to_b['frame-ID'])

cwd = os.getcwd()
can_data_path = os.path.join(cwd, 'canlog_ana')
# Read CAN csv files as pd.dataframe
df1 = pd.read_csv(os.path.join(can_data_path, 'CANlog_adb_reboot_bootloader.csv'), encoding='GB2312')
df2 = pd.read_csv(os.path.join(can_data_path, 'CANlog_adb_reboot.csv'), encoding='GB2312')

# Drop first column and rename rest of the columns
df1 = df1.iloc[:, 1:]
df2 = df2.iloc[:, 1:]
columns = ["sys-time", "hardware-time", "source-channel", "frame-ID", "frame-type", "frame-format", "CAN-type", "direction", "length", "data"]
df1.columns = columns
df2.columns = columns

can_data_convert_bin(can_data_path)
can_id_compare(df1, df2)
