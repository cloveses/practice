import time
import struct

def parse_link_header(data):
    '''解析三次握手数据包head'''
    seq = int.from_bytes(data[:4], byteorder='big')
    ack = int.from_bytes(data[4:8], byteorder='big')
    pack_len = int.from_bytes(data[8:11], byteorder='big')
    pack_second = data[12]
    pack_msecond = int.from_bytes(data[13:16], byteorder='big')
    return(seq,ack,pack_len,(pack_second,pack_msecond))

def make_link_header(seq, ack=0, pack_len=0, flag=0, time_stamp=None):
    '''构造数据包head'''
    datas = []
    seq = seq.to_bytes(4, byteorder='big')
    ack = ack.to_bytes(4, byteorder='big')
    pack_len = pack_len.to_bytes(3, byteorder='big')
    flag = flag.to_bytes(1, byteorder='big')
    datas.extend((seq, ack, pack_len, flag))
    if time_stamp is None:
        ts = time.time()
        seconds = int(ts) % (2 ** 8)
        seconds = seconds.to_bytes(1,byteorder = 'big')
        ms = int(str(ts)[str(ts).index('.')+1:])
        ms = ms.to_bytes(3,byteorder = 'big')
        datas.extend((seconds, ms))
    else:
        datas.append(time_stamp)
    checksum = 0
    checksum = checksum.to_bytes(2,byteorder='big')
    w_size = 1024
    w_size = w_size.to_bytes(2,byteorder='big')
    datas.append(checksum)
    datas.append(w_size)
    return b''.join(datas)

def loop_add(checksum):
    while True:
        if (checksum >> 16) == 0:
            break
        checksum = (checksum >> 16) + (checksum&0xffff)
    return checksum


def get_checksum(IP_head):
    checksum = 0
    headlen = len(IP_head)
    i=0
    while i<headlen:
        temp = struct.unpack('!H',IP_head[i:i+2])[0]
        checksum = checksum+temp
        i = i+2
    checksum = 65535 - loop_add(checksum)
    return struct.pack('!H',checksum)

# if __name__ == '__main__':
#     import random
#     random.seed(50)
#     data = [random.randint(0,256) for i in range(50)]
#     data.extend((0,0))
#     datab = bytearray(data)
#     print(data,'\n',datab)
#     ret = get_checksum(datab)
#     print(ret)
#     datac = datab[:-2] + ret
#     print(datac)
#     print(get_checksum(datac))
