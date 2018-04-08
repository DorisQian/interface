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

		self.tree = ElementTree(file=self.file)

	def parse_xml(self):
		u"""
		解析xml，获取所有节点信息,根据节点拼接正则
		:return: 正则模型pattern
		"""
		roots = self.tree.getroot()
		pattern = []
		for node in roots:
			patt = '<%s>(.*?)</%s>' % (node.tag, node.tag)
			pattern.append(patt)
		self.logger.info(u'正则模型：%s' % pattern)
		return pattern

	def get_parm(self, pattern):
		u"""
		:param pattern: 匹配的正则
		:return: 获取到的参数，queryinfo
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

	def get_total(self):
		u"""
		获得response中总记录条数
		:return: 返回记录数count（1）
		"""
		for elem in self.tree.iterfind('Record1/TotalCount'):
			total = elem.text
		self.logger.info('parse xml get total:%s' % total)
		return total

	def get_tag_value(self, node):
		u"""
		获取node中的value值，写入list中
		:param node: 具体node参数
		:return: 返回最终值组成的list
		"""
		result = []
		for elem in self.tree.iterfind(node):
			result.append(elem.text)
		self.logger.info('paras xml get tag value %s' % result)
		return result


if __name__ == '__main__':
	a = Parse(name='result.xml')
	a.get_tag_value('Record/MAN_ID')
