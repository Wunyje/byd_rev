# -*- coding: utf-8 -*-
from ctypes import *
from frame import Frame
import os


class VCI_INIT_CONFIG(Structure):
    _fields_ = [("AccCode", c_uint),      # 过滤验收滤波器      DeviceInd 设备索引 插入的第一个设备就是0，第二个设备为1
                ("AccMask", c_uint),       # 过滤屏蔽寄存器          CANIndex 通道索引  CAN通道号 CAN1为0，CAN2为1
                ("Reserved", c_uint),       # 保留
                ("Filter", c_ubyte),        # 滤波模式 0和1.接收所有类型 2.只收标准帧 3.只收拓展帧
                ("Timing0", c_ubyte),    # 定时器0
                ("Timing1", c_ubyte),   # 定时器1
                ("Mode", c_ubyte)     # 三种工作模式  0.正常模式  1.侦听模式 2.环回模式
                ]


class VCI_CAN_OBJ(Structure):
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),     # 记录时间
                ("TimeFlag", c_ubyte),    # 是否有时间标识
                ("SendType", c_ubyte),  # 发送帧的类型 =0为正常发送（发送失败会自动重发）=1为单次发送（发送失败不会自动重发）
                ("RemoteFlag", c_ubyte),   # 是否是远程帧 =0 为数据帧  =1 为远程帧
                ("ExternFlag", c_ubyte),   # 是否是拓展帧 =0 为标准帧  =1 为拓展帧
                ("DataLen", c_ubyte),
                ("Data", c_ubyte * 8),
                ("Reserved", c_ubyte * 3)     # 系统保留
                ]


class MyDevice(object):
    def __init__(self, device_type=c_long(4), device_index=c_ulong(0), can_index=c_ulong(0), reserved=c_ulong(0)):
        self.canDLL = cdll.LoadLibrary(os.path.dirname(__file__)+"/libcontrolcan.so")
        self.device_type = device_type
        self.device_index = device_index
        self.can_index = can_index
        self.reserved = reserved
        self.filter_mode = 0
        self.run_flag = False
        self.status_flag = 1

    def start(self, baud_rate=500):
        open_device = self.canDLL.VCI_OpenDevice(self.device_type, self.device_index, self.reserved)
        if open_device == self.status_flag:
            print("open device successfully %d" % self.can_index.value)
        if open_device != self.status_flag:
            print("open device unsuccessfully %d" % self.can_index.value)

        if baud_rate == 500:
            baud_value = 0x00
        elif baud_rate == 250:
            baud_value = 0x01
        elif baud_rate == 125:
            baud_value = 0x03
        else:
            raise Exception("input the baud error")
# 初始0通道
        vci_init_config = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, self.reserved.value,
                                          self.filter_mode, baud_value, 0x1C, 0)  # 波特率500k，正常模式
        init_can = self.canDLL.VCI_InitCAN(self.device_type, self.device_index, self.can_index, byref(vci_init_config))
        if init_can == self.status_flag:
            print("initialize device successfully %d,baud is %d." % (self.can_index.value, baud_rate))
        if init_can != self.status_flag:
            print("initialize device  unsuccessfully %d" % self.can_index.value)

        start_can = self.canDLL.VCI_StartCAN(self.device_type, self.device_index, self.can_index)
        if start_can == self.status_flag:
            print("device start success %d" % self.can_index.value)
        if start_can != self.status_flag:
            print("device start failure %d" % self.can_index.value)

        if open_device == self.status_flag and init_can == self.status_flag and start_can == self.status_flag:
            self.run_flag = True

    def stop(self):
        if False is self.run_flag:
            print("close device %d" % self.can_index.value)

        else:
            close_device = self.canDLL. VCI_CloseDevice(self.device_type, self.device_index)

            if close_device == self.status_flag:
                self.run_flag = False
                print("close device successfully %d" % self.can_index.value)
            else:
                print("close device unsuccessfully %d" % self.can_index.value)

    def transmit(self, tx_frame=None):
        vci_obj = VCI_CAN_OBJ()
        vci_obj.ID = tx_frame.id
        for i in range(len(tx_frame.data)):
            vci_obj.Data[i] = tx_frame.data[i]
        vci_obj.DataLen = tx_frame.data_len
        # vci_obj.TimeStamp = 0
        vci_obj.ExternFlag = 0
        vci_obj.RemoteFlag = 0
        vci_obj.SendType = 1
        while True:
            value = self.canDLL.VCI_Transmit(self.device_type, self.device_index, self.can_index, byref(vci_obj), c_long(1))
            if value == self.status_flag:
                break

    def receive(self):
        while True:
            vci_can = VCI_CAN_OBJ()
            value = self.canDLL.VCI_Receive(self.device_type, self.device_index, self.can_index, byref(vci_can), 1, 0)
            if value == self.status_flag:
                break
        return vci_can

    def clear_buffer(self):
        value = self.canDLL.VCI_StartCAN(self.device_type, self.device_index, self.can_index)
        if value == self.status_flag:
            return True
        else:
            return False

    def reset_can(self):
        value = self.canDLL.VCI_ResetCAN(self.device_type, self.device_index, self.can_index)
        if value == self.status_flag:
            return True
        else:
            return False


if __name__ == "__main__":
    my_device = MyDevice()
    my_device.start()
    temporary = 0
    try:

        while True:
            rx_frame = my_device.receive()
            print(hex(rx_frame.ID), end="  ")
            time = rx_frame.TimeStamp
            gap = time - temporary
            temporary = time
            print("TimeStamp is %d" % gap)

    except Exception as result:
        print("异常错误:%s" % result)

    finally:
        my_device.stop()

