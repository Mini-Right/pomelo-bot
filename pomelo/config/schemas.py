#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/12/21 13:43
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : schemas.py
# @Software    : PyCharm
# @Description :
from pydantic import BaseSettings, Field

class DBItemSchema(BaseSettings):
    host: str = Field(...)
    port: int = Field(...)
    user: str = Field(...)
    password: str = Field(...)
    database: str = Field(None)


class RedisItemSchema(BaseSettings):
    host: str
    port: int
    password: str
    db: int


class DBSchema(BaseSettings):
    POMELO: DBItemSchema


class RedisSchema(BaseSettings):
    POMELO: RedisItemSchema


class ConfigSchema(BaseSettings):
    DB: DBSchema
    REDIS: RedisSchema
