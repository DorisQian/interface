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
import time


class Knowledge(unittest.TestCase):
	u"""测试知识库"""
	@classmethod
	def setUpClass(cls):
		cls.logger = log(os.path.basename(__file__))
		cls.logger.info('start test knowledge type')
		cls.data = Database()
		cls.url = configure.conf['base_url'] + 'BMPSystemService?wsdl'
		cls.result = configure.conf['result']
		cls.origin = configure.knowledgetype['origin']
		# 查询参数
		cls.k_table = configure.Knowledge['knowledge_table']
		cls.c_table = configure.Knowledge['comment_table']
		cls.k_id = configure.Knowledge['k_id'].split(',')
		cls.c_id = configure.Knowledge['c_id'].split(',')
		cls.query_add_k = configure.Knowledge['query_add_k']
		cls.query_add_c = configure.Knowledge['query_add_c']
		# cls.query_update = configure.knowledgetype['query_update']
		# cls.order_by = configure.knowledgetype['order_by']

		cls.client = Client(cls.url)
		cls.para_xml = Parse(cls.origin)
		cls.query = Query()

	def test_add_knowledge(self):
		u"""测试添加知识库"""
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		self.para_xml.update_value(node='InsertKnowledge/BMP_KNOWLEDGE/CREATE_TIME', value=now)
		self.para_xml.update_value(node='InsertKnowledge/BMP_KNOWLEDGE/UPDATE_TIME', value=now)
		param = self.para_xml.get_case_param(tag='InsertKnowledge', para='objXml')
		param['tableName'] = self.k_table
		self.logger.info('最终参数： %s' % param)
		response = self.client.service.bmpObjInsert(**param)
		new_id = self.data.select(self.k_table, self.k_id, self.query_add_k)
		self.logger.info('mysql data new_id is %s' % new_id)
		self.logger.info('response id is %s' % response['resultVal'])
		self.assertEqual(response['errorCode'], 0)
		self.assertEqual(response['errorString'], None)
		self.assertEqual(response['resultVal'], str(new_id))

	def test_add_k_comment(self):
		u"""测试添加评论"""
		k_id = self.data.select(self.k_table, self.k_id, self.query_add_k)
		self.para_xml.update_value(node='InsertComment/BMP_KNOWLEDGECOMMENT/KNOWLEDGE_ID', value=k_id)
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		self.para_xml.update_value(node='InsertComment/BMP_KNOWLEDGECOMMENT/CREATE_TIME', value=now)
		param = self.para_xml.get_case_param(tag='InsertComment', para='objXml')
		param['tableName'] = self.c_table
		self.logger.info('最终参数： %s' % param)
		response = self.client.service.bmpObjInsert(**param)
		new_id = self.data.select(self.c_table, self.c_id, self.query_add_c)
		self.logger.info('mysql data new_id is %s' % new_id)
		self.logger.info('response id is %s' % response['resultVal'])
		self.assertEqual(response['errorCode'], 0)
		self.assertEqual(response['errorString'], None)
		self.assertEqual(response['resultVal'], str(new_id))

	def test_update_knowledge(self):
		u"""测试修改知识库"""
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		self.para_xml.update_value(node='UpdateKnowledge/BMP_KNOWLEDGE/UPDATE_TIME', value=now)
		k_id = self.data.select(self.k_table, self.k_id, self.query_add_k)
		self.para_xml.update_value(node='UpdateKnowledge/BMP_KNOWLEDGE/KNOWLEDGE_ID', value=k_id)
		param = self.para_xml.get_case_param(tag='UpdateKnowledge', para='objXml')
		param['tableName'] = self.k_table
		self.logger.info('最终参数： %s' % param)
		response = self.client.service.bmpObjUpdate(**param)
		self.data.commit()
		type_id = self.data.select('bmp_knowledge2type', fields=['type_id'], where_dic={'knowledge_id': k_id})
		title = self.data.select(self.k_table, fields=['knowledge_title'], where_dic={'knowledge_id': k_id})
		summary = self.data.select(self.k_table, fields=['KNOWLEDGE_SUMMARY'], where_dic={'knowledge_id': k_id})
		content = self.data.select(self.k_table, fields=['KNOWLEDGE_CONTENT'], where_dic={'knowledge_id': k_id})
		source = self.data.select(self.k_table, fields=['KNOWLEDGE_SOURCE'], where_dic={'knowledge_id': k_id})
		try:
			self.assertEqual(0, response['errorCode'])
			self.assertEqual('1', response['resultVal'])
			self.assertEqual(11, type_id)
			self.assertEqual(u'test修改知识库标题', title)
			self.assertEqual(u'test修改关键字', summary)
			self.assertEqual(u'@test知识库内容修改@', content)
			self.assertEqual(u'test来源修改', source)
		except Exception as msg:
			self.logger.warning(msg)
			raise

	def test_update_comment(self):
		u"""测试修改评论"""
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		self.para_xml.update_value(node='UpdateComment/BMP_KNOWLEDGECOMMENT/CREATE_TIME', value=now)
		k_id = self.data.select(self.k_table, self.k_id, self.query_add_k)
		self.para_xml.update_value(node='UpdateComment/BMP_KNOWLEDGECOMMENT/KNOWLEDGE_ID', value=k_id)
		c_id = self.data.select(self.c_table, self.c_id, self.query_add_c)
		self.para_xml.update_value(node='UpdateComment/BMP_KNOWLEDGECOMMENT/COMMENT_ID', value=c_id)
		param = self.para_xml.get_case_param(tag='UpdateComment', para='objXml')
		param['tableName'] = self.k_table
		self.logger.info('最终参数： %s' % param)
		response = self.client.service.bmpObjUpdate(**param)
		self.data.commit()
		content = self.data.select(self.c_table, fields=['comment_content'], where_dic={'comment_id': c_id})
		try:
			self.assertEqual(0, response['errorCode'])
			self.assertEqual('1', response['resultVal'])
			self.assertEqual(u'@test添加第一条评论-编辑评论@', content)
		except Exception as msg:
			self.logger.warning(msg)
			raise

	def test_query_integration(self):
		u"""测试整合有所信息筛选"""


	@classmethod
	def tearDownClass(cls):
		cls.data.close()
