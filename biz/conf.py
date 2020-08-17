# coding: utf-8

import os
from datetime import date, timedelta

# spreadsheet 的 token
# 获取方式参考https://open.feishu.cn/document/ugTM5UjL4ETO14COxkTN/uczNzUjL3czM14yN3MTN 第4项
spreadsheetToken = "shtxxxxxx"

# 日期
today = date.today()

# 路径
proj_path = os.path.dirname(os.path.dirname(__file__))
excel_path = os.path.join(proj_path, "template", "日报汇总.xlsx")
daily_report_path = os.path.join(proj_path, "daily_reports")

# 邮箱相关配置，请修改为自己的信息
username = "xxx@example.com"  # 登录名，修改成自己的
password = "xxxxxxxxx"  # 登陆密码，修改成自己的
sender_name = "HeapsortYi"  # 发件人的名字，修改成自己的
send_from = username  # 发件人。一般与登录名相同
send_to = [username]    # 收件人

# 邮箱服务器及端口号
smtp_server = "smtp.example.com"  # smtp服务器
smtp_port = 465  # smtp端口号
imap_server = "imap.example.com"  # imap服务器
imap_port = 993  # imap端口号
