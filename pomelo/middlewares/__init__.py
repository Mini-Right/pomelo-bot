#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/5 20:48
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :

from uuid import uuid4

from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.middleware import is_valid_uuid4
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 也可以设置为"*"，即为所有。
        allow_credentials=True,
        allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
        allow_headers=["*"],  # 允许跨域的headers，可以用来鉴别来源等作用。
    )
    app.add_middleware(
        CorrelationIdMiddleware,
        header_name='X-Request-ID',
        generator=lambda: uuid4().hex,
        validator=is_valid_uuid4,
        transformer=lambda a: a,
    )
