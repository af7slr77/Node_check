from sqlalchemy import Column, Integer
from sqlalchemy import String, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from config.zilliqa import TRUST_COEFFICIENT

BaseModel = declarative_base()

class NodesUsers(BaseModel):
	__tablename__ = "nodes_users"

	node_id = Column(
		Integer, ForeignKey("nodes.node_id"), 
		primary_key=True, nullable=False
	)
	user_id = Column(
		Integer, ForeignKey("users.user_id"), 
		primary_key=True, nullable=False
	)

	def __repr__(self):
		return f'{self.user_id, self.node_id}'


class Node(BaseModel):
	__tablename__ = 'nodes'

	node_id = Column(
		Integer, unique=True,  
		primary_key=True, nullable=False
	)
	node_url = Column(
		String, unique=True, 
		nullable=False
	)
	node_name = Column(String, nullable=False)
	nodes_users = relationship(
		"User", secondary='nodes_users', 
		backref='nodes', lazy='selectin'
	)
	records = relationship(
		'Records', backref='nodes',
		 lazy='selectin'
	)
	trust_coefficient = Column(
		Integer, default=TRUST_COEFFICIENT, 
		nullable=False
	)
	def __repr__(self):
		return f'{self.node_id, self.node_url, self.node_name}'


class User(BaseModel):
	__tablename__ = 'users'
	user_id = Column(
		Integer, unique=True, 
		nullable=False,  primary_key=True
	)
	user_telegram_id = Column(
		Integer, unique=True, 
		nullable=False
	)
	username = Column(
		VARCHAR(32), unique=True, 
		nullable=False
	)
	reg_date = Column(Integer, default=50, nullable=False)
	users_nodes = relationship(
		'Node', secondary='nodes_users', 
		backref='users', lazy='selectin', 
		viewonly=True
	)

	def __repr__(self):
		return f'{self.user_id, self.user_telegram_id, self.username, self.reg_date}'

class Records(BaseModel):
	__tablename__ = 'records'

	record_id = Column(
		Integer, unique=True,  
		primary_key=True
	)
	update_time = Column(Integer, nullable=False)
	node_id = Column(Integer, ForeignKey('nodes.node_id'))
	current_ds_epoch = Column(Integer)
	current_mini_epoch = Column(Integer)
	response_time = Column(Integer)
	rating = Column(Integer)
	stake_amount = Column(String)
	commission = Column(String)
	number_of_delegates = Column(Integer)

	def __repr__(self):
		return f"{self.record_id, self.score, self.update_time, self.node_id, self.current_ds_epoch, self.current_mini_epoch, self.response_time}"

	
class Blocks(BaseModel):
	__tablename__ = 'blocks'

	block_id = Column(Integer, unique=True,  primary_key=True)
	update_time = Column(Integer, nullable=False)
	current_ds_epoch = Column(Integer)
	current_mini_epoch = Column(Integer)
	response_time = Column(Integer)

	def __repr__(self):
		return f"{self.record_id, self.update_time, self.current_ds_epoch, self.current_mini_epoch, self.response_time}"