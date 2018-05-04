# !/usr/bin/env python3
# -*- coding = utf-8 -*-
import os

# http://10.0.190.103:8080/JNMP20/services/BMPSystemService?wsdl
conf = {
	'base_url': 'http://172.17.1.208:8888/SOC2.0/services/',
	'db': {
		'host': '172.17.1.208',
		'port': 3306,
		'user': 'root',
		'password': 'Anchiva@123',
		'db': 'jnmp20db',
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

keyattention = {
	'origin': 'Keyattention.xml',
	'tablename': 'nmp_keyattention',
	'field_id': 'ID',
	'query_exact': {'ATTENTION_NAME': '测试添加重点关注'},
	'query_null': {'ATTENTION_NAME': '测试查询结果为空'},
	'query_add': {'ATTENTION_NAME': '测试接口I/F添加重点关注'}
}

knowledgetype = {
	'origin': 'Knowledge_type.xml',
	'tablename': 'BMP_KNOWLEDGETYPE',
	'field_id': 'TYPE_ID',
	'order_by': 'order by type_id desc',
	'query_add': {'TYPE_NAME': 'test添加I/F父类分类'},
	'query_add_child': {'TYPE_NAME': 'test添加I/F子类'},
	'query_update': {'TYPE_NAME': 'test修改I/F子类'}
}
