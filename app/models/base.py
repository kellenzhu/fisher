from sqlalchemy import Column, SmallInteger

from app import db


class Base(db.Model):
    # 不创建表，Base仅作为基类使用
    __abstract__ = True
    # create_time = Column("create_time", Integer)

    # 用户做删除操作，status = 0
    status = Column(SmallInteger, default=1)

    def set_attrs(self, dict_attrs):
        for key, value in dict_attrs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)
