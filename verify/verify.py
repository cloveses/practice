import re
import os
import sys
from myxl import *


# 以下为可用限制条件参数示例
# {
#     'length_min':3,
#     'length_max':6,
#     'min':0,
#     'max':100,
#     're_exp':r'[ab]',
#     'choices':['A','B'],
# }

def verify_data_int(data,cols_limits=None):
    info = ""
    if not isinstance(data,float):
        info = "此数据类型不符合要求"
        return info
    if cols_limits is None:
        cols_limits = {}
    data = int(data)
    if cols_limits:
        if 'min' in cols_limits:
            if data < cols_limits['min']:
                info = "此数据不得小于%d" % cols_limits['min']
                return info
        if 'max' in cols_limits:
            if data > cols_limits['max']:
                info = "此数据不得大于%d" % cols_limits['max']
                return info
    return info

def verify_data_float(data,cols_limits=None):
    info = ""
    if not isinstance(data,float):
        info = "此数据类型不符合要求"
        return info
    if cols_limits is None:
        cols_limits = {}
    if cols_limits:
        if 'min' in cols_limits:
            if data < cols_limits['min']:
                info = "此数据不得小于%f" % cols_limits['min']
                return info
        if 'max' in cols_limits:
            if data > cols_limits['max']:
                info = "此数据不得大于%f" % cols_limits['max']
                return info
    return info

def verify_data_str(data,cols_limits=None):
    info = ""
    if not isinstance(data,str):
        info = "此数据类型不符合要求"
        return info
    if cols_limits is None:
        cols_limits = {}
    if cols_limits:
        if 'length_min' in cols_limits:
            if len(data) < cols_limits['length_min']:
                info = "此字符串长度不得小于%d" % cols_limits['length_min']
                return info
        if 'length_max' in cols_limits:
            if len(data) > cols_limits['length_max']:
                info = "此字符串长度不得大于%d" % cols_limits['length_max']
                return info
        if 'choices' in cols_limits:
            if data not in cols_limits['choices']:
                info = "此字符串不是候选数据"
                return info
        if 're_exp' in cols_limits:
            if not re.search(cols_limits['re_exp'],data):
                info = "此字符串模式不符合要求"
                return info
    return info

def verify_file(filename,filters,limits,ncols,headline_row_num=0):
    """
    验证单个文件
    filters 每列过滤方法列表
    limits  每列限制条件字典
    ncols   总列数
    """
    info = ""
    if not os.path.exists(filename):
        info = '文件不存在！\n'
        return info
    datass = get_data_cols(filename,headline_row_num)
    if len(datass) != ncols:
        info = "表格列数不符合要求！\n"
        print(info)
        return info
    for ncol,(datas,fun,limit) in enumerate(zip(datass,filters,limits)):
        for nrow,data in enumerate(datas):
            cell_info = fun(data,limit)
            if cell_info:
                pos_info = "行:%d 列:%d:" % (nrow + 1 + headline_row_num,ncol + 1)
                info += ' '.join((pos_info,cell_info,'\n'))
    return info

def verify_files(mdir,filters,limits,ncols,headline_row_num=0):
    # 验证目录下多个文件
    files = get_files(mdir)
    infos = []
    for mfile in files:
        info = verify_file(mfile,filters,limits,ncols,headline_row_num)
        infos.append((mfile,info))
    return infos    


if __name__ == "__main__":
    # 验证DEMO
    # cols_A = {
    #     'min':0,
    #     'max':100,
    # }

    # cols_B = {
    #     'length_min':4,
    #     'length_max':8,
    #     're_exp':r'[ab]',
    # }

    # cols_C = {
    #     'length_min':4,
    #     're_exp':r'[ab]',
    #     'choices':['dkdakk','dddkb'],
    # }

    # cols_D = {
    #     'min':0,
    #     'max':100,
    # }
    # limits = [cols_A,cols_B,cols_C,cols_D]
    # filters = [verify_data_int,verify_data_str,verify_data_str,verify_data_float]
    # verify_file('tst.xls',filters,limits,4)

    # summary_col(filename,col_seq_num,res_filename='res.xlsx'):
    # 统计指定电子表格文件中的指定序号列到指定的文件中
    # filename 指定电子表格文件
    # col_seq_num 列序号从0开始
    # res_filename 统计结果存放文件名

    # merge_files_data(mydir,res_filename):
    # 合并指定目录(mydir)下的所有分表数据到一个电子表格文件(res_filename)中的一张表中
    # 验证配置文件见实例：szcp.py
    # 默认验证配置文件为mylimits.py
    # 默认验证目录为当前目录
    # 可以使用参数形式来指定配置文件
    # 例如配置文件名为：szcp.py,命令行为：python3 verify.py szcp
    default_limit = 'mylimits'
    if len(sys.argv) > 1:
        default_limit = sys.argv[1]
    mylimits = __import__(default_limit)
    infos = verify_files(mylimits.verify_dir,mylimits.filters,
        mylimits.limits,mylimits.cols_sum,mylimits.headline_row_num)
    print()
    for info in infos:
        if info[1]:
            print(info[0],info[1])
        else:
            print(info[0],'Data right!\n')
