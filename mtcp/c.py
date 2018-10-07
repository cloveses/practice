import random
import time
import socket
from tools import parse_link_header, make_link_header


HOST = 'localhost'
PORT = 10888
MAX_SEQ = 2 ** 32
HEAD_LEN = 20

class Client:

    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.server = (self.host,self.port)
        self.seq = None
        self.sock = self.get_socket()
        self.status = 'CLOSED'
        self.data_length = 0
        self.wn_size = 600
        self.bufed_size = 0
        self.buf = []

    def get_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return s

    def make_start_head(self):
        self.seq = random.randint(0,2**16) # x
        flag = 1
        return make_link_header(self.seq, flag=flag)

    def parse_ack_data(self,data):
        seq,ack,pack_len,ts = parse_link_header(data)
        seq += 1
        if ack  == self.seq + 1 and data[11] == 3:
            flag = 2
            return make_link_header(ack,seq,flag=2)
            
    def deal_fin1(self,data):
        res = parse_link_header(data)
        self.ack = res[1]
        if self.ack == self.seq + 1 and data[11] == 1:
            return True

    def deal_fin2(self,data):
        res = parse_link_header(data)
        seq,ack = res[0],res[1]
        if ack == self.ack and data[11] == 6:
            return make_link_header(ack, seq+1, flag=2, time_stamp=data[-8:-4])

    def build_con(self):
        self.sock.sendto(self.make_start_head(),self.server)
        self.status = 'SYN-SENT'
        data,addr = self.sock.recvfrom(HEAD_LEN)
        data = self.parse_ack_data(data)
        if data:
            self.sock.sendto(data,addr)
            self.status = 'ESTABLISHED'

    def release(self):
        self.seq += 1
        self.seq %= MAX_SEQ
        data = make_link_header(self.seq, flag=4)
        self.sock.sendto(data,self.server)
        self.status = 'FIN-WAIT-1'

        data,addr = self.sock.recvfrom(HEAD_LEN)
        if self.deal_fin1(data):
            self.status = 'FIN-WAIT-2'
        #  关闭连接第二阶段
        data,addr = self.sock.recvfrom(HEAD_LEN)
        data = self.deal_fin2(data)
        if data:
            self.sock.sendto(data,self.server)
            self.status = 'TIME-WAIT'

    def send_file(self):
        with open(self.filename,'rb') as f:
            data = True
            self.seq = 0
            while data:
                pass #接收确认并调整缓存等
                if self.bufed_size + self.data_length > self.wn_size:
                    time.sleep(2)
                    continue

                data = f.read(self.data_length)
                self.buf.append((self.seq,data))
                pass #发送
                self.bufed_size += self.data_length


    def main(self):
        self.build_con()
        print(self.status)
        # self.send_file()
        self.release()

if __name__ == '__main__':
    c = Client()
    c.main()
