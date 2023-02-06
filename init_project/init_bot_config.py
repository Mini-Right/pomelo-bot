#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/3 17:13
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from pomelo.databases.pomelo_bot_config_table import PomeloBotConfigTable
from pomelo.ext.curd import PomeloMySQLCURD


def init_pomelo_bot_config_table_data():
    bot_config = {
        "bot_name": "",
        "bot_app_id": "",
        "bot_app_secret": "",
        "encrypt_key": "",
    }
    PomeloMySQLCURD().add_one(
        table_class=PomeloBotConfigTable(
            id=bot_config.get('bot_app_id'),
            bot_type='LarkSuite',
            bot_name=bot_config.get('bot_name'),
            bot_app_id=bot_config.get('bot_app_id'),
            bot_app_secret=bot_config.get('bot_app_secret'),
            encrypt_key=bot_config.get('encrypt_key'),
        )
    )


if __name__ == '__main__':
    init_pomelo_bot_config_table_data()
