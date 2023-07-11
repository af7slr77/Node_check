import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, VARCHAR, Table
from sqlalchemy.orm import relationship, lazyload
from datetime import datetime
from lib.get_nodes_urls import get_nodes_urls
BaseModel = declarative_base()


# class UsersNodes(BaseModel):
# 	__tablename__ = "users_nodes"

# 	user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
# 	node_id = Column(Integer,ForeignKey('nodes.node_id'), primary_key=True, nullable=False)

# 	def __repr__(self):
# 		return f'{self.user_id, self.node_id}'


class Node(BaseModel):
	__tablename__ = 'nodes'

	node_id = Column(Integer, unique=True,  primary_key=True, nullable=False)
	node_url = Column(String, unique=True, nullable=False)
	node_name = Column(String, nullable=False)

	# users = relationship('User', secondary='users_nodes', back_populates='nodes', lazy=True)
	nodes_users = relationship(
        "User",
        secondary=Table(
            "nodes_users",
            BaseModel.metadata,
            Column("nodes.node_id", Integer, ForeignKey("nodes.node_id"), primary_key=True),
            Column("users.user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
        ),
        backref="nodes", lazy='selectin'
    )
	records = relationship('Records', backref='node', lazy=True)
	
	def __repr__(self):
		return f'{self.node_id, self.node_url, self.node_name}'


class User(BaseModel):
	__tablename__ = 'users'
	user_id = Column(Integer, unique=True, nullable=False,  primary_key=True)
	user_telegram_id = Column(Integer, unique=True, nullable=False)
	username = Column(VARCHAR(32), unique=True, nullable=False)
	reg_date = Column(Integer, nullable=False)
	
	# nodes = relationship('Node', secondary='users_nodes_', back_populates='users', lazy=True)

	def __repr__(self):
		return f'{self.user_id, self.user_telegram_id, self.username, self.reg_date}'

class Records(BaseModel):
	__tablename__ = 'records'

	record_id = Column(Integer, unique=True,  primary_key=True)
	score = Column(Integer)
	update_time = Column(Integer, nullable=False)
	node_id = Column(Integer, ForeignKey('nodes.node_id'))
	current_ds_epoch = Column(Integer)
	current_mini_epoch = Column(Integer)
	response_time = Column(Integer)

	def __repr__(self):
		return f"{self.record_id, self.score, self.update_time, self.node_id, self.current_ds_epoch, self.current_mini_epoch, self.response_time}"