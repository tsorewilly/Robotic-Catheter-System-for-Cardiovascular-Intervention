#!/usr/bin/python3.6
# -*- coding: utf-8 -*-


import re
import time
import socket
from MaxonMotor3 import MaxonMotor
#import threading


class SlavClient(object):
    def __init__(self):
        # 定义服务端对象
        self.vel = -400
        self.vel2 = 0
        self.position2 = 0
        self.position = 0
        self.pre_velocity = 0
        self.displacement = 0
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket类型的成员变量
        self.maxonmotor = MaxonMotor(1, "EPOS2", "MAXON SERIAL V2", "USB", "USB0", 1000000)
        # 得到本机的ip地址
        self.host_name = socket.gethostname()
        #print("hostname:%s" % self.host_name)
        self.host_ip = socket.gethostbyname(self.host_name)
        #print("IP address: %s" % self.host_ip)
        
        #self.fileObject = open("/home/pi/Desktop/vrp_slave2/current.txt","w")
        #self.current = threading.Thread(None, self.checkCurrent)

    def compute_shift(self, *args):
        shift_message = args[0].encode("utf-8")
        return shift_message
    
    def checkCurrent(self):
        while True:
            self.maxonmotor.get_current()
            self.fileObject.write(str(self.maxonmotor.current))
            self.fileObject.write("\n")

    def process(self):
        # 输入服务器的ip地址
        #HostIp = input("[Client] Input host ip address:")
        # 检测是否为本机
        #if re.match("/localip", HostIp, re.I):
         #   print("You choose to use local Ip!")
            #HostName = socket.gethostname()
            #HostIp = socket.gethostbyname(HostName)
        #elif re.match("/localhost", HostIp, re.I):
            #print("You choose local host!")
            #try:
                #HostIp = socket.gethostbyname('localhost')
                #print("get host ip successfully!")
            #except Exception as e:
                #print("Get host ip failed!Exception:", e)
                #print("[Client] Choose local ip instead!")
                #HostName = socket.gethostname()
                #HostIp = socket.gethostbyname(HostName)
            #print("[Client] This function is still under debug")

        # 输出确定的ip地址
        #print("[Client] host ip address:", HostIp)
        self.ServerSocket.connect(('172.20.141.42', 1071))
        # 开始数据传送
        shift_Message = self.compute_shift("5mm")
        self.ServerSocket.send(shift_Message)
        electric_volt_Message = self.ServerSocket.recv(2048)
        position = float(electric_volt_Message) * 1000
        self.position2 = int(position)
        print('position2 = ', self.position2)
        count = 0
        zero_count = 0
        #self.current.start()
        while True:
            # 数据传送测试
            # 等待反应0.2s
            
            time.sleep(0.01)
            shift_Message = self.compute_shift("5mm")
            self.ServerSocket.send(shift_Message)
            # 接收反馈4096b
            #print("[Client] Wait electric_current_Message...")
            electric_volt_Message = self.ServerSocket.recv(2048)
            position = float(electric_volt_Message) * 1000
            self.position = int(position)
            print('position = ', self.position)
            #print("[Client] electric_current_Message:", self.position)
            self.displacement = self.position - self.position2
            self.position2 = int(position)
            print('position2 = ', self.position2)
            err = 1
            """
            while self.displacement== 0:
                time.sleep(0.01)
                shift_Message = self.compute_shift("5mm")
                self.ServerSocket.send(shift_Message)
                electric_volt_Message = self.ServerSocket.recv(2048)
                position = float(electric_volt_Message) * 1000
                self.position = int(position)
                print('position = ', self.position)
                #print("[Client] electric_current_Message:", self.position)
                self.displacement = self.position - self.position2
                pre1 =  self.displacement 
                print('displacement = ', self.displacement)
                self.position2 = int(position)
                zero_count = zero_count + 1
                if 20 == zero_count:
                    zero_count = 0
                    break
          """
            if self.displacement > 0 or self.displacement == 0:
                self.vel = int(self.displacement * 0.04 / 0.06 * 4130 / 460)
            else:
                vel = abs(self.displacement) * 0.04 / 0.06 * 4130 / 460
                self.vel = -int(vel)
            # 0.04mm/mv,0.06采样间隔时间，460是皮带的额定转速 ，4130是电机的额定转速
            print('velocity = ', self.vel)
            if(self.vel > -400) and (self.vel < 400):
                print('vel = ', self.vel)
                self.maxonmotor.rm_move(2*self.vel)
                #time.sleep(0.01)
                """
                if abs(self.vel-self.vel2) > 10:
                    self.maxonmotor.rm_move(self.vel)
                else:
                    self.maxonmotor.rm_move(0)
                self.vel2 = self.vel
                
                for i in range(4):
                    self.maxonmotor.rm_move(250)
                    time.sleep(1.2)
                    self.maxonmotor.rm_move(-250)
                    #self.maxonmotor.rm_move(250)
                    time.sleep(1.2)
                self.maxonmotor.rm_disable()
                self.maxonmotor.close_device()
                self.ServerSocket.close()
                self.current.stop()
                """
            else:
                if self.vel > 400:
                    self.vel = 400
                if self.vel < -400:
                    self.vel = -400
                self.maxonmotor.rm_move(2*self.vel)
                #time.sleep(0.02)
                """
                if abs(self.vel-self.vel2)>10:
                    self.maxonmotor.rm_move(self.vel)
                else:
                    self.maxonmotor.rm_move(0)
                self.vel2 = self.vel
                
                #print('vel400= ', self.vel)
            count = count + 1
            if count == 1:
                self.pre_velocity = self.vel
            if(200 == count) and (self.vel == self.pre_velocity):
                count = 0
                self.maxonmotor.rm_disable()
                self.maxonmotor.close_device()
             """

            #time.sleep(0.01)
            # 终止数据传输
            # print ("[Client] send End flag")
            # self.ServerSocket.send(('/end').encode('utf-8'))
            # break

    def __del__(self):
        # 关闭端口
        self.ServerSocket.close()


if __name__ == "__main__":
    client = SlavClient()
    client.process()
