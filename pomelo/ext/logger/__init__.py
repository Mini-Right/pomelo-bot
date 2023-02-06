#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/1/29 11:49
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
# 初始化日志对象

import logging

from asgi_correlation_id import CorrelationIdFilter

from root_path import root_path

__all__ = ['logging']


def configure_logging_basic() -> None:
    cid_filter = CorrelationIdFilter(uuid_length=32)
    console_handler = logging.StreamHandler()
    console_handler.addFilter(cid_filter)
    file_handler = logging.FileHandler(f"{root_path()}/logs/log.log")
    logging.basicConfig(
        handlers=[console_handler, file_handler],
        level=logging.INFO,
        format='%(levelname)s: \t  %(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] %(message)s',
    )
    logging.getLogger("requests").setLevel(logging.WARNING)


configure_logging_basic()
