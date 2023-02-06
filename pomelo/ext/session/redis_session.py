#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/7/5 15:44
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : redis_session.py
# @Software    : PyCharm
# @Description :
from redis import StrictRedis

from pomelo.config.schemas import RedisItemSchema


def init_session(redis_config: RedisItemSchema):
    session = StrictRedis(
        host=redis_config.host,
        port=redis_config.port,
        password=redis_config.password,
        db=redis_config.db,
        decode_responses=True,
    )
    return session
