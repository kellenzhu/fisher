from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models.base import Base


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
    isdn = Column(String(15), nullable=False)
