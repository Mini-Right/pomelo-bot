#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/3 16:17
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from typing import List

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html

from pomelo.apps import event
from pomelo.apps.public.routers import public
from pomelo.cache.bot_app import flush_bot_config, get_bot_config_list
from pomelo.databases.pomelo_bot_config_table import PomeloBotConfigTable
from pomelo.ext.curd import PomeloMySQLCURD
from pomelo.ext.sdk.lark_suite.events import LarkSuiteEventsServices
from pomelo.ext.session import MySQLSession, RedisSession
from pomelo.middlewares import middlewares
from pomelo.utils.decrypt import decrypt_data

pomelo = FastAPI()

pomelo.include_router(router=public, prefix='/public')


@pomelo.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="小右机器人",
        swagger_js_url="https://firefly-eff.oss-cn-beijing.aliyuncs.com/static/swagger-ui-bundle.js",
        swagger_css_url="https://firefly-eff.oss-cn-beijing.aliyuncs.com/static/swagger-ui.css",
    )


middlewares(pomelo)


@pomelo.middleware("http")
async def add_process_time_header(request: Request, call_next):
    bot_config_list = get_bot_config_list()
    request.state.bot_config = {bot_config.get('app_id'): bot_config for bot_config in bot_config_list}
    response = await call_next(request)
    return response


@pomelo.on_event('startup')
async def create_bot_events_challenge():
    flush_bot_config()
    bot_config_list = get_bot_config_list()
    for bot_config in bot_config_list:
        pomelo.include_router(
            router=event,
            prefix=f"/event/{bot_config.get('app_id')}",
            tags=['事件订阅'],
        )
