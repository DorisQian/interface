# !/usr/bin/env python3
# -*- coding = utf-8 -*-

import unittest
import time
import os
import HTMLTestRunnerCN
from common.Logger import log
from common.send_mail import SendMail


log = log(os.path.basename(__file__))
now = time.strftime('%Y-%m-%d_%H-%M-%S')


def create_suit():
    u"""
    遍历testCase文件夹，添加用例到testsuite
    :return: testunit
    """
    test_unit = unittest.TestSuite()
    test_dir = 'testCase'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py', top_level_dir=None)
    for case in discover:
        log.info('add case %s to testSuit' % case)
        test_unit.addTest(case)
    return test_unit

report_name = 'reports' + os.sep + now + '_result.html'
fp = open(report_name, 'wb')
log.info('generated report %s' % report_name)

runner = HTMLTestRunnerCN.HTMLTestRunner(
    stream=fp,
    title=u'SOC接口测试报告',
    tester='Doris'
)

if __name__ == '__main__':
    tests = create_suit()
    runner.run(tests)
    fp.close()
    path = os.path.abspath('.') + os.sep + 'reports' + os.sep
    SendMail().send_report(path)
