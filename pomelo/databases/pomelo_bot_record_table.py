#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/4 22:29
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : pomelo_bot_record_table.py
# @Software    : PyCharm
# @Description :
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import LONGTEXT, JSON, INTEGER

from pomelo.databases import Base


class PomeloBotRecordTable(Base):
    __tablename__ = "pomelo_bot_record"
    bot_id = Column(String(50), nullable=False, comment="botID")
    request_url = Column(LONGTEXT, nullable=False, comment="Url")
    request_method = Column(String(50), nullable=False, comment="method")
    request_params = Column(LONGTEXT, comment="params")
    request_headers = Column(LONGTEXT, comment="headers")
    request_body = Column(LONGTEXT, comment="body")
    request_kwargs = Column(LONGTEXT, comment="kwargs")
    response_text = Column(LONGTEXT, comment="response text")
    response_headers = Column(LONGTEXT, comment="response headers")
    response_status_code = Column(INTEGER, comment='response status code')


