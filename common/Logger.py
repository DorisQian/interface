# !/usr/bin/env python3
# -*- coding=utf-8 -*-

import logging
import time
import os
from logging import handlers


class Logger:
    """
    output logs to console and log files
    """
    def __init__(self):
        U"""
        封装log类
        :return:
        """
        self.logging = logging
        self.logger = logging.getLogger()
        self.logger.setLevel('INFO')

        path = os.getcwd().split('interface')[0] + 'interface' + os.sep + 'logs' + os.sep
        date = time.strftime('%Y-%m-%d')
        file = path + date + '.log'

        ch = logging.StreamHandler()
        # ch.setLevel(self.level)

        # save five days log(backupcount)
        fh = handlers.TimedRotatingFileHandler(file, when='D', interval=1, backupCount=5, encoding='utf8')
        # fh.setLevel(self.level)
        fh.suffix = '%Y-%m-%d.log'

        log_format = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]  %(message)s')
        ch.setFormatter(log_format)
        fh.setFormatter(log_format)

        self.logger.addHandler(ch)
        self.logger.addHandler(fh)


if __name__ == '__main__':
    logger = Logger()
    logging.info('testing')
    logging.error('test111')
