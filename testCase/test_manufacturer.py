# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from common.Logger import Logger
from common.parse_xml import Parse
from common.dataConnect import Database
from data import configure
from suds.client import Client
from math import ceil
import unittest
import logging
import os


class Manufacturer(unittest.TestCase):
	u"""
	测试厂商管理接口
	"""
	logger = Logger()
	logging.info("start test manufacturer")
	data = Database()
	url = configure.conf['url']
	query = 'bmpObjQuery.xml'
	ro = 'result.xml'
	file = os.path.abspath('../data') + os.sep + 'result.xml'

	@staticmethod
	def operator_xml(name, total=0, change=0, page=1):
		xml = Parse(name)
		if name != 'result.xml' and change == 0:
			pattern = xml.parse_xml()
			# 获取接口参数，访问接口，返回结果result
			for pat in pattern:
				if 'Manufacturer' in pat:
					logging.info(u'匹配正则: %s' % pat)
					param = xml.get_parm(pat)
			parm = {'queryInfo': param}
			return parm
		elif name != 'result.xml' and change == 1:
			xml.set_current_page('Manufacturer', page)
		elif name == 'result.xml' and total == 1:  # 解析结果文件，用以断言
			re = xml.get_total()  # 获取total值
			return re
		# elif name == 'result.xml' and total == 0:
		else:
			tag_value = xml.get_tag_value('Record/MAN_ID')
			return tag_value

	@classmethod
	def setUpClass(cls):
		cls.client = Client(cls.url)

	def test_query_all(self):
		u"""
		查询厂商测试
		"""
		mysql = self.data.select(tablename='bmp_manufacturers', fields=['count(1)'])[0][0]  #计算总记录数

		# 分页查询所有页的数据并断言
		page = ceil(mysql / 20)
		for current in range(1, page + 1):
			id_database_list = []
			man_id = self.data.select(tablename='bmp_manufacturers', fields=['MAN_ID'], limit='%d,%d' % (current * 20 - 20, 20))
			for id in man_id:
				id_database_list.append(id[0])

			self.operator_xml(self.query, change=1, page=current)  # 修改xml分页数
			parm = self.operator_xml(self.query)
			result = self.client.service.bmpObjQuery(**parm)
			with open(self.file, 'w+', encoding='utf8') as f:  # 结果写入result.xml文件
				print(str(result).split('resultVal = "')[1].rstrip(' }').strip('"\n'), file=f)

			id_xml_list = self.operator_xml(self.ro)
			id_xml_list = [int(man_id) for man_id in id_xml_list]

			logging.info('id_xml_list: %s' % id_xml_list)
			logging.info('id_database_list: %s' % id_database_list)
			self.assertEqual(id_database_list, id_xml_list)
			self.assertEqual(result['errorCode'], 0)

		# 断言总记录数
		logging.info('mysql result is %s' % mysql)
		re = self.operator_xml(self.ro, total=1)
		self.assertEqual(mysql, int(re))

	@classmethod
	def tearDownClass(cls):
		pass
