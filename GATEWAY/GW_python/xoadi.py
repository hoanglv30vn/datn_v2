from logging import error
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import threading
import time
import datetime
import socket
import sys
import glob
import serial
from threading import Thread
from PyQt5.QtCore import QDate, Qt
import pyrebase
import array as arr
import re
############################# DATABASE SQL #########################################

#################################################################################### 
# # khởi tạo com
com_input = input("COM:")
com_port = "COM"+com_input
global serial__ 
serial__=serial.Serial()     

serial__=serial.Serial(com_port, baudrate=9600 ,timeout=0.1)                


# def get_ip_socket_serve():
IP = socket.gethostbyname(socket.gethostname())
data_send_uart = "CF_CLIENT_TCP%"+IP+"#TCP%OKE"
serial__.write(data_send_uart.encode())       
print(data_send_uart.encode())        
# a= no_accent_vietnamese("Việt Nam ẳ ấ ồ ư ị ỳ ùúụủũưừứựửữ  àáạảãâầấậẩẫăằắặẳẵ ý ỷĐất Nước Con Người")
# b= no_accent_vietnamese("Welcome to Vietnam !")
# c =no_accent_vietnamese("VIỆT NAM ĐẤT NƯỚC CON NGƯỜI")

# print(a,b,c)
# mang = ['*', '26', 'SS', '026636', '7599', '30', '28','2','54','82', '#']
# for index in mang[5:-1]:
#     print(index)
# a=str(bin(158))[2:10]
# b=a
# # a.reverse()
# b=a[::-1]
# print(a)
# print(b)
while True:
    data_send_uart =input("hi:")
    data_send_uart = "*#277339#7415#2#20#8."
    serial__.write(data_send_uart.encode())
    # c= input("hi")

# a= [1,5,0]
# # print(a[-1])
# a[2]= 6
# print(a)
# hihi = input("v")


# while True:
#     id_device_control= input("a:")
#     state_control= input("a:")
#     hello=f'*#127102#0589#2#{id_device_control}#{state_control}'
#     len_data_send_uart = len(hello) + 3
#     hello=f'*#127102#0589#2#'
#     data_send_uart = hello + str(len_data_send_uart)+ '#' + str(id_device_control) +'_'+ str(state_control) +'.'
#     data_send_uart = "*@21@C_F@063233@7458@#@"
#     serial__.write(data_send_uart.encode())       
#     print(data_send_uart.encode())    
#     print(data_send_uart) 
#     print(len(data_send_uart))     


    # a = input("hihi")
    # hello=f'*#127302#0519#1#chaohoang'
    # len_data_send_uart = len(hello) + 3
    # hello=f'*#128102#0519#1#'
    # data_send_uart = hello + str(len_data_send_uart) +'#chaohoang' +'.'
    # serial__.write(data_send_uart.encode())       
    # print(data_send_uart.encode()) 
    # print(data_send_uart) 
    # print(len(data_send_uart))     

# a = {
#     'TB0': 
#         {
#             'namethietbi': 'tb0',
#             'phanloai': 'cambien',
#             'trangthai': 'off'
#         }, 
#     'namephong': 'phong 1080'
#     }
# for i in a:
#     if i!= 'namephong':
#         for s in a:
#             if s=='namephong':
#                 print(a[s])       
#         for k in a[i]:
#             print(k)
#             print(a[i][k])
#     else:
#         print(a[i])
# b= input("hi:")



 