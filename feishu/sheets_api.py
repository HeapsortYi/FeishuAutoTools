# coding: utf-8

import os.path as osp
import sys

sys.path.append(osp.dirname(osp.dirname(__file__)))

import feishu.conf as cfg
from feishu.http_utils import get_http_request


def metainfo_api(spreadsheetToken):
    """
    该接口用于根据 spreadsheetToken 获取表格元数据。
    :return:
    """
    metainfo_url = cfg.metainfo_url.format(spreadsheetToken=spreadsheetToken)
    headers = {
        "Authorization": "Bearer " + cfg.access_token,
        "Content-Type": "application/json"
    }
    result = get_http_request(metainfo_url, headers=headers)
    return result


def get_range_api(spreadsheetToken, sheet_id, range, valueRenderOption=False):
    """
    该接口用于根据 spreadsheetToken 和 range 读取表格单个范围的值，返回数据限制为10M。
    :return:
    """
    range_fmt = sheet_id + '!' + range
    get_range_url = cfg.get_range_url.format(spreadsheetToken=spreadsheetToken, range=range_fmt)
    headers = {
        "Authorization": "Bearer " + cfg.access_token,
        "Content-Type": "application/json"
    }
    params = {
        "valueRenderOption": "ToString" if valueRenderOption else None
    }
    result = get_http_request(get_range_url, headers=headers, params=params)
    return result
