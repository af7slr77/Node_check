from .base import BaseModel
from sqlalchemy import Column, Integer, String, DateTime

class Records(BaseModel):
    __tablename__ = 'records'

    id = Column(Integer, unique=True,  primary_key=True)
    score = Column(Integer)
    update_time = Column(DateTime)
