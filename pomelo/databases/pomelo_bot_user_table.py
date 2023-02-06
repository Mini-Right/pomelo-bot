#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/3 23:44
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : pomelo_bot_user_table.py
# @Software    : PyCharm
# @Description :
from sqlalchemy import Column, String

from pomelo.databases import Base


class PomeloBotUserTable(Base):
    __tablename__ = "pomelo_bot_user"
    bot_id = Column(String(50), nullable=False, comment="bot_id")
    name = Column(String(50), nullable=False, comment="姓名")
    open_id = Column(String(50), nullable=False, comment="openID")
    email = Column(String(255), comment="邮箱")
    mobile = Column(String(50), comment="手机号")