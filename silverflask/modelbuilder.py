import sqlalchemy
from sqlalchemy import Column

def get_column(col_type):
    print("GETTIGN A COPLUMN")
    return Column(sqlalchemy.Integer())

def modelbuilder(cls):
    cols = []
    for key in cls.db.keys():
        el = cls.db[key]
        if type(el) == str:
            setattr(cls, key, get_column(el))

    return