# coding: utf-8

import os.path as osp
import sys

sys.path.append(osp.dirname(osp.dirname(__file__)))

import biz.conf as cfg
from biz.log_conf import logger
from feishu.authen_api import refresh_access_token_api
import feishu.conf as fscfg


def refresh_old_user_tokens():
    result = refresh_access_token_api()
    if result:
        code = result["code"]
        msg = result["msg"]
        if code == 0:
            access_token = result["data"]["access_token"]
            refresh_token = result["data"]["refresh_token"]
            # 更新token.txt
            token_txt_path = osp.join(cfg.proj_path, "feishu", "token.txt")
            with open(token_txt_path, "w") as f:
                f.write("\n".join([access_token, refresh_token]))
            # 更新一下全局变量的值
            fscfg.access_token = access_token
            fscfg.refresh_token = refresh_token

            logger.info("user tokens刷新成功！")
            return True
        else:
            logger.error("refresh_access_token接口请求失败！code: %s, msg: %s" % (code, msg))
            logger.error("user tokens刷新失败！")
            return False
    else:
        logger.error("refresh_access_token post请求失败！返回结果为None！")
        logger.error("user tokens刷新失败！")
        return False


if __name__ == '__main__':
    refresh_old_user_tokens()
