#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/4 23:37
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : bot_app.py
# @Software    : PyCharm
# @Description :

import json
from typing import List

from pomelo.databases.pomelo_bot_config_table import PomeloBotConfigTable
from pomelo.ext import logging
from pomelo.ext.curd import PomeloMySQLCURD
from pomelo.ext.session import RedisSession

logger = logging.getLogger(__name__)


def bot_config(bot_id: str):
    redis_key = f"bot-{bot_id}"
    res = RedisSession.pomelo.get(redis_key)
    if not res:
        bot_info: PomeloBotConfigTable = PomeloMySQLCURD().query_table_one(
            table_class=PomeloBotConfigTable,
            params=[PomeloBotConfigTable.id == bot_id]
        )
        bot_config = {'app_id': bot_info.bot_app_id, 'app_secret': bot_info.bot_app_secret, 'encrypt_key': bot_info.encrypt_key}
        RedisSession.pomelo.set(name=redis_key, value=json.dumps(bot_config))
        return bot_config
    bot_config = json.loads(res)
    return bot_config


def flush_bot_config():
    empty_bot_config()
    bot_info_list: List[PomeloBotConfigTable] = PomeloMySQLCURD().query_table_all(table_class=PomeloBotConfigTable, is_list=True)
    for bot_info in bot_info_list:
        redis_key = f"bot-{bot_info.get('bot_app_id')}"
        bot_config = {
            'app_id': bot_info.get('bot_app_id'),
            'app_secret': bot_info.get('bot_app_secret'),
            'encrypt_key': bot_info.get('encrypt_key'),
            'bot_name': bot_info.get('bot_name'),

        }
        RedisSession.pomelo.set(name=redis_key, value=json.dumps(bot_config))


def empty_bot_config():
    redis_key_list = RedisSession.pomelo.keys('bot-*')
    for redis_key in redis_key_list:
        RedisSession.pomelo.delete(redis_key)


def get_bot_config_list():
    redis_key_list = RedisSession.pomelo.keys('bot-*')
    bot_config_list = [
        json.loads(RedisSession.pomelo.get(redis_key))
        for redis_key in redis_key_list
    ]
    return bot_config_list
