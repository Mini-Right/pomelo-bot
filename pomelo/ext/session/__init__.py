#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/6/15 20:56
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from redis.client import Redis

from pomelo.config import config
from pomelo.ext.session.mysql_session import init_session as init_mysql_session
from pomelo.ext.session.redis_session import init_session as init_redis_session

__all__ = ['MySQLSession', 'RedisSession']


class MySQLSession(object):
    pomelo = init_mysql_session(config.DB.POMELO)


class RedisSession(object):
    pomelo: Redis = init_redis_session(config.REDIS.POMELO)
