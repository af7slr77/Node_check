from datetime import datetime
from .base import BaseModel
from sqlalchemy import Column, Integer, String, DATE, VARCHAR


class User(BaseModel):
    __tablename__ = 'users'
    user_id = Column(Integer, unique=True, nullable=False, primary_key = True)
    username = Column(VARCHAR(32), unique=False, nullable=True)
    reg_date = Column(DATE, default=datetime.now().timestamp())
    upd_date = Column(DATE, default=datetime.now().timestamp())