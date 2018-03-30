# !/usr/bin/env python3
# -*- coding=utf-8 -*-

import unittest
from suds.client import Client
from common.Logger import Logger


class Login(unittest.TestCase):
    """
    test login interface
    """
    logger = Logger('INFO')

    @classmethod
    def setUpClass(cls):
        url = 'http://172.17.1.206:8888/SOC2.0/services/UUMSystemService?wsdl'
        cls.client = Client(url)
        #print(cls.client)

    def test_wrong_password(self):
        u"""
        密码错误
        :return:
        """
        param = {'loginId': 'cfgadmin', 'passWord': ''}
        result = self.client.service.uumCheckingUserLogin(**param)
        self.logger.info('wrong_password')
        self.logger.info(result)
        self.assertEqual(result['errorCode'], -1)
        self.assertIn(u"密码错误", result['errorString'])
        self.assertEqual(result['resultVal'], None)

    def test_right(self):
        u"""
        登录成功
        :return:
        """
        param = {'loginId': 'cfgadmin', 'passWord': 'password'}
        result = self.client.service.uumCheckingUserLogin(**param)
        self.logger.info('right')
        self.logger.info(result)
        self.assertEqual(result['errorCode'], 0)
        self.assertEqual(result['errorString'], None)
        self.assertIn('cfgadmin',result['resultVal'])

    @classmethod
    def tearDownClass(cls):
        pass

