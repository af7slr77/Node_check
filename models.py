import sqlalchemy as db
from sqlalchemy.sql import text


engine = db.create_engine("sqlite:///db.test")

connection = engine.connect()

metadata = db.MetaData()

nodes = db.Table('nodes', metadata,
				 db.Column('nodes_id', db.Integer, primary_key=True),
				 db.Column('node_url', db.String),
				 db.Column('node_name', db.String),
				 db.Column('current_dse_poch', db.String),
				 db.Column('current_mini_epoch', db.String),
				 db.Column('uptime', db.String),
				 db.Column('downtime', db.String),
				 db.Column('update_time', db.String)
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
			# current_dse_poch=current_dse_poch, 
			# current_mini_epoch=current_mini_epoch,
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


async def get_all_recors():
	all_records_from_db = connection.execute(db.select(nodes)).fetchall()
	return all_records_from_db

#update('https://valkyrie2-api.seed.zilliqa.com ', 'current_dse_poch', 'current_mini_epoch', 'uptime', 'downtime', 'update_time')
# u = db.update(nodes)
# u = u.values({"uptime": "0-fi", 'update_time':'update_time'})
# u = u.where(nodes.c.node_url == "https://valkyrie2-api.seed.zilliqa.com ")
# connection.execute(u)
# connection.commit()