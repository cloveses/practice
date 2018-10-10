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
        self.data_length = 100
        self.wn_size = 6   #size = 6*data_length
        self.buf = [[],[],[]]
        self.time_out = 2

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

    def deal_buf(self,ack,buf):
        # clear buffer
        for i in len(buf[0]):
            if buf[0][i] < ack:
                buf[0] = buf[0][1:]
                buf[1] = buf[1][1:]
                self.wn_size -= 1

    def send_timeout_data(self):
        t = time.time()
        for index,time_stamp in enumerate(self.buf[2]):
            if t - time_stamp > self.time_out:
                time_data = tools.make_timestamp()
                self.buf[2][i] = time_data[0]
                data_head = tools.make_link_header(self.buf[0][i],pack_len=self.data_length,flag=2,time_stamp=time_data[1])
                data = data_head + self.buf[1][i]
                self.sock.sendto(data,self.server)

    def reset_time_out(self):
        pass
        #添加检验

    def send_file(self):
        with open(self.filename,'rb') as f:
            data = True
            # self.seq = 0
            while data:
                # 接收确认并调整缓存等
                try:
                    data,addr = self.sock.recvfrom(HEAD_LEN)
                except:
                    pass
                else:
                    res = tools.parse_link_header(data)
                    ack = res[1]
                    self.deal_buf(ack,self.buf)

                if len(self.buf[0]) >= self.wn_size :
                    self.send_timeout_data()
                    time.sleep(2)
                    continue

                data = f.read(self.data_length)
                time_data = tools.make_timestamp()
                self.buf[2].append(time_data[0])
                self.buf[0].append(self.seq)
                self.buf[1].append(data)
                data_head = tools.make_link_header(self.seq,pack_len=self.data_length,flag=2,time_stamp=time_data[1])
                data = data_head + data
                self.sock.sendto(data,self.server)
                self.seq += self.data_length


    def main(self):
        self.build_con()
        print(self.status)
        # self.send_file()
        self.release()

if __name__ == '__main__':
    c = Client()
    c.main()
