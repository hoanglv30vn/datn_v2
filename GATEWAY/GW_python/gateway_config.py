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
#                                 GHI CHÚ - README
#                                CODE BY: HOÀNG LÊ
#                       https://github.com/hoanglv30vn/datn_v2
#
#####################################################################################
# LỆNH TRONG DATA SEND UART - PIC:| 1-CONFIG | 2: CONTROL | 3: ...
# 
# 
#
# 
# 
#####################################################################################


from logging import error
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

############################# DATABASE SQL #########################################
conn = sqlite3.connect('data_config.db')   #kết nối tới database
curr = conn.cursor()    #con trỏ
curr.execute('''CREATE TABLE IF NOT EXISTS CONFIG_GW(ATTRIBUTES char[30], THONGTIN char[20])''') 
curr.execute('''CREATE TABLE IF NOT EXISTS DATA_NODE(ID_NODE char[20], NAME_ID_NODE char[20],  ID_THIETBI CHAR[20], NAME_THIETBI CHAR[20], PHANLOAI CHAR[20], PHANLOAI_ID_THIETBI CHAR[10], TRANGTHAI_ACTIVE CHAR[20])''') 
conn.commit()


# cấu hình firebase 
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
class Ui_MainWindow(object):    

    def stream_handler(self, message):    
        # hàm lắng nghe sự kiện từ firebase
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
        for key, value in data_object.items():
            if isinstance(value, dict):
                key__temp = key
                self.get_data_control(value ,id_node_ctrl,key__temp)
            else:
                if(str(key)) == "onoff":      
                    conn_read_tb = sqlite3.connect('data_config.db')
                    cursor_tb = conn_read_tb.cursor()
                    cursor_tb.execute("SELECT PHANLOAI FROM DATA_NODE WHERE ID_NODE = ? AND ID_THIETBI = ? ", [id_node_ctrl,key__temp] )  
                    # print(key__temp)
                    if cursor_tb.fetchone()[0] == "Thiết bị":    
                        get_id_phanloai_node = cursor_tb.execute("SELECT PHANLOAI_ID_THIETBI FROM DATA_NODE WHERE ID_NODE = ? AND ID_THIETBI = ? ", [id_node_ctrl,key__temp] )  
                        stt_thietbi_control = get_id_phanloai_node.fetchone()[0] 
                        value_encode = str(value)
                        print(value_encode)
                        state_thietbi_control = self.decode_data(value_encode)
                        print(f'mã hóa:{state_thietbi_control}')
                        chuoinhiphan [int(stt_thietbi_control[2])]= int(state_thietbi_control)
                        print(key__temp+ "-" + stt_thietbi_control + '__' + stt_thietbi_control[2])
                        # print(chuoinhiphan)
        binTOdec = self.binaryToDecimal(chuoinhiphan)
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
        len_data_send_uart = len(hello) + 3
        hello=f'*#{id_gw}#{id_node_control}#2#'
        data_send_uart = hello + str(len_data_send_uart)+ '#' + str(binTOdec) +'.'
        serial__.write(data_send_uart.encode())       
        print(data_send_uart.encode())  

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
        # check đang dùng hệ điều hành nào
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
            # kiểm tra các cổng com đang sẵn sàng
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        # danh sách các cổng com
        return result
    def add_com(self):
        # add danh sách cổng com vào box
        self.box_comport.clear()                
        self.box_comport.addItems(self.serial_ports())

    def set_serial_change(self):            
        serial_com = self.box_comport.currentText()    
        curr.execute("UPDATE CONFIG_GW SET THONGTIN = ? WHERE ATTRIBUTES = ?",[serial_com, "COM_PORT"])
        conn.commit() 
        self.set_serial()

    def set_serial(self):
        global serial__
        # chọn cổng com, tốc độ baud                             
        serial_baud = int(self.box_baudrate.currentText())
        # Đọc từ SQL Để xem đã có cổng com chưa
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
    def readDataUART(self):
        # thread: lắng nghe uart
        global id_gw
        if serial__.in_waiting >0:
            data_recv = serial__.readline()
            data_recv = data_recv.decode('utf-8')            
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
                    print("đúng độ dài - đúng id")
                    # phân tích lệnh, xử lý.
                    if thongtinlenh_nhan == 'CF':
                        self.thongtincauhinhnode(data)
                    # S_S == dữ liệu cảm biến.
                    elif thongtinlenh_nhan == 'SS':
                        self.uploadDataSensor(data)     
                    elif thongtinlenh_nhan == 'DK':
                        print("đúng lệnh đk")              
                        self.update_state_thietbi(data)
                else:
                    print("config error")        
                    # gửi lại xác nhận cho node.            
                    hello=f'*#{id_gw_nhan}#{id_node_nhan}#1#ERROR GW'
                    len_data_send_uart = len(hello) + 3
                    hello=f'*#{id_gw_nhan}#{id_node_nhan}#1#'
                    data_send_uart = hello + str(len_data_send_uart) +'#ERROR GW' +'.'
                    serial__.write(data_send_uart.encode())       
                    print(data_send_uart.encode())                    

    def read_interval(self):
        # thread
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        try:
            self.timer.timeout.connect(self.readDataUART)
        except:
            print("readDataUART error")
        self.timer.start()


    def update_state_thietbi(self, data):
        state_thietbi_dec = int(data[5])
        state_thietbi_bin= str(bin(state_thietbi_dec))[2:10]
        id_gw_upload_state = data[3]
        id_node_upload_state = data[4]        
        onoff =" 0"
        index = 0
        print(state_thietbi_bin)
        curr = conn.cursor()
        curr.execute("SELECT ID_THIETBI FROM DATA_NODE WHERE ID_NODE = ? AND PHANLOAI = ? ", [id_node_upload_state,"Thiết bị"] )          
        id_thietbi_upload_state_sss = curr.fetchall() 
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

    def uploadDataSensor(self, data):
        print("up load sensor")
        print(data)
        id_gw_upload_sensor = data[3]
        id_node_upload_sensor = data[4]
        index = 0
        curr = conn.cursor()
        curr.execute("SELECT ID_THIETBI FROM DATA_NODE WHERE ID_NODE = ? AND PHANLOAI = ? ", [id_node_upload_sensor,"Cảm biến"] )  
        id_thietbi_upload_sensor_sss = curr.fetchall()    
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

    def no_accent_vietnamese(self,s):
        s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
        s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
        s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
        s = re.sub(r'[ìíịỉĩ]', 'i', s)
        s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
        s = re.sub(r'[Đ]', 'D', s)
        s = re.sub(r'[đ]', 'd', s)
        return s
               
    def thongtincauhinhnode(self,data):
        # tách thông tin cấu hình node
        # xử lý, gửi thông tin
        print("xu ly node moi")
        print(f'data nhận được là :{data}')
        id_node_nhan = data[4]    
        soluongcambien = 0
        soluongthietbi = 0    
        curr = conn.cursor()
        curr.execute("SELECT * FROM DATA_NODE WHERE ID_NODE = ? ", [id_node_nhan] ) 
        if (len(curr.fetchall())>0): 
            get_name_node = curr.execute("SELECT NAME_ID_NODE FROM DATA_NODE WHERE ID_NODE = ? ", [id_node_nhan] )             
            name_node = get_name_node.fetchone()[0]
            name_node_no_VN = self.no_accent_vietnamese(name_node)
            print(name_node_no_VN)
            get_phanloai_node = curr.execute("SELECT PHANLOAI FROM DATA_NODE WHERE ID_NODE = ? ", [id_node_nhan] )             
            danhsachphanloai = get_phanloai_node.fetchall()
            print(danhsachphanloai)
            for phanloaithietbi in danhsachphanloai:
                # phanloai = phanloaithietbi[0].split("_")
                if phanloaithietbi[0] == "Thiết bị":
                    soluongthietbi +=1
                elif phanloaithietbi[0] == "Cảm biến":
                    soluongcambien +=1
            print("id node nhận đc:"+ id_node_nhan )
            curr.execute("UPDATE DATA_NODE SET TRANGTHAI_ACTIVE = 'active' WHERE ID_NODE = ? ", [id_node_nhan] ) 
            conn.commit()
            # gửi lại xác nhận cho node.
            hello=f'*#{id_gw}#{id_node_nhan}#1#{name_node_no_VN}'+'_'+str(soluongthietbi)+'_'+str(soluongcambien)
            len_data_send_uart = len(hello) + 3
            hello=f'*#{id_gw}#{id_node_nhan}#1#'
            data_send_uart = hello + str(len_data_send_uart) +f'#{name_node_no_VN}' + '_'+str(soluongthietbi)+'_'+str(soluongcambien)+'.'
            serial__.write(data_send_uart.encode())       
            print(data_send_uart.encode()) 
            print(data_send_uart) 
            print(len(data_send_uart)) 


            # in lại table            
        else:
            print("sai idnode")
            # gửi lại xác nhận cho node.            
            hello=f'*#{id_gw}#{id_node_nhan}#1#ERROR NODE'
            len_data_send_uart = len(hello) + 3
            hello=f'*#{id_gw}#{id_node_nhan}#1#'
            data_send_uart = hello + str(len_data_send_uart) +'#ERROR NODE' +'.'
            serial__.write(data_send_uart.encode())       
            print(data_send_uart.encode())           


        self.ALL_DATA(1)          
        # DATA_NODE(ID_NODE char[20], NAME_ID_NODE char[20], PHANLOAI CHAR[20], ID_THIETBI CHAR[20], NAME_THIETBI CHAR[20]                  

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
        # in tên + id nhà
        # result = conn.execute("SELECT * FROM CONFIG_GW")  
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
                # đoạn này là in ra bảng
                self.table_danhsach.setItem(row_number, colum_number,QtWidgets.QTableWidgetItem(str(data)))                 
                self.table_danhsach.item(row_number, colum_number).setBackground(color_row)              
                if colum_number == 0:
                    id_node_update = data
                elif colum_number == 2:
                    id_device_update = data
                elif colum_number == 4:
                    phanloai_device_update = data
                    if phanloai_device_update == "Cảm biến":
                        giatri_update = "analog"                        
                    elif phanloai_device_update == "Thiết bị":
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

                # đổi màu
                curr.execute("SELECT TRANGTHAI_ACTIVE FROM DATA_NODE WHERE NAME_ID_NODE = ? AND TRANGTHAI_ACTIVE = 'active'", [data])
                if (len(curr.fetchall())>0): 
                    # self.table_danhsach.item(row_number, colum_number).setBackground(color_active)
                    self.table_danhsach.setItem(row_number, colum_number,QtWidgets.QTableWidgetItem(str(data)+" -active"))                                
            # đoạn này xuống dưới + hàm apply_span_to_sales_table là:
            # so sánh gộp các hàng của cột 0, cột 1 nếu tên phòng và tên id giống nhau
            if last_id != current_id and last_id != -1:
                self.apply_span_to_sales_table(start_row, row_number - start_row)
                start_row = row_number
            last_id = current_id
            if start_row != row_number:
                # pass
                self.apply_span_to_sales_table(start_row, self.table_danhsach.rowCount())        
        # conn.close()   
        print(id_gw)
        db = firebase.database().child("ADMIN")  
        db.child(id_gw).stream(self.stream_handler) 
        # db.child(id_gw).update(result)  
    def check_data_from_sql(self,id_nha,id_gw_from_line,name_nha):
        # check xem có data chưa, nếu có rồi thì xóa.

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
        for phong, nha in data_object.items():
            # print("phòng:" + str(phong))
            if isinstance(nha, dict):
                sothutu_thietbi = 0
                sothutu_cambien = 0
                for thietbi, tenphong in nha.items():
                    # print("tên thiết bị "+ thietbi)
                    if isinstance(tenphong, dict):
                        for doituong, dulieu in tenphong.items():                            
                            if doituong == "namethietbi":
                                namethietbi = self.decode_data(dulieu)
                                # print(namethietbi)
                            elif doituong == "phanloai":
                                phanloai =  self.decode_data(dulieu)
                                # print(phanloai)
                        # print (str(phong) + ":"+ str(thietbi)+ ":" + str(namethietbi)+ ":" + str(phanloai) )
                        if phanloai == 'Thiết bị':
                            # phanloai = phanloai + '_TB' +str(sothutu_thietbi)
                            phanloai_id_thietbi =  'TB' +str(sothutu_thietbi)
                            sothutu_thietbi +=1
                        elif phanloai == 'Cảm biến':
                            # phanloai = phanloai + '_CB' +str(sothutu_cambien)
                            phanloai_id_thietbi =  'CB' +str(sothutu_cambien)
                            sothutu_cambien +=1                            
                        curr.execute("INSERT INTO DATA_NODE VALUES (?,?,?,?,?,?,?)",[phong,tenphongsql,thietbi,namethietbi,phanloai,phanloai_id_thietbi,trangthai_active])                                        
                    else:
                        # print("tên phòng:" + tenphong)
                        tenphongsql =  self.decode_data(tenphong)
                        curr.execute("UPDATE DATA_NODE SET NAME_ID_NODE = ? WHERE ID_NODE = ?",[tenphongsql,phong])                                             
                # pass
            else:
                tennhasql= self.decode_data(nha)
                print("nhà" + tennhasql)    
                curr.execute("INSERT INTO CONFIG_GW VALUES (?,?)",["name_nha",tennhasql])                            
        conn.commit()        
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
        kqmahoa = kqmahoa + "_æ_" + str(c) + "_æ_" + str(n)
        return kqmahoa


    def decode_data (self,datas):
        data = str(datas).split("_æ_")
        if len(data)<2:
            return datas
        elif len(data)>2:
            print("data:_æ_")
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
        t1 = Thread(target = self.read_interval())
        t1.start()         
        # nhập id gw, nhấn nút thì đọc từ firebase.
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
        item.setText(_translate("MainWindow", "ID THIẾT BỊ"))
        item = self.table_danhsach.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "NAME THIẾT BỊ"))      
        item = self.table_danhsach.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "PHÂN LOẠI"))

        # self.lab_name_gw.setText(_translate("MainWindow", "    NAME GATEWAY"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_hienthi), _translate("MainWindow", "LIST"))
        self.butt_oke.setText(_translate("MainWindow", "OK"))
        self.butt_ip_socket.setText(_translate("MainWindow", "IP"))
        self.label.setText(_translate("MainWindow", "   ID GATEWAY "))
        self.lab_comport.setText(_translate("MainWindow", "       COM PORT"))
        self.lab_baudrate.setText(_translate("MainWindow", "       BAUD RATE"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_config), _translate("MainWindow", "CONFIG"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
