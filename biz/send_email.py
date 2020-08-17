# coding: utf-8

import os.path as osp
import sys

sys.path.append(osp.dirname(osp.dirname(__file__)))

import smtplib
from datetime import datetime
from email.header import Header
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate, formataddr
from email import encoders
from biz.log_conf import logger, logfile_path
import biz.conf as cfg


def send_mail(send_from, send_to, subject, message, server, smtp_port=465, files=[], sender_name=None,
              signature=None, username='', password='', use_tls=True):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        server (str): mail server host name
        smtp_port (int): smtp port number
        imap_port (int): imap port number
        files (list[str]): list of file paths to be attached to email
        sender_name (str): sender's nickname
        signature (str): sender's signature
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    msg = MIMEMultipart()
    msg['From'] = formataddr((str(Header(sender_name, 'utf-8')), send_from)) if sender_name else send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    message_html = "<p>" + message.replace("\n", "<br>").replace(" ", "&nbsp;") + "</p>"
    body_html_format = """
    <html>
    <head></head>
        <body>
        {body_content}
        </body>
    </html>
    """
    body_html = body_html_format.format(body_content=(message_html + '\n' + signature if signature else message_html))
    msg.attach(MIMEText(body_html, 'html'))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment', filename=Header(Path(path).name, 'utf-8').encode())
        msg.attach(part)

    # 使用smtp服务器发送邮件
    smtp = smtplib.SMTP_SSL(server, smtp_port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

    logger.info("邮件已成功投递，并保存到”已发送“文件夹！")


def run():
    """
    发送每日的邮件
    :return:
    """
    logger.info("####### 欢迎使用邮件发送助手！ #######")

    send_from = cfg.send_from
    send_to = cfg.send_to
    sender_name = cfg.sender_name
    username = cfg.username
    password = cfg.password
    server = cfg.smtp_server
    smtp_port = cfg.smtp_port

    dt = datetime.today()
    daily_report_path = osp.join(cfg.daily_report_path, "%s工作日报.docx" % dt.strftime("%m%d"))
    if osp.exists(daily_report_path):
        subject = "[{dt} 成功]今日日报".format(dt=dt.strftime("%Y-%m-%d %T"))
        body = "处理成功！日报见附件……"
        attachment_paths = [daily_report_path]
    else:  # 如果没生成日报，则发送log
        subject = "[{dt} 失败]今日日报".format(dt=dt.strftime("%Y-%m-%d %T"))
        body = "处理失败！log见附件……"
        attachment_paths = [logfile_path]

    send_mail(send_from, send_to, subject, body, server, smtp_port, attachment_paths,
              sender_name, username=username, password=password, use_tls=False)

    logger.info("####### 邮件发送完成！谢谢使用：) #######")


if __name__ == '__main__':
    run()
