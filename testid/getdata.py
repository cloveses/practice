from pg import DB

def getdb():
    return DB(dbname='test',user='postgres',password='123456')

def get_schs():
    db = getdb()
    q = db.query('select distinct(sch) from datatab;')
    res = q.getresult()
    schs = []
    for r in res:
        schs.append(r[0])
    db.close()
    return schs

def get_studs(sch):
    '''获取一个学校的所有学生'''
    db = getdb()
    q = db.query('select * from datatab where sch=$1;',(sch,))
    ret = q.getresult()
    db.close()
    return ret

