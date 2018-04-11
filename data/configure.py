# !/usr/bin/env python3
# -*- coding = utf-8 -*-
import os

# http://10.0.190.103:8080/JNMP20/services/BMPSystemService?wsdl
conf = {
	'url': 'http://172.17.1.207:8080/SOC2.0/services/BMPSystemService?wsdl',
	'db': {
		'host': '172.17.1.213',
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
	'if_tag': 'Manufacturer',
	'result_tag': 'Record/MAN_ID',
	'tablename': 'bmp_manufacturers',
	'manid': 'MAN_ID',
	'where': {'MAN_NAME': '测试添加test_add'},
	'class2class': 'bmp_class2class',
	'attribtable': 'bmp_attribclass',
	'where_parent': {'parent_id': '11432'}
}

