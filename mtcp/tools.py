import time

def parse_link_header(data):
    '''解析三次握手数据包head'''
    seq = int.from_bytes(data[:4], byteorder='big')
    ack = int.from_bytes(data[4:8], byteorder='big')
    pack_len = int.from_bytes(data[8:11], byteorder='big')
    pack_second = data[12]
    pack_msecond = int.from_bytes(data[13:], byteorder='big')
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
    return b''.join(datas)



