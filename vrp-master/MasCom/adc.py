#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : adc.py
# Author            : orglanss <orglanss@gmail.com>
# Date              : 16.10.2017
# Last Modified Date: 20.10.2017
# Last Modified By  : orglanss <orglanss@gmail.com>

import  as wpi
import time

'''pcf8591 adc 读Ain值 或输出Aout'''
class Pcf8591:
    def __init__(self, address = 0x48):
        # address:pcf8591在树莓派上的地址
        # 可用i2cdetect -y 0/1 查看
        self.d = wpi.wiringPiSetup()
        self.fd = wpi.wiringPiI2CSetup(address)
        # 4个Ain的地址
        self.Ain = [0x40, 0x41, 0x42, 0x43]
        self.Aout = 0x40
    '''读取Ain0~3中任意通道上的电压值'''
    def Read(self, channel = 0):
        # 读取上一次AD转换的遗留数据，并丢弃 
        wpi.wiringPiI2CReadReg8(self.fd, self.Ain[channel])

        return wpi.wiringPiI2CReadReg8(self.fd, self.Ain[channel]) / 255.0 * 5

    '''Aout输出0~5v电压'''
    def Write(self, data):
        # pcf8591 DA输出最大值为5v
        if (data > 5):
            data = 5 
        data = int(data / 5.0 * 255)
        return wpi.wiringPiI2CWriteReg8(self.fd, self.Aout, data)


