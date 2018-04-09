# !/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import re
import logging
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
		self.path = os.path.abspath('../') + os.sep + 'data' + os.sep
		self.file = self.path + name
		logging.info(u'解析参数文件: %s' % self.file)
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
		logging.info(u'正则模型：%s' % pattern)
		return pattern

	def get_parm(self, pattern):
		u"""
		:param pattern: 匹配的正则
		:return: 获取到的参数，queryinfo
		"""
		try:
			with open(self.file, 'r', encoding='utf8') as f:
				content = ''.join([i.strip() for i in f.readlines()])
			# print(content)
			matches = re.findall(pattern, content)
			logging.info(u'获取参数：%s' % matches)
			return matches
		except FileNotFoundError as msg:
			logging.error(msg)

	def get_total(self):
		u"""
		获得response中总记录条数
		:return: 返回记录数count（1）
		"""
		for elem in self.tree.iterfind('Record1/TotalCount'):
			total = elem.text
		try:
			logging.info('parse xml get total:%s' % total)
			return total
		except UnboundLocalError as msg:
			logging.error('there\'re no total node. The error message:%s' % msg)

	def get_tag_value(self, node):
		u"""
		获取某标签中的value值，将标签名称为此的value写入list中
		:param node: 具体node参数
		:return: 返回最终值组成的list
		"""
		result = []
		for elem in self.tree.iterfind(node):
			result.append(elem.text)
		logging.info('paras xml get tag value %s' % result)
		return result

	def set_current_page(self, node, page):
		u"""
		修改显示的当前页数，实现翻页
		:param node: 要修改页数的二层根节点,string
		:param page: 修改成第page页
		:return: 重写xml文件
		"""
		full_node = node + '/SqlQuery/PageInfo/CurrentPage'
		for elem in self.tree.iterfind(full_node):
			elem.text = str(page)
		self.tree.write(self.file, encoding='utf8', xml_declaration=True)

if __name__ == '__main__':
	from common.Logger import Logger
	logger = Logger()
	a = Parse(name='bmpObjQuery.xml')
	a.get_total()
