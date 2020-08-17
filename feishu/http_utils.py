# coding: utf-8
import requests
import json
import os.path as osp
import sys

sys.path.append(osp.dirname(osp.dirname(__file__)))

from biz.log_conf import logger


def get_http_request(url, headers=None, params=None):
    logger.info("发送get请求：url={url},".format(url=url))
    logger.info("headers={headers},params={params}".format(headers=headers, params=params))

    resp = requests.get(url, params=params, headers=headers)
    result = None
    if resp.ok:
        try:
            result = resp.json()
        except Exception as e:
            logger.error("返回json解析失败！")
            logger.exception(e)
    resp.close()
    return result


def post_http_request(url, headers=None, payload=None):
    logger.info("发送post请求：url={url},".format(url=url))
    logger.info("headers={headers},payload={payload}".format(headers=headers, payload=payload))

    payload = json.dumps(payload)
    resp = requests.post(url, data=payload, headers=headers)
    result = None
    if resp.ok:
        try:
            result = resp.json()
        except Exception as e:
            logger.error("返回json解析失败！")
            logger.exception(e)
    resp.close()
    return result
