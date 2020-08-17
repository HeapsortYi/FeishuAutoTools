# coding: utf-8

import os.path as osp
import sys

sys.path.append(osp.dirname(osp.dirname(__file__)))

from feishu.sheets_api import metainfo_api, get_range_api
from biz.refresh_token import refresh_old_user_tokens
from biz.log_conf import logger
from biz.work_summary import open_excel
import biz.conf as cfg


def _excel_col(col):
    """Covert 1-relative column number to excel-style column label."""
    quot, rem = divmod(col - 1, 26)
    return _excel_col(quot) + chr(rem + ord('A')) if col != 0 else ''


def _get_sheet_id(spreadsheetToken, idx=0):
    """
    获得对应表的sheet_id
    :return:
    """
    result = metainfo_api(spreadsheetToken)
    if not result:
        logger.error("metainfo post请求失败！返回结果为None！")
        return None
    if result["code"] != 0:
        logger.error("metainfo接口请求失败！code: %s, msg: %s" % (result["code"], result["msg"]))
        return None

    sheet_id = None
    try:
        sheet_id = result["data"]["sheets"][idx]["sheetId"]
    except Exception as e:
        logger.error("获取sheetId字段时发生异常！")
        logger.exception(e)

    return sheet_id


def get_sheet_data():
    """
    从飞书日报汇总表下载当日的日报
    :return:
    """
    spreadsheetToken = cfg.spreadsheetToken
    # 获得sheet_id
    sheet_id = _get_sheet_id(spreadsheetToken, idx=0)
    if not sheet_id:
        logger.error("sheet_id获取失败！")
        return None

    # 获取表格内容
    today_weekday = cfg.today.weekday()
    range = "{col}5:{col}12".format(col=_excel_col(5 + today_weekday * 3))
    # 向get_range_api发送请求
    result = get_range_api(spreadsheetToken, sheet_id, range)
    # 解析结果
    if not result:
        logger.error("get_range post请求失败！返回结果为None！")
        return None
    if result["code"] != 0:
        logger.error("get_range接口请求失败！code: %s, msg: %s" % (result["code"], result["msg"]))
        return None

    range_values = None
    try:
        range_values = result["data"]["valueRange"]["values"]
    except Exception as e:
        logger.error("获取values字段时发生异常！")
        logger.exception(e)

    return range_values


def copy_data_to_csv(data=[]):
    """
    将从飞书下载的数据存储到csv模板里
    :param data:
    :return:
    """
    csv_path = cfg.excel_path

    try:
        csv_df = open_excel(csv_path)

        data_fmt = [str(item[0]) for item in data]
        csv_df["完成情况"] = data_fmt

        # 保存
        csv_df.to_excel(csv_path, index=False, encoding='utf-8')

        return True
    except Exception as e:
        logger.exception(e)
        return False


def run():
    # step1：刷新user token
    rst = refresh_old_user_tokens()
    if not rst:
        logger.error("step1：刷新user token【失败】！")
        return False
    logger.info("step1：刷新user token【成功】！")

    # step2：获取sheet对应range的值
    rst = get_sheet_data()
    if not rst:
        logger.error("step2：获取sheet对应range的值【失败】！")
        return False
    logger.info("step2：获取sheet对应range的值【成功】！")

    # step3：将从飞书sheet下载的数据复制到本地模板
    rst = copy_data_to_csv(data=rst)
    if not rst:
        logger.error("step3：将从飞书sheet下载的数据复制到本地模板【失败】！")
        return False
    logger.info("step3：将从飞书sheet下载的数据复制到本地模板【成功】！")

    return True


if __name__ == '__main__':
    run()
