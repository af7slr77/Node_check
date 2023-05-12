from .base import BaseModel
from sqlalchemy import Column, Integer, String

class Node(BaseModel):
	__tablename__ = 'nodes'

	nodes_id = Column(Integer, unique=True,  primary_key=True)
	node_url = Column(String, unique=True)
	node_name = Column(String)
	score = Column(Integer)
	update_time = Column(Integer)

	