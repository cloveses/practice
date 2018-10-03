import socket

HOST = ''
PORT = 10888
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.bind((HOST, PORT))
# data = True
# while data:
#     data,address = s.recvfrom(1024)
#     if data==b'bye':
#         break
#     print('Received String:',data.decode('utf-8'))
#     s.sendto(data,address)
# s.close()

WORK_STATUS = None

def get_socket(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    return s

def make_handshake(data,s):
    

def get_head(s):
    while True:
        data,addr = s.recvfrom(16)
        status = data[11]
        status = int.from_bytes(status,,byteorder = 'big')
        if status == 1:
            make_handshake(data,s)