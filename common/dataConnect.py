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

	def _execute(self, sql=''):
		u"""
		执行sql语句，针对读操作返回结果集
		:param sql: sql语句
		:return: 查询结果
		"""
		try:
			self._cursor.execute(sql)
			records = self._cursor.fetchall()
			if len(records) == 1:
				records = records[0][0]
			elif len(records) > 1:
				if len(records[0]) == 1:
					records = [r[0] for r in records]
			return records
		except pymysql.Error as msg:
			logging.error('MySQL execute failed! Error:%s' % msg)

	def _commit(self, sql=''):
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

	def select(self, tablename, fields='*', where_dic='', order='', limit=''):
		u"""
		查询数据
		:param tablename:表名
		:param where_dic:where条件，dict类型
		:param order:order by 或者 group by 需带关键字写全
		:param fields:展示的列名
		:param limit:直接传入条数str型，例如 '10，20'
		:return:执行execute
		"""
		where_sql = ' '
		if where_dic:
			for k, v in where_dic.items():
				if ',' in v:
					where_sql = where_sql + k + ' in ' + '(' + v + ')' + ' and '
				elif 'like' in v:
					v = v.split('like')[1].strip()
					where_sql = where_sql + k + ' like' + '\'%' + v + '%\'' + ' and '
				else:
					where_sql = where_sql + k + '=' + '\'' + v + '\'' + ' and '
		where_sql += '1=1'
		if limit:
			limit_sql = ' limit ' + limit
		else:
			limit_sql = ''
		try:
			if fields == '*':
				sql = 'select * from %s where' % tablename
			else:
				if isinstance(fields, list):
					field = ','.join(fields)
					sql = 'select %s from %s where' % (field, tablename)
				else:
					raise TypeError('fields input error, please input list fields.')
			sql += where_sql + order + limit_sql
			logging.info(sql)
			return self._execute(sql)
		except TypeError as msg:
			logging.error(msg)

	def count(self, tablename, where_dic=''):
		where_sql = ' '
		if where_dic:
			for k, v in where_dic.items():
				if ',' in v:
					where_sql = where_sql + k + ' in ' + '(' + v + ')' + ' and '
				elif 'like' in v:
					v = v.split('like')[1].strip()
					where_sql = where_sql + k + ' like' + '\'%' + v + '%\'' + ' and '
				else:
					where_sql = where_sql + k + '=' + '\'' + v + '\'' + ' and '
		where_sql += '1=1'
		sql = 'select count(1) from %s where' % tablename
		sql += where_sql
		logging.info(sql)
		return self._execute(sql)

	def insert(self, tablename, args):
		u"""
		插入单条数据
		:param tablename: 表名
		:param args: 插入的数据，dict类型 例如：{'MAN_ID': '350', 'MAN_NAME': 'TEST'}
		:return: 执行commit函数
		"""
		key, value = [], []
		for tmp_key, tmp_value in args.items():
			key.append(tmp_key)
			if isinstance(tmp_value, str):
				value.append('\'' + tmp_value + '\'')
			else:
				value.append(tmp_value)
		key_sql = ' (' + ','.join(key) + ')'
		value_sql = ' values (' + ','.join(value) + ')'
		sql = 'insert into %s' % tablename
		sql += key_sql + value_sql
		logging.info(sql)
		return self._commit(sql)

	def update(self, tablename, new_dict, where_dict):
		u"""
		更新数据
		:param tablename: 表名
		:param new_dict: 更新后的数据，新数据，dict型，对应字段：值
		:param where_dict: 判断条件，及where语句，dict型，对应 字段：值
		:return: 执行commit
		"""
		new_param = []
		for k, v in new_dict.items():
			new_param.append('%s=\'%s\'' % (k, v))
		new_sql = ','.join(new_param)

		for key, value in where_dict.items():
			if not isinstance(value, str):
				value = '\'' + str(value) + '\''
			where = key + '=' + value + ' and '
			where += '1=1'
		sql = 'update %s set %s where %s' % (tablename, new_sql, where)
		logging.info(sql)
		return self._commit(sql)

	def delete(self, tablename, where_dict):
		u"""
		删除数据
		:param tablename:表名
		:param where_dict:where条件，dict型，对应 字段：值
		:return:执行commit方法
		"""
		for k, v in where_dict.items():
			where_sql = k + '=\'' + v + '\'' + ' and '
		where_sql += '1=1'
		sql = 'delete from %s where %s' % (tablename, where_sql)
		logging.info(sql)
		return self._commit(sql)

	def close(self):
		self._con.close()

if __name__ == '__main__':
	from common.Logger import Logger
	logger = Logger()
	param = {'MAN_ID': '350', 'MAN_NAME': 'TEST', 'MAN_DESC': 'TEST1', 'FIELD_1': 'WIND', 'CLASS_ID': '100105'}
	new_args = {'MAN_DESC': 'TEST123'}
	where_args = {'MAN_ID': '350'}
	query = Database()
	# a = query.select(tablename='bmp_manufacturers')
	# b = query.insert(tablename='bmp_manufacturers', args=param)
	# c = query.update(tablename='bmp_manufacturers', new_dict=new_args, where_dict=where_args)
	# d = query.delete(tablename='bmp_manufacturers', where_dict=where_args)
	test = {'CLASS_LEVEL': '1', 'CLASS_ID': '11433,11434,11435,11436,11437,11438,11439,100105,100114'}
	a = query.select('bmp_attribclass', where_dic=test)
	mysql_manuname = query.select('bmp_manufacturers', ['DISTINCT MAN_NAME'])
	print(mysql_manuname)