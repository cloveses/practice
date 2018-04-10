import random,math,itertools
from phdl import *
from booktab_sets import arrange_datas

__author__ = "cloveses"



UNITS = 30

# 为所有考生设定随机数，以打乱报名号
@db_session
def set_rand():
    for s in StudPh.select(): 
        s.sturand = random.random() * 10000

@db_session
def arrange_phid():
    prefix = 1822250000
    phid = 1
    for arrange_data in arrange_datas:
        if len(arrange_data) == 4:
            studs = select(s for s in StudPh if s.sch in arrange_data[-2] and 
                sex == arrange_data[-1])
        else: ## len(arrange_data) == 3
            studs = select(s for s in StudPh if s.sch in arrange_data[-1]).order_by(StudPh.sex)
        for stud in studs:
            stud.exam_addr = arrange_data[0]
            stud.exam_date = arrange_data[1]
            stud.phid = phid
            phid +=1


if __name__ == '__main__':
    db.bind(**DB_PARAMS)
    db.generate_mapping(create_tables=True)
