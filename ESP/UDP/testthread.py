import threading
import time
import socket
import select

count_=0
class chaylen (threading.Thread):
    def __init__(self,  threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("Bat dau " + self.name)
        self.readData()     
       
    def readData(self):
        count_+=1
        print(count_) 
class udp (threading.Thread):
    def __init__(self,  threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        # self.counter = counter
    def run(self):
        print ("Bat dau " + self.name)
        self.print_time()
    def print_time(self,receive_message):
        print(time) 
try:
    thread1 = chaylen(1, "Thread-1")
    thread2 = udp(2, "Thread-2")# Bat dau cac thread moi
    thread1.start()
    thread2.start()
    print ("Ket thuc Main Thread")
except:
    print("error")

