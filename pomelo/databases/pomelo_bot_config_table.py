#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/3 16:19
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : pomelo_bot_config.py
# @Software    : PyCharm
# @Description :

from sqlalchemy import Column, String

from pomelo.databases import Base


class PomeloBotConfigTable(Base):
    __tablename__ = "pomelo_bot_config"
    bot_type = Column(String(50), nullable=False, comment="机器人类型 钉钉 飞书 企微")
    bot_name = Column(String(50), nullable=False, comment="机器人名称")
    bot_app_id = Column(String(50), nullable=False, comment="机器人 APP_ID")
    bot_app_secret = Column(String(50), nullable=False, comment="机器人 APP_SECRET")
    encrypt_key = Column(String(50), comment="机器人 EncryptKey")

