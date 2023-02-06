#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/5/9 21:19
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from fastapi import APIRouter

from pomelo.apps.public.routers.im import im

public = APIRouter()

public.include_router(router=im, prefix='/im', tags=['飞书消息通知'])
