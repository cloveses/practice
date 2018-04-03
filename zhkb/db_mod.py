from pony.orm import *

__author__ = "cloveses"

DB_PARAMS = {
    'provider':'postgres',
    'user':'postgres',
    'password':'123456',
    'host':'localhost',
    'database':'zkbm2018'
}
db = Database()

# 所有转学记录
class StudZhAll(db.Entity):
    gsrid = Optional(str,nullable = True)
    dsrid = Optional(str,nullable = True)
    idcode = Optional(str,nullable = True)
    name = Required(str)
    sex = Required(str)
    birth = Optional(str,nullable = True)
    sch = Required(str)
    zhtype = Required(str)
    optdate = Optional(str,nullable = True)
    zhsrc = Optional(str,nullable = True)
    zhdes = Optional(str,nullable = True)

# 三年级学生记录
class GradeY18(db.Entity):
    sch = Required(str)
    grade = Required(str)
    sclass = Required(str)
    gsrid = Optional(str,nullable = True)
    ssrid = Optional(str,nullable = True)
    dsrid = Optional(str,nullable = True)
    name = Required(str)
    idcode = Optional(str,nullable = True)
    oidcode = Optional(str,nullable = True)
    sex = Required(str)
    outzh = Optional(int,nullable = True) #null 无县外转入记录 1 有县外转学记录 2 有县外转学记录且有县内转学记录
    localzh = Optional(int,nullable = True) # outzh=None localzh=1 有县内转学记录 outzh=None localzh=None 

# 关键信息变更表
class KeyInfoChg(db.Entity):
    ssrid = Optional(str,nullable = True)
    oname = Required(str)
    name = Required(str)
    osex = Required(str)
    sex = Required(str)
    obirth = Required(str)
    birth = Required(str)
    oidcode = Optional(str,nullable = True)
    idcode = Required(str)
    sch = Required(str)
    grade = Required(str)
    sclass = Required(str)
