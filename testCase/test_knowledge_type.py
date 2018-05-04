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


class KnowledgeType(unittest.TestCase):
	u"""测试知识库分类"""

	@classmethod
	def setUpClass(cls):
		cls.logger = log(os.path.basename(__file__))
		cls.logger.info('start test knowledge type')
		cls.data = Database()
		cls.url = configure.conf['base_url'] + 'BMPSystemService?wsdl'
		cls.result = configure.conf['result']
		cls.origin = configure.knowledgetype['origin']
		# 查询参数
		cls.tablename = configure.knowledgetype['tablename']
		cls.field_id = configure.knowledgetype['field_id'].split(',')
		cls.query_add = configure.knowledgetype['query_add']
		cls.query_add_child = configure.knowledgetype['query_add_child']
		cls.query_update = configure.knowledgetype['query_update']
		cls.order_by = configure.knowledgetype['order_by']

		cls.client = Client(cls.url)
		cls.para_xml = Parse(cls.origin)
		cls.query = Query()

	def test_query(self):
		u"""测试知识库分类分页查询"""
		records = self.data.count(self.tablename)  # 计算总记录数
		# 分页查询所有页的数据并断言
		page = ceil(records / 20)
		if page:
			for current in range(1, page + 1):
				id_database_list = self.data.select(self.tablename, self.field_id, order=self.order_by,
													limit='%d,%d' % (current * 20 - 20, 20))
				self.data.commit()
				id_xml_list, total = self.query.get_query_result(self.origin, current, 'knowledgetype', 'Record/TYPE_ID')
				self.logger.info('id_database_list: %s' % id_database_list)
				self.assertEqual(id_database_list, id_xml_list)

			# 断言总记录数
			self.logger.info('mysql result is %s' % records)
			self.assertEqual(records, int(total))
		else:
			id_xml_list, total = self.query.get_query_result(self.origin, page, 'knowledgetype', 'Record/TYPE_ID')
			self.assertEqual(total, 0)

	def test_add_a_father_type(self):
		u"""测试成功添加父类别"""
		''' 添加后调用查询，查询最后一页数据'''
		param = self.para_xml.get_case_param(tag='InsertKnowledgeTypeFather', para='objXml')
		param['tableName'] = self.tablename
		self.logger.info('最终参数： %s' % param)
		response = self.client.service.bmpObjInsert(**param)
		new_id = self.data.select(self.tablename, self.field_id, self.query_add)
		self.logger.info('mysql data new_id is %s' % new_id)
		self.logger.info('response id is %s' % response['resultVal'])
		self.assertEqual(response['errorCode'], 0)
		self.assertEqual(response['errorString'], None)
		self.assertEqual(response['resultVal'], str(new_id))

		# 查询最后一页
		records = self.data.count(self.tablename)  # 计算总记录数
		page = ceil(records / 20)
		id_database_list = self.data.select(self.tablename, self.field_id, order=self.order_by,
											limit='%d,%d' % (page * 20 - 20, 20))

		id_xml_list, total = self.query.get_query_result(self.origin, page, 'knowledgetype', 'Record/TYPE_ID')
		self.assertEqual(id_database_list, id_xml_list)
		self.assertEqual(records, int(total))

	def test_add_child_type(self):
		u"""测试成功添加子类别"""
		''' 添加后调用查询，查询最后一页数据'''
		id = self.data.select(self.tablename, self.field_id, self.query_add)
		self.para_xml.update_value('InsertKnowledgeTypeChild/BMP_KNOWLEDGETYPE/PARENT_ID', id)
		param = self.para_xml.get_case_param(tag='InsertKnowledgeTypeChild', para='objXml')
		param['tableName'] = self.tablename
		self.logger.info('最终参数： %s' % param)
		response = self.client.service.bmpObjInsert(**param)
		self.data.commit()
		new_id = self.data.select(self.tablename, self.field_id, self.query_add_child)
		self.logger.info('mysql data new_id is %s' % new_id)
		self.logger.info('response id is %s' % response['resultVal'])
		self.assertEqual(response['errorCode'], 0)
		self.assertEqual(response['errorString'], None)
		self.assertEqual(response['resultVal'], str(new_id))
		record_id = self.data.select(self.tablename, fields=['parent_id'], where_dic=self.query_add_child)
		self.assertEqual(id, record_id)

		# 查询最后一页
		records = self.data.count(self.tablename)  # 计算总记录数
		page = ceil(records / 20)
		id_database_list = self.data.select(self.tablename, self.field_id, order=self.order_by,
											limit='%d,%d' % (page * 20 - 20, 20))

		id_xml_list, total = self.query.get_query_result(self.origin, page, 'knowledgetype', 'Record/TYPE_ID')
		self.assertEqual(id_database_list, id_xml_list)
		self.assertEqual(records, int(total))

	def test_update_knowledge_type(self):
		u"""测试修改知识库分类"""
		id = self.data.select(self.tablename, self.field_id, self.query_add_child)
		self.para_xml.update_value('UpdateKnowledgeType/BMP_KNOWLEDGETYPE/TYPE_ID', id)
		param = self.para_xml.get_case_param(tag='UpdateKnowledgeType', para='objXml')
		param['tableName'] = self.tablename
		self.logger.info('最终参数： %s' % param)
		response = self.client.service.bmpObjUpdate(**param)
		self.data.commit()
		record_id = self.data.select(self.tablename, fields=['parent_id'], where_dic=self.query_update)
		try:
			self.assertEqual(0, response['errorCode'])
			self.assertEqual('1', response['resultVal'])
			self.assertEqual(10, record_id)
		except Exception as msg:
			self.logger.warning(msg)
			raise

		# 查询最后一页
		records = self.data.count(self.tablename)  # 计算总记录数
		page = ceil(records / 20)
		id_database_list = self.data.select(self.tablename, self.field_id, order=self.order_by,
											limit='%d,%d' % (page * 20 - 20, 20))

		id_xml_list, total = self.query.get_query_result(self.origin, page, 'knowledgetype', 'Record/TYPE_ID')
		self.assertEqual(id_database_list, id_xml_list)
		self.assertEqual(records, int(total))

	def test_z_success_delete(self):
		u"""测试删除知识库分类"""
		del_id = self.data.select(self.tablename, self.field_id, self.query_update)
		parm = {'tableName': self.tablename, 'objId': del_id}
		response = self.client.service.bmpObjDelete(**parm)
		self.assertEqual(response['errorCode'], 0)
		self.assertEqual(response['errorString'], None)
		self.assertEqual(response['resultVal'], '1')

		# 查询最后一页
		self.data.commit()
		records = self.data.count(self.tablename)  # 计算总记录数
		page = ceil(records / 20)
		id_database_list = self.data.select(self.tablename, self.field_id, order=self.order_by,
											limit='%d,%d' % (page * 20 - 20, 20))
		id_xml_list, total = self.query.get_query_result(self.origin, page, 'knowledgetype', 'Record/TYPE_ID')
		self.assertEqual(id_database_list, id_xml_list)
		self.assertEqual(records, int(total))

	@classmethod
	def tearDownClass(cls):
		cls.data.close()
