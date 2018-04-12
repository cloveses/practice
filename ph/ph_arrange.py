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
    # 考号前缀
    prefix = 18250000
    # 起始考号
    phid = 1
    for arrange_data in arrange_datas:
        all_studs = []
        if len(arrange_data) == 4:
            for sch in arrange_data[-2]:
                studs = select(s for s in StudPh if s.sch==sch and
                    s.sex==arrange_data[-1]).order_by(StudPh.sturand)[:]
                all_studs.extend(studs)

        elif len(arrange_data) == 3:
            for sex in ('女','男'):
                for sch in arrange_data[-1]:
                    studs = select(s for s in StudPh if s.sch==sch and
                        s.sex==sex).order_by(StudPh.sturand)[:]
                    all_studs.extend(studs)

        for stud in all_studs:
            print(prefix+phid)
            stud.exam_addr = arrange_data[0]
            stud.exam_date = arrange_data[1]
            stud.phid = str(prefix + phid)
            phid +=1

# # 测试用函数
# @db_session
# def arrange_phid_test():
#     prefix = 18250000
#     phid = 1
#     for arrange_data in arrange_datas:
#         all_studs = []
#         if len(arrange_data) == 4:
#             for sch in arrange_data[-2]:
#                 studs = select(s for s in StudPhTest if s.sch==sch and
#                     s.sex==arrange_data[-1]).order_by(StudPhTest.sturand)[:]
#                 all_studs.extend(studs)

#         elif len(arrange_data) == 3:
#             for sex in ('女','男'):
#                 for sch in arrange_data[-1]:
#                     studs = select(s for s in StudPhTest if s.sch==sch and
#                         s.sex==sex).order_by(StudPhTest.sturand)[:]
#                     all_studs.extend(studs)

#         for stud in all_studs:
#             stud.exam_addr = arrange_data[0]
#             stud.exam_date = arrange_data[1]
#             stud.phid = str(prefix + phid)
#             phid +=1

# @db_session
# def test_same():
#     for sa,sb in zip(select(s for s in StudPh).order_by(StudPh.phid),
#         select(s for s in StudPhTest).order_by(StudPhTest.phid)):
#         if not (sa.exam_addr == sb.exam_addr and sa.exam_date==sb.exam_date and 
#             sa.phid==sb.phid):
#             print(sa.name,sa.exam_addr,sa.exam_date,sb.name,sb.exam_addr,sb.exam_date,'Different.')


def save_datas_xlsx(filename,datas):
    #将一张表的信息写入电子表格中XLSX文件格式
    import xlsxwriter
    w = xlsxwriter.Workbook(filename)
    w_sheet = w.add_worksheet('sheet1')
    for rowi,row in enumerate(datas):
        for coli,celld in enumerate(row):
            w_sheet.write(rowi,coli,celld)
    w.close()

# 导出各校中考报名号和体育准考证号
@db_session
def get_sch_data_xls():
    schs = select(s.sch for s in StudPh)

    tab_title = ['中考报名号','准考证号','姓名']
    for sch in schs:
        datas = [tab_title,]
        studs = select([s.signid,s.phid,s.name] for s in StudPh 
            if s.sch==sch)[:]
        datas.extend(studs)
        save_datas_xlsx(''.join((sch,'体育考号.xlsx')),datas)



if __name__ == '__main__':
    db.bind(**DB_PARAMS)
    db.generate_mapping(create_tables=True)

    # arrange_phid_test()
    # test_same()

    # set_rand()
    # arrange_phid()
    get_sch_data_xls()
