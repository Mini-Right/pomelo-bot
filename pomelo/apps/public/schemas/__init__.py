#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/5/9 21:20
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from enum import Enum

from pydantic import BaseModel


class PomeloPublicMessageReceiveIDTypeEnum(str, Enum):
    open_id = 'open_id'
    chat_id = 'chat_id'


class PomeloPublicMessageScheme(BaseModel):
    bot_id: str
    user_id: str
    content: str


class PomeloPublicMessageInteractiveScheme(BaseModel):
    bot_id: str
    user_id: str
    content: dict


class PomeloPublicMessageImageSchema(BaseModel):
    bot_id: str
    user_id: str
    image_url: str


class PomeloPublicMessageDownloadSchema(BaseModel):
    bot_id: str
    user_id: str
    title: str
    file_url: str
    desc: str = None
