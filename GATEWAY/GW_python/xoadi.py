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
############################# DATABASE SQL #########################################

#################################################################################### 
# khởi tạo com
global serial__ 
serial__=serial.Serial()        
serial__=serial.Serial('COM11', baudrate=9600 ,timeout=0.1)                

while True:
    xxxx = input("hihi")
    hello=f'*#127102#0589#1#chaohoang'
    len_data_send_uart = len(hello) + 3
    hello=f'*#127102#0589#1#'
    data_send_uart = hello + str(len_data_send_uart) +'#chaohoang' +'.'
    serial__.write(data_send_uart.encode())       
    print(data_send_uart.encode()) 
    print(data_send_uart) 
    print(len(data_send_uart)) 



    xxxx = input("hihi")
    hello=f'*#127302#0519#1#chaohoang'
    len_data_send_uart = len(hello) + 3
    hello=f'*#128102#0519#1#'
    data_send_uart = hello + str(len_data_send_uart) +'#chaohoang' +'.'
    serial__.write(data_send_uart.encode())       
    print(data_send_uart.encode()) 
    print(data_send_uart) 
    print(len(data_send_uart))     
