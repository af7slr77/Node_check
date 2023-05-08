from .base import BaseModel
from sqlalchemy import Column, Integer, String, DATE

class Node(BaseModel):
    __tablename__ = 'nodes'

    nodes_id = Column(Integer, unique=True,  primary_key=True)
    node_url = Column(String, unique=True)
    node_name = Column(String)
    current_dse_poch = Column(Integer)
    current_mini_epoch = Column(Integer)
    uptime = Column(Integer)
    downtime = Column(Integer)
    update_time = Column(Integer)
