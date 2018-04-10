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

	@classmethod
	def setUpClass(cls):
		cls.logger = Logger()
		logging.info("start test manufacturer")
		cls.data = Database()
		cls.url = configure.conf['url']
		cls.result = configure.conf['result']
		cls.file = configure.conf['result_file']
		cls.query = configure.manufacture['query']
		# 查询参数
		cls.tablename = configure.manufacture['tablename']
		cls.fields = configure.manufacture['manid'].split(',')
		cls.where = configure.manufacture['where']
		# 插入参数
		cls.class2class = configure.manufacture['class2class']
		cls.attrib_table = configure.manufacture['attribtable']
		cls.con_parent = configure.manufacture['where_parent']

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

	def test_add_page(self):
		u"""
		测试增加修改页面数据查询
		"""
		# 数据库查询数据结果
		classid = self.data.select(self.class2class, ['CLASS_ID'], self.con_parent)
		id_list = [str(n[0]) for n in classid]
		mysql_id = ','.join(id_list)
		logging.info('上一查询结果 %s' % mysql_id)
		conditions = {'CLASS_LEVEL': '1', 'CLASS_ID': mysql_id}
		mysql = self.data.select(self.attrib_table, ['CLASS_ID'], conditions)
		mysql_attr_list = [cid[0] for cid in mysql]
		mysql_manuname = self.data.select(self.tablename, ['DISTINCT MAN_NAME'])
		mysql_manuname = [name[0] for name in mysql_manuname]
		mysql_total_class = self.data.select(self.class2class, ['count(1)'], self.con_parent)[0][0]
		mysql_total_attr = self.data.select(self.attrib_table, ['count(1)'], conditions)[0][0]
		mysql_manuname_total = self.data.select(self.tablename, ['count(1)'])[0][0]

		# xml查询结果classid
		class_xml = Parse(self.query)
		parm = class_xml.get_case_param(tag='Attribchildnode')
		response = self.client.service.bmpObjQuery(**parm)
		with open(self.file, 'w+', encoding='utf8') as f:
			print(str(response).split('resultVal = "')[1].rstrip(' }').strip('"\n'), file=f)

		rs_xml = Parse(self.result)
		xml_total_class = rs_xml.get_case_param(total=1)
		xml_id = ','.join(rs_xml.get_case_param(tag='Record/CLASS_ID'))
		logging.info('mysql total %s' % mysql_total_class)
		logging.info('mysql_id %s' % mysql_id)
		logging.info('xml_id %s' % xml_id)
		self.assertEqual(mysql_total_class, int(xml_total_class))
		self.assertEqual(mysql_id, xml_id)

		# xml查询结果attrib
		attr_xml = Parse(self.query)
		parm = attr_xml.get_case_param(tag='Attriblevle1')
		response = self.client.service.bmpObjQuery(**parm)
		with open(self.file, 'w+', encoding='utf8') as f:
			print(str(response).split('resultVal = "')[1].rstrip(' }').strip('"\n'), file=f)

		ro_xml = Parse(self.result)
		xml_total_attr = ro_xml.get_case_param(total=1)
		xml_attr_list = ro_xml.get_case_param(tag='Record/CLASS_ID')
		xml_attr_list = [int(id) for id in xml_attr_list]
		logging.info('mysql total %s' % mysql_total_attr)
		logging.info('mysql_attr_list %s' % mysql_attr_list)
		logging.info('xml_attr_list %s' % xml_attr_list)
		self.assertEqual(mysql_total_attr, int(xml_total_attr))
		self.assertEqual(mysql_attr_list, xml_attr_list)

		# xml查询结果manuname
		manu_xml = Parse(self.query)
		parm = manu_xml.get_case_param(tag='Manuname')
		response = self.client.service.bmpObjQuery(**parm)
		with open(self.file, 'w+', encoding='utf8') as f:
			print(str(response).split('resultVal = "')[1].rstrip(' }').strip('"\n'), file=f)

		r_xml = Parse(self.result)
		xml_manuname_total = r_xml.get_case_param(total=1)
		xml_manuname = r_xml.get_case_param(tag='Record/MAN_NAME')
		logging.info('mysql_manuname_total %s' % mysql_manuname_total)
		logging.info('mysql_manuname %s' % (mysql_manuname, ))
		logging.info('xml_manuname %s' % xml_manuname)
		self.assertEqual(mysql_manuname_total, int(xml_manuname_total))
		self.assertEqual(mysql_manuname, xml_manuname)

	@classmethod
	def tearDownClass(cls):
		cls.data.close()
