#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/3 23:42
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from fastapi import APIRouter, BackgroundTasks

from pomelo.cache.bot_app import bot_config
from pomelo.ext.sdk.lark_suite.events import LarkSuiteEventsServices
from pomelo.utils.decrypt import decrypt_data

event = APIRouter()


@event.post('/{app_id}/callback', name='事件回调')
async def callback_event_handler(app_id: str, data: dict, background_tasks: BackgroundTasks):
    bot_info = bot_config(bot_id=app_id)
    data = decrypt_data(encrypt_key=bot_info.get('encrypt_key'), data=data)
    if data.get("type") == "url_verification":
        return {'challenge': data.get("challenge")}
    background_tasks.add_task(LarkSuiteEventsServices(data).main)
    return {"code": 200, "message": "success"}
