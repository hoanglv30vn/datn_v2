import socket
import errno
import sys
import threading
import time
import serial
exitFlag = 0
global flagsenduart 
flagsenduart=0
global serial__ 
global data
data='hi'
# serial__=serial.Serial()
serial_com = input("SELLECT COM: ")
# serial_com = "COM11"
serial__=serial.Serial(serial_com, baudrate=9600 ,timeout=0.1)
IP = "192.168.0.212"
PORT = 8888

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to a given ip and port
try:
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)
except:
    print("looxi get addr info failed")
    
# serial__.write("HELLO PRT".encode())
class chaylen (threading.Thread):
    def __init__(self,  threadID, name ):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("Bat dau " + self.name)
        self.readData()       
    def readData(self):
        while True: 
            # print("wait data")
            if serial__.in_waiting >0:
                global data
                data = serial__.readline()                
                client_socket.send(data)      
                print(data)
class udp (threading.Thread):
    def __init__(self,  threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("Bat dau " + self.name)
        self.udp_truyen_nhan()
    def udp_truyen_nhan(self):
        message__ = ""
        while True:        
            try:
                while True:
                    message = client_socket.recv(1).decode('utf-8')
                    if message == '#':
                        print(message__.encode())
                        serial__.write(message__.encode())
                    elif message == '*':
                        message__ = ''
                        message = ''                        
                    else:
                        message__+= str(message)         
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    # sys.exit()

                # We just did not receive anything
                continue

            except Exception as e:
                # Any other exception - something happened, exit
                print('Reading error: '.format(str(e)))
                # sys.exit()
                pass
try:
    thread1 = chaylen(1, "Thread-1")
    thread2 = udp(2, "Thread-2")# Bat dau cac thread moi
    thread1.start()
    thread2.start()
    print ("Ket thuc Main Thread")
except:
    print("error")                