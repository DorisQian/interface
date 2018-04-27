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
		cls.query_null = configure.keyattition['query_null']
		cls.query_add = configure.keyattition['query_add']

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

	def test_query_null(self):
		u"""测试查询结果为空"""
		records = self.data.count(self.tablename, where_dic=self.query_null)
		mysql_null = self.data.select(self.tablename, fields=self.field_id, where_dic=self.query_null)
		xml_null, total = self.query.get_query_result(self.origin, origintag='NullQuery', resulttag='Record/ID')
		self.assertEqual(mysql_null, xml_null)
		self.assertEqual(records, int(total))

	def test_add_attention(self):
		u"""测试成功添加重点关注"""
		''' 添加后调用查询，查询最后一页数据，以及所有关注名称'''
		param = self.para_xml.get_case_param(tag='InsertAttention', para='objXml')
		param['tableName'] = 'NMP_KEYATTENTION'
		self.logging.info('最终参数： %s' % param)
		response = self.client.service.bmpObjInsert(**param)
		new_id = self.data.select(self.tablename, self.field_id, self.query_add, limit='1, 2')
		self.logging.info('mysql data new_manid is %s' % new_id)
		self.logging.info('response manid is %s' % response['resultVal'])
		self.assertEqual(response['errorCode'], 0)
		self.assertEqual(response['errorString'], None)
		self.assertEqual(response['resultVal'], str(new_id))

		# 查询最后一页
		records = self.data.count(self.tablename)  # 计算总记录数
		page = ceil(records / 20)
		id_database_list = self.data.select(self.tablename, self.field_id,
											limit='%d,%d' % (page * 20 - 20, 20))

		id_xml_list, total = self.query.get_query_result(self.origin, page, 'keyattention', 'Record/ID')
		self.assertEqual(id_database_list, id_xml_list)
		self.assertEqual(records, int(total))

	def test_update_attention(self):
		u"""测试修改重点关注"""
		id = self.data.select(self.tablename, self.field_id, self.query_exact)
		update_xml = Parse(self.origin)
		update_xml.update_value('UpdateAttention/NMP_KEYATTENTION/ID', id)
		param = self.para_xml.get_case_param(tag='UpdateAttention', para='objXml')
		param['tableName'] = 'NMP_KEYATTENTION'
		self.logging.info('最终参数： %s' % param)
		response = self.client.service.bmpObjUpdate(**param)
		try:
			self.assertEqual(0, response['errorCode'])
			self.assertEqual('1', response['resultVal'])
		except Exception as msg:
			self.logging.warning(msg)
			raise

		# 查询最后一页
		records = self.data.count(self.tablename)  # 计算总记录数
		page = ceil(records / 20)
		id_database_list = self.data.select(self.tablename, self.field_id,
											limit='%d,%d' % (page * 20 - 20, 20))

		id_xml_list, total = self.query.get_query_result(self.origin, page, 'keyattention', 'Record/ID')
		self.assertEqual(id_database_list, id_xml_list)
		self.assertEqual(records, int(total))

		# 修改成原始状态
		update_xml.update_value('UpdateOrigin/NMP_KEYATTENTION/ID', id)
		param = self.para_xml.get_case_param(tag='UpdateOrigin', para='objXml')
		param['tableName'] = 'NMP_KEYATTENTION'
		self.logging.info('最终参数： %s' % param)
		self.client.service.bmpObjUpdate(**param)

	def test_success_delete(self):
		u"""测试删除重点关注"""
		del_id = self.data.select(self.tablename, self.field_id, self.query_add, limit='1, 2')
		# del_id2 = self.data.select(self.tablename, self.field_id, where_dic={'FIELD_1': '型号1'})
		parm = {'tableName': 'NMP_KEYATTENTION', 'objId': del_id}
		response = self.client.service.bmpObjDelete(**parm)
		self.assertEqual(response['errorCode'], 0)
		self.assertEqual(response['errorString'], None)
		self.assertEqual(response['resultVal'], '1')

		# 查询最后一页
		self.data.commit()
		records = self.data.count(self.tablename)  # 计算总记录数
		page = ceil(records / 20)
		id_database_list = self.data.select(self.tablename, self.field_id,
											limit='%d,%d' % (page * 20 - 20, 20))
		id_xml_list, total = self.query.get_query_result(self.origin, page, 'keyattention', 'Record/ID')
		self.assertEqual(id_database_list, id_xml_list)
		self.assertEqual(records, int(total))

	@classmethod
	def tearDownClass(cls):
		cls.data.close()
