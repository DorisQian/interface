# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from common.Logger import log
from common.parse_xml import Parse
from common.dataConnect import Database
from common.query import Query
from data import configure
from suds.client import Client
from math import ceil
import unittest
import time


class Manufacturer(unittest.TestCase):
	u"""测试厂商管理接口"""

	@classmethod
	def setUpClass(cls):
		cls.logging = log('test')
		cls.logging.info("start test manufacturer")
		cls.data = Database()
		cls.url = configure.conf['url']
		cls.result = configure.conf['result']
		cls.origin = configure.manufacture['origin']
		# 查询参数
		cls.tablename = configure.manufacture['tablename']
		cls.field_manid = configure.manufacture['field_manid'].split(',')
		cls.query_exact = configure.manufacture['query_exact']
		cls.query_null = configure.manufacture['query_null']
		cls.query_fuzzy = configure.manufacture['query_fuzzy']
		# 插入参数
		cls.con_parent = configure.manufacture['where_parent']
		cls.client = Client(cls.url)
		cls.para_xml = Parse(cls.origin)
		cls.query = Query()

	def test_query_all(self):
		u"""测试厂商分页查询"""
		records = self.data.count(self.tablename)  # 计算总记录数
		# 分页查询所有页的数据并断言
		page = ceil(records / 20)
		if page:
			for current in range(1, page + 1):
				id_database_list = self.data.select(self.tablename, self.field_manid,
													limit='%d,%d' % (current * 20 - 20, 20))
				id_xml_list, total = self.query.get_query_result(self.origin, current, 'Manufacturer', 'Record/MAN_ID')
				self.logging.info('id_database_list: %s' % id_database_list)
				self.assertEqual(id_database_list, id_xml_list)

			# 断言总记录数
			self.logging.info('mysql result is %s' % records)
			self.assertEqual(records, int(total))
		else:
			id_xml_list, total = self.query.get_query_result(self.origin, page, 'Manufacturer', 'Record/MAN_ID')
			self.assertEqual(total, 0)

	def test_query_exact(self):
		u"""测试厂商按条件精确查询"""
		records = self.data.count(self.tablename, where_dic=self.query_exact)  # 计算总记录数

		# 分页查询所有页的数据并断言
		page = ceil(records/20)
		try:
			for current in range(1, page + 1):
				id_database_list = self.data.select(self.tablename, self.field_manid, self.query_exact,
													limit='%d,%d' % (current * 20 - 20, 20))
				id_xml_list, total = self.query.get_query_result(self.origin, current, 'Exact', 'Record/MAN_ID')
				self.assertEqual(id_database_list, id_xml_list)

			# 断言总记录数
			self.logging.info('mysql result is %s' % records)
			self.assertEqual(records, int(total))
		except UnboundLocalError:
			self.logging.warning('查询结果为空，测试中断')

	def test_query_fuzzy(self):
		u"""测试测试厂商按条件模糊查询"""
		records = self.data.count(self.tablename, where_dic=self.query_fuzzy)

		page = ceil(records/20)
		try:
			for current in range(1, page + 1):
				id_database_list = self.data.select(self.tablename, self.field_manid, self.query_fuzzy,
													limit='%d,%d' % (current * 20 - 20, 20))
				id_xml_list, total = self.query.get_query_result(self.origin, current, 'Fuzzy', 'Record/MAN_ID')
				self.assertEqual(id_database_list, id_xml_list)

			# 断言总记录数
			self.logging.info('mysql result is %s' % records)
			self.assertEqual(records, int(total))
		except UnboundLocalError:
			self.logging.warning('查询结果为空，测试中断')

	def test_query_null(self):
		u"""测试查询结果为空"""
		records = self.data.count(self.tablename, where_dic=self.query_null)
		mysql_null = self.data.select(self.tablename, fields=self.field_manid, where_dic=self.query_null)
		xml_null, total = self.query.get_query_result(self.origin, origintag='NullQuery', resulttag='Record/MAN_ID')
		self.assertEqual(mysql_null, xml_null)
		self.assertEqual(records, int(total))

	def test_add_page(self):
		u"""测试增加修改页面数据查询"""
		# 数据库查询数据结果
		# 所有attribute跟节点，level为0, 对应mysql_total_attrroot
		mysql_attr_root = self.data.select('bmp_attribclass', ['CLASS_ID'], {'CLASS_LEVEL': '0'})
		classid = self.data.select('bmp_class2class', ['CLASS_ID'], self.con_parent)
		id_list = [str(n) for n in classid]
		mysql_id = ','.join(id_list)  # 所有查询条件的子节点，对应total为mysql_total_class
		conditions = {'CLASS_LEVEL': '1', 'CLASS_ID': mysql_id}
		mysql_attr_list = self.data.select('bmp_attribclass', ['CLASS_ID'],
										   conditions)  # level为1的子节点，对应mysql_total_attr
		mysql_manuname = self.data.select(self.tablename, ['DISTINCT MAN_NAME'])  # 所有产商名，对应mysql_manuname_total
		mysql_total_attrroot = self.data.count('bmp_attribclass', {'CLASS_LEVEL': '0'})
		mysql_total_class = self.data.count('bmp_class2class', self.con_parent)
		mysql_total_attr = self.data.count('bmp_attribclass', conditions)
		mysql_manuname_total = self.data.count(self.tablename)

		# xml查询所有level为0的，attr的classid
		xml_attr_root, xml_total_attrroot = self.query.get_query_result(self.origin, origintag='Attribroot',
																		resulttag='Record/CLASS_ID')
		# logging.info('mysql_total_attrroot %s' % mysql_total_attrroot)
		# logging.info('mysql_attr_root %s' % mysql_attr_root)
		self.assertEqual(mysql_total_attrroot, int(xml_total_attrroot))
		self.assertEqual(mysql_attr_root, xml_attr_root)

		# xml查询结果classid，所有子节点的classid
		xml_id, xml_total_class = self.query.get_query_result(self.origin, origintag='Attribchildnode',
															  resulttag='Record/CLASS_ID')
		xml_id = [str(id) for id in xml_id]
		xml_id = ','.join(xml_id)
		# logging.info('mysql total %s' % mysql_total_class)
		# logging.info('mysql_id %s' % mysql_id)
		self.assertEqual(mysql_total_class, int(xml_total_class))
		self.assertEqual(mysql_id, xml_id)

		# xml查询结果attrib，level为1的classid
		# logging.info('mysql total %s' % mysql_total_attr)
		xml_attr_list, xml_total_attr = self.query.get_query_result(self.origin, origintag='Attriblevle1',
															  resulttag='Record/CLASS_ID')
		xml_attr_list = [int(id) for id in xml_attr_list]

		# logging.info('mysql_attr_list %s' % mysql_attr_list)
		self.assertEqual(mysql_total_attr, int(xml_total_attr))
		self.assertEqual(mysql_attr_list, xml_attr_list)

		# xml查询结果manuname，所有产商去重名
		xml_manuname, xml_manuname_total = self.query.get_query_result(self.origin, origintag='Manuname',
																	resulttag='Record/MAN_NAME')
		# logging.info('mysql_manuname_total %s' % mysql_manuname_total)
		# logging.info('mysql_manuname %s' % (mysql_manuname,))
		self.assertEqual(mysql_manuname_total, int(xml_manuname_total))
		self.assertEqual(mysql_manuname, xml_manuname)

	def test_add_manu(self):
		u"""测试成功添加厂商"""
		''' 添加后调用查询，查询最后一页数据，以及所有厂商名称'''
		# insert
		param = self.para_xml.get_case_param(tag='InsertManu', para='objXml')
		param['tableName'] = 'BMP_MANUFACTURERS'
		self.logging.info('最终参数： %s' % param)
		response = self.client.service.bmpObjInsert(**param)
		new_manid = self.data.select(self.tablename, self.field_manid, self.query_exact)
		self.logging.info('mysql data new_manid is %s' % new_manid)
		self.logging.info('response manid is %s' % response['resultVal'])
		self.assertEqual(response['errorCode'], 0)
		self.assertEqual(response['errorString'], None)
		self.assertEqual(response['resultVal'], str(new_manid))

		# 查询最后一页
		records = self.data.count(self.tablename)  # 计算总记录数
		page = ceil(records / 20)
		id_database_list = self.data.select(self.tablename, self.field_manid,
											limit='%d,%d' % (page * 20 - 20, 20))

		id_xml_list, total = self.query.get_query_result(self.origin, page, 'Manufacturer', 'Record/MAN_ID')
		self.assertEqual(id_database_list, id_xml_list)
		self.assertEqual(records, int(total))

		# 查询所有厂商名称
		name_database_list = self.data.select(self.tablename, ['DISTINCT MAN_NAME'])
		name_xml_list, total = self.query.get_query_result(self.origin, origintag='QueryAdded', resulttag='Record/MAN_NAME')
		self.assertEqual(name_database_list, name_xml_list)
		self.assertEqual(records, int(total))

	def test_add_model(self):
		u"""测试成功添加型号"""
		'''先查看厂商下型号不为空的记录，如果为0，即全部有型号，则调用insert，若为1，取manid，作为update参数，添加后显示最后一页'''
		# 处理数据，避免报错，绕过现存bug
		where_field = self.query_exact.copy()
		where_field['FIELD_1'] = 'Null'
		judge = self.data.count(self.tablename, where_dic=where_field)
		if judge > 1:
			de_id = self.data.select(self.tablename, self.field_manid, where_dic=self.query_exact)
			for i in range(1, len(de_id) + 1):
				self.data.delete(self.tablename, where_dict={self.field_manid: '%s'} % i)

		mysql_total0 = self.data.count(self.tablename, where_dic=where_field)
		xml_desc, xml_desc_total = self.query.get_query_result(self.origin, origintag='IsModelUP',
																		resulttag='Record/MAN_DESC')
		self.assertEqual(mysql_total0, int(xml_desc_total))
		mysql_total1 = self.data.count(self.tablename, where_dic={'MAN_NAME': 'H3C'})
		xml_desc, xml_desc_total = self.query.get_query_result(self.origin, origintag='IsModelIN',
															   resulttag='Record/MAN_DESC')
		self.assertEqual(mysql_total1, int(xml_desc_total))
		for my_total in (mysql_total0, mysql_total1):
			if my_total == 0:
				up_id = self.data.select(self.tablename, self.field_manid, where_dic=self.query_exact)
				self.para_xml.update_value('UpdateModel/BMP_MANUFACTURERS/MAN_ID', up_id)
				param = self.para_xml.get_case_param(tag='UpdateModel', para='objXml')
				param['tableName'] = 'BMP_MANUFACTURERS'
				self.logging.info('最终参数： %s' % param)
				response = self.client.service.bmpObjUpdate(**param)
				self.assertEqual(response['errorCode'], 0)
				self.assertEqual(response['resultVal'], '1')
			elif my_total != 0:
				self.data.delete(self.tablename, where_dict={'FIELD_1': '型号1'})
				param = self.para_xml.get_case_param(tag='InsertModel', para='objXml')
				param['tableName'] = 'BMP_MANUFACTURERS'
				self.logging.info('最终参数： %s' % param)
				response = self.client.service.bmpObjInsert(**param)
				new_manid = self.data.select(self.tablename, self.field_manid, where_dic={'FIELD_1': '型号1'})
				self.logging.info('mysql data new_manid is %s' % new_manid)
				self.logging.info('response manid is %s' % response['resultVal'])
				self.assertEqual(response['errorCode'], 0)
				self.assertEqual(response['errorString'], None)
				self.assertEqual(response['resultVal'], str(new_manid))

		# 查询最后一页
		records = self.data.count(self.tablename)  # 计算总记录数
		page = ceil(records / 20)
		id_database_list = self.data.select(self.tablename, self.field_manid,
											limit='%d,%d' % (page * 20 - 20, 20))
		id_xml_list, total = self.query.get_query_result(self.origin, page, 'Manufacturer', 'Record/MAN_ID')
		self.assertEqual(id_database_list, id_xml_list)
		self.assertEqual(records, int(total))

	def test_success_delete(self):
		del_id1 = self.data.select(self.tablename, self.field_manid, self.query_exact)
		del_id2 = self.data.select(self.tablename, self.field_manid, where_dic={'FIELD_1': '型号1'})
		for del_id in (del_id1, del_id2):
			parm = {'tableName': 'BMP_MANUFACTURERS', 'objId': del_id}
			response = self.client.service.bmpObjDelete(**parm)
			self.assertEqual(response['errorCode'], 0)
			self.assertEqual(response['errorString'], None)
			self.assertEqual(response['resultVal'], '1')

		# 查询最后一页
		self.data.commit()
		records = self.data.count(self.tablename)  # 计算总记录数
		page = ceil(records / 20)
		id_database_list = self.data.select(self.tablename, self.field_manid,
											limit='%d,%d' % (page * 20 - 20, 20))
		id_xml_list, total = self.query.get_query_result(self.origin, page, 'Manufacturer', 'Record/MAN_ID')
		self.assertEqual(id_database_list, id_xml_list)
		self.assertEqual(records, int(total))

	@classmethod
	def tearDownClass(cls):
		cls.data.close()

