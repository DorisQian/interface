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
    def __init__(self, level):
        self.level = level

    def output_log(self, level, message):
        """
        :param level: set log level
        :param message: output to file or console
        :return:
        """
        logger = logging.getLogger()
        logger.setLevel(self.level)

        path = os.getcwd().split('interface')[0] + 'interface' + os.sep + 'logs' + os.sep
        date = time.strftime('%Y-%m-%d')
        file = path + date + '.log'
        # print(file)

        ch = logging.StreamHandler()
        ch.setLevel(self.level)

        # save five days log(backupcount)
        fh = handlers.TimedRotatingFileHandler(file, when='D', interval=1, backupCount=5, encoding='utf8')
        fh.setLevel(self.level)
        fh.suffix = '%Y-%m-%d.log'

        log_format = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]  %(message)s')
        ch.setFormatter(log_format)
        fh.setFormatter(log_format)

        logger.addHandler(ch)
        logger.addHandler(fh)

        if level == 'info':
            logging.info(message)
        elif level == 'debug':
            logging.debug(message)
        elif level == 'warning':
            logging.warning(message)
        elif level == 'error':
            logging.error(message)

        logger.removeHandler(ch)
        logger.removeHandler(fh)

    def debug(self, message):
        self.output_log('debug', message)

    def info(self, message):
        self.output_log('info', message)

    def warning(self, message):
        self.output_log('warning', message)

    def error(self, message):
        self.output_log('error', message)

'''
if __name__ == '__main__':
    logger = Logger('INFO')
    logger.info('testing')
'''