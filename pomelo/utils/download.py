#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/5 00:29
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : download.py
# @Software    : PyCharm
# @Description :
import os

import requests

from pomelo.ext import logging

logger = logging.getLogger(__name__)


def download(url: str, local_path: str, refresh: bool = False):
    """
    :param url:         目标url地址
    :param local_path:  保存本地路径
    :param refresh:     当本地文件已存在 是否刷新
    :return:
    """
    logger.debug(f"开始下载 {url} 本地路径: {local_path}")
    if os.path.exists(local_path) and refresh is False:
        logger.warning(f"{local_path} 已存在 不进行刷新处理")
        return
    response = requests.get(url=url, stream=True).content
    with open(local_path, "wb") as code:
        code.write(response)

    logger.debug(f"{local_path} 下载完成 文件大小: {len(response) / 1024}kb")
