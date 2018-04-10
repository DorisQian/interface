# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from common.Logger import Logger
from common.parse_xml import Parse
from common.dataConnect import Database
from data import configure
from suds.client import Client
from configparser import ConfigParser
from math import ceil
import unittest
import logging
import os


class Manufacturer(unittest.TestCase):
	u"""
	测试厂商管理接口
	"""

	@classmethod
	def setUpClass(cls):
		cls.logger = Logger()
		logging.info("start test manufacturer")
		cls.data = Database()
		cls.url = configure.conf['url']
		cls.result = configure.conf['result']
		cls.file = configure.conf['result_file']
		cls.query = configure.manufacture['query']
		cls.tablename = configure.manufacture['tablename']
		cls.fields = configure.manufacture['manid'].split(',')
		cls.where = configure.manufacture['where']
		cls.client = Client(cls.url)

	def test_query_all(self):
		u"""
		测试厂商分页查询
		"""
		mysql = self.data.select(self.tablename, fields=['count(1)'])[0][0]  # 计算总记录数
		# 分页查询所有页的数据并断言
		page = ceil(mysql / 20)
		for current in range(1, page + 1):
			id_database_list = []
			man_id = self.data.select(self.tablename, self.fields, limit='%d,%d' % (current * 20 - 20, 20))
			for id in man_id:
				id_database_list.append(id[0])
			if_xml = Parse(self.query)
			if_xml.get_case_param(change=1, page=current, tag='Manufacturer')  # 修改xml分页数
			parm = if_xml.get_case_param(tag='Manufacturer')  # 获取接口参数
			response = self.client.service.bmpObjQuery(**parm)
			with open(self.file, 'w+', encoding='utf8') as f:  # 结果写入result.xml文件
				response = str(response).split('resultVal = "')[1].rstrip(' }').strip('"\n')
				print(response, file=f)
			
			rs_xml = Parse(self.result)
			id_xml_list = rs_xml.get_case_param(tag='Record/MAN_ID')
			id_xml_list = [int(man_id) for man_id in id_xml_list]

			logging.info(u'测试第 %d 页' % current)
			logging.info('id_xml_list: %s' % id_xml_list)
			logging.info('id_database_list: %s' % id_database_list)
			self.assertEqual(id_database_list, id_xml_list)

		# 断言总记录数
		logging.info('mysql result is %s' % mysql)
		re = rs_xml.get_case_param(total=1)
		self.assertEqual(mysql, int(re))

	def test_condition_query(self):
		u"""
		测试厂商按条件查询
		"""
		mysql = self.data.select(self.tablename, fields=['count(1)'], where_dic=self.where)[0][0]  # 计算总记录数
		# 分页查询所有页的数据并断言
		page = ceil(mysql / 20)
		for current in range(1, page + 1):
			id_database_list = []
			man_id = self.data.select(self.tablename, self.fields, self.where, limit='%d,%d' % (current * 20 - 20, 20))
			for id in man_id:
				id_database_list.append(id[0])
			if_xml = Parse(self.query)
			if_xml.get_case_param(change=1, page=current, tag='Manuquery')  # 修改xml分页数
			parm = if_xml.get_case_param(tag='Manuquery')  # 获取接口参数
			response = self.client.service.bmpObjQuery(**parm)
			with open(self.file, 'w+', encoding='utf8') as f:  # 结果写入result.xml文件
				response = str(response).split('resultVal = "')[1].rstrip(' }').strip('"\n')
				print(response, file=f)

			rs_xml = Parse(self.result)
			id_xml_list = rs_xml.get_case_param(tag='Record/MAN_ID')
			id_xml_list = [int(man_id) for man_id in id_xml_list]

			logging.info(u'测试第 %d 页' % current)
			logging.info('id_xml_list: %s' % id_xml_list)
			logging.info('id_database_list: %s' % id_database_list)
			self.assertEqual(id_database_list, id_xml_list)
		# 断言总记录数
		logging.info('mysql result is %s' % mysql)
		re = rs_xml.get_case_param(total=1)
		self.assertEqual(mysql, int(re))


	@classmethod
	def tearDownClass(cls):
		cls.data.close()
