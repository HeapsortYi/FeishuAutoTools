# coding: utf-8

import os.path as osp
import sys

sys.path.append(osp.dirname(osp.dirname(__file__)))

import biz.conf as cfg

# 应用凭证
app_id = "cli_xxxxxxxx"  # 登录开发者后台获取
app_secret = "xxxxxxxxxxx"  # 登录开发者后台获取

# tokens
tokens = []
token_txt_path = osp.join(cfg.proj_path, "feishu", "token.txt")
for line in open(token_txt_path):
    tokens.append(line.strip())
# user_access_token，用于获取用户资源
access_token = tokens[0]
# 刷新用户access_token时使用的 token
refresh_token = tokens[1]

# 接口地址
# 获取 app_access_token的接口
app_access_token_url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/"
# 请求身份验证的接口
request_id_authen_url = "https://open.feishu.cn/open-apis/authen/v1/index"
# 重定向url
redirect_uri = "https://open.feishu.cn/document"
# 获取登录用户身份的接口
access_token_url = "https://open.feishu.cn/open-apis/authen/v1/access_token"
# 刷新access_token的接口
refresh_access_token_url = "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token"
# 获取登录用户身份的接口（旧）
access_token_old_url = "https://open.feishu.cn/connect/qrconnect/oauth2/access_token/"

# 获取表格元数据的接口
metainfo_url = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{spreadsheetToken}/metainfo"
# 读取单个范围的接口
get_range_url = "https://open.feishu.cn/open-apis/sheet/v2/spreadsheets/{spreadsheetToken}/values/{range}"
