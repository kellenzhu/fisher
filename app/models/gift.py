from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
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

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        count_list = db.session.query(func.count(Wish.id), Wish.isbn
                                      ).filter(Wish.launched == False,
                                               Wish.isbn.in_(isbn_list),
                                               Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{"count": w[0], "isbn": w[1]} for w in count_list]
        return count_list
