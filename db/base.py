import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.get_nodes_urls import get_nodes_urls

BaseModel = declarative_base()


class UsersNodes(BaseModel):
	__tablename__ = "users_nodes"

	user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
	node_id = Column(Integer,
		ForeignKey('nodes.nodes_id'), primary_key=True, nullable=False
	)


class Node(BaseModel):
	__tablename__ = 'nodes'

	nodes_id = Column(Integer, unique=True,  primary_key=True, nullable=False)
	node_url = Column(String, unique=True, nullable=False)
	node_name = Column(String, nullable=False)
	# score = Column(Integer, nullable=False)
	# update_time = Column(Integer, nullable=False)

	users = relationship('User', secondary='users_nodes', back_populates='nodes')
	records = relationship('Records')


class User(BaseModel):
	__tablename__ = 'users'
	user_id = Column(Integer, unique=True, nullable=False, primary_key = True)
	user_telegram_id = Column(Integer, unique=True, nullable=False, primary_key = True)
	username = Column(VARCHAR(32), unique=True, nullable=False)
	reg_date = Column(Integer, nullable=False)
	upd_date = Column(Integer, nullable=False)
	
	nodes = relationship('Node', secondary='users_nodes', back_populates='users')

class Records(BaseModel):
	__tablename__ = 'records'

	id = Column(Integer, unique=True,  primary_key=True)
	score = Column(Integer)
	update_time = Column(Integer, nullable=False)
	nodes_id = Column(Integer, ForeignKey('nodes.nodes_id'))