#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/5 22:01
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : contact.py
# @Software    : PyCharm
# @Description :
from pomelo.apps.public.services import PomeloLarkSuiteServices
from pomelo.ext.sdk.lark_suite.contact import LarkSuiteContactAPI


class PomeloLarkSuiteContactServices(PomeloLarkSuiteServices):
    def __init__(self, bot_id: str):
        super().__init__(bot_id=bot_id)
        self.contact = LarkSuiteContactAPI(app_id=self.bot_config_info.get('app_id'), app_secret=self.bot_config_info.get('app_secret'))

    def get_all_departments_users(self):
        """获取所有部门的所有用户"""
        department_list = self.contact.departments_children()
        department_list.append({'department_name': '根部门', 'open_department_id': '0'})
        departments_user_map = {}
        for department in department_list:
            department_user_list = self.contact.users_find_by_department(department_id=department.get('open_department_id'))
            # 由于一个人可以同时在多个部门 所以需要根据open_id去重后重新组装
            for department_user in department_user_list:
                open_id = department_user.get('open_id')
                if open_id not in departments_user_map.keys():
                    departments_user_map[open_id] = department_user
        departments_users_list = list(departments_user_map.values())
        return departments_users_list
