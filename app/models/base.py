from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, SmallInteger, Integer


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            # db.session.commit会保证事务一致性，但一旦插入操作出现异常则需要立即回滚
            self.session.rollback()
            raise e


db = SQLAlchemy()


class Base(db.Model):
    # 不创建表，Base仅作为基类使用
    __abstract__ = True
    create_time = Column("create_time", Integer)

    # 用户做删除操作，status = 0
    status = Column(SmallInteger, default=1)

    def set_attrs(self, dict_attrs):
        for key, value in dict_attrs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)
