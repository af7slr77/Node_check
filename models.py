import sqlalchemy as db



engine = db.create_engine("sqlite:///db.test")
connection = engine.connect()
metadata = db.MetaData()
nodes = db.Table('nodes', metadata,
	db.Column('id', db.String, primary_key=True),
	db.Column('node_url', db.String),
	db.Column('node_name', db.String),
	db.Column('CurrentDSEpoch', db.String),
	db.Column('CurrentMiniEpoch', db.String),
)

metadata.create_all(engine)

def write_to_db(node_url, node_name, node_query):
	insertian_query = nodes.insert().values([
		{
			'node_url': node_url,
			'node_name': node_name,
			'CurrentDSEpoch': node_query['CurrentDSEpoch'],
			'CurrentMiniEpoch': node_query['CurrentMiniEpoch'],
		}
	])