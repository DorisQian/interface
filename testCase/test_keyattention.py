# ! /usr/bin/env python3
# -*- coding = utf-8 -*-

from common.Logger import log
from common.parse_xml import Parse
from common.dataConnect import Database
from common.query import Query
from data import configure
from suds.client import Client
from math import ceil
import unittest
import os


class KeyAttention(unittest.TestCase):
	u"""测试重点关注接口"""

	@classmethod
	def setUpClass(cls):
		cls.logging = log(os.path.basename(__file__))
		cls.logging.info("start test key attention")
		cls.data = Database()
		cls.url = configure.conf['base_url'] + 'BMPSystemService?wsdl'
		cls.result = configure.conf['result']
		cls.origin = configure.keyattition['origin']
		# 查询参数
		cls.tablename = configure.keyattition['tablename']
		cls.field_id = configure.keyattition['field_id'].split(',')
		cls.query_exact = configure.keyattition['query_exact']

		cls.client = Client(cls.url)
		cls.para_xml = Parse(cls.origin)
		cls.query = Query()

	def test_query_all(self):
		u"""测试重点关注分页查询"""
		records = self.data.count(self.tablename)  # 计算总记录数
		# 分页查询所有页的数据并断言
		page = ceil(records / 20)
		if page:
			for current in range(1, page + 1):
				id_database_list = self.data.select(self.tablename, self.field_id,
													limit='%d,%d' % (current * 20 - 20, 20))
				id_xml_list, total = self.query.get_query_result(self.origin, current, 'keyattention', 'Record/ID')
				self.logging.info('id_database_list: %s' % id_database_list)
				self.assertEqual(id_database_list, id_xml_list)

			# 断言总记录数
			self.logging.info('mysql result is %s' % records)
			self.assertEqual(records, int(total))
		else:
			id_xml_list, total = self.query.get_query_result(self.origin, page, 'Manufacturer', 'Record/ID')
			self.assertEqual(total, 0)

	def test_query_exact(self):
		u"""测试重点关注按条件精确查询"""
		records = self.data.count(self.tablename, where_dic=self.query_exact)  # 计算总记录数

		# 分页查询所有页的数据并断言
		page = ceil(records / 20)
		try:
			for current in range(1, page + 1):
				id_database_list = self.data.select(self.tablename, self.field_id, self.query_exact,
													limit='%d,%d' % (current * 20 - 20, 20))
				id_xml_list, total = self.query.get_query_result(self.origin, current, 'Exact', 'Record/ID')
				self.assertEqual(id_database_list, id_xml_list)

			# 断言总记录数
			self.logging.info('mysql result is %s' % records)
			self.assertEqual(records, int(total))
		except UnboundLocalError:
			self.logging.warning('查询结果为空，测试中断')