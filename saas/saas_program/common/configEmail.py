import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from saas.saas_program import readConfig
import os
import logging
logging.basicConfig(level=logging.INFO)
#logging.disable(logging.INFO)

def sendEmail(title='saas接口自动化测试报告'):
    report=readConfig.get_testReport()
    emailManage=readConfig.get_emailManage()
    # smtp = smtplib.SMTP()
    # smtp.connect(emailManage["host"], emailManage["port"])
    smtp = smtplib.SMTP_SSL('smtp.51cto.com', 465)
    smtp.login(emailManage["account"], emailManage["password"])

    message = MIMEMultipart()
    # message['From'] = 'liaohx@51cto.com'
    message['From'] =emailManage["sendEmail"]
    message['To'] = emailManage["acceptEmail"]

    logging.info("邮件接收列表：%s"%emailManage["acceptEmail"])
    # message['To'] = 'liaohx@51cto.com'
    receipts=emailManage["acceptEmail"].split(',')
    title=title+':'+readConfig.get_testSheet()
    message['Subject'] = title
    # 暂时隐藏
    # with open(report, 'r',
    #           encoding='UTF-8') as f:
    #     content = f.read()
    #     logging.debug("替换前")
    #     logging.debug(content)
    #     content=content.replace("{ font-family: verdana, arial, helvetica, sans-serif; font-size: 80%; }","{ font-family: verdana, arial, helvetica, sans-serif; font-size: 13px; }")
    #     content = content.replace("class='hiddenRow'", 'class')
    #     logging.debug("替换后")
    #     logging.debug(content)
    # # 设置html格式参数
    # part1 = MIMEText(content, 'html', 'utf-8')
    # message.attach(part1)

    part1 = MIMEText("test", 'plain', 'utf-8')
    message.attach(part1)

    report_log = readConfig.get_testReport_log()
    with open(report_log, 'r',
              encoding='UTF-8') as n:
        content_log = n.read()
    part2 = MIMEText(content_log, 'base64', 'utf-8')
    part2["Content-Type"] = 'application/octet-stream'
    part2["Content-Disposition"] = 'attachment; filename=%s'%os.path.split(report_log)[1]
    message.attach(part2)
    
    for receipt in receipts:
        smtp.sendmail(emailManage["sendEmail"], receipt, message.as_string())
    smtp.quit()

