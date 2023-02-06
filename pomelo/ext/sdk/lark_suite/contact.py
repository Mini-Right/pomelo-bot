#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/4 23:24
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : contact.py
# @Software    : PyCharm
# @Description :
from pomelo.ext.sdk.lark_suite import LarkSuiteBaseAPI


class LarkSuiteContactAPI(LarkSuiteBaseAPI):
    def __init__(self, app_id: str, app_secret: str):
        super().__init__(app_id=app_id, app_secret=app_secret)

    def departments_children(self):
        """
        获取子部门列表
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/department/children
        """
        url = self.domain + '/open-apis/contact/v3/departments/0/children'
        params = {
            'department_id_type': 'open_department_id',
            'page_size': 50,
            'user_id_type': 'open_id',
        }
        department_list = self.recursion_invoke_api(url=url, method='GET', params=params)
        department_list = [
            {
                'department_name': item.get('name'),
                'open_department_id': item.get('open_department_id')
            }
            for item in department_list
        ]
        return department_list

    def users_find_by_department(self, department_id: str, department_id_type: str = 'open_department_id'):
        """
        获取部门直属用户列表
        https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/find_by_department
        :param department_id:       根部门: 0
        :param department_id_type:  部门ID类型: open_department_id / department_id
        """
        url = self.domain + '/open-apis/contact/v3/users/find_by_department'
        params = {
            'department_id': department_id,
            'department_id_type': department_id_type,
            'page_size': 50,
            'user_id_type': 'open_id',
        }
        department_user_list = self.recursion_invoke_api(url=url, method='GET', params=params)
        department_user_list = [
            {
                'name': item.get('name'),
                'job_title': item.get('job_title'),
                'open_id': item.get('open_id'),
                'avatar': item.get('avatar').get('avatar_origin'),
                'email': item.get('enterprise_email'),
                'mobile': item.get('mobile').replace('+86', ''),
                'department_ids': item.get('department_ids'),
            }
            for item in department_user_list
        ]
        return department_user_list

    def get_all_departments_users(self):
        """获取所有部门的所有用户"""
        department_list = self.departments_children()
        departments_user_map = {}
        for department in department_list:
            department_user_list = self.users_find_by_department(department_id=department.get('open_department_id'))
            # 由于一个人可以同时在多个部门 所以需要根据open_id去重后重新组装
            for department_user in department_user_list:
                open_id = department_user.get('open_id')
                if open_id not in departments_user_map.keys():
                    departments_user_map[open_id] = department_user

        departments_users_list = list(departments_user_map.values())
        return departments_users_list
