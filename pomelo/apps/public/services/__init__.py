#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/5/9 21:20
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from pomelo.cache.bot_app import bot_config


class PomeloLarkSuiteServices(object):
    def __init__(self, bot_id: str):
        self.bot_id = bot_id
        self.bot_config_info: dict = bot_config(bot_id=bot_id)
