# !/usr/bin/python3.6
# -*- coding: utf-8 -*-

import time
import re
import socket
from adc import Pcf8591

class MasServ(object):
    def __init__(self):
        # 创建本地端口
        self.LocalSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 得到本机的ip地址
        self.host_name = socket.gethostname()
        print ("hostname:%s" % self.host_name)
        self.host_ip = socket.gethostbyname(self.host_name)
        print ("IP address: %s" % self.host_ip)
        self.I2C = None

        self.LocalSocket.bind((self.host_ip, 1071))
        # 最大连接数
        self.LocalSocket.listen(5)

    def compute_electric_current(self, *args):

        electric_current_message = args[0].encode("utf-8")
        return electric_current_message

    def process(self):
        # 开始传输数据
        print ("[Server] Data Start...")
        while True:
            # 等待建立连接
            print ("[Server] Wait for connection...")
            ClientSocket, Address = self.LocalSocket.accept()
            print ("[Server] Get connection Sucessfully!")
            # 输出连接信息
            print (ClientSocket, " ", Address, "\n")
            self.I2C = Pcf8591(0x48)
            while True:
                # 从用户端得到信息
                print ("[Server] Wait for apply from Client...")
                shift_Message = ClientSocket.recv(1024).decode("utf-8")
                # 输出反馈信息
                print ("[Server] Get message shift:", shift_Message)
                # 终止数据传输

                # 检测终止指令
                if re.match("/end", shift_Message, re.I):
                    print ("[Server] End instruction checked!")
                    break
                else:
                    data = self.I2C.Read(0)
                    print (data)
                    electric_current_Message = self.compute_electric_current(str(data))
                    print ("[Server] electric_current should be:", electric_current_Message.decode('utf-8'))
                    ClientSocket.sendall(electric_current_Message)
                    time.sleep(0.01)
            ClientSocket.close()
            break

    def __del__(self):
        self.LocalSocket.close()


if __name__ == "__main__":
    server = MasServ()
    server.process()
