#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/3 17:00
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
import toml

from pomelo.config.schemas import ConfigSchema
from root_path import root_path

__all__ = ['config']


def pomelo_config():
    _config = toml.load(f"{root_path()}/pomelo/config/dev.toml")
    return ConfigSchema(**_config)


config: ConfigSchema = pomelo_config()
