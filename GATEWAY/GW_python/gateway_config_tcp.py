#################################################################################### 
##                                           ``..``                               ##    
##                                         -ymNMNmds:`                            ##     
##                                 `.:/+osyMMMNmNMMMMms:                          ##     
##                             `:sdNMMMMMMMMMy.  .+hNMMMd/                        ##     
##                           :yNMMMMNdyso+++-       `+mMMMd:                      ##     
##                         /mMMMNy/.                   /NMMMo                     ##     
##                       .hMMMd+`                       .hMMMo                    ##     
##               -yyyyyyyNMMMMhyyyyyyyyyyyyyyyyyyyyyyyyyyhMMMM/                   ##     
##               :NMMMMMMMMMMddMmdNm...mMMMMMMMMMMNdmMddMNNMMMm                   ##     
##                .sdMMMMMNmdmmdmNmh   ydMMMMMMMNddNmdNNd/.yMMM:                  ##     
##                 ``yNMMMdmMmdMmh-`   `.hmMMMMmdNNdmMhs`  +MMM+                  ##     
##                   `NMMNssssss:         :sssssssssss`    /MMMo                  ##     
##                   :MMMy     .+/`         ..             oMMM+                  ##     
##                   /MMMo     :NMd/.   `.:ymd.            hMMM.                  ##     
##                   -MMMh      -yNMmhyydmMNh/            :MMMh                   ##     
##                    dMMN-       ./shddys/.            `oNMMm-                   ##     
##                    :NMMm-                         `.omMMMh.                    ##     
##                     /NMMNo.                  ``.:sdNMMNd/                      ##     
##                      -hMMMNho/-.``````..-:+oyhmMMMMNms-                        ##     
##                        :yNMMMMMN HOANGLE MMMMMMNds/-                           ##     
##                           -+shdmNNMMMMmdhyso/:.                                ##     
##                                  `MMMm                                         ##     
##                                  /MMMo                                         ##     
##           .`                     yMMM-                                         ##     
##     .----oNm`                    mMMN                                          ##     
##    -mNNNNMMMy.                  .MMMh                                          ##     
##     .../MMMMMm+`              `/yMMMo                                          ##     
##         :oydMMMm/           -smMMMMMo                                          ##     
##            `+mMMNs`       .yNMMMMMMMNy.                                        ##     
##              .hMMMh.     /mMMNh:dMMMMMm/                                       ##     
##               `sMMMd.  `yMMMm/  mMMMdMMNs`                                     ##     
##                 sMMMh`-dMMMh.   NMMN`yMMMh.                                    ##     
##                 `yMMMhmMMMo`    NMMN  +NMMd-                                   ##     
##                  `yMMMMMMy      NMMN   /NMMm-                                  ##     
##                   `hMMMMM-      dMMM`   :NMMm.                                 ##     
##                    `dMMMs       yMMM-    /MMMd`                                ##     
##                     `/+:        oMMM+     oMMMs                                ##     
##                                 -MMMh      dMMM:                               ##
#################################################################################### 
#                               -*- coding: utf-8 -*-   
#                                 GHI CH?? - README
#                                CODE BY: HO??NG L??
#                       https://github.com/hoanglv30vn/datn_v2
#
#####################################################################################
# L???NH TRONG DATA SEND UART - PIC:| 1-CONFIG | 2: CONTROL | 3: ...
# 
# 
#
# 
# 
#####################################################################################


from logging import error
from sqlite3.dbapi2 import connect
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import sys
import glob
import serial
from threading import Thread
from PyQt5.QtCore import QDate, Qt
import pyrebase
import array as arr
import re
import random
import socket
import threading
import time
import socket
from socket import SHUT_RDWR
import select

############################# DATABASE SQL #########################################
conn_db = sqlite3.connect('data_config.db')   #k???t n???i t???i database
curr = conn_db.cursor()    #con tr???
curr.execute('''CREATE TABLE IF NOT EXISTS CONFIG_GW(ATTRIBUTES char[30], THONGTIN char[20])''') 
curr.execute('''CREATE TABLE IF NOT EXISTS DATA_NODE(ID_NODE char[20], NAME_ID_NODE char[20],  ID_THIETBI CHAR[20], NAME_THIETBI CHAR[20], PHANLOAI CHAR[20], PHANLOAI_ID_THIETBI CHAR[10], TRANGTHAI_ACTIVE CHAR[20])''') 
conn_db.commit()




# c???u h??nh firebase 
firebaseConfig = {
  'apiKey': "AIzaSyAEqi81NFMPBJGxWRy7QtQv961efPzL9LA",
  'authDomain': "hellodatn.firebaseapp.com",
  'databaseURL': "https://hellodatn-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "hellodatn",
  'storageBucket': "hellodatn.appspot.com",
  'messagingSenderId': "559705579450",
  'appId': "1:559705579450:web:3421e5377912259256c783",
  'measurementId': "G-YK901S5FXQ"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database().child("ADMIN")

name_gw = 'gateway'
global serial__ 
serial__=serial.Serial()
global id_gw
id_gw = 'gateway'
curr.execute("SELECT * FROM CONFIG_GW WHERE ATTRIBUTES = ? ", ["id_nha"] ) 
if (len(curr.fetchall())>0): 
    thongtin_cfig=curr.execute("SELECT * FROM CONFIG_GW WHERE ATTRIBUTES = 'id_nha' ")
    id_gw = thongtin_cfig.fetchone()[1]

global chuoinhiphan
chuoinhiphan =[0,0,0,0,0,0,0,0]


HEADER_LENGTH = 10

print(socket.gethostbyname(socket.gethostname()))
IP = socket.gethostbyname(socket.gethostname())
PORT = 8888
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

conn_db.close()









class Ui_MainWindow(object):    

    def stream_handler(self, message):    
        # h??m l???ng nghe s??? ki???n t??? firebase
        event_fb = message["event"] # put
        print("event:" + event_fb)
        path_fb = message["path"] # /-K7yGTTEp7O549EzTYtI
        print("path:" )      
        print(path_fb)
        mess_fb = message["data"] # {'title': 'Pyrebase', "body": "etc..."}   
        print("mess")
        # print(mess_fb)
        link_fb = path_fb.split("/")
        print(link_fb)
        # print(len(link_fb))
        if len(link_fb) == 4 and link_fb[-1]=="onoff":
            print('data thay doi tu firebase:')     
            id_node_control = link_fb[1]
            # id_device_control = link_fb[2]
            # state_control = mess_fb
            # self.send_data_control(id_node_control,id_device_control,state_control) 
            global chuoinhiphan
            chuoinhiphan =[0,0,0,0,0,0,0,0]

            data_control = firebase.database().child("ADMIN")
            data_gw = data_control.child(id_gw).child(id_node_control).get()
            data_object = data_gw.val()
            # print(chuoinhiphan)
            binTOdec = self.get_data_control(data_object,id_node_control,"")           
            print(binTOdec)
            self.send_data_control(id_node_control,binTOdec) 
        elif  len(link_fb) == 3:
            pass
            # self.load_data_node()
    def get_data_control( self, data_object,id_node_ctrl, key__idtb):
        stt_thietbi_control=""
        state_thietbi_control=''  
        key__temp = key__idtb
        conn_read_tb = sqlite3.connect('data_config.db')
        cursor_tb = conn_read_tb.cursor()
        for key, value in data_object.items():
            if isinstance(value, dict):
                key__temp = key
                self.get_data_control(value ,id_node_ctrl,key__temp)
            else:
                if(str(key)) == "onoff":      
                    cursor_tb.execute("SELECT PHANLOAI FROM DATA_NODE WHERE ID_NODE = ? AND ID_THIETBI = ? ", [id_node_ctrl,key__temp] )  
                    # print(key__temp)
                    if cursor_tb.fetchone()[0] == "Thi???t b???":    
                        get_id_phanloai_node = cursor_tb.execute("SELECT PHANLOAI_ID_THIETBI FROM DATA_NODE WHERE ID_NODE = ? AND ID_THIETBI = ? ", [id_node_ctrl,key__temp] )  
                        stt_thietbi_control = get_id_phanloai_node.fetchone()[0] 
                        value_encode = str(value)
                        print(value_encode)
                        state_thietbi_control = self.decode_data(value_encode)
                        print(f'm?? h??a:{state_thietbi_control}')
                        chuoinhiphan [int(stt_thietbi_control[2])]= int(state_thietbi_control)
                        print(key__temp+ "-" + stt_thietbi_control + '__' + stt_thietbi_control[2])
                        # print(chuoinhiphan)
        binTOdec = self.binaryToDecimal(chuoinhiphan)
        conn_read_tb.close()
        return binTOdec
        # print(binTOdec)

    def binaryToDecimal(self,n):        
        dec_value = 0        
        base = 1                
        for i in n:                       
            dec_value += i * base
            base = base * 2        
        return dec_value
    def send_data_control(self,id_node_control,binTOdec):
        hello=f'*#{id_gw}#{id_node_control}#2#{binTOdec}'
        len_data_send = len(hello) + 3
        hello=f'*#{id_gw}#{id_node_control}#2#'
        data_send_tcp = hello + str(len_data_send)+ '#' + str(binTOdec) +'.'    
        print(data_send_tcp.encode())  
        for client_socket in clients:
            # client_socket.send( userheader + userdata + messheader + messdata)     
            client_socket.send(data_send_tcp.encode())    
    def load_data_node(self):
        db = firebase.database().child("ADMIN")        
        name_nha = "name_nha"
        id_nha = "id_nha"
        data_gw = db.child(id_gw).get()
        try:
            self.check_data_from_sql(id_nha,id_gw,name_nha)             
            data_object=data_gw.val()   
        except:
            print("error")
        self.pretty(data_object)    
        print("oke")           
    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        # check ??ang d??ng h??? ??i???u h??nh n??o
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            # ki???m tra c??c c???ng com ??ang s???n s??ng
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        # danh s??ch c??c c???ng com
        return result
    def add_com(self):
        # add danh s??ch c???ng com v??o box
        self.box_comport.clear()                
        self.box_comport.addItems(self.serial_ports())

    def set_serial_change(self):       
        conn = sqlite3.connect('data_config.db')   #k???t n???i t???i database
        curr = conn.cursor()    #con tr???            
        serial_com = self.box_comport.currentText()    
        curr.execute("UPDATE CONFIG_GW SET THONGTIN = ? WHERE ATTRIBUTES = ?",[serial_com, "COM_PORT"])
        conn.commit() 
        conn.close()
        self.set_serial()

    def set_serial(self):
        global serial__
        conn = sqlite3.connect('data_config.db')   #k???t n???i t???i database
        curr = conn.cursor()    #con tr???    
        # ch???n c???ng com, t???c ????? baud                             
        serial_baud = int(self.box_baudrate.currentText())
        # ?????c t??? SQL ????? xem ???? c?? c???ng com ch??a
        curr.execute("SELECT * FROM CONFIG_GW WHERE ATTRIBUTES = 'COM_PORT' ")
        if (len(curr.fetchall())>0): 
            thongtin_cfig=curr.execute("SELECT * FROM CONFIG_GW WHERE ATTRIBUTES = 'COM_PORT' ")
            serial_com = thongtin_cfig.fetchone()[1]
        else:
            serial_com = self.box_comport.currentText()    
            curr.execute("INSERT INTO CONFIG_GW VALUES (?,?)",["COM_PORT",serial_com])
            conn.commit()    
        serial__.close()

        try:
            serial__=serial.Serial(serial_com, baudrate=serial_baud ,timeout=0.1)
        except:
            serial_com = self.box_comport.currentText()    
            curr.execute("UPDATE CONFIG_GW SET THONGTIN = ? WHERE ATTRIBUTES = ?",[serial_com, "COM_PORT"])
            conn.commit()              
            serial__=serial.Serial(serial_com, baudrate=serial_baud ,timeout=0.1)
        print(serial__)
        conn.close()  

    def read_interval(self):
        # thread
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        try:
            self.timer.timeout.connect(self.readDataUART)
        except:
            print("readDataUART error")
        self.timer.start()


    def no_accent_vietnamese(self,s):
        s = re.sub(r'[??????????????????????????????????????????????]', 'a', s)
        s = re.sub(r'[??????????????????????????????????????????????]', 'A', s)
        s = re.sub(r'[??????????????????????????????]', 'e', s)
        s = re.sub(r'[??????????????????????????????]', 'E', s)
        s = re.sub(r'[??????????????????????????????????????????????]', 'o', s)
        s = re.sub(r'[??????????????????????????????????????????????]', 'O', s)
        s = re.sub(r'[????????????]', 'i', s)
        s = re.sub(r'[????????????]', 'I', s)
        s = re.sub(r'[?????????????????????????????]', 'u', s)
        s = re.sub(r'[?????????????????????????????]', 'U', s)
        s = re.sub(r'[??????????????]', 'y', s)
        s = re.sub(r'[??????????????]', 'Y', s)
        s = re.sub(r'[??]', 'D', s)
        s = re.sub(r'[??]', 'd', s)
        return s
 
# ###############################3
    def apply_span_to_sales_table(self, row, nrow):
        if nrow <= 1:
            return
        for c in (0, 1):
            self.table_danhsach.setSpan(row, c, nrow, 1)
            for r in range(row + 1, row + nrow):
                t = self.table_danhsach.takeItem(r, c)
                del t
    def ALL_DATA(self,update_firebase): 
        # in t??n + id nh??
        # result = conn.execute("SELECT * FROM CONFIG_GW")  
        conn = sqlite3.connect('data_config.db')   #k???t n???i t???i database
        curr = conn.cursor()    #con tr???    
         
        db = firebase.database().child("ADMIN")          
        global id_gw    
        name_home = "     HOME:"
        id_home_hienthi = "   -   ID:"
        curr.execute("SELECT * FROM CONFIG_GW WHERE ATTRIBUTES = ? ", ["id_nha"] ) 
        if (len(curr.fetchall())>0): 
            thongtin_cfig=curr.execute("SELECT * FROM CONFIG_GW WHERE ATTRIBUTES = 'id_nha' ")
            id_gw = thongtin_cfig.fetchone()[1]
            id_home_hienthi += id_gw
        curr.execute("SELECT * FROM CONFIG_GW WHERE ATTRIBUTES = ? ", ["name_nha"] ) 
        if (len(curr.fetchall())>0): 
            thongtin_cfig=curr.execute("SELECT * FROM CONFIG_GW WHERE ATTRIBUTES = 'name_nha' ")
            name_home += thongtin_cfig.fetchone()[1]
        self.lab_name_gw.setText(name_home + id_home_hienthi)
        
        # ___________ #
        # in ra table
        result = conn.execute("SELECT ID_NODE, NAME_ID_NODE, ID_THIETBI, NAME_THIETBI, PHANLOAI FROM DATA_NODE")        
        self.table_danhsach.setRowCount(0)    
        last_id = -1
        start_row = 0        
        color=arr.array( 'i' ,[230,230,230,255,255,255])
        color_active = (QtGui.QColor(100,255,150))
        for row_number, row_data in enumerate(result): 
            self.table_danhsach.insertRow(row_number)  
            current_id, *other_values = row_data
            row_color_number = row_number%2
            color_row = (QtGui.QColor(color[3*row_color_number],color[3*row_color_number+1],color[3*row_color_number+2]))
            for colum_number, data in enumerate (row_data):
                # ??o???n n??y l?? in ra b???ng
                self.table_danhsach.setItem(row_number, colum_number,QtWidgets.QTableWidgetItem(str(data)))                 
                self.table_danhsach.item(row_number, colum_number).setBackground(color_row)              
                if colum_number == 0:
                    id_node_update = data
                elif colum_number == 2:
                    id_device_update = data
                elif colum_number == 4:
                    phanloai_device_update = data
                    if phanloai_device_update == "C???m bi???n":
                        giatri_update = "analog"                        
                    elif phanloai_device_update == "Thi???t b???":
                        giatri_update = 0                        
                    else:
                        giatri_update = "undefind"
                    giatri_update_encode = self.encode_data(giatri_update)
                    # db = firebase.database().child("ADMIN")          
                    # db.child(id_gw).child(id_node_update).child(id_device_update).update({'phanloai':phanloai_device_update})  
                    if update_firebase == 0:
                        db = firebase.database().child("ADMIN") 
                        db.child(id_gw).child(id_node_update).child(id_device_update).update({'trangthai':giatri_update_encode,'onoff':giatri_update_encode})  
                        # db.child(id_gw).child(id_node_update).child(id_device_update).update({'onoff':giatri_update}) 

                # ?????i m??u
                curr.execute("SELECT TRANGTHAI_ACTIVE FROM DATA_NODE WHERE NAME_ID_NODE = ? AND TRANGTHAI_ACTIVE = 'active'", [data])
                if (len(curr.fetchall())>0): 
                    # self.table_danhsach.item(row_number, colum_number).setBackground(color_active)
                    self.table_danhsach.setItem(row_number, colum_number,QtWidgets.QTableWidgetItem(str(data)+" -active"))                                
            # ??o???n n??y xu???ng d?????i + h??m apply_span_to_sales_table l??:
            # so s??nh g???p c??c h??ng c???a c???t 0, c???t 1 n???u t??n ph??ng v?? t??n id gi???ng nhau
            if last_id != current_id and last_id != -1:
                self.apply_span_to_sales_table(start_row, row_number - start_row)
                start_row = row_number
            last_id = current_id
            if start_row != row_number:
                # pass
                self.apply_span_to_sales_table(start_row, self.table_danhsach.rowCount())        
        conn.close()   
        print(id_gw)
        db = firebase.database().child("ADMIN")  
        db.child(id_gw).stream(self.stream_handler) 

        # db.child(id_gw).update(result)  
    def check_data_from_sql(self,id_nha,id_gw_from_line,name_nha):
        # check xem c?? data ch??a, n???u c?? r???i th?? x??a.
        conn = sqlite3.connect('data_config.db')   #k???t n???i t???i database
        curr = conn.cursor()    #con tr???     
        curr.execute("SELECT * FROM DATA_NODE")
        if (len(curr.fetchall())>0): 
            curr.execute("SELECT * FROM DATA_NODE")
            curr.execute("DELETE FROM DATA_NODE")

        curr.execute("SELECT * FROM CONFIG_GW WHERE ATTRIBUTES = ? ", [id_nha] )
        if (len(curr.fetchall())>0): 
            curr.execute("DELETE FROM CONFIG_GW WHERE ATTRIBUTES = ?",[id_nha])  
            curr.execute("INSERT INTO CONFIG_GW VALUES (?,?)",[id_nha,id_gw_from_line])  
        else:
            curr.execute("INSERT INTO CONFIG_GW VALUES (?,?)",[id_nha,id_gw_from_line])  

        curr.execute("SELECT * FROM CONFIG_GW WHERE ATTRIBUTES = ? ", [name_nha] )
        if (len(curr.fetchall())>0): 
            curr.execute("DELETE FROM CONFIG_GW WHERE ATTRIBUTES = ?",[name_nha])  
        conn.commit()
        conn.close()          
    def read_idGW_firebase(self):
        db = firebase.database().child("ADMIN")        
        id_gw_from_line = self.line_idgw.text()
        name_nha = "name_nha"
        id_nha = "id_nha"
        data_gw = db.child(id_gw_from_line).get()
        try:
            self.check_data_from_sql(id_nha,id_gw_from_line,name_nha)             
            data_object=data_gw.val()   
        except:
            print("error")
        self.pretty(data_object)
        print("oke")    
    def pretty( self, data_object):
        tenphongsql = "tentam"
        trangthai_active = "inactive"
        sothutu_thietbi = 0
        sothutu_cambien = 0
        phanloai_id_thietbi = "none"
        conn = sqlite3.connect('data_config.db')   #k???t n???i t???i database
        curr = conn.cursor()    #con tr???           
        for phong, nha in data_object.items():
            # print("ph??ng:" + str(phong))
            if isinstance(nha, dict):
                sothutu_thietbi = 0
                sothutu_cambien = 0
                for thietbi, tenphong in nha.items():
                    # print("t??n thi???t b??? "+ thietbi)
                    if isinstance(tenphong, dict):
                        for doituong, dulieu in tenphong.items():                            
                            if doituong == "namethietbi":
                                namethietbi = self.decode_data(dulieu)
                                # print(namethietbi)
                            elif doituong == "phanloai":
                                phanloai =  self.decode_data(dulieu)
                                # print(phanloai)
                        # print (str(phong) + ":"+ str(thietbi)+ ":" + str(namethietbi)+ ":" + str(phanloai) )
                        if phanloai == 'Thi???t b???':
                            # phanloai = phanloai + '_TB' +str(sothutu_thietbi)
                            phanloai_id_thietbi =  'TB' +str(sothutu_thietbi)
                            sothutu_thietbi +=1
                        elif phanloai == 'C???m bi???n':
                            # phanloai = phanloai + '_CB' +str(sothutu_cambien)
                            phanloai_id_thietbi =  'CB' +str(sothutu_cambien)
                            sothutu_cambien +=1                            
                        curr.execute("INSERT INTO DATA_NODE VALUES (?,?,?,?,?,?,?)",[phong,tenphongsql,thietbi,namethietbi,phanloai,phanloai_id_thietbi,trangthai_active])                                        
                    else:
                        # print("t??n ph??ng:" + tenphong)
                        tenphongsql =  self.decode_data(tenphong)
                        curr.execute("UPDATE DATA_NODE SET NAME_ID_NODE = ? WHERE ID_NODE = ?",[tenphongsql,phong])                                             
                # pass
            else:
                tennhasql= self.decode_data(nha)
                print("nh??" + tennhasql)    
                curr.execute("INSERT INTO CONFIG_GW VALUES (?,?)",["name_nha",tennhasql])                            
        conn.commit()  
        conn.close()       
        self.ALL_DATA(0)

    # def pretty( self, data_object):
    #     for key, value in data_object.items():
    #         print("key:" + str(key))
    #         if isinstance(value, dict):
    #             self.pretty(value)
    #         else:
    #             print("value" + str(value))    


    def encode_data(self,data):
        # d=103
        d=463
        p=19
        q=11
        n=p*q  
        wn = (p-1)*(q-1)      
        e=7    
        list_m_int = [5, 7, 17, 31, 57,23,19,29,41,47,63,97,61]
        m=  random.choice(list_m_int)    
        c= pow(m,e) % n
        kqmahoa=''
        j=1
        for i in str(data):
            # char to ascii
            j=j+1
            somahoaascii = j*m - j + 3
            dauconghoactru = pow(-1,j%2+1)
            somahoaascii = somahoaascii % 15 + 1
            kqmahoa += chr( ord(i)+ dauconghoactru*somahoaascii)
        kqmahoa = kqmahoa + "_??_" + str(c) + "_??_" + str(n)
        return kqmahoa


    def decode_data (self,datas):
        data = str(datas).split("_??_")
        if len(data)<2:
            return datas
        elif len(data)>2:
            print("data:_??_")
            print(data)        
            c= int(data[1])
            n= int(data[2])
            d=463
            kq_M=pow(c,d)%n
            kqgiaima=''
            j=1
            for i in data[0]:
                j=j+1
                somahoaascii = j*kq_M - j + 3
                dauconghoactru = pow(-1,j%2+1)
                somahoaascii = somahoaascii % 15 + 1
                kqgiaima += chr( ord(i)- dauconghoactru*somahoaascii)
            return kqgiaima 

    def get_ip_socket_serve(self):
        IP = socket.gethostbyname(socket.gethostname())
        data_send_uart = "CF_CLIENT_TCP%"+IP+"#TCP%OKE"
        serial__.write(data_send_uart.encode())       
        print(data_send_uart.encode())          



# ####################################################################

    def setupUi(self, MainWindow):
#         
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(819, 540)
        MainWindow.setStyleSheet("#centralwidget{\n"
            "    background-color:qlineargradient(spread:pad, x1:1, y1:0.25, x2:0.988636, y2:1, stop:0.0909091 rgba(29, 113, 133, 248), stop:1 rgba(255, 255, 255, 255));\n"
            "font-size:16px;\n"
            "}\n"
            "\n"
            "#line_idgw,#box_comport,#box_baudrate{\n"
            "font-size:24px;\n"
            "}\n"
            "\n"
            "QLabel{\n"
            "border-radius: 10%;\n"
            "font-size:20px;\n"
            "background-color:rgb(217, 232, 217);\n"
            "}\n"
            "#tab_config,#tab_hienthi{\n"
            "background-color:rgba(0, 124, 91, 206)\n"
            "}\n"
            "\n"
            "#butt_oke{\n"
            "border-radius: 30%;\n"
            "font-size:20px;\n"
            "background-color:rgb(223, 223, 167)\n"
            "}\n"
            "#table_danhsach{\n"
            "font-size:20px;\n"
            "}\n"
            "#butt_ip_socket{\n"
            "border-radius: 30%;\n"
            "font-size:20px;\n"
            "background-color:rgb(223, 223, 167)\n"
            "}\n"
            "#table_danhsach{\n"
            "font-size:20px;\n"
            "}\n"            
            "")
# 
#
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 20, 791, 511))
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_hienthi = QtWidgets.QWidget()
        self.tab_hienthi.setObjectName("tab_hienthi")
        self.table_danhsach = QtWidgets.QTableWidget(self.tab_hienthi)
        self.table_danhsach.setGeometry(QtCore.QRect(10, 110, 761, 331))
        self.table_danhsach.setObjectName("table_danhsach")
        self.table_danhsach.setColumnCount(5)
        self.table_danhsach.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_danhsach.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_danhsach.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_danhsach.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_danhsach.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_danhsach.setHorizontalHeaderItem(4, item)      
        self.table_danhsach.horizontalHeader().setDefaultSectionSize(150)
        self.lab_name_gw = QtWidgets.QLabel(self.tab_hienthi)
        self.lab_name_gw.setGeometry(QtCore.QRect(10, 40, 421, 41))
        self.lab_name_gw.setObjectName("lab_name_gw")
        self.tabWidget.addTab(self.tab_hienthi, "")
        self.tab_config = QtWidgets.QWidget()
        self.tab_config.setObjectName("tab_config")
        self.butt_oke = QtWidgets.QPushButton(self.tab_config)
        self.butt_oke.setGeometry(QtCore.QRect(550, 120, 91, 61))
        self.butt_oke.setObjectName("butt_oke")
        self.butt_ip_socket = QtWidgets.QPushButton(self.tab_config)
        self.butt_ip_socket.setGeometry(QtCore.QRect(670, 340, 91, 61))
        self.butt_ip_socket.setObjectName("butt_ip_socket")        
        self.line_idgw = QtWidgets.QLineEdit(self.tab_config)
        self.line_idgw.setGeometry(QtCore.QRect(120, 120, 381, 61))
        self.line_idgw.setText("")
        self.line_idgw.setObjectName("line_idgw")
        self.label = QtWidgets.QLabel(self.tab_config)
        self.label.setGeometry(QtCore.QRect(120, 60, 151, 41))
        self.label.setObjectName("label")
        self.lab_comport = QtWidgets.QLabel(self.tab_config)
        self.lab_comport.setGeometry(QtCore.QRect(120, 260, 191, 41))
        self.lab_comport.setObjectName("lab_comport")
        self.lab_baudrate = QtWidgets.QLabel(self.tab_config)
        self.lab_baudrate.setGeometry(QtCore.QRect(410, 260, 191, 41))
        self.lab_baudrate.setObjectName("lab_baudrate")
        self.box_comport = QtWidgets.QComboBox(self.tab_config)
        self.box_comport.setGeometry(QtCore.QRect(120, 340, 191, 51))
        self.box_comport.setObjectName("box_comport")
        self.box_baudrate = QtWidgets.QComboBox(self.tab_config)
        self.box_baudrate.setGeometry(QtCore.QRect(410, 340, 191, 51))
        self.box_baudrate.setObjectName("box_baudrate")
        self.box_baudrate.addItems(["9600", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200", "128000"])

        self.tabWidget.addTab(self.tab_config, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 819, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
#
# ####################################################################
        # self.check_data_from_sql()
        self.ALL_DATA(0)
        self.add_com()
        self.set_serial()
        self.box_comport.currentIndexChanged.connect(self.set_serial_change)
        self.box_baudrate.currentIndexChanged.connect(self.set_serial_change)
        # t1 = Thread(target = self.read_interval())
        # t1.start()         
        # nh???p id gw, nh???n n??t th?? ?????c t??? firebase.
        self.butt_oke.clicked.connect(self.read_idGW_firebase)
        self.butt_ip_socket.clicked.connect(self.get_ip_socket_serve)
        # db.child(id_gw).stream(self.stream_handler) 
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GATEWAY"))
        item = self.table_danhsach.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID NODE"))  
        item = self.table_danhsach.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "NAME NODE"))                  
        item = self.table_danhsach.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "ID THI???T B???"))
        item = self.table_danhsach.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "NAME THI???T B???"))      
        item = self.table_danhsach.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "PH??N LO???I"))

        # self.lab_name_gw.setText(_translate("MainWindow", "    NAME GATEWAY"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_hienthi), _translate("MainWindow", "LIST"))
        self.butt_oke.setText(_translate("MainWindow", "OK"))
        self.butt_ip_socket.setText(_translate("MainWindow", "IP"))
        self.label.setText(_translate("MainWindow", "   ID GATEWAY "))
        self.lab_comport.setText(_translate("MainWindow", "       COM PORT"))
        self.lab_baudrate.setText(_translate("MainWindow", "       BAUD RATE"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_config), _translate("MainWindow", "CONFIG"))

                   
class udp (threading.Thread, Ui_MainWindow):
    def __init__(self,  threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        # self.counter = counter
    def run(self):
        print ("Bat dau " + self.name)
        self.udp_truyen_nhan(self.receive_message)
    def receive_message(self, client_socket):
        try:
            # Receive our "header" containing message length, it's size is defined and constant
            message_header = client_socket.recv(HEADER_LENGTH)
            # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(message_header):
                return False
            # Convert header to int value
            message_length = int(message_header.decode('utf-8').strip())
            # Return an object of message header and message data
            data_client_rcv = client_socket.recv(message_length)
            print(f"header: {message_header}---data:{data_client_rcv}")

            return {'header': message_header, 'data':data_client_rcv}

        except:

            # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
            # or just lost his connection
            # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
            # and that's also a cause when we receive an empty message
            pass
            # return False
            

    def udp_truyen_nhan(self,receive_message):
        while True:       
            try:     
                # Calls Unix select() system call or Windows select() WinSock call with three parameters:
                #   - rlist - sockets to be monitored for incoming data
                #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
                #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
                # Returns lists:
                #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
                #   - writing - sockets ready for data to be send thru them
                #   - errors  - sockets with some exceptions
                # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
                read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


                # Iterate over notified sockets
                for notified_socket in read_sockets:

                    # If notified socket is a server socket - new connection, accept it
                    if notified_socket == server_socket:

                        # Accept new connection
                        # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                        # The other returned object is ip/port set
                        client_socket, client_address = server_socket.accept()

                        # Client should send his name right away, receive it
                        user = receive_message(client_socket)

                        # If False - client disconnected before he sent his name
                        if user is False:
                            continue

                        # Add accepted socket to select.select() list
                        sockets_list.append(client_socket)

                        # Also save username and username header
                        clients[client_socket] = user                          
                        print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
                            

                    # Else existing socket is sending a message
                    else:
                        # Receive message
                        message = receive_message(notified_socket)
                        # If False, client disconnected, cleanup
                        if message is False:
                            # pass
                            # continue
                            print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                            # Remove from list for socket.socket()
                            sockets_list.remove(notified_socket)

                            # Remove from our list of users
                            del clients[notified_socket]

                            # server_socket.shutdown(SHUT_RDWR)  
                            continue

                        # Get user by notified socket, so we will know who sent the message
                        try:
                            user = clients[notified_socket]
                            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                            hello= message["data"].decode("utf-8") + '.'
                            self.readData_TCP(hello)
                        except:
                            print("l???i tcp")
                        #     pass
                        # khi nhan data from udp --> uart
                        # client_socket.send(b'oke')
                        # try:
                        #     serial__.write(hello.encode())    
                        # except:
                        #     print("disconnect uart")
                # It's not really necessary to have this, but will handle some socket exceptions just in case
                for notified_socket in exception_sockets:

                    # Remove from list for socket.socket()
                    sockets_list.remove(notified_socket)

                    # Remove from our list of users
                    del clients[notified_socket]   
            except:
                print("?? bi???t l???i ????u")                  
    def readData_TCP(self,data_read_fr_tcp):
        # thread: l???ng nghe uart
        global id_gw
        if len(data_read_fr_tcp) >10:
            data_recv = data_read_fr_tcp         
            print(data_recv)   
            lenght_data = str(len(data_recv[data_recv.find('*'):data_recv.find('#')]))
            print(lenght_data) 
            data = data_recv.split("@")
            print(data)
            print(id_gw)
            if len(data)>2:
                do_dai_chuoi_nhan = data[1]
                thongtinlenh_nhan = data[2]
                id_gw_nhan = data[3]
                id_node_nhan = data[4]            
                if do_dai_chuoi_nhan == lenght_data and id_gw_nhan == id_gw :
                    print("????ng ????? d??i - ????ng id")
                    # ph??n t??ch l???nh, x??? l??.
                    if thongtinlenh_nhan == 'CF':
                        self.thongtincauhinhnode(data)
                    # S_S == d??? li???u c???m bi???n.
                    elif thongtinlenh_nhan == 'SS':
                        self.uploadDataSensor(data)     
                    elif thongtinlenh_nhan == 'DK':
                        print("????ng l???nh ??k")              
                        self.update_state_thietbi(data)
                else:
                    print("config error")        
                    # g???i l???i x??c nh???n cho node.                                 
    def thongtincauhinhnode(self,data):
        # t??ch th??ng tin c???u h??nh node
        # x??? l??, g???i th??ng tin
        print("xu ly node moi")
        print(f'data nh???n ???????c l?? :{data}')
        id_node_nhan = data[4]    
        soluongcambien = 0
        soluongthietbi = 0    
        connect_sql = sqlite3.connect('data_config.db')   #k???t n???i t???i database
        cursor_ = connect_sql.cursor()
        cursor_.execute("SELECT * FROM DATA_NODE WHERE ID_NODE = ? ", [id_node_nhan] ) 
        if (len(cursor_.fetchall())>0): 
            get_name_node = cursor_.execute("SELECT NAME_ID_NODE FROM DATA_NODE WHERE ID_NODE = ? ", [id_node_nhan] )             
            name_node = get_name_node.fetchone()[0]
            name_node_no_VN = self.no_accent_vietnamese(name_node)
            print(name_node_no_VN)
            get_phanloai_node = cursor_.execute("SELECT PHANLOAI FROM DATA_NODE WHERE ID_NODE = ? ", [id_node_nhan] )             
            danhsachphanloai = get_phanloai_node.fetchall()
            print(danhsachphanloai)
            for phanloaithietbi in danhsachphanloai:
                # phanloai = phanloaithietbi[0].split("_")
                if phanloaithietbi[0] == "Thi???t b???":
                    soluongthietbi +=1
                elif phanloaithietbi[0] == "C???m bi???n":
                    soluongcambien +=1
            print("id node nh???n ??c:"+ id_node_nhan )
            cursor_.execute("UPDATE DATA_NODE SET TRANGTHAI_ACTIVE = 'active' WHERE ID_NODE = ? ", [id_node_nhan] ) 
            connect_sql.commit()

            # g???i l???i x??c nh???n cho node.
            hello=f'*#{id_gw}#{id_node_nhan}#1#{name_node_no_VN}'+'_'+str(soluongthietbi)+'_'+str(soluongcambien)
            len_data_send = len(hello) + 3
            hello=f'*#{id_gw}#{id_node_nhan}#1#'
            data_send_tcp = hello + str(len_data_send) +f'#{name_node_no_VN}' + '_'+str(soluongthietbi)+'_'+str(soluongcambien)+'.'      
            print(data_send_tcp.encode()) 
            for client_socket in clients:
                # client_socket.send( userheader + userdata + messheader + messdata)     
                client_socket.send(data_send_tcp.encode())    
                print(data) 


            # in l???i table            
        else:
            print("sai idnode")
            # g???i l???i x??c nh???n cho node.            
            hello=f'*#{id_gw}#{id_node_nhan}#1#ERROR NODE'
            len_data_send = len(hello) + 3
            hello=f'*#{id_gw}#{id_node_nhan}#1#'
            data_send_tcp = hello + str(len_data_send) +'#ERROR NODE' +'.'               
            print(data_send_tcp.encode())           
            for client_socket in clients:
                # client_socket.send( userheader + userdata + messheader + messdata)     
                client_socket.send(data_send_tcp.encode())    
                print(data) 
        connect_sql.close()
        # self.ALL_DATA(1)          
        # DATA_NODE(ID_NODE char[20], NAME_ID_NODE char[20], PHANLOAI CHAR[20], ID_THIETBI CHAR[20], NAME_THIETBI CHAR[20]                  


    def update_state_thietbi(self, data):
        state_thietbi_dec = int(data[5])
        state_thietbi_bin= str(bin(state_thietbi_dec))[2:10]
        id_gw_upload_state = data[3]
        id_node_upload_state = data[4]        
        onoff =" 0"
        index = 0
        print(state_thietbi_bin)
        connect_sql = sqlite3.connect('data_config.db')   #k???t n???i t???i database
        cursor_ = connect_sql.cursor()        
        cursor_.execute("SELECT ID_THIETBI FROM DATA_NODE WHERE ID_NODE = ? AND PHANLOAI = ? ", [id_node_upload_state,"Thi???t b???"] )          
        id_thietbi_upload_state_sss = cursor_.fetchall() 
        len_thietbi = len(id_thietbi_upload_state_sss)
        print(len_thietbi)
        state_bin_temp = state_thietbi_bin[0:len_thietbi]
        state_bin = state_bin_temp
        state_bin = state_bin_temp[::-1]
        for idx in range (len_thietbi - len(state_bin)):
            state_bin +='0'

        db = firebase.database().child("ADMIN")  
        db.child("NONE").stream(self.stream_handler) 
        for i in state_bin:
            id_thietbi_upload_state = id_thietbi_upload_state_sss[index][0]
            onoff_encode = self.encode_data(i)
            db = firebase.database().child("ADMIN")  
            db.child(id_gw_upload_state).child(id_node_upload_state).child(id_thietbi_upload_state).update({'trangthai':onoff_encode,'onoff':onoff_encode})                  
            # db.child(id_gw_upload_state).child(id_node_upload_state).child(id_thietbi_upload_state).update({'onoff':onoff})                  
            print(id_thietbi_upload_state +":--:"+ str(onoff))
            index +=1     

        db = firebase.database().child("ADMIN")  
        db.child(id_gw_upload_state).stream(self.stream_handler)       
        connect_sql.close() 


    def uploadDataSensor(self, data):
        print("up load sensor")
        print(data)
        id_gw_upload_sensor = data[3]
        id_node_upload_sensor = data[4]
        index = 0
        connect_sql = sqlite3.connect('data_config.db')   #k???t n???i t???i database
        cursor_ = connect_sql.cursor()
        cursor_.execute("SELECT ID_THIETBI FROM DATA_NODE WHERE ID_NODE = ? AND PHANLOAI = ? ", [id_node_upload_sensor,"C???m bi???n"] )  
        id_thietbi_upload_sensor_sss = cursor_.fetchall()    
        print(id_thietbi_upload_sensor_sss)           
        for analog in data[5:-1]:
            id_thietbi_upload_sensor = id_thietbi_upload_sensor_sss[index][0]
            print(id_thietbi_upload_sensor)
            analog_encode = self.encode_data(analog)
            db = firebase.database().child("ADMIN") 
            db.child(id_gw_upload_sensor).child(id_node_upload_sensor).child(id_thietbi_upload_sensor).update({'trangthai':analog_encode})              
            index +=1
        # * ss idgw id node cb cb cb cb
        # dodai = len(data)
        # for 
        #     pass
        connect_sql.close()
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    thread2 = udp(2, "Thread-2")# Bat dau cac thread moi    
    thread2.start()
    sys.exit(app.exec_())
