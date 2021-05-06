from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)

    # launched用于表示礼物是否已送出
    launched = Column(Boolean, default=False)

    user = relationship("User")
    # 外键，user.id中的user为 relationship对象
    uid = Column(Integer, ForeignKey("user.id"))

    # 图书从API获取没保存至数据库，注释以下
    # book = relationship("Book")
    # bid = Column(Integer, ForeignKey("book.id"))
    isbn = Column(String(15), nullable=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        # 链式调用方式显示最近的礼物清单，要求进行去重（不显示重复赠送的礼物）并限制返回结果为30条
        # group_by() 查询分组 针对相同的isbn进行分组
        # order_by() 查询排序  desc取create_time的倒序
        # limit() 查询结果数量限制
        # distinct() 去重 去掉相同的isbn
        # all() 或者 first() 触发生成SQL语句

        recent_gift = Gift.query.filter_by(
            launched=False).group_by(Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config["RECENT_BOOK_COUNT"]).distinct().all()
        return recent_gift
