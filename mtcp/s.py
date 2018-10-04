import socket
import random
import time
from tools import parse_link_header, make_link_header


HOST = ''
PORT = 10888
MAX_SEQ = 2 ** 32
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

class Server:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.seq = None
        self.server = (self.host,self.port)
        self.sock = self.get_socket(self.host,self.port)
        self.status = 'LISTEN'

    def get_socket(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((HOST, PORT))
        return s

    def make_handshake(self, data):
        self.seq = random.randint(0,2**16) # y
        self.ack = parse_link_header(data)[0] + 1 # x +1
        flag = 3
        return make_link_header(self.seq, self.ack, flag=flag, time_stamp=data[-4:])

    def parse_third_data(self, data):
        res = parse_link_header(data)
        seq,ack = res[0],res[1]
        if seq == self.ack and ack == self.seq + 1:
            return True

    def close1(self,data,addr):
        res = parse_link_header(data)
        self.seq += 1
        self.seq %= MAX_SEQ
        ack = res[0] + 1
        flag = 2
        data = make_link_header(self.seq,ack,flag=flag,time_stamp=data[-4:])
        self.sock.sendto(data,addr)
        self.status = 'CLOSE-WAIT'

        self.seq %= MAX_SEQ
        data = make_link_header(self.seq,ack,flag=6)
        self.sock.sendto(data,addr)
        self.status = 'LAST-ACK'

    def close2(self,data):
        res = parse_link_header(data)
        ack = res[1]
        if ack == self.seq + 1:
            print('close....')
            self.status = 'CLOSED'
            return True

    def main(self):
        while True:
            print(self.status)
            data,addr = self.sock.recvfrom(16)
            status = data[11]
            print(status)
            if status == 1:
                data =self.make_handshake(data)
                self.sock.sendto(data,addr)
                self.status = 'SYNRCVD'
            if status == 2 and self.status == 'SYNRCVD':
                v = self.parse_third_data(data)
                if v:
                    self.status = 'ESTABLISHED'

            if status == 4 and 'ESTABLISHED':
                self.close1(data,addr)

            if status == 2 and self.status == 'LAST-ACK':
                if self.close2(data):
                    break


if __name__ == '__main__':
    s = Server()
    s.main()
