# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from common.Logger import Logger
from common.parse_xml import Parse
from suds.client import Client
from data import configure
import logging


class QueryPage:
	def __init__(self):
		self._url = configure.conf['url']
		self._client = Client(self._url)
		self._file = configure.conf['result_file']
		self._result = configure.conf['result']

	def get_page_result(self, xml, page, origintag='', resulttag=''):
		u"""
		分页数据查询
		:param xml: 原始数据的xml
		:param page: 当前页数，用以更改xml
		:param origintag: 原始数据xml中获取数据和要更改标签值的tag
		:param resulttag: response结果中获取断言值的tag
		:return:
		"""
		data_xml = Parse(xml)
		data_xml.get_case_param(change=1, page=page, tag=origintag)
		parm = data_xml.get_case_param(tag=origintag)  # 获取接口参数
		response = self._client.service.bmpObjQuery(**parm)
		with open(self._file, 'w+', encoding='utf8') as f:  # 结果写入result.xml文件
			response = str(response).split('resultVal = "')[1].rstrip(' }').strip('"\n')
			print(response, file=f)

		rs_xml = Parse(self._result)
		xml_list = rs_xml.get_case_param(tag=resulttag)
		xml_list = [int(man_id) for man_id in xml_list]
		total = rs_xml.get_case_param(total=1)
		logging.info(u'测试第 %d 页' % page)
		logging.info('xml_list: %s' % xml_list)
		return xml_list, total

if __name__ == '__main__':
	logger = Logger()
	p = QueryPage()
	re = p.get_page_result('Manufacturers.xml', 1, origintag='Manufacturer', resulttag='Record/MAN_ID')
	print(re)