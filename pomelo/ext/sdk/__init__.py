#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/3 17:32
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
import copy
import json
import typing
from functools import wraps

from requests import Response

from pomelo.databases.pomelo_bot_record_table import PomeloBotRecordTable
from pomelo.ext import logging
from pomelo.ext.curd import PomeloMySQLCURD

logger = logging.getLogger(__name__)

T = typing.TypeVar("T")


def bot_record(func: T) -> T:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        response = None
        for k, v in kwargs.items():
            logger.info(f"[{k}]: {v}")
        error = None
        try:
            response: Response = func(self, *args, **kwargs)
        except Exception as e:
            error = e

        new_kwargs = copy.deepcopy(kwargs)
        request_url = new_kwargs.get('url')
        request_method = new_kwargs.get('method')
        request_params = new_kwargs.get('params')
        request_headers = new_kwargs.get('headers')
        request_body = new_kwargs.get('body')
        del_key_list = ['url', 'method', 'params', 'headers', 'body']
        for del_key in del_key_list:
            try:
                del new_kwargs[del_key]
            except:
                pass

        PomeloMySQLCURD().add_one(
            table_class=PomeloBotRecordTable(
                bot_id='111',
                request_url=request_url,
                request_method=request_method,
                request_params=json.dumps(request_params) if request_params else None,
                request_headers=json.dumps(request_headers) if request_headers else None,
                request_body=json.dumps(request_body) if request_body else None,
                request_kwargs=json.dumps(new_kwargs) if new_kwargs else None,
                response_text=response.text,
                response_headers=json.dumps(dict(response.headers)),
                response_status_code=response.status_code
            )
        )
        if error:
            raise error
        return response

    return wrapper
