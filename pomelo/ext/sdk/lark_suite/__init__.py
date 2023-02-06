#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/3 17:33
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from typing import List

import requests

from pomelo.ext import logging
from pomelo.ext.sdk import bot_record
from pomelo.utils.analytic_body import analytic

logger = logging.getLogger(__name__)


class LarkSuiteBaseAPI(object):
    def __init__(self, app_id: str, app_secret: str):
        self.APP_ID = app_id
        self.APP_SECRET = app_secret
        self.domain = 'https://open.feishu.cn'
        self.session = requests.Session()

    @bot_record
    def invoke_api(self, url: str, method: str, params=None, body=None, headers=None, **kwargs):
        """
        调用API
        """
        headers = headers or {
            "Authorization": self.get_tenant_access_token_api(),
            "Content-Type": "application/json"
        }
        response = requests.request(method.upper(), url, params=params, json=body, headers=headers, verify=True, **kwargs)
        return response

    def recursion_invoke_api(self, url: str, method: str, params: dict = None):
        data_list = []
        page_token = ''
        while True:
            params = params if params else {}
            params['page_token'] = page_token
            response = self.invoke_api(url=url, method=method, params=params)
            response_data = response.json()
            if not response_data.get('data').get('has_more') and not response_data.get('data').get('items'):
                break
            items: List[dict] = response_data.get('data').get('items')
            data_list += items
            page_token = response_data.get('data').get('page_token')
            if not page_token:
                break
        return data_list

    def get_tenant_access_token_api(self):
        """
        获取用户token
        https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3/auth/tenant_access_token_internal
        :return: tenant_access_token
        """
        url = f"{self.domain}/open-apis/auth/v3/tenant_access_token/internal"
        body = {"app_id": self.APP_ID, "app_secret": self.APP_SECRET}
        response = requests.request('POST', url, json=body)
        return f"Bearer {analytic(response.json(), 'tenant_access_token')}"

    def get_headers_api(self):
        """
        获取headers
        """
        return {
            "Authorization": self.get_tenant_access_token_api(),
            "Content-Type": "application/json"
        }
