# !/usr/bin/env python3
# -*- coding = utf-8 -*-

import smtplib
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from common.Logger import log

__author__ = 'Doris'


class SendMail:

    logger = log(os.path.basename(__file__))
    now = time.strftime('%Y-%m-%d')

    def send_mail(self, msg):
        host = 'smtp.sina.com'
        mail_user = 'doris_test'
        mail_pwd = 'admin@123'

        sender = 'doris_test@sina.com'
        receiver = '1609047552@qq.com'

        html = '''
                <html><body><h1>测试报告链接</h1><p>link <a href="http://172.17.1.213:8080/job/test_interface/测试报告/">report</a>...</p>
                <p><img src="cid:0"></p>
                </body></html>
                '''
        with open(msg, 'rb') as f:
            report = f.read()
        message = MIMEMultipart()
        message.attach(MIMEText(html, 'html', 'utf-8'))
        message.attach(MIMEText(report, 'html', 'utf-8'))
        message['From'] = Header('doris_test@sina.com')
        message['To'] = Header('1609047552@qq.com', 'utf-8')
        message['Subject'] = Header(u'SOC-interface测试报告', 'utf-8')

        attach = MIMEApplication(open(msg, 'rb').read())
        name = msg.split(os.sep)[-1]
        attach.add_header('Content-Disposition', 'attachment', filename=name)
        message.attach(attach)
        self.logger.info('attach reports')

        try:
            server = smtplib.SMTP(host, 25)
            server.login(mail_user, mail_pwd)
            server.sendmail(sender, receiver, message.as_string())
            self.logger.info('send email to %s successful' % receiver)
            server.close()
        except smtplib.SMTPException:
            self.logger.error('send email failed')
            server.close()

    def send_report(self, path):
        reports = os.listdir(path)
        reports.sort(key=lambda fn: os.path.getmtime(path + fn))
        self.logger.info('the newest report is %s' % reports[-1])
        file = os.path.join(path, reports[-1])
        self.logger.info('preparing send report %s' % file)
        self.send_mail(file)

