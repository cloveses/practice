import random
import time
import socket

HOST = 'localhost'
PORT = 10888
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# data = "你好！"
# while data:
#     s.sendto(data.encode('utf-8'),(HOST,PORT))
#     if data=='bye':
#         break
#     data,addr = s.recvfrom(512)
#     print("Receive from server:\n",data.decode('utf-8'))
#     data = input('please input a info:\n')
# s.close()

def get_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return s

def make_start_head():
    seq = random.randint(0,2**16)
    seq = seq.to_bytes(4,byteorder = 'big')
    ack = bytearray(4)
    trd = (1).to_bytes(4,byteorder = 'big')
    ts = time.time()
    seconds = int(ts) % (2 ** 8)
    seconds = seconds.to_bytes(1,byteorder = 'big')
    ms = int(str(ts)[str(ts).index('.')+1:])
    ms = ms.to_bytes(3,byteorder = 'big')
    return b''.join((seq,ack,trd,seconds,ms))
