# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from suds.client import Client
from common.parse_xml import Parse

url = 'http://10.0.190.103:8080/JNMP20/services/BMPSystemService?wsdl'
client = Client(url)
header = client.factory.create('userAuth')
header.loginId = 'cfgadmin'
header.userId = 19

client.set_options(soapheaders=[header, ])
print(header)


path = 'bmpObjQuery.xml'
params = Parse(path)
pattern = params.parse_xml()
for pa in pattern:
	if 'test1' in pa:
		param = params.get_parm(pa)
parm = {'queryInfo': param}
result = client.service.bmpObjQuery(**parm)
print(result)