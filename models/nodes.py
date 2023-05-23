# from db.base import BaseModel
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship
# from models.users_nodes import UsersNodes


# class Node(BaseModel):
# 	__tablename__ = 'nodes'

# 	nodes_id = Column(Integer, unique=True,  primary_key=True)
# 	node_url = Column(String, unique=True)
# 	node_name = Column(String)
# 	score = Column(Integer)
# 	update_time = Column(Integer)

# 	users = relationship('User', secondary=UsersNodes, back_populates='nodes')

