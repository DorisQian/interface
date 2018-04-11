# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from common.Logger import Logger
from common.parse_xml import Parse
from common.dataConnect import Database
from common.queryPage import QueryPage
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
		cls.origin = configure.manufacture['origin']
		# 查询参数
		cls.tablename = configure.manufacture['tablename']
		cls.fields = configure.manufacture['manid'].split(',')
		cls.where = configure.manufacture['where']
		# 插入参数
		cls.class2class = configure.manufacture['class2class']
		cls.attrib_table = configure.manufacture['attribtable']
		cls.con_parent = configure.manufacture['where_parent']

		cls.client = Client(cls.url)
		cls.para_xml = Parse(cls.origin)
		cls.query_page = QueryPage()

	def test_query_all(self):
		u"""
		测试厂商分页查询
		"""

		records = self.data.select(self.tablename, fields=['count(1)'])[0][0]  # 计算总记录数

		# 分页查询所有页的数据并断言
		page = ceil(records / 20)
		for current in range(1, page + 1):
			id_database_list = []
			man_id = self.data.select(self.tablename, self.fields, limit='%d,%d' % (current * 20 - 20, 20))
			for id in man_id:
				id_database_list.append(id[0])
			id_xml_list, total = self.query_page.get_page_result(self.origin, current, 'Manufacturer', 'Record/MAN_ID')
			logging.info('id_database_list: %s' % id_database_list)
			self.assertEqual(id_database_list, id_xml_list)

		# 断言总记录数
		logging.info('mysql result is %s' % records)
		self.assertEqual(records, int(total))

	def test_query_condition(self):
		u"""
		测试厂商按条件查询
		"""

		records = self.data.select(self.tablename, fields=['count(1)'], where_dic=self.where)[0][0]  # 计算总记录数

		# 分页查询所有页的数据并断言
		page = ceil(records / 20)
		for current in range(1, page + 1):
			id_database_list = []
			man_id = self.data.select(self.tablename, self.fields, self.where, limit='%d,%d' % (current * 20 - 20, 20))
			for id in man_id:
				id_database_list.append(id[0])
			id_xml_list, total = self.query_page.get_page_result(self.origin, current, 'Exact', 'Record/MAN_ID')
			self.assertEqual(id_database_list, id_xml_list)

		# 断言总记录数
		logging.info('mysql result is %s' % records)
		self.assertEqual(records, int(total))

	def test_add_page(self):
		u"""
		测试增加修改页面数据查询
		"""
		# 数据库查询数据结果
		attr_root = self.data.select(self.attrib_table, ['CLASS_ID'], {'CLASS_LEVEL': '0'})
		mysql_attr_root = [node[0] for node in attr_root]  # 所有attribute跟节点，level为0, 对应mysql_total_attrroot
		classid = self.data.select(self.class2class, ['CLASS_ID'], self.con_parent)
		id_list = [str(n[0]) for n in classid]
		mysql_id = ','.join(id_list)  # 所有查询条件的子节点，对应total为mysql_total_class
		logging.info('上一查询结果 %s' % mysql_id)
		conditions = {'CLASS_LEVEL': '1', 'CLASS_ID': mysql_id}
		mysql = self.data.select(self.attrib_table, ['CLASS_ID'], conditions)
		mysql_attr_list = [cid[0] for cid in mysql]  # level为1的子节点，对应mysql_total_attr
		mysql_manuname = self.data.select(self.tablename, ['DISTINCT MAN_NAME'])
		mysql_manuname = [name[0] for name in mysql_manuname]  # 所有产商名，对应mysql_manuname_total
		mysql_total_attrroot = self.data.select(self.attrib_table, ['count(1)'], {'CLASS_LEVEL': '0'})[0][0]
		mysql_total_class = self.data.select(self.class2class, ['count(1)'], self.con_parent)[0][0]
		mysql_total_attr = self.data.select(self.attrib_table, ['count(1)'], conditions)[0][0]
		mysql_manuname_total = self.data.select(self.tablename, ['count(1)'])[0][0]

		# xml查询所有level为0的，attr的classid
		query_xml = Parse(self.query)
		parm = query_xml.get_case_param(tag='Attribroot')
		response = self.client.service.bmpObjQuery(**parm)
		with open(self.file, 'w+', encoding='utf8') as f:
			print(str(response).split('resultVal = "')[1].rstrip(' }').strip('"\n'), file=f)

		root_xml = Parse(self.result)
		xml_total_attrroot = root_xml.get_case_param(total=1)
		xml_attr_root = root_xml.get_case_param(tag='Record/CLASS_ID')
		xml_attr_root = [int(root) for root in xml_attr_root]
		logging.info('mysql_total_attrroot %s' % mysql_total_attrroot)
		logging.info('mysql_attr_root %s' % mysql_attr_root)
		logging.info('xml_attr_root %s' % xml_attr_root)
		self.assertEqual(mysql_total_attrroot, int(xml_total_attrroot))
		self.assertEqual(mysql_attr_root, xml_attr_root)

		# xml查询结果classid，所有子节点的classid
		parm = query_xml.get_case_param(tag='Attribchildnode')
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

		# xml查询结果attrib，level为1的classid
		parm = query_xml.get_case_param(tag='Attriblevle1')
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

		# xml查询结果manuname，所有产商去重名
		parm = query_xml.get_case_param(tag='Manuname')
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

	def test_add_manu(self):
		u"""
		测试成功添加厂商
		"""
		# 添加后调用查询，查询最后一页数据，以及所有厂商名称
		# insert
		param = self.para_xml.get_case_param(tag='InsertManu', para='objXml')
		param['tableName'] = 'BMP_MANUFACTURERS'
		logging.info('最终参数： %s' % param)
		response = self.client.service.bmpObjInsert(**param)
		new_manid = self.data.select(self.tablename, ['MAN_ID'], self.where)
		new_manid = [str(id[0]) for id in new_manid]
		logging.info('mysql data new_manid is %s' % new_manid)
		logging.info('response manid is %s' % response['resultVal'])
		self.assertEqual(response['errorCode'], 0)
		self.assertEqual(response['errorString'], None)
		self.assertIn(response['resultVal'], new_manid)



	@classmethod
	def tearDownClass(cls):
		cls.data.close()
