import select
import socket
import time 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = socket.gethostbyname(socket.gethostname())
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((IP, 8888 ))
s.listen(0)                  
while True:
    # read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    client, addr = s.accept()
    # print (client)
    # print(addr)
    # client.settimeout(5)
    while True:
        content = client.recv(40)
        if len(content) ==0:
           break
        if str(content,'utf-8') == '\r\n':
            continue
        else:
            print(str(content,'utf-8')+'oke')
            # client.send(b'Hello From Python')
    # client.close()