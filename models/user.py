# from datetime import datetime
# from db.base import BaseModel
# from sqlalchemy import Column, Integer, String, DateTime, VARCHAR
# from sqlalchemy.orm import relationship
# from models.users_nodes import UsersNodes


# class User(BaseModel):
#     __tablename__ = 'users'
#     user_id = Column(Integer, unique=True, nullable=False, primary_key = True)
#     user_telegram_id = Column(Integer, unique=True, nullable=False, primary_key = True)
#     username = Column(VARCHAR(32), unique=False, nullable=True)
#     reg_date = Column(default=datetime.now().timestamp())
#     upd_date = Column(default=datetime.now().timestamp())
    
#     nodes = relationship('Node', secondary=UsersNodes, back_populates='users')