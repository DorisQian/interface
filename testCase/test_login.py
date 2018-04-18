# !/usr/bin/env python3
# -*- coding=utf-8 -*-

from suds.client import Client
from common.Logger import log
from data.configure import conf
import unittest
import os


class Login(unittest.TestCase):
    """
    test login interface
    """

    @classmethod
    def setUpClass(cls):
        cls.logger = log(os.path.basename(__file__))
        cls.logger.info("Begin test Login...")
        cls.url = conf['base_url'] + 'UUMSystemService?wsdl'
        cls.client = Client(cls.url)

    def test_wrong_username(self):
        u"""无效用户"""
        param = {'loginId': 'wronguser', 'passWord': 'password'}
        response = self.client.service.uumCheckingUserLogin(**param)
        self.assertEqual(response['errorCode'], -1)
        self.assertEqual(response['errorString'], '无效的登录用户!')
        self.assertEqual(response['resultVal'], None)

    def test_wrong_password(self):
        u"""密码错误"""
        param = {'loginId': 'cfgadmin', 'passWord': ''}
        result = self.client.service.uumCheckingUserLogin(**param)
        self.logger.info('wrong_password')
        self.assertEqual(result['errorCode'], -1)
        self.assertIn(u"密码错误", result['errorString'])
        self.assertEqual(result['resultVal'], None)

    def test_right(self):
        u"""登录成功"""
        param = {'loginId': 'cfgadmin', 'passWord': 'password'}
        result = self.client.service.uumCheckingUserLogin(**param)
        self.logger.info('right')
        self.assertEqual(result['errorCode'], 0)
        self.assertEqual(result['errorString'], None)
        self.assertIn('cfgadmin', result['resultVal'])

    def test_logout(self):
        u"""登出"""
        auth = self.client.factory.create('userAuth')
        auth.userId = 19
        self.client.set_options(soapheaders=auth)
        response = self.client.service.uumLogout()
        self.logger.info('test_logout')
        self.assertEqual(response['errorCode'], 0)
        self.assertEqual(response['errorString'], None)
        self.assertEqual(response['resultVal'], None)

    @classmethod
    def tearDownClass(cls):
        pass

