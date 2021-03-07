from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.libs.helper import is_isbn_or_key
from app.models.base import Base
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float(), default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))
    _password = Column("password", String(128))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, plain_password):
        return check_password_hash(self._password, plain_password)

    def can_save_to_list(self, isbn):
        # 判断用户输入是否为isbn
        if is_isbn_or_key(isbn) != "isbn":
            return False

        # 判断输入isbn是否真实存在（API能查到）
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        # 赠送图书不能存在于用户心愿清单中（不能同时赠送和同时索要）
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        # 不能同时赠送相同图书
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not wishing and not gifting:
            return True
        else:
            return False


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
