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
    sex = Required(str)
    outzh = Optional(int,nullable = True) #null 无县外转入记录 1 有县外转学记录 2 有县外转学记录且有县内转学记录
    localzh = Optional(int,nullable = True) # 1 有县内转学记录

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
            if zh.startswith(out_flag):
                return True

def has_local(zh_data):
    """判别是否有县内转学记录"""
    for zh in zh_data:
        if zh.startswith('县区内转'):
            return True

# 依据身份证号分拣出跨省市县转学
@db_session
def get_reg_data():
    for stud in GradeY18.select():
        if stud.idcode:
            zh_data = select(s.zhtype for s in StudZhAll if s.idcode==stud.idcode  and ('初中' in s.zhsrc or '初中' in s.zhdes))[:]
            if zh_data and is_out(zh_data):
                # print(zh_data)
                stud.outzh = 1
        else:
            # 无身份证号，暂放无县外转入记录
            print(stud.sch,stud.name,stud.gsrid,'No id number!')

# # 用姓名的唯一性或姓名+学校作为关键字来判别无身份证号或修改过身份证号学生转学情况
# @db_session
# def check_regdata_name_sch():
#     nooutstuds = GradeY18.select(lambda s:s.outzh==None)
#     # 用姓名+学校判别
#     for nooutstud in nooutstuds:
#         has_zhs = select(s.zhtype for s in StudZhAll 
#             if s.name==nooutstud.name and s.sch==nooutstud.sch  and ('初中' in s.zhsrc or '初中' in s.zhdes))[:]
#         if has_zhs and is_out(has_zhs):
#             if count(select(s for s in GradeY18 if s.name==nooutstud.name and s.sch==nooutstud.sch)) >= 2:
#                 print(nooutstud.name,nooutstud.sch,"Needs person check!")
#             else:
#                 print('Move a stud from NoOutZh to OutZh:',nooutstud.name,nooutstud.sch)
#                 nooutstud.outzh =1


# 依据身份证号从OutZh表分拣出跨省市县转学，又进行了县内转学的学生
@db_session
def get_out_local():
    for out_stud in GradeY18.select(lambda s:s.outzh==1):
        if out_stud.idcode:
            zh_data = select(s.zhtype for s in StudZhAll 
                if s.idcode==out_stud.idcode)[:]
            # print(zh_data)
            if has_local(zh_data):
                out_stud.outzh = 2
        else:
            # 无身份证号，不做操作，暂放无县内转入记录
            print(stud.sch,stud.name,stud.gsrid,'No id number!')

# # 依据姓名+学校查找有县外转学记录，又有县内转学记录的
# @db_session
# def get_out_local_by_name():
#     for out_stud in GradeY18.select(lambda s:s.outzh==1):
#         has_zhs = select(s.zhtype for s in StudZhAll 
#             if s.name==out_stud.name and ('初中' in s.zhsrc or '初中' in s.zhdes))[:]
#         if out_stud.name == '田高':
#             print('tg',has_zhs)
#         if has_zhs and has_local(has_zhs):
#             print(has_zhs,out_stud.name,out_stud.sch)
#             if count(select(s for s in GradeY18 if s.name==out_stud.name)) >= 2:
#                 print(out_stud.name,out_stud.sch,"Needs person check!")
#             else:
#                 print('Move a stud from OutZh to OutZhLocal:',out_stud.name,out_stud.sch)
#                 out_stud.outzh = 2


# 依据身份证从无县外转学记录表（NoOutZh）中分拣出有县内转学记录LocalZh和无县内转学记录NoZh
@db_session
def get_localzh_or_not():
    for stud in GradeY18.select(lambda s:s.outzh==None):
        if stud.idcode:
            zh_data = select(s.zhtype for s in StudZhAll if s.idcode==stud.idcode)[:]
            if zh_data:
                # print(zh_data)
                stud.localzh = 1
        else:
            # 无身份证号，暂放无县内转学记录
            print(stud.sch,stud.name,stud.gsrid,'No id number!')


# # # 用姓名+学校作为关键字来判别无身份证号或修改过身份证号（NoZh)学生有无县内转学情况
# @db_session
# def check_localzh_name_sch():
#     need_person_checks = []
#     for nozhstud in GradeY18.select(lambda s:s.localzh==None):
#         has_zhs = select(s.zhtype for s in StudZhAll 
#             if s.name==nozhstud.name and s.sch==nozhstud.sch)[:]
#         if has_zhs:
#             if count(select(s for s in GradeY18 if s.name==nozhstud.name and s.sch==nozhstud.sch and s.localzh==None)) >= 2:
#                 print(nozhstud.name,nozhstud.sch,"Needs person check!")
#                 need_person_checks.append(nozhstud)
#             else:
#                 print('Move a stud from NoZh to LocalZh:',nozhstud.name,nozhstud.sch)
#                 nozhstud.localzh = 1
    # print("The following data need to be examined manually...")
    # for nozhstud in need_person_checks:
    #     for zh_info in select(s for s in StudZhAll if s.name==nozhstud.name and s.sch==nozhstud.sch):
    #         print('Stud info:')
    #         print(nozhstud.to_dict())
    #         print('Zh info:')
    #         print(zh_info.to_dict())
    # zh_records = []
    # stud_check = []
    # zh_keys = ('gsrid','dsrid','idcode','name','sex','birth','sch','zhtype','optdate','zhsrc','zhdes')
    # stud_keys = ('sch','grade','sclass','gsrid','ssrid','dsrid','name','idcode','sex')
    # for nozhstud in need_person_checks:
    #     nozhstud_dict = nozhstud.to_dict()
    #     stud_check.append([nozhstud_dict[i] for i in stud_keys])
    #     for zh_info in select(s for s in StudZhAll if s.name==nozhstud.name and s.sch==nozhstud.sch):
    #         info_dict = zh_info.to_dict()
    #         zh_records.append([info_dict[i] for i in zh_keys])
    # save_datas_xlsx('待检查的转学记录.xlsx',zh_records)
    # save_datas_xlsx('待检查的学生信息.xlsx',stud_check)



# 将数据导出为excel
@db_session
def get_sch_data_xls():
    schs = select(s.sch for s in GradeY18)

    # 导出各校无从县外转入的应届生（从各校报名）,每学校一个文件
    for sch in schs:
        datas = [['学校','年级','班级','全国学籍号','学籍号','地区学号','姓名','身份证号','性别'],]
        query = select([s.sch,s.grade,s.sclass,s.gsrid,s.ssrid,s.dsrid,s.name,s.idcode,s.sex] 
            for s in GradeY18 if s.sch == sch and s.outzh == None)[:]
        datas.extend(query)
        save_datas_xlsx('.'.join((sch,'xlsx')),datas)
        print(count(select(s for s in GradeY18 if s.sch == sch and s.outzh == None)),sch)

    # 导出所有学校有县外转入记录的应届生（从招办报名）
    datas = [['学校','年级','班级','全国学籍号','学籍号','地区学号','姓名','身份证号','性别'],]
    query = select([s.sch,s.grade,s.sclass,s.gsrid,s.ssrid,s.dsrid,s.name,s.idcode,s.sex] 
        for s in GradeY18 if s.outzh != None)[:]
    datas.extend(query)
    save_datas_xlsx('.'.join(('招办报名名单','xlsx')),datas)
    print('招办报名人数：',count(select(s for s in GradeY18 if s.outzh != None)))

    # 导出从各校报名的总名单
    datas = [['学校','年级','班级','全国学籍号','学籍号','地区学号','姓名','身份证号','性别'],]
    query = select(s for s in GradeY18 if s.outzh == None).order_by(GradeY18.sch)
    for s in query:
        datas.append([s.sch,s.grade,s.sclass,s.gsrid,s.ssrid,s.dsrid,s.name,s.idcode,s.sex])
    save_datas_xlsx('.'.join(('各校报名总名单','xlsx')),datas)
    print('各校报名总人数：',count(select(s for s in GradeY18 if s.outzh == None)))


if __name__ == '__main__':
    db.bind(**DB_PARAMS)
    db.generate_mapping(create_tables=True)
    # enter_csv()
    get_reg_data()
    # check_regdata_name_sch()
    # get_sch_data()
    # get_out_local()
    # get_out_local_by_name()
    # get_localzh_or_not()
    # check_localzh_name_sch()
    get_sch_data_xls()