import random,math,itertools
from pony.orm import *

__author__ = "cloveses"

DB_PARAMS = {
    'provider':'postgres',
    'user':'postgres',
    'password':'123456',
    'host':'localhost',
    'database':'test'
}
db = Database()

class  StudArrg(db.Entity):
    signid = Required(str)
    name = Required(str)
    schcode = Required(str)
    sch = Required(str)
    sch_seq = Optional(int)
    room_code = Optional(int)
    number = Optional(int)
    sturand = Optional(float)

db.bind(**DB_PARAMS)
db.generate_mapping(create_tables=True)

ROOM_UNIT = 30

# 为所有考生设定随机数，以打乱报名号
@db_session
def set_rand():
    for s in StudArrg.select():
        s.sturand = random.random() * 10000

# 查询获取考生数、计算考场数、尾场人数、各报名学校人数
@db_session
def get_sch_data(room_unit=ROOM_UNIT):
    totals = count(StudArrg.select())
    rooms = math.ceil(totals / room_unit)
    tails = totals % room_unit
    sch_data = select((s.schcode,count(s.name)) for s in StudArrg)[:]
    sch_data.sort(key=lambda s:s[1],reverse=True)
    return (rooms,tails),sch_data

# 为报名学生设置序号（报名人数较多优先排定,让学生均匀分布各考场）
@db_session
def set_sch_seq(sch_seq):
    for index,sch in enumerate(sch_seq):
        for s in select(s for s in StudArrg if s.schcode == sch[0]):
            s.sch_seq = index

# 安排考生的考场和座位号
@db_session
def arrange_room():
    rooms,sch_data = get_sch_data()
    set_rand()
    set_sch_seq(sch_data)
    # print(rooms)
    totals,tails = rooms
    # 安排定考室
    for i in range(tails):
        rc = 0
        while True:
            stud = StudArrg.select(lambda s:s.room_code <= 0 or s.room_code is None).order_by(StudArrg.sturand).order_by(StudArrg.sch_seq).first()
            if stud:
                stud.room_code = rc + 1
                rc += 1
            if rc >= totals:
                break
    totals -= 1 ## 去除尾场考生安排
    for i in range(ROOM_UNIT - tails):
        rc = 0
        while True:
            stud = StudArrg.select(lambda s:s.room_code <= 0 or s.room_code is None).order_by(StudArrg.sturand).order_by(StudArrg.sch_seq).first()
            if stud:
                stud.room_code = rc + 1
                rc += 1
            if rc >= totals:
                break
    # 排定座位号
    for i in range(totals):
        arrange_seat(i+1)

# 排定一场座位号（考点学生从多到少排列后确定）
@db_session
def arrange_seat(roomth):
    studs = StudArrg.select(lambda s:s.room_code == roomth)[:]
    schs = [s.schcode for s in studs]
    sch_num_dict = {sch:schs.count(sch) for sch in schs}
    studs.sort(key=lambda s:sch_num_dict[s.schcode],reverse=True)
    half = math.ceil(len(studs) / 2)
    res = []
    for x,y in itertools.zip_longest(studs[:half],studs[half:]):
        res.extend([x,y])
    if not res[-1]:
        res = res[:len(res) - 1]
    for i,s in enumerate(res):
        s.number = i + 1

if __name__ == '__main__':
    arrange_room()
