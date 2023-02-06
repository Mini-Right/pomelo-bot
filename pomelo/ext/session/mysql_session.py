#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/6/15 20:57
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : mysql_session.py
# @Software    : PyCharm
# @Description :
import types
from contextlib import contextmanager
from urllib import parse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pomelo.config.schemas import DBItemSchema


def assembly_uri(database_config: DBItemSchema):
    if database_config.database:
        return f"mysql+pymysql://{database_config.user}:{parse.quote_plus(database_config.password)}@{database_config.host}:{database_config.port}/{database_config.database}?charset=utf8mb4"
    return f"mysql+pymysql://{database_config.user}:{parse.quote_plus(database_config.password)}@{database_config.host}:{database_config.port}/?charset=utf8mb4"


def init_engine(database_config: DBItemSchema):
    return create_engine(assembly_uri(database_config), echo=False)


def init_session(database_config: DBItemSchema):
    engine = init_engine(database_config)
    _session = sessionmaker(expire_on_commit=False)
    _session.configure(bind=engine)

    @contextmanager
    def session_scope(_session):
        session = _session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    engine.session_scope = types.MethodType(session_scope, _session)
    return engine.session_scope
