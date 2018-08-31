import os
import fileinput
from m import *

@db_session
def get_data(filename):
    i = 0
    seq = 0
    for line in fileinput.input(filename):
        if i < 9:
            i += 1
            continue
        group = line.split(' ')
        if not (group[0]).strip().isdigit():
            i = 1
            seq += 1
        else:
            group = int(group[0])
            Data(group=group,seq=seq,mdata=line)

@db_session
def verify(filename):
    max_seq = max(d.seq for d in Data)
    with open(filename,'wt') as f:
        for i in range(max_seq+1):
            datas = select(d for d in Data if d.seq == i).order_by(Data.group)
            for data in datas:
                # f.write(data.mdata)
                f.write(data.mdata[data.mdata.index(' ')+1:])
                f.write('\n')

if __name__ == '__main__':
    # get_data('dumpnew.atom')
    verify('myt.txt')