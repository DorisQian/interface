# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from common.Logger import Logger
from common.parse_xml import Parse
from common.dataConnect import Database
from data import configure
from suds.client import Client
import unittest
import logging
import os


class Manufacturer(unittest.TestCase):
	u"""
	测试厂商管理接口
	"""
	logger = Logger()
	logging.info("start test manufacturer")
	database = Database()
	url = configure.conf['url']
	query = 'bmpObjQuery.xml'
	ro = 'result.xml'
	file = os.path.abspath('../data') + os.sep + 'result.xml'
	data = Database()

	@classmethod
	def setUpClass(cls):
		cls.client = Client(cls.url)

	def test_query_all(self):
		u"""
		查询厂商测试
		"""
		params = Parse(self.query)
		pattern = params.parse_xml()
		for pat in pattern:
			if 'Manufacturer' in pat:
				param = params.get_parm(pat)
				logging.info(u'匹配正则: %s' % pat)
		try:
			parm = {'queryInfo': param}
			result = self.client.service.bmpObjQuery(**parm)
			self.logger.logging.info('the result is %s' % result)

			# 结果写入result.xml文件
			with open(self.file, 'w+', encoding='utf8') as f:
				print(str(result).split('resultVal = "')[1].rstrip(' }').strip('"\n'), file=f)

			xml_result = Parse(self.ro)
			# 查询数据库进行断言
			re = xml_result.get_total()
			mysql = self.data.query('select count(1) from bmp_manufacturers')[0][0]
			logging.info('mysql result is %s' % mysql)
			self.assertEqual(mysql, int(re))

			id_database_list = []
			id_xml_list = xml_result.get_tag_value('Record/MAN_ID')
			id_xml_list = [int(man_id) for man_id in id_xml_list]
			man_id = self.data.query('select MAN_ID from bmp_manufacturers limit 20')
			for id in man_id:
				id_database_list.append(id[0])
			logging.info('id_xml_list: %s' % id_xml_list)
			logging.info('id_database_list: %s' % id_database_list)
			self.assertEqual(id_database_list, id_xml_list)
			self.assertEqual(result['errorCode'], 0)
			self.data.close()
		except UnboundLocalError:
			logging.error(u'没有可以匹配的正则，无参数传入，测试中断')

	@classmethod
	def tearDownClass(cls):
		pass
