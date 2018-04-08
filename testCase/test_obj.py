# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from suds.client import Client
from common.parse_xml import Parse
from data import configure
from common.Logger import Logger
import unittest
import os


class Device(unittest.TestCase):
	"""
	test device operation
	"""

	url = configure.conf['url']
	logger = Logger('INFO')
	logger.info('start device······')

	@classmethod
	def setUpClass(cls):
		cls.client = Client(cls.url)
		cls.header = cls.client.factory.create('userAuth')
		cls.header.loginId = 'cfgadmin'
		cls.header.userId = 19
		cls.client.set_options(soapheaders=[cls.header, ])
		cls.logger.info('the header is %s' % cls.header)

	def test_query_obj(self):
		u"""
		查询资产接口测试
		"""
		path = 'bmpObjQuery.xml'
		params = Parse(path)
		pattern = params.parse_xml()
		for pa in pattern:
			if 'test1' in pa:
				param = params.get_parm(pa)
		parm = {'queryInfo': param}
		result = self.client.service.bmpObjQuery(**parm)
		self.logger.info('the result is %s' % result)
		file = os.path.abspath('../data') + os.sep + 'result.xml'
		with open(file, 'w+', encoding='utf8') as f:
			print(str(result).split('resultVal = "')[1].rstrip(' }').strip('"\n'), file=f)

	@classmethod
	def tearDownClass(cls):
		pass
