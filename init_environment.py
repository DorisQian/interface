# !/usr/bin/env python3
# -*- coding=utf-8 -*-

from common.Logger import log
from common.dataConnect import Database
from common.parse_xml import Parse
from suds.client import Client
from data import configure
import os
import time


class InitEnvironment:
	u"""
	初始化测试环境，增加基础数据
	"""
	def __init__(self):
		self.logger = log(os.path.basename(__file__))
		self.logger.info('start init environment···')
		self.data = Database()
		self.url = configure.conf['base_url'] + 'BMPSystemService?wsdl'
		self.para_xml = Parse('init_environment.xml')
		self.client = Client(self.url)

	def init_keyattention(self):
		u"""
		初始化重点关注
		先在数据库进行查询，如果存在pass，不存在insert
		:return:
		"""
		tablename = configure.keyattention['tablename']
		where = {'attention_name': '测试添加重点关注', 'log_type': '2'}
		count = self.data.select(tablename, fields=['ID'], where_dic=where)
		if str(count).isdigit():
			pass
		else:
			self.logger.info('add key attention dates')
			param = self.para_xml.get_case_param(tag='InsertAttention', para='objXml')
			param['tableName'] = 'NMP_KEYATTENTION'
			self.logger.info('最终参数： %s' % param)
			self.client.service.bmpObjInsert(**param)
			count = self.data.select(tablename, fields=['ID'], where_dic=where)
			if str(count).isdigit():
				self.logger.info('init key attention success!')
			else:
				self.logger.info('init key attention failed!')

	def init_manufacturers(self):
		u"""
		初始化厂商环境
		增加必要厂商
		增加相应资产
		:return:
		"""
		pass

	def init_knowledge(self):
		u"""
		初始化知识库
		增加知识库分类为10：漏洞信息的知识库，用于测试删除被引用分类时使用
		:return:
		"""
		tablename = configure.Knowledge['knowledge_table']
		where = {'knowledge_title': '初始化init添加知识库标题'}
		count = self.data.count(tablename, where_dic=where)
		if count == 1:
			pass
		else:
			self.logger.info('add knowledge dates')
			now = time.strftime('%Y-%m-%d %H:%M:%S')
			self.para_xml.update_value(node='InsertKnowledge/BMP_KNOWLEDGE/CREATE_TIME', value=now)
			self.para_xml.update_value(node='InsertKnowledge/BMP_KNOWLEDGE/UPDATE_TIME', value=now)
			param = self.para_xml.get_case_param(tag='InsertKnowledge', para='objXml')
			param['tableName'] = tablename
			self.logger.info('最终参数： %s' % param)
			self.client.service.bmpObjInsert(**param)
			self.data.commit()
			count = self.data.count(tablename, where_dic=where)
			if count == 1:
				self.logger.info('init knowledge success!')
			else:
				self.logger.info('init knowledge failed!')

		where_1 = {'knowledge_title': '测试多选删除1'}
		where_2 = {'knowledge_title': '测试多选删除2'}
		count_1 = self.data.count(tablename, where_dic=where_1)
		count_2 = self.data.count(tablename, where_dic=where_2)
		if count_1 == 1:
			pass
		else:
			self.logger.info('add knowledge for delete_1')
			now = time.strftime('%Y-%m-%d %H:%M:%S')
			self.para_xml.update_value(node='InsertKnowledgefordelete1/BMP_KNOWLEDGE/CREATE_TIME', value=now)
			self.para_xml.update_value(node='InsertKnowledgefordelete1/BMP_KNOWLEDGE/UPDATE_TIME', value=now)
			param = self.para_xml.get_case_param(tag='InsertKnowledgefordelete1', para='objXml')
			param['tableName'] = tablename
			self.logger.info('最终参数： %s' % param)
			self.client.service.bmpObjInsert(**param)
			self.data.commit()
			count = self.data.count(tablename, where_dic=where)
			if count == 1:
				self.logger.info('add knowledge success!')
			else:
				self.logger.info('add knowledge failed!')

		if count_2 == 1:
			pass
		else:
			self.logger.info('add knowledge for delete_2')
			now = time.strftime('%Y-%m-%d %H:%M:%S')
			self.para_xml.update_value(node='InsertKnowledgefordelete2/BMP_KNOWLEDGE/CREATE_TIME', value=now)
			self.para_xml.update_value(node='InsertKnowledgefordelete2/BMP_KNOWLEDGE/UPDATE_TIME', value=now)
			param = self.para_xml.get_case_param(tag='InsertKnowledgefordelete2', para='objXml')
			param['tableName'] = tablename
			self.logger.info('最终参数： %s' % param)
			self.client.service.bmpObjInsert(**param)
			self.data.commit()
			count = self.data.count(tablename, where_dic=where)
			if count == 1:
				self.logger.info('add knowledge success!')
			else:
				self.logger.info('add knowledge failed!')

	def start_init(self):
		self.init_keyattention()
		self.init_manufacturers()
		self.init_knowledge()

if __name__ == '__main__':
	init = InitEnvironment()
	init.start_init()

