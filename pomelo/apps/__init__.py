#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/3 23:42
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from fastapi import APIRouter, Request, BackgroundTasks

from pomelo.apps.public.routers import public
from pomelo.ext.sdk.lark_suite.events import LarkSuiteEventsServices
from pomelo.utils.decrypt import decrypt_data

event = APIRouter()


@event.post('')
async def callback_event_handler(data: dict, request: Request, background_tasks: BackgroundTasks):
    app_id = request.url.path.split('/')[-1]
    bot_config = request.state.bot_config[app_id]
    data = decrypt_data(encrypt_key=bot_config.get('encrypt_key'), data=data)
    if data.get("type") == "url_verification":
        return {'challenge': data.get("challenge")}
    background_tasks.add_task(LarkSuiteEventsServices(data).main)
    return {"code": 200, "message": "success"}
