# !/usr/bin/env python3
# -*- coding = utf-8 -*-

from suds.client import Client

url = 'http://172.17.1.206:8888/SOC2.0/services/BMPSystemService?wsdl '
client = Client(url)
print(client)