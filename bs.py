import xlrd
from pony.orm import *

db = Database()

class SchRec(db.Entity):
    sch = Required(str)
    grade = Required(int)
    seq_class = Required(int)
    number = Required(int)

# set_sql_debug(True)
db.bind(provider='sqlite', filename=':memory:', create_db=True)
db.generate_mapping(create_tables=True)

def get_data(filename):
     #既可以打开xls类型的文件，也可以打开xlsx类型的文件
    #w = xlrd.open_workbook('text.xls')
    #w = xlrd.open_workbook('acs.xlsx')
    datas = []
    w = xlrd.open_workbook(filename)
    ws = w.sheets()[0]
    nrows = ws.nrows
    for i in range(nrows):
        data = ws.row_values(i)
        datas.append(data)
    #    print(datas)
    return datas

@db_session
def import_data(datas):
    for data in datas:
        params = {}
        keys = ('sch','grade','seq_class','number')
        for key,d in zip(keys,data):
            if isinstance(d,float):
                d = int(d)
            params[key] = d
        SchRec(**params)

@db_session
def get_result():
    schs = select(s.sch for s in SchRec)
    grades = (7,8,9)
    for grade in grades:
        print('%s年级统计：' % grade)
        for sch in schs:
            rets = [sch,]
            grade_num = count(s for s in SchRec if s.sch==sch and s.grade==grade)
            totals = sum(s.number for s in SchRec if s.sch==sch and s.grade==grade)
            rets.append(grade_num)
            rets.append(totals)
            rets.append(round(totals/grade_num,2))
            min_num = min(s.number for s in SchRec if s.sch==sch and s.grade==grade)
            max_num = max(s.number for s in SchRec if s.sch==sch and s.grade==grade)
            for ret in rets:
                print(ret,end=' ')
            print()
    print('学校总体统计：')
    for sch in schs:
        rets = [sch,]
        grade_num = count(s for s in SchRec if s.sch==sch)
        totals = sum(s.number for s in SchRec if s.sch==sch)
        rets.append(grade_num)
        rets.append(totals)
        rets.append(round(totals/grade_num,2))
        min_num = min(s.number for s in SchRec if s.sch==sch)
        max_num = max(s.number for s in SchRec if s.sch==sch)
        for ret in rets:
            print(ret,end=' ')
        print()

if __name__ == '__main__':
    datas = get_data('bj.xlsx')
    import_data(datas)
    get_result()