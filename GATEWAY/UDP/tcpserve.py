import threading
import time
import socket
import select
import serial


exitFlag = 0
global flagsenduart 
flagsenduart=0

global serial__ 
global data
data='hi'
# serial__=serial.Serial()
serial_com = input("SELLECT COM: ")
serial__=serial.Serial(serial_com, baudrate=9600 ,timeout=0.1)
HEADER_LENGTH = 40

# IP = "127.0.0.161"
IP = socket.gethostbyname(socket.gethostname())
PORT = 8888

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind, so server informs operating system that it's going to use given IP and port
# For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
server_socket.bind((IP, PORT))

# This makes server listen to new connections
server_socket.listen()

# List of sockets for select.select()
sockets_list = [server_socket]

# List of connected clients - socket as a key, user header and name as data
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

class chaylen (threading.Thread):
    def __init__(self,  threadID, name ):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("Bat dau " + self.name)
        self.readData()

    # def readData():
    #     if serial__.in_waiting >0:
    #         data = serial__.readline()
    #         data = data.decode('utf-8')
    #         print(data)   
    #         data = (data[data.find('LENGHT')+6:data.find('LENGHT')+8])
    #         print(data)   
    def senddata(tt):   
        if (tt==1):
            hello= 'on' + '.'
        else:
            hello='off' + '.'
        serial__.write(hello.encode())       
        print(hello.encode())    
        # read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)    
        # for notified_socket in read_sockets:

        
       
        # pass

       
    def readData(self):
        while True: 
            # print("wait data")
            if serial__.in_waiting >0:
                global data
                data = serial__.readline()
                data = data.decode('utf-8')
                print(data)   

                userheader= f"{len('H'):<{HEADER_LENGTH}}".encode('utf-8')
                userdata= 'H'.encode('utf-8')
                messheader= f"{len(data):<{HEADER_LENGTH}}".encode('utf-8')
                messdata= data.encode('utf-8')
                for client_socket in clients:
                    client_socket.send( userheader + userdata + messheader + messdata)                      
                    
class udp (threading.Thread):
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
            return {'header': message_header, 'data': client_socket.recv(message_length)}

        except:

            # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
            # or just lost his connection
            # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
            # and that's also a cause when we receive an empty message
            return False

    def udp_truyen_nhan(self,receive_message):
        while True:            
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
                        print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                        # Remove from list for socket.socket()
                        sockets_list.remove(notified_socket)

                        # Remove from our list of users
                        del clients[notified_socket]

                        continue

                    # Get user by notified socket, so we will know who sent the message
                    user = clients[notified_socket]

                    print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                    # khi nhan data from udp --> uart
                    hello= message["data"].decode("utf-8") + '.'
                    serial__.write(hello.encode())    
            # It's not really necessary to have this, but will handle some socket exceptions just in case
            for notified_socket in exception_sockets:

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]        
try:
    thread1 = chaylen(1, "Thread-1")
    thread2 = udp(2, "Thread-2")# Bat dau cac thread moi
    thread1.start()
    thread2.start()
    print ("Ket thuc Main Thread")
except:
    print("error")

