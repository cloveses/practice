import os
import datetime
from pony.orm import *

db = Database()

class Data(db.Entity):
    group = Required(int)
    seq = Required(int)
    mdata = Required(str)


# set_sql_debug(True)
filename = os.path.join(os.path.abspath(os.curdir),'my.db')
db.bind(provider='sqlite', filename=filename, create_db=True)
db.generate_mapping(create_tables=True)
