import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum

from .database import Base
from .utils import encode_pwd


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, comment='人员编号')
    username = Column(String, comment='姓名')
    nickname = Column(String,comment='昵称')
    phone = Column(Integer, unique=True, index=True, comment='电话号码')
    hashed_password = Column(String, comment='密码')
    sex = Column(Boolean,default=True,comment='性别')
    avatar = Column(String,default='https://cdn.nzxf.net/OIP-C.jpg',comment='头像')
    is_admin = Column(Boolean, default=False, comment='是否为管理员')

    def check_password(self, password):
        return self.hashed_password == encode_pwd(password)
