from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Wish(Base):
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

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn
                                      ).filter(Gift.launched == False,
                                               Gift.isbn.in_(isbn_list),
                                               Gift.status == 1).group_by(Gift.isbn).all()
        count_list = [{"count": w[0], "isbn": w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first
