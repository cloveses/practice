from db_mod import *


# zhtype=1  县外转入              outzh=1 
# zhtype=2  县外转入且县内转入    outzh=2
# zhtype=3  县内有转学            localzh=1
# zhtype=4  无转学记录            ouzh=None and localzh=None
# zhtype=0  历届学生

def save_datas_xlsx(filename,datas):
    #将一张表的信息写入电子表格中XLSX文件格式
    import xlsxwriter
    w = xlsxwriter.Workbook(filename)
    w_sheet = w.add_worksheet('sheet1')
    for rowi,row in enumerate(datas):
        for coli,celld in enumerate(row):
            w_sheet.write(rowi,coli,celld)
    w.close()

@db_session
def set_signall_zhtype():
    for stud in SignAll.select():
        gradey18 = GradeY18.select(lambda s:s.idcode=stud.idcode).first()
        if gradey18:
            if gradey18.outzh == 1:
                stud.zhtype = 1
            elif gradey18.outzh == 2:
                stud.zhtype = 2
            elif stud.localzh == 1:
                stud.zhtype = 3
            elif stud.outzh == None and localzh == None:
                stud.zhtype = 4
        else:
            stud.zhtype = 0
            # 查不到身份证号，即为历届生

@db_session
def get_all_data():
    data_title = ['中考报名号','姓名','性别','身份证号','学校','学校代码']
    datas = [data_title,]
    query = select((s.signid,s.name,s.sex,s.idcode,s.sch) 
        for s in SignAll if s.zhtype==0)
    datas.append(query)
    save_datas_xlsx('.'.join(('全县历届学生名单','xlsx')),datas)

    datas = datas[:1]


# # 将数据导出为excel
# @db_session
# def get_sch_data_xls():
#     schs = select(s.sch for s in GradeY18)

#     # 导出各校无从县外转入的应届生（从各校报名）,每学校一个文件
#     for sch in schs:
#         datas = [['学校','年级','班级','全国学籍号','学籍号','地区学号','姓名','身份证号','性别'],]
#         query = select([s.sch,s.grade,s.sclass,s.gsrid,s.ssrid,s.dsrid,s.name,s.idcode,s.sex] 
#             for s in GradeY18 if s.sch == sch and s.outzh == None)[:]
#         datas.extend(query)
#         save_datas_xlsx('.'.join((sch,'xlsx')),datas)
#         print(count(select(s for s in GradeY18 if s.sch == sch and s.outzh == None)),sch)

#     # 导出所有学校有县外转入记录的应届生（从招办报名）
#     datas = [['学校','年级','班级','全国学籍号','学籍号','地区学号','姓名','身份证号','性别'],]
#     query = select([s.sch,s.grade,s.sclass,s.gsrid,s.ssrid,s.dsrid,s.name,s.idcode,s.sex] 
#         for s in GradeY18 if s.outzh != None)[:]
#     datas.extend(query)
#     save_datas_xlsx('.'.join(('招办报名名单','xlsx')),datas)
#     print('招办报名人数：',count(select(s for s in GradeY18 if s.outzh != None)))

#     # 导出从各校报名的总名单
#     datas = [['学校','年级','班级','全国学籍号','学籍号','地区学号','姓名','身份证号','性别'],]
#     query = select(s for s in GradeY18 if s.outzh == None).order_by(GradeY18.sch)
#     for s in query:
#         datas.append([s.sch,s.grade,s.sclass,s.gsrid,s.ssrid,s.dsrid,s.name,s.idcode,s.sex])
#     save_datas_xlsx('.'.join(('各校报名总名单','xlsx')),datas)
#     print('各校报名总人数：',count(select(s for s in GradeY18 if s.outzh == None)))


if __name__ == '__main__':
    db.bind(**DB_PARAMS)
    db.generate_mapping(create_tables=True)

    # get_sch_data_xls()