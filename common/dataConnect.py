# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from data import configure
import pymysql
import logging


class Database:
	u"""
	数据库连接与操作
	"""
	def __init__(self):
		conf = configure.conf['db']
		self._con = pymysql.connect(**conf)
		self._cursor = self._con.cursor()

	def execute(self, sql=''):
		u"""
		执行sql语句，针对读操作返回结果集
		:param sql: sql语句
		:return: 查询结果
		"""
		try:
			self._cursor.execute(sql)
			records = self._cursor.fetchall()
			return records
		except pymysql.Error as msg:
			logging.error('MySQL execute failed! Error:%s' % msg)

	def commit(self, sql=''):
		u"""
		执行sql语句，针对更新，删除，事务等操作失败时回滚
		:param sql:sql语句
		:return:error信息
		"""
		try:
			self._cursor.execute(sql)
			self._con.commit()
		except pymysql.Error as msg:
			self._con.rollback()
			error = 'MySQL execute failed! Error:%s' % msg
			logging.error(error)
			return error

	def select(self, tablename, where_dic='', order='', fields='*'):
		where_sql = ' '
		if where_dic:
			for k, v in where_dic.items():
				where_sql = where_sql + k + '=' + v + ' and'
		where_sql += '1=1'
		if fields == '*':
			sql = 'select * from %s where' % tablename
		else:
			try:
				isinstance(fields, list)
				field = ','.join(fields)
				sql = 'select %s from %s where' % (field, tablename)
			except:
				raise 'fields input error, please input list fields.'
		sql = sql + where_sql + order
		logging.info(sql)
		return self.execute(sql)

	def insert(self, sql):
		u"""
		插入操作
		:param sql: 传入的sql语句
		:return:
		"""
		try:
			self._cursor.execute(sql)
			self._con.commit()
			logging.info(sql)
		except Exception as msg:
			self._con.rollback()
			logging.error('MySQL execute failed ! Error:%s' % msg)

	def update(self, sql):
		u"""
		更新操作
		:param sql: 传入的sql语句
		:return:
		"""
		try:
			self._cursor.execute(sql)
			self._con.commit()
			logging.info(sql)
		except Exception as msg:
			self._con.rollback()
			logging.error(msg)

	def delete(self, sql):
		u"""
		删除操作
		:param sql: 传入的sql语句
		:return:
		"""
		try:
			self._cursor.execute(sql)
			self._con.commit()
			logging.info(sql)
		except Exception as msg:
			self._con.rollback()
			logging.error(msg)

	def close(self):
		self._con.close()

if __name__ == '__main__':
	from common.Logger import Logger
	logger = Logger()
	query = Database()
	s = query.select(tablename='bmp_manufacturers', fields='MAN_ID')
	print(s)