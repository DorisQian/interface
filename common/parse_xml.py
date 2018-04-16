# !/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
import re
from common.dataConnect import Database
from xml.etree.ElementTree import ElementTree


class Parse:
	u"""
	传入接口参数xml文件，name
	最终获取需要的参数
	"""
	def __init__(self, name):
		u"""
		:param name:xml具体文件,以data为根目录
		"""
		self._log = Database.logging
		self._name = name
		self._path = os.getcwd().split('interface')[0] + 'interface' + os.sep + 'data' + os.sep
		self._file = self._path + self._name
		self._log.info(u'解析参数文件: %s' % self._file)
		self._tree = ElementTree(file=self._file)

	def _parse_xml(self):
		u"""
		解析xml，获取所有二层节点,根据节点拼接正则
		:return: 正则模型pattern 如['<test1>(.*?)</test1>', '<node2>(.*?)</node2>']
		"""
		roots = self._tree.getroot()
		pattern = []
		for node in roots:
			patt = '<%s>(.*?)</%s>' % (node.tag, node.tag)
			pattern.append(patt)
		return pattern

	def _get_parm(self, pattern):
		u"""
		通过正则匹配到标签，获取标签下数据，返回数据即接口参数
		:param pattern: 要匹配的正则，例如<Manufacturer>(.*?)</Manufacturer>
		:return: 获取到的参数，queryinfo，便签下的全部数据
		"""
		try:
			with open(self._file, 'r', encoding='utf8') as f:
				content = ''.join([i.strip() for i in f.readlines()])
			matches = re.findall(pattern, content)
			self._log.info(u'获取参数：%s' % matches)
			return matches
		except FileNotFoundError as msg:
			self._log.error(msg)

	def _get_total(self):
		u"""
		获得response中总记录条数
		:return: 返回记录数count（1）
		"""
		for elem in self._tree.iterfind('Record1/TotalCount'):
			total = elem.text
		try:
			self._log.info('parse xml get total:%s' % total)
			return total
		except UnboundLocalError as msg:
			self._log.error('there\'re no total node. The error message:%s' % msg)

	def _get_tag_value(self, node):
		u"""
		获取某标签中的value值，将标签名称为此的value写入list中
		:param node: 具体node参数
		:return: 返回最终值组成的list
		"""
		result = []
		for elem in self._tree.iterfind(node):
			result.append(elem.text)
		# logging.info('paras xml get tag value %s' % result)
		return result

	def _set_current_page(self, node, page):
		u"""
		修改显示的当前页数，实现翻页
		:param node: 要修改页数的二层根节点,string
		:param page: 修改成第page页
		:return: 重写xml文件
		"""
		full_node = node + '/SqlQuery/PageInfo/CurrentPage'
		for elem in self._tree.iterfind(full_node):
			elem.text = str(page)
		with open(self._file, 'wb') as f:
			self._tree.write(f, encoding='UTF-8', xml_declaration=True)

	def update_value(self, node, value):
		u"""
		修改xml内容
		:param node: 具体要修改的标签
		:param value: 修改后的值
		:return: 重写xml文件
		"""
		for elem in self._tree.iterfind(node):
			elem.text = str(value)
		with open(self._file, 'wb') as f:
			self._tree.write(f, encoding='UTF-8', xml_declaration=True)

	def get_case_param(self, total=0, change=0, page=1, tag='', para='queryInfo'):
		u"""
		封装xml各方法，实现参数、标签值的获取和xml的改变
		:param total: 是否计算total，一般与result.xml合用，1是获取，0不获取，默认为不获取
		:param change: 是否改变xml，一般与非结果xml合用，1为改变，默认为0不改变，改变显示页数
		:param page: 为当前页数current，page为改变值
		:param tag: 标签名称，例如'Record/MAN_ID'，'Manufacturer'
		:param para: 拼凑xml参数时，key的值，默认为queryInfo
		:return: 返回取值结果，接口参数param，total值 re，
		"""
		if self._name != 'result.xml' and change == 0:
			# 获取接口参数，访问接口，返回结果result
			pattern = self._parse_xml()
			try:
				for pat in pattern:
					if tag in pat:
						self._log.info(u'匹配正则: %s' % pat)
						param = self._get_parm(pat)
				parm = {para: param}
				return parm
			except UnboundLocalError as msg:
				self._log.error(u'没有匹配到正则，获取参数失败。error：%' % msg)

		elif self._name != 'result.xml' and change == 1:
			self._set_current_page(tag, page)

		elif self._name == 'result.xml' and total == 1:  # 解析结果文件，用以断言
			amount = self._get_total()  # 获取total值
			return amount
		else:
			tag_value = self._get_tag_value(tag)
			return tag_value


if __name__ == '__main__':
	a = Parse(name='bmpObjQuery.xml')

