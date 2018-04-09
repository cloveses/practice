import os
import csv
import xlrd
from phdl import *


# 导入初三考生免考申请表、选考项目确认表（excel格式）到数据库中
# 二类表分别存放子目录：freeexam,itemselect之中

FREE_EXAM_KS = ('schseq','signid','phid','name','reason',
    'material','memo')
FREE_EXAM_TYPE = (int,str,str,str,str,str,str)
ITEM_SELECT_KS = ('schseq','signid','phid','name',
    'jump_option','rope_option','globe_option','bend_option')
ITEM_SELECT_TYPE = (int,str,str,str,int,int,int,int)

STUDPH_KS = ('signid','name','sex','idcode','sch','schcode')

def get_files(directory):
    files = []
    files = os.listdir(directory)
    files = [f for f in files if f.endswith('.xls') or f.endswith('.xlsx')]
    files = [os.path.join(directory,f) for f in files]
    return files

def check_files_select(directory,types,grid_end=0,start_row=1):
    files = get_files(directory)
    if files:
        infos = []
        for file in files:
            wb = xlrd.open_workbook(file)
            ws = wb.sheets()[0]
            nrows = ws.nrows
            for i in range(start_row,nrows-grid_end):
                datas = ws.row_values(i)
                for index,(d,t) in enumerate(zip(datas,types)):
                    try:
                        if d != '':
                            t(d)
                    except:
                        infos.append('文件：{}中，第{}行，第{}列数据有误'.format(file,i+1,index+1))
                selects = [int(i) for i in datas[-4:]]
                if not (sum(selects) == 0 or (selects[0]+selects[1] == 1 and selects[-2]+selects[-1]==1)):
                    infos.append('文件：{}中，第{}行选项有误'.format(file,i+1))
        print('检验的目录：',directory)
        if infos:
            for info in infos:
                print(info)
        else:
            print(file,'数据检验通过！')

def check_files_other(directory,types,grid_end=0,start_row=1):
    files = get_files(directory)
    if files:
        infos = []
        for file in files:
            wb = xlrd.open_workbook(file)
            ws = wb.sheets()[0]
            nrows = ws.nrows
            for i in range(start_row,nrows-grid_end):
                datas = ws.row_values(i)
                for index,(d,t) in enumerate(zip(datas,types)):
                    try:
                        if d != '':
                            t(d)
                    except:
                        infos.append('文件：{}中，第{}行，第{}列数据有误'.format(file,i+1,index+1))
        print('检验的目录：',directory)
        if infos:
            for info in infos:
                print(info)
        else:
            print(file,'数据检验通过！')


@db_session
def gath_data(tab_obj,ks,chg_dir,grid_end=1,start_row=1,types=None,start_col=0):
    """start_row＝1 有一行标题行；grid_end=1 末尾行不导入"""
    files = get_files(chg_dir)
    for file in files:
        wb = xlrd.open_workbook(file)
        ws = wb.sheets()[0]
        nrows = ws.nrows
        for i in range(start_row,nrows-grid_end):
            datas = ws.row_values(i)
            if types is None:
                datas = {k:v for k,v in zip(ks,datas[start_col:]) if v}
            else:
                datas = {k:t(v) for k,v,t in zip(ks,datas[start_col:],types) if v}
            # print(datas)
            tab_obj(**datas)

@db_session
def get_sch(signid):
    stud = StudPh.select(lambda s:s.signid == signid).first()
    if stud:
        return stud.sch
    else:
        '没有查到该生所在学校。'

@db_session
def check_select():
    for stud in ItemSelect.select():
        if (stud.jump_option + stud.rope_option + stud.globe_option +
                    stud.bend_option) == 0:
            if count(FreeExam.select(lambda s:s.signid == stud.signid)) != 1:
                print(stud.signid,stud.name,get_sch(stud.signid),'未免考考生无选项！')
        else:
            if not (stud.jump_option + stud.rope_option == 1 and 
                    stud.globe_option + stud.bend_option == 1):
                print(stud.signid,stud.name,get_sch(stud.signid),'选项有误，请检查！')

@db_session
def put2studph():
    for stud in ItemSelect.select():
        studph = StudPh.select(lambda s:s.signid == stud.signid).first()
        if not studph:
            print(stud.signid,stud.name,get_sch(stud.signid),'考号错误，查不到此人！')
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

    check_files_other('freeexam',FREE_EXAM_TYPE)
    check_files_select('itemselect',ITEM_SELECT_TYPE)
    # gath_data(FreeExam,FREE_EXAM_KS,'freeexam',0,types=FREE_EXAM_TYPE)
    # gath_data(ItemSelect,ITEM_SELECT_KS,'itemselect',0,types=ITEM_SELECT_TYPE) # 末尾行无多余数据
    # gath_data(StudPh,STUDPH_KS,'studph',0) 
    # check_select()
    # put2studph()
