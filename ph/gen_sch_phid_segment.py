from phdl import *

@db_session
def gen_seg_for_sch():
    datas = []
    schs = select(s.sch for s in StudPh)
    for sch in schs:
        woman_min = min(s.phid for s in StudPh if s.sch==sch and s.sex=='女')
        woman_max = max(s.phid for s in StudPh if s.sch==sch and s.sex=='女')
        man_min = min(s.phid for s in StudPh if s.sch==sch and s.sex=='男')
        man_max = max(s.phid for s in StudPh if s.sch==sch and s.sex=='男')
        datas.append((sch,woman_min,woman_max,man_min,man_max))
    for data in datas:
        print(data)

if __name__ == '__main__':
    db.bind(**DB_PARAMS)
    db.generate_mapping(create_tables=True)
    gen_seg_for_sch()
