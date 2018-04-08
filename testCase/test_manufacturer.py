# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from common.Logger import Logger
from common.parse_xml import Parse
from common.dataConnect import Database
from data import configure
from suds.client import Client
import unittest
import os


class Manufacturer(unittest.TestCase):
	u"""
	测试厂商管理接口
	"""
	logger = Logger('INFO')
	logger.info("start test manufacturer")
	database = Database()
	url = configure.conf['url']
	query = 'bmpObjQuery.xml'
	ro = 'result.xml'
	file = os.path.abspath('../data') + os.sep + 'result.xml'
	data = Database()

	@classmethod
	def setUpClass(cls):
		cls.client = Client(cls.url)

	def test_query_manufacturer(self):
		u"""
		查询厂商测试
		"""
		params = Parse(self.query)
		pattern = params.parse_xml()
		for pat in pattern:
			if 'manufacturer' in pat:
				param = params.get_parm(pat)
				self.logger.info(u'匹配正则: %s' % pat)
		parm = {'queryInfo': param}
		result = self.client.service.bmpObjQuery(**parm)
		self.logger.info('the result is %s' % result)

		# 结果写入result.xml文件
		with open(self.file, 'w+', encoding='utf8') as f:
			print(str(result).split('resultVal = "')[1].rstrip(' }').strip('"\n'), file=f)

		# 查询数据库进行断言
		mysql = self.data.query('select count(1) from bmp_manufacturers')[0][0]
		re = Parse(self.ro).get_total()
		self.assertEqual(result['errorCode'], 0)
		self.assertEqual(mysql, int(re))
		man_id = self.data.query('select MAN_ID from bmp_manufacturers limit 20')
		self.data.db.close()
		print(man_id)

	@classmethod
	def tearDownClass(cls):
		pass
