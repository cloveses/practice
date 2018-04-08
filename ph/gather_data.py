import os
import csv
import xlrd
from phdl import *


# 导入初三考生免考申请表、选考项目确认表（excel格式）到数据库中
# 二类表分别存放子目录：freeexam,itemselect之中

FREE_EXAM_KS = ('schseq','signid','phid','name','reason',
    'material','memo')
ITEM_SELECT_KS = ('schseq','signid','phid','name',
    'jump_option','rope_option','globe_option','bend_option')

def get_files(directory):
    files = []
    files = os.listdir(directory)
    files = [f for f in files if f.endswith('.xls') or f.endswith('.xlsx')]
    files = [os.path.join(directory,f) for f in files]
    return files

@db_session
def gath_data(tab_obj,ks,chg_dir,grid_end=1,start_row=1):
    """start_row＝1 有一行标题行；gred_end=1 末尾行不导入"""
    files = get_files(chg_dir)
    for file in files:
        wb = xlrd.open_workbook(file)
        ws = wb.sheets()[0]
        nrows = ws.nrows
        for i in range(start_row,nrows-grid_end):
            datas = ws.row_values(i)
            datas = {k:v for k,v in zip(ks,datas) if v}
            tab_obj(**datas)

@db_session
def check_select():
    for stud in ItemSelect.select():
        if (stud.jump_option + stud.rope_option + stud.globe_option +
                    stud.bend_option) == 0:
            if count(FreeExam.select(lambda s:s.signid == stud.signid)) != 1:
                print(stud.signid,stud.name,stud.sch,'未免考考生无选项！')
        else:
            if not (stud.jump_option + stud.rope_option == 1 and 
                    stud.globe_option + stud.bend_option == 1):
                print(stud.signid,stud.name,stud.sch,'选项有误，请检查！')

@db_session
def put2studph():
    for stud in ItemSelect.select():
        studph = StudPh.select(lambda s:s.signid == stud.signid).first()
        if not studph:
            print('考号错误，查不到此人！')
        else:
            if stud.jump_option + stud.rope_option + stud.globe_option + stud.bend_option == 0:
                studph.free_flag = True
            else:
                studph.free_flag = False
            studph.set(jump_option=stud.jump_option,
                rope_option=stud.rope_option,
                globe_option=stud.globe_option,
                bend_option=stud.bend_option)

if __name__ == '__main__':
    db.bind(**DB_PARAMS)
    db.generate_mapping(create_tables=True)

    gath_data(FreeExam,FREE_EXAM_KS,'freeexam',0)
    gath_data(ItemSelect,ITEM_SELECT_KS,'itemselect',0) # 末尾行无多余数据
    check_select()
