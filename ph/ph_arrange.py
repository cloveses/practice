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
    prefix = 18250000
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
            stud.exam_addr = arrange_data[0]
            stud.exam_date = arrange_data[1]
            stud.phid = str(prefix + phid)
            phid +=1

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
    # set_rand()
    # arrange_phid()
    get_sch_data_xls()