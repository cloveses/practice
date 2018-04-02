import csv
from pony.orm import *

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
    localzh = Optional(int,nullable = True) # 1 有县内转学记录

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

# # \copy gradey18 (sch,grade,sclass,gsrid,ssrid,dsrid,name,idcode,sex) from g:\grade32018\grade183.csv with csv

# #  \copy studzhall (gsrid,dsrid,idcode,name,sex,birth,sch,zhtype,optdate,zhsrc,zhdes) from 1516zh.csv with csv

# #  \copy studzhall (gsrid,dsrid,idcode,name,sex,birth,sch,zhtype,optdate,zhsrc,zhdes) from 1617zh.csv with csv

# #  \copy studzhall (gsrid,dsrid,idcode,name,sex,birth,sch,zhtype,optdate,zhsrc,zhdes) from 1718zh.csv with csv

# # delete from studzhall where zhtype='跨省就学转学(入)';

# # select distinct(zhtype) from studzhall;

# # 转学后修改了身份证
# # select sch,name,idcode from studzhall where (sch,name) in (select sch,name from gradey18) and idcode not in (select idcode from gradey18);


def save_datas_xlsx(filename,datas):
    #将一张表的信息写入电子表格中XLSX文件格式
    import xlsxwriter
    w = xlsxwriter.Workbook(filename)
    w_sheet = w.add_worksheet('sheet1')
    for rowi,row in enumerate(datas):
        for coli,celld in enumerate(row):
            w_sheet.write(rowi,coli,celld)
    w.close()


def is_out(zh_data):
    """判别是否有县外转学记录"""
    out_flags = ('市内转','跨市转','跨省转','跨境转')
    for zh in zh_data:
        for out_flag in out_flags:
            if zh.zhtype and zh.zhtype.startswith(out_flag):
                return True

def has_local(zh_data):
    """判别是否有县内转学记录"""
    zh_data = [zh.zhtype for zh in zh_data]
    for zh in zh_data:
        if zh.zhtype and zh.startswith('县区内转'):
            return True

# 清除小学和高中学籍变动
@db_session
def clear_studzhall():
    for zh_stud in select(s for s in StudZhAll):

        if zh_stud.zhsrc and ('小学' in zh_stud.zhsrc or '高中' in zh_stud.zhsrc):
            zh_stud.delete()
        if zh_stud.zhdes and ('高中' in zh_stud.zhdes or '小学' in zh_stud.zhdes):
            zh_stud.delete()

@db_session
def clear_keyinfo():
    for keyinfo in select(s for s in KeyInfoChg):
        if '小学' in keyinfo.grade:
            keyinfo.delete()

@db_session
def insert_oidcode():
    for keyinfo in select(s for s in KeyInfoChg):
        if keyinfo.oidcode and keyinfo.oidcode != keyinfo.idcode:
            if count(select(s for s in GradeY18 if s.idcode == keyinfo.idcode)) == 1:
                stud = select(s for s in GradeY18 if s.idcode == keyinfo.idcode).first()
                stud.oidcode = keyinfo.oidcode

@db_session
def set_zh_from_out():
    for stud in select(s for s in GradeY18):
        zh_recos = []
        if stud.idcode:
            zhs = select(zh for zh in StudZhAll 
                if zh.idcode == stud.idcode)[:]
            if zhs:
                zh_recos.extend(zhs)
            if stud.oidcode:
                zhs = select(zh for zh in StudZhAll
                    if zh.idcode == stud.oidcode)[:]
                if zhs:
                    zh_recos.extend(zhs)
        else:
            print(stud.name,stud.sch,'No id number!')

        zhs = select(zh for zh in StudZhAll 
            if zh.gsrid == stud.gsrid)[:]
        if zhs:
            zh_recos.extend(zhs)

        zh_recos = set(zh_recos)
        if zh_recos and is_out(zh_recos):
            stud.outzh = 1


# @db_session
# def test():
#     for stud in select(s for s in GradeY18):
#         zh_recos = select(zh for zh in StudZhAll if zh.gsrid == stud.gsrid)
#         for zh_reco in zh_recos:
#             if stud.dsrid != zh_reco.dsrid:
#                 print('地区学号不同:')
#                 print(stud.name,stud.sch,stud.idcode,stud.dsrid)
#                 print(zh_reco.name,zh_reco.sch,zh_reco.idcode,zh_reco.dsrid)


# @db_session
# def test2():
#     for keyinfo in select(s for s in KeyInfoChg):
#         studs = select(s for s in GradeY18 if s.idcode == keyinfo.idcode)
#         for stud in studs:
#             if stud.ssrid != keyinfo.ssrid:
#                 print(stud.name,stud.sch,stud.ssrid,stud.idcode)
#                 print(keyinfo.name,keyinfo.sch,keyinfo.ssrid,keyinfo.idcode)


# # 依据身份证号分拣出跨省市县转学
# @db_session
# def get_reg_data():
#     for stud in GradeY18.select():
#         if stud.idcode:
#             zh_data = select(zh for zh in StudZhAll if zh.idcode==stud.idcode 
#                 and ('初中' in zh.zhsrc or '初中' in zh.zhdes))[:]
#             if zh_data and is_out(zh_data):
#                 stud.outzh = 1
#         else:
#             # 无身份证号，暂放无县外转入记录
#             print(stud.sch,stud.name,stud.gsrid,'No id number!')


# # 用姓名的唯一性或姓名+学校作为关键字来判别无身份证号或修改过身份证号学生转学情况
# @db_session
# def check_regdata_name_sch():
#     nooutstuds = select(s.name for s in GradeY18 if s.outzh==None)
#     # 用姓名+学校判别
#     pre_datas = []
#     for nooutstud in nooutstuds:
#         cur_zh_datas = select(s for s in StudZhAll 
#             if s.name==nooutstud and ('初中' in s.zhsrc or '初中' in s.zhdes))[:]
#         if cur_zh_datas and is_out(cur_zh_datas):
#             studs = select(s for s in GradeY18 if s.name==nooutstud and s.outzh == None)[:]
#             pre_datas.append((studs,cur_zh_datas))
#     stud_datas = []
#     zh_datas = []
#     for studs,cur_zh_datas in pre_datas:
#         for stud in studs:
#             # print(stud.to_dict())
#             stud_datas.append(list(stud.to_dict().values()))
#         for cur_zh_data in cur_zh_datas:
#             # print(cur_zh_data.to_dict())
#             zh_datas.append(list(cur_zh_data.to_dict().values()))
#     save_datas_xlsx('待核查县外转学生名单.xlsx',stud_datas)
#     save_datas_xlsx('待核查县外转学数据.xlsx',zh_datas)


# # 依据身份证号从OutZh表分拣出跨省市县转学，又进行了县内转学的学生
# @db_session
# def get_out_local():
#     for out_stud in GradeY18.select(lambda s:s.outzh==1):
#         if out_stud.idcode:
#             zh_data = select(zh for zh in StudZhAll if zh.idcode==out_stud.idcode 
#                 and ('初中' in zh.zhsrc or '初中' in zh.zhdes))[:]
#             # print(zh_data)
#             if zh_data and has_local(zh_data):
#                 out_stud.outzh = 2
#         else:
#             # 无身份证号，不做操作，暂放无县内转入记录
#             print(stud.sch,stud.name,stud.gsrid,'No id number!')

# # 依据姓名查找需要核对的有县外转学记录，又有县内转学记录的
# @db_session
# def get_out_local_by_name():
#     need_person_checks = []
#     for stud_name in select(s.name for s in GradeY18 if s.outzh == 1):
#         zh_datas = select(zh for zh in StudZhAll if zh.name == stud_name 
#             and ('初中' in zh.zhsrc or '初中' in zh.zhdes))[:]
#         if zh_datas and has_local(zh_datas):
#             studs = select(s for s in GradeY18 if s.outzh == 1 and s.name == stud_name)[:]
#             need_person_checks.append((studs,zh_datas))
#     stud_datas = []
#     zh_datas = []
#     for studs,zhs in need_person_checks:
#         for stud in studs:
#             stud_datas.append(list(stud.to_dict().values()))
#         for zh in zhs:
#             zh_datas.append(list(zh.to_dict().values()))
#     save_datas_xlsx('待核查县外且县内转学生名单.xlsx',stud_datas)
#     save_datas_xlsx('待核查县外且县内转学数据.xlsx',zh_datas)


# # 依据身份证从无县外转学记录表（NoOutZh）中分拣出有县内转学记录LocalZh和无县内转学记录NoZh
# @db_session
# def get_localzh_or_not():
#     for stud in GradeY18.select(lambda s:s.outzh==None):
#         if stud.idcode:
#             zh_data = select(zh for zh in StudZhAll if zh.idcode==stud.idcode 
#                 and ('初中' in zh.zhsrc or '初中' in zh.zhdes))[:]
#             if zh_data and has_local(zh_data):
#                 # print(zh_data)
#                 stud.localzh = 1
#         else:
#             # 无身份证号，暂放无县内转学记录
#             print(stud.sch,stud.name,stud.gsrid,'No id number!')


# # # 用姓名作为关键字来收集无身份证号或修改过身份证号（NoZh)学生有无县内转学情况供核对
# @db_session
# def check_localzh_name_sch():
#     need_person_checks = []
#     for stud_name in select(s.name for s in GradeY18 if s.localzh == None):
#         zh_datas = select(zh for zh in StudZhAll 
#             if zh.name==stud_name and ('初中' in zh.zhsrc or '初中' in zh.zhdes))[:]
#         if zh_datas and has_local(zh_datas):
#             studs = select(s for s in GradeY18 if s.name==stud_name and s.localzh==None)[:]
#             need_person_checks.append((studs,zh_datas))
#     stud_datas = []
#     zh_datas = []
#     for studs,zhs in need_person_checks:
#         for stud in studs:
#             stud_datas.append(list(stud.to_dict().values()))
#         for zh in zhs:
#             zh_datas.append(list(zh.to_dict().values()))
#     save_datas_xlsx('待核查县内转学生名单.xlsx',stud_datas)
#     save_datas_xlsx('待核查县内转学数据.xlsx',zh_datas)



# 将数据导出为excel
@db_session
def get_sch_data_xls():
    # schs = select(s.sch for s in GradeY18)

    # # 导出各校无从县外转入的应届生（从各校报名）,每学校一个文件
    # for sch in schs:
    #     datas = [['学校','年级','班级','全国学籍号','学籍号','地区学号','姓名','身份证号','性别'],]
    #     query = select([s.sch,s.grade,s.sclass,s.gsrid,s.ssrid,s.dsrid,s.name,s.idcode,s.sex] 
    #         for s in GradeY18 if s.sch == sch and s.outzh == None)[:]
    #     datas.extend(query)
    #     save_datas_xlsx('.'.join((sch,'xlsx')),datas)
    #     print(count(select(s for s in GradeY18 if s.sch == sch and s.outzh == None)),sch)

    # 导出所有学校有县外转入记录的应届生（从招办报名）
    datas = [['学校','年级','班级','全国学籍号','学籍号','地区学号','姓名','身份证号','性别'],]
    query = select([s.sch,s.grade,s.sclass,s.gsrid,s.ssrid,s.dsrid,s.name,s.idcode,s.sex] 
        for s in GradeY18 if s.outzh != None)[:]
    datas.extend(query)
    save_datas_xlsx('.'.join(('招办报名名单','xlsx')),datas)
    print('招办报名人数：',count(select(s for s in GradeY18 if s.outzh != None)))

    # # 导出从各校报名的总名单
    # datas = [['学校','年级','班级','全国学籍号','学籍号','地区学号','姓名','身份证号','性别'],]
    # query = select(s for s in GradeY18 if s.outzh == None).order_by(GradeY18.sch)
    # for s in query:
    #     datas.append([s.sch,s.grade,s.sclass,s.gsrid,s.ssrid,s.dsrid,s.name,s.idcode,s.sex])
    # save_datas_xlsx('.'.join(('各校报名总名单','xlsx')),datas)
    # print('各校报名总人数：',count(select(s for s in GradeY18 if s.outzh == None)))


if __name__ == '__main__':
    db.bind(**DB_PARAMS)
    db.generate_mapping(create_tables=True)

    # clear_studzhall()
    # clear_keyinfo()
    # insert_oidcode()
    set_zh_from_out()
    # get_reg_data()
    # check_regdata_name_sch()
    # get_out_local()
    # get_out_local_by_name()
    # get_localzh_or_not()
    # check_localzh_name_sch()
    # get_sch_data_xls()