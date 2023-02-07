#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/3 16:17
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from pomelo.apps import event
from pomelo.apps.public.routers import public
from pomelo.cache.bot_app import flush_bot_config, get_bot_config_list, bot_config
from pomelo.databases.pomelo_bot_config_table import PomeloBotConfigTable
from pomelo.ext.curd import PomeloMySQLCURD
from pomelo.ext.sdk.lark_suite.events import LarkSuiteEventsServices
from pomelo.ext.session import MySQLSession, RedisSession
from pomelo.middlewares import middlewares
from pomelo.utils.decrypt import decrypt_data

pomelo = FastAPI()

pomelo.include_router(router=public, prefix='/public')
pomelo.include_router(router=event, prefix='/event')


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
    response = await call_next(request)
    return response


def reload_openapi():
    pomelo.openapi_schema = get_openapi(
        title=pomelo.title,
        version=pomelo.version,
        openapi_version=pomelo.openapi_version,
        description=pomelo.description,
        terms_of_service=pomelo.terms_of_service,
        contact=pomelo.contact,
        license_info=pomelo.license_info,
        routes=pomelo.routes,
        tags=pomelo.openapi_tags,
        servers=pomelo.servers,
    )


@pomelo.on_event('startup')
async def create_bot_events_challenge():
    flush_bot_config()
