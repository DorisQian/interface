# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from data import configure
from common.Logger import Logger
import pymysql


class Database:
	u"""
	数据库连接与操作
	"""
	def __init__(self):
		self.logger = Logger('INFO')
		conf = configure.conf['db']
		self.db = pymysql.connect(**conf)
		self.cursor = self.db.cursor()

	def query(self, sql):
		"""
		查询所有结果
		:param sql: 传入的sql语句
		:return: 查询结果
		"""
		try:
			self.cursor.execute(sql)
			self.logger.info(sql)
			result = self.cursor.fetchall()
			self.logger.info('the result: %s' % (result, ))
			return result
		except Exception as msg:
			self.logger.error(msg)

	def insert(self, sql):
		u"""
		插入操作
		:param sql: 传入的sql语句
		:return:
		"""
		try:
			self.cursor.execute(sql)
			self.db.commit()
			self.logger.info(sql)
		except Exception as msg:
			self.db.rollback()
			self.logger.error(msg)

	def update(self, sql):
		u"""
		更新操作
		:param sql: 传入的sql语句
		:return:
		"""
		try:
			self.cursor.execute(sql)
			self.db.commit()
			self.logger.info(sql)
		except Exception as msg:
			self.db.rollback()
			self.logger.error(msg)

	def delete(self, sql):
		u"""
		删除操作
		:param sql: 传入的sql语句
		:return:
		"""
		try:
			self.cursor.execute(sql)
			self.db.commit()
			self.logger.info(sql)
		except Exception as msg:
			self.db.rollback()
			self.logger.error(msg)


if __name__ == '__main__':
	query = Database()
	s = query.query('select MAN_ID from bmp_manufacturers limit 20')
	l =[]
	for n in s:
		l.append(n[0])
	print(l)