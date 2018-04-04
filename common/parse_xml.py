# !/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import re
from common.Logger import Logger
from xml.etree.ElementTree import ElementTree


class Parse:
	u"""
	传入接口参数xml文件，name
	最终获取需要的参数
	"""
	def __init__(self, name):
		u"""
		:param name:xml具体文件
		"""
		self.logger = Logger('INFO')
		self.path = os.path.abspath('../') + os.sep + 'data' + os.sep
		self.file = self.path + name
		self.logger.info(u'解析参数文件: %s' % self.file)

	def parse_xml(self):
		u"""
		解析xml，获取所有节点信息
		:return: 正则模型pattern
		"""
		tree = ElementTree(file=self.file)
		roots = tree.getroot()
		pattern = []
		for node in roots:
			patt = '<%s>(.*?)</%s>' % (node.tag, node.tag)
			pattern.append(patt)
		self.logger.info(u'正则模型：%s' % pattern)
		return pattern

	def get_parm(self, pattern):
		u"""
		:param pattern: 匹配的正则
		:return: 获取到的参数
		"""
		try:
			with open(self.file, 'r') as f:
				content = ''.join([i.strip() for i in f.readlines()])
			print(content)
			matches = re.findall(pattern, content)
			self.logger.info(u'获取参数：%s' % matches)
			return matches
		except FileNotFoundError as msg:
			self.logger.error(msg)

if __name__ == '__main__':
	a = Parse(name='bmpObjQuery.xml')
	a.get_parm()
