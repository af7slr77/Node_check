import sqlalchemy as db
from sqlalchemy.sql import text


engine = db.create_engine("sqlite:///db.test")

connection = engine.connect()

metadata = db.MetaData()

nodes = db.Table('nodes', metadata,
				 db.Column('nodes_id', db.Integer, primary_key=True),
				 db.Column('node_url', db.String),
				 db.Column('node_name', db.String),
				 db.Column('current_dse_poch', db.Integer),
				 db.Column('current_mini_epoch', db.Integer),
				 db.Column('uptime', db.Integer),
				 db.Column('downtime', db.Integer),
				 db.Column('update_time', db.Integer)
				 )

metadata.create_all(engine)


async def write_to_db(node_url, node_name, current_dse_poch, current_mini_epoch, uptime, downtime, update_time):
	insertian_query = nodes.insert().values([
		{
			'node_url': node_url,
			'node_name': node_name,
			'current_dse_poch': current_dse_poch, 
			'current_mini_epoch': current_mini_epoch,
			'uptime':uptime,
			'downtime':downtime,
			'update_time':update_time
		}
	])
	connection.execute(insertian_query)
	connection.commit()

async def update(node_url, current_dse_poch, current_mini_epoch, uptime, downtime, update_time):
	if uptime:
		update_query = db.update(nodes).where(nodes.columns.node_url == node_url).values(
			current_dse_poch=current_dse_poch, 
			current_mini_epoch=current_mini_epoch,
			uptime=uptime,
			update_time=update_time
			)
		update_query_result = connection.execute(update_query)
		connection.commit()
	elif downtime:
		update_query = db.update(nodes).where(nodes.columns.node_url == node_url).values(**{
			'downtime':downtime,
			'update_time':update_time
			})
		update_query_result = connection.execute(update_query)
		connection.commit()


async def get_all_records():
	all_records_from_db = connection.execute(db.select(nodes)).fetchall()
	return all_records_from_db


async def get_recording_from_database(node_url):
	row = db.select(nodes).where(nodes.columns.node_url == node_url)
	row = connection.execute(row).fetchall()[0]
	return row