# coding: utf-8
from urllib.parse import quote
import os.path as osp
import sys

sys.path.append(osp.dirname(osp.dirname(__file__)))

import feishu.conf as cfg
from feishu.http_utils import get_http_request, post_http_request
from biz.log_conf import logger


def app_access_token_api():
    """
    企业自建应用通过此接口获取 app_access_token，调用接口获取应用资源时，需要使用 app_access_token 作为授权凭证
    :return:
    """
    app_access_token_url = cfg.app_access_token_url
    headers = {"Content-Type": "application/json"}
    payload = {
        "app_id": cfg.app_id,
        "app_secret": cfg.app_secret,
    }
    result = post_http_request(app_access_token_url, headers=headers, payload=payload)
    return result


def _get_app_access_token():
    result = app_access_token_api()
    if not result:
        logger.error("app_access_token post请求失败！返回结果为None！")
        return None
    if result["code"] != 0:
        logger.error("app_access_token接口请求失败！code: %s, msg: %s" % (result["code"], result["msg"]))
        return None
    app_access_token = result["app_access_token"]

    return app_access_token


def request_id_authen_api():
    """
    应用请求用户身份验证时，需按如下方式构造登录链接，并引导用户跳转至此链接。
    飞书客户端内用户免登，系统浏览器内用户需完成扫码登录。
    登录成功后会生成登录预授权码 code，并作为参数重定向到重定向URL。
    :return:
    """
    request_id_authen_url = cfg.request_id_authen_url
    params = {"redirect_uri": quote(cfg.redirect_uri), "app_id": cfg.app_id}

    result = get_http_request(request_id_authen_url, params=params)
    return result


def access_token_api(authen_code):
    """
    通过此接口获取登录预授权码 code 对应的登录用户身份。
    :return:
    """
    # 先获取app_access_token
    app_access_token = _get_app_access_token()
    if not app_access_token:
        return None

    access_token_url = cfg.access_token_url
    headers = {"Content-Type": "application/json"}
    payload = {
        "app_access_token": app_access_token,
        "grant_type": "authorization_code",
        "code": authen_code
    }
    result = post_http_request(access_token_url, headers=headers, payload=payload)
    return result


def refresh_access_token_api():
    """
    该接口用于在 access_token 过期时用 refresh_token 重新获取 access_token。
    此时会返回新的 refresh_token，再次刷新 access_token 时需要使用新的 refresh_token。
    :return:
    """
    # 先获取app_access_token
    app_access_token = _get_app_access_token()
    if not app_access_token:
        return None

    refresh_access_token_url = cfg.refresh_access_token_url
    headers = {"Content-Type": "application/json"}
    payload = {
        "app_access_token": app_access_token,
        "grant_type": "refresh_token",
        "refresh_token": cfg.refresh_token
    }
    result = post_http_request(refresh_access_token_url, headers=headers, payload=payload)
    return result


def access_token_old_api(authen_code):
    """
    通过此接口获取登录用户身份（疑似是一个旧接口）
    :param authen_code:
    :return:
    """
    # 先获取app_access_token
    app_access_token = _get_app_access_token()
    if not app_access_token:
        return None

    access_token_old_url = cfg.access_token_old_url
    headers = {"Content-Type": "application/json"}
    payload = {
        "app_id": cfg.app_id,
        "app_secret": cfg.app_secret,
        "app_access_token": app_access_token,
        "grant_type": "authorization_code",
        "code": authen_code,
    }
    result = post_http_request(access_token_old_url, headers=headers, payload=payload)
    return result


if __name__ == '__main__':
    # 用户登录预授权码。扫描二维码可得到，5分钟内有效，只能使用一次。
    # 第一次使用时，构造一个https://open.feishu.cn/open-apis/authen/v1/index?redirect_uri={跳转url}&app_id={app_id}
    # 的链接，扫描二维码后开放平台生成登录预授权码，302跳转至重定向地址
    authen_code_ = "T6eOTVAwc1idLrSS8ynEKa"
    rst = access_token_api(authen_code_)
    print(rst)
