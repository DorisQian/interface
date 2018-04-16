# !/usr/bin/env python3
# -*- coding=utf-8 -*-

import logging
import time
import os
from logging import handlers


def log(name):
    U"""
    封装logger
    :return:logging,供外部使用
    """
    logger = logging.getLogger(name)
    logger.setLevel('INFO')

    path = os.getcwd().split('interface')[0] + 'interface' + os.sep + 'logs' + os.sep
    file = path + 'interface'

    ch = logging.StreamHandler()
    # ch.setLevel(self.level)

    # save five days log(backupcount)
    fh = handlers.TimedRotatingFileHandler(file, when='D', interval=1, backupCount=5, encoding='utf8')
    # fh.setLevel(self.level)
    fh.suffix = '%Y-%m-%d.log'

    log_format = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]  %(message)s')
    ch.setFormatter(log_format)
    fh.setFormatter(log_format)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

if __name__ == '__main__':

    logging = log('test')
    logging.info('test')

