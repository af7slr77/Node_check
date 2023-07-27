import asyncio
from query_modules_2.get_nodes_urls import get_nodes_urls
from query_modules_2.call_url import call_url
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
# from db.base import  Records, User, NodesUsers, Node
from models.models import Node, Records, User, NodesUsers, Blocks
# from models.block import Blocks

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import lazyload, joinedload
from sqlalchemy import func
from db.engine import async_session
import time
from commands.sending_warnings_to_users import sending_warnings_to_users
from config.zilliqa import *
from block_worker.blocks_db import BlocksWorker

class Worker():

	def __init__(self, async_session):
		self._async_session = async_session

	async def run(self):
		while True:
			await self._write_or_update_node_to_db()
			# await self._checking_the_operation_of_node()

	async def _delete_user_from_user_nodes(self, node_name, tg_user_id):
		async with self._async_session() as session:
			node = await self._get_one_node_from_db(node_name)
			user = await self._get_one_user_from_db(tg_user_id)
			nodes_user_query = await session.execute(select(NodesUsers).filter_by(node_id=node.node_id))
			nodes_user = nodes_user_query.unique().one_or_none()[0]
			await session.delete(nodes_user)
			await session.commit()

	async def _get_max_curent_ds_epoch(self):
		async with self._async_session() as session:
			max_curent_ds_epoch_query = await session.execute(select(func.max(Records.current_ds_epoch)))
			max_curent_ds_epoch = max_curent_ds_epoch_query.unique().one_or_none()
			if max_curent_ds_epoch == None:
				return max_curent_ds_epoch
			return max_curent_ds_epoch[0]
			
	async def _get_max_current_mini_epoch(self):
		blocks_worker = BlocksWorker(async_session)
		max_current_mini_epoch = await blocks_worker._get_max_current_mini_epoch()
		return max_current_mini_epoch

	async def _sending_warnings(self, nodes_users, args):
		for user in nodes_users:
			user_telegram_id = user.user_telegram_id
			if user_telegram_id:
				await sending_warnings_to_users(user_telegram_id, args)
			else:
				pass

	async def _searching_for_empty_values_and_delays(self, node, max_mini_epoch):
		node_name = node[0].node_name
		last_record = node[0].records[-1]
		current_ds_epoch = last_record.current_ds_epoch
		current_mini_epoch = last_record.current_mini_epoch
		nodes_users = node[0].nodes_users
		if current_ds_epoch == None:
			args = {
				'node_name': node_name,
				'current_ds_epoch': current_ds_epoch
			}
			await self._sending_warnings(nodes_users, args)
		else:
			if current_mini_epoch < max_mini_epoch - MAX_DIFFERENCE_OF_BLOCKS:
				mini_epoch_diff = max_mini_epoch - current_mini_epoch
				args = {
					'node_name': node_name,
					'current_ds_epoch': current_ds_epoch,
					'mini_epoch_diff': mini_epoch_diff
				}
				await self._sending_warnings(nodes_users, args)			

	async def _checking_the_operation_of_node(self):
		try:
			async with self._async_session() as session:
				max_mini_epoch = await self._get_max_current_mini_epoch()
				all_nodes =  await self._get_all_nodes_from_db()
				for node in all_nodes:
					await self._searching_for_empty_values_and_delays(node, max_mini_epoch)
		except Exception as ex:
			print('checking_the_operation_of_node: ', ex)

	async def _buttons(self):
		async with self._async_session() as session:
			buttons_query = await session.execute(select(Node))
			buttons = buttons_query.all()
		return buttons

	async def _get_one_node_from_db(self, node_name):
		async with self._async_session() as session:
			node = await session.execute(select(Node).filter_by(node_name = node_name).options(joinedload(Node.records)))
			node = node.unique().one_or_none()
			if node == None:
				return node
			return node[0]

	async def _get_all_nodes_from_db(self):
		async with self._async_session() as session:
			all_nodes = await session.execute(select(Node).options(joinedload(Node.records)).options(joinedload(Node.nodes_users)))
			all_nodes = all_nodes.unique().all()
			return all_nodes
	
	async def _get_one_user_from_db(self, tg_user_id):
		async with self._async_session() as session:
			user = await session.execute(select(User).filter_by(user_telegram_id = tg_user_id ))
			user = user.unique().one_or_none()
			if user == None:
				return user
			else:
				return user[0]
			return user

	async def _get_nodes_users(self, node_name, ):
		async with self._async_session() as session:
			node_query = await session.execute(select(Node).options(joinedload(Node.nodes_users)).filter_by(node_name = node_name ))
			node = node_query.first()[0]
			nodes_users = node.nodes_users
			return nodes_users
			
	async def _check_subscribe(self, node_name, tg_user_id):
		"""This func check subscribe"""
		nodes_users = await self._get_nodes_users(node_name)
		for user in nodes_users:
			tg_user_id_from_db = user.user_telegram_id
			if tg_user_id_from_db == tg_user_id:
				return True
			else:
				continue
		return False

	async def _subscribe(self, node_name, tg_user_id):
		async with self._async_session() as session:
			try:
				node = await self._get_one_node_from_db(node_name)
				user = await self._get_one_user_from_db(tg_user_id)
				node.nodes_users.append(user)
				session.add(node)
				await session.commit()
			except Exception as ex:
				print('worker.subscribe ', ex)

	async def _response_time_score(self, response_time):
		if response_time > AVERAGE_RESPONSE_SECONDS and response_time < MAX_RESPONSE_SECONDS:
			response_time_score = MIN_RESPONSE_TIME_SCORE
			return response_time_score
		elif response_time > MIN_RESPONSE_SECONDS and response_time < AVERAGE_RESPONSE_SECONDS:
			response_time_score = AVERAGE_RESPONSE_TIME_SCORE
			return response_time_score
		elif response_time < MIN_RESPONSE_SECONDS:
			response_time_score = MAX_RESPONSE_TIME_SCORE
			return response_time_score

	async def _current_mini_epoch_score(self, current_mini_epoch, max_mini_epoch):
		if current_mini_epoch >= max_mini_epoch - MIN_DIFFERENCE_OF_BLOCKS:
				mini_epoch_score = POSITIVE_MINI_EPOCH_SCORE
				return mini_epoch_score
		elif current_mini_epoch < max_mini_epoch - MAX_DIFFERENCE_OF_BLOCKS:
			mini_epoch_score = AVERAGE_NEGATIVE_TOTAL_SCORE
			return mini_epoch_score

	async def _current_score(self, current_mini_epoch, response_time, max_mini_epoch):
		mini_epoch_score = None
		response_time_score = None
		total_score = None
		if current_mini_epoch is not None and response_time is not None and max_mini_epoch is not None:
			current_mini_epoch_score = await self._current_mini_epoch_score(current_mini_epoch, max_mini_epoch)
			response_time_score = await self._response_time_score(response_time)
			return current_mini_epoch_score + response_time_score
		else: 
			return MAX_NEGATIVE_TOTAL_SCORE

	async def _get_last_node_score(self, node):
		async with self._async_session() as session:
			node_id = node.node_id
			last_rating_query = await session.execute(select(Records).filter_by(node_id=node_id).order_by(Records.record_id.desc()))
			last_rating = last_rating_query.first()[0].score
			return last_rating
	
	async def _get_ratings_number(self, node_name):
		async with self._async_session() as session:
			node = await self._get_one_node_from_db(node_name)
			node_id = node.node_id
			ratings_number_query = await session.execute(select(Records).filter_by(node_id=node_id))
			last_rating = len(ratings_number_query.fetchall())
			return last_rating

	async def _get_rating(self, node_name, last_score_from_db):
		ratings_number = await self._get_ratings_number(node_name)
		maximum_score = MAX_POINTS_PER_ASSESSMENT * ratings_number
		rating = (last_score_from_db / maximum_score) * 100
		return rating

	async def _create_new_node(self, node_args):
		new_node = Node(
			node_url = node_args['node_url'],
			node_name = node_args['node_name'],
			)
		return new_node

	async def _create_new_record(self, record_args):
		new_record = Records(
			update_time = datetime.utcnow().timestamp(),
			current_ds_epoch = record_args['current_ds_epoch'],
			current_mini_epoch = record_args['current_mini_epoch'],
			response_time = record_args['response_time'],
			score = record_args['score'],
			rating = record_args['rating']
			)
		return new_record

	async def _get_new_score(self, last_score_from_db, current_responce_score):
		new_score = last_score_from_db + current_responce_score
		if new_score <= 0:
			return 0
		return new_score

	async def _write_node_db(self, node_from_responce):
		async with self._async_session() as session:
			node_url = node_from_responce['node_url'],
			node_name = node_from_responce['node_name']
			current_ds_epoch = node_from_responce['current_ds_epoch']
			current_mini_epoch = node_from_responce['current_mini_epoch']
			response_time = node_from_responce['response_time']
			node_db = await self._get_one_node_from_db(node_name)
			if node_db is not None:
				try:
					max_mini_epoch = int(await self._get_max_current_mini_epoch())
					last_score_from_db = int(await self._get_last_node_score(node_db))
					current_responce_score = await self._current_score(current_mini_epoch, response_time, max_mini_epoch)
					score = await self._get_new_score(last_score_from_db, current_responce_score)
					rating = round(await self._get_rating(node_name, last_score_from_db))
					record_args = {
						'current_ds_epoch': current_ds_epoch,
						'current_mini_epoch': current_mini_epoch,
						'response_time': response_time,
						'score': score,
						'rating': rating
					}
					new_record = await self._create_new_record(record_args)
					node_db.records.append(new_record)
					session.add(new_record)
					await session.commit()
				except Exception as ex:
					print(ex)
			else:
				node_args = {
					'node_url': node_url[0],
					'node_name' : node_name
				}
				record_args = {
					'current_ds_epoch': current_ds_epoch,
					'current_mini_epoch': current_mini_epoch,
					'response_time': response_time,
					'score': 0,
					'rating':0
				}
				new_node = await self._create_new_node(node_args)
				new_record = await self._create_new_record(record_args)
				new_node.records.append(new_record)
				session.add(new_node)
				session.add(new_record)
				await session.commit()

	async def _write_or_update_node_to_db(self):
		try:
			urls = get_nodes_urls()
			for url in urls:
				responce = call_url(url['node_url'], url['name'])
				print(responce)
				await self._write_node_db(responce)
				time.sleep(PAUSE_BETWEEN_REQUESTS)
		except Exception as ex:
			print('write_or_update_node_to_db: ', ex)

if __name__ == '__main__':
	worker = Worker(async_session)
	asyncio.run(worker.run())