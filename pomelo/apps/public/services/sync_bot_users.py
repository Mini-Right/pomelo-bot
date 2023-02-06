#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/3 23:46
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : sync_bot_users.py
# @Software    : PyCharm
# @Description :
from pomelo.apps.public.services.contact import PomeloLarkSuiteContactServices
from pomelo.databases.pomelo_bot_user_table import PomeloBotUserTable
from pomelo.ext import logging
from pomelo.ext.curd import PomeloMySQLCURD

logger = logging.getLogger(__name__)


class PomeloLarkSuiteSyncBotUsers(object):
    def __init__(self, bot_id: str):
        self.bot_id = bot_id
        self.pomelo_contact = PomeloLarkSuiteContactServices(bot_id=bot_id)

    def main(self):
        logger.info(f"飞书【{self.bot_id}】用户信息同步开始")

        users = self.pomelo_contact.get_all_departments_users()
        logger.debug(f"用户信息: {users}")

        curd = PomeloMySQLCURD()
        curd.delete(
            table_class=PomeloBotUserTable,
            params=[PomeloBotUserTable.bot_id == self.bot_id]
        )

        curd.add_list(
            table_class_list=[
                PomeloBotUserTable(
                    bot_id=self.bot_id,
                    name=user.get('name'),
                    open_id=user.get('open_id'),
                    email=user.get('email'),
                    mobile=user.get('mobile')
                )
                for user in users
            ]
        )
        logger.info(f"飞书【{self.bot_id}】用户信息同步成功")
