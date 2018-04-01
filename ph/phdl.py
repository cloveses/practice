from pony.orm import *
DB_PARAMS = {
    'provider':'postgres',
    'user':'postgres',
    'password':'123456',
    'host':'localhost',
    'database':'ph18'
}
db = Database()

# class  StudPh(db.Entity):
#     name = Required(str)
#     sa = Optional(int,default=0)
#     sb = Optional(int,default=0)
#     sc = Optional(int,default=0)
#     a = Optional(float)
#     b = Optional(float)
#     c = Optional(float)
#     score = Optional(float)

# class Tssd(db.Entity):
#     name = Required(str)
#     run8 = Optional(int)
#     run10 = Optional(int)
#     ropeskip = Optional(int)
#     longskip = Optional(int)
#     shotput = Optional(int)
#     sitreach = Optional(int)

# class Tssdw(db.Entity):
#     examid = Required(text)
#     name = Required(str)
#     run8 = Optional(int)
#     run10 = Optional(int)
#     ropeskip = Optional(int)
#     longskip = Optional(int)
#     shotput = Optional(int)
#     sitreach = Optional(int)
#     noflag = Optional(bool)

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
# class  StudPh(db.Entity):
#     signid = Required(str)
#     phid = Required(str)
#     name = Required(str)
#     sex = Required(str)
#     sch = Required(str)
#     free_flag = Required(bool,sql_default=False)
#     # 选项
#     jump_option = Optional(int)
#     rope_option = Optional(int)
#     globe_option = Optional(int)
#     bend_option = Optional(int)
#     # 测试数据
#     run = Optional(int)
#     jump = Optional(int)
#     skill = Optional(int)
#     # 测试成绩
#     run_score = Optional(int)
#     jump_score = Optional(int)
#     skill_score = Optional(int)
#     total_score = Optional(int)

#     memo = Optional(str)

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
    schseq = Optional(int)
    signid = Required(str)
    phid = Required(str)
    name = Required(str)
    jump_option = Required(int,sql_default=0)
    rope_option = Required(int,sql_default=0)
    globe_option = Required(int,sql_default=0)
    bend_option = Required(int,sql_default=0)

db.bind(**DB_PARAMS)
db.generate_mapping(create_tables=True)
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
    print(score_run_man(800))
    print(score_run_woman(500))
    print(score_globe_man(323))
    print(score_bend_woman(8))