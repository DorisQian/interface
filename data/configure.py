# !/usr/bin/env python3
# -*- coding = utf-8 -*-
import os

# http://10.0.190.103:8080/JNMP20/services/BMPSystemService?wsdl
conf = {
	'url': 'http://127.0.0.1:8080/SOC2.0/services/BMPSystemService?wsdl',
	'db': {
		'host': '192.168.0.120',
		'port': 3306,
		'user': 'root',
		'password': 'Anchiva@123',
		'db': 'cntv',
		'charset': 'utf8'
	},
	'result_file': os.getcwd().split('interface')[0] + 'interface' + os.sep + 'data' + os.sep + 'result.xml',
	'result': 'result.xml',
	'ini_file': os.getcwd().split('interface')[0] + 'interface' + os.sep + 'data' + os.sep + 'sqldata.ini'
}

manufacture = {
	'origin': 'Manufacturers.xml',
	'tablename': 'bmp_manufacturers',
	'field_manid': 'MAN_ID',
	'query_fuzzy': {'MAN_NAME': 'like 信'},
	'query_null': {'MAN_NAME': '测试查询结果为空'},
	'query_exact': {'MAN_NAME': '测试添加test_add'},
	'where_parent': {'parent_id': '11432'}
}

