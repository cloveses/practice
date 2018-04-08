import random,math,itertools
from phdl import *

__author__ = "cloveses"



ROOM_UNIT = 30

# 为所有考生设定随机数，以打乱报名号
@db_session
def set_rand():
    for s in StudPh.select():
        s.sturand = random.random() * 10000



if __name__ == '__main__':
    db.bind(**DB_PARAMS)
    db.generate_mapping(create_tables=True)
    # arrange_room()
