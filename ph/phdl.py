from pony.orm import *

DB_PARAMS = {
    'provider':'postgres',
    'user':'postgres',
    'password':'123456',
    'host':'localhost',
    'database':'ph18'
}

db = Database()

# 跑步评分标准
class RunLvl(db.Entity):
    score = Required(int)
    run_man = Required(int)
    run_woman = Required(int)

# 其它评分标准
class SkilLvl(db.Entity):
    score = Required(int)
    globe_man = Required(int)
    globe_woman = Required(int)
    jump_man = Required(int)
    jump_woman = Required(int)
    rope_man = Required(int)
    rope_woman = Required(int)
    bend_man = Required(int)
    bend_woman = Required(int)

# 体育成绩总表
class  StudPh(db.Entity):
    signid = Required(str)
    phid = Optional(str,nullable = True)
    name = Required(str)
    sex = Required(str)
    idcode = Required(str)
    sch = Required(str)
    schcode = Required(str)
    # 用于乱序
    sturand = Optional(float,nullable = True)
    # 免考标志
    free_flag = Optional(bool,nullable = True)
    # 选项
    jump_option = Optional(int,nullable = True)
    rope_option = Optional(int,nullable = True)
    globe_option = Optional(int,nullable = True)
    bend_option = Optional(int,nullable = True)
    # 测试数据
    run = Optional(int,nullable = True)
    jump = Optional(int,nullable = True)
    skill = Optional(int,nullable = True)
    # 测试成绩
    run_score = Optional(int,nullable = True)
    jump_score = Optional(int,nullable = True)
    skill_score = Optional(int,nullable = True)
    total_score = Optional(int,nullable = True)

    memo = Optional(str,nullable = True)


# 免考申请表 附件5
class FreeExam(db.Entity):
    schseq = Optional(int)
    signid = Required(str)
    phid = Required(str)
    name = Required(str)
    reason = Required(str)
    material = Required(str)
    memo = Optional(str)

# 选考项目确认表 附件6
class ItemSelect(db.Entity):
    schseq = Optional(int,nullable = True)
    signid = Required(str)
    phid = Required(str)
    name = Required(str)
    jump_option = Optional(int,default=0)
    rope_option = Optional(int,default=0)
    globe_option = Optional(int,default=0)
    bend_option = Optional(int,default=0)

# with db_session:
#     for p in select(p for p in Tssd):
#         print(p.name)
#         if not((p.run8 or p.run10) and (p.ropeskip or p.longskip) and
#                     (p.shotput or p.sitreach)):
#             print(p.name,'error!')

def score_run_man(time):
    with db_session:
        ret = select(r.score for r in RunLvl if r.run_man >= time).max()
    return 0 if ret is None  else ret

def score_run_woman(time):
    with db_session:
        ret = select(r.score for r in RunLvl if r.run_woman >= time).max()
    return 0 if ret is None  else ret

def score_globe_man(long):
    with db_session:
        ret = select(r.score for r in SkilLvl if r.globe_man <= long).max()
    return 0 if ret is None  else ret

def score_globe_woman(long):
    with db_session:
        ret = select(r.score for r in SkilLvl if r.globe_woman <= long).max()
    return 0 if ret is None  else ret

def score_jump_man(long):
    with db_session:
        ret = select(r.score for r in SkilLvl if r.jump_man <= long).max()
    return 0 if ret is None  else ret

def score_jump_woman(long):
    with db_session:
        ret = select(r.score for r in SkilLvl if r.jump_woman <= long).max()
    return 0 if ret is None  else ret

def score_rope_man(long):
    with db_session:
        ret = select(r.score for r in SkilLvl if r.rope_man <= long).max()
    return 0 if ret is None  else ret

def score_rope_woman(long):
    with db_session:
        ret = select(r.score for r in SkilLvl if r.rope_woman <= long).max()
    return 0 if ret is None  else ret

def score_bend_man(long):
    with db_session:
        ret = select(r.score for r in SkilLvl if r.bend_man <= long).max()
    return 0 if ret is None  else ret

def score_bend_woman(long):
    with db_session:
        ret = select(r.score for r in SkilLvl if r.bend_woman <= long).max()
    return 0 if ret is None  else ret

if __name__ == '__main__':
    db.bind(**DB_PARAMS)
    db.generate_mapping(create_tables=True)
    print(score_run_man(800))
    print(score_run_woman(500))
    print(score_globe_man(323))
    print(score_bend_woman(8))