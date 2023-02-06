#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/5/9 21:20
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
from fastapi import APIRouter

from pomelo.apps.public.schemas import PomeloPublicMessageScheme, PomeloPublicMessageReceiveIDTypeEnum, PomeloPublicMessageImageSchema, PomeloPublicMessageDownloadSchema, PomeloPublicMessageInteractiveScheme
from pomelo.apps.public.services.message import PomeloLarkSuiteMessageServices
from pomelo.handler import success_response, fail_response

im = APIRouter()


@im.post('/send_text', name='发送文本消息')
async def public_send_text(receive_id_type: PomeloPublicMessageReceiveIDTypeEnum, data: PomeloPublicMessageScheme):
    try:
        message = PomeloLarkSuiteMessageServices(bot_id=data.bot_id)
        message_id = ''
        if receive_id_type is PomeloPublicMessageReceiveIDTypeEnum.open_id:
            message_id = message.send_text_with_open_id(open_id=data.user_id, content=data.content)
        elif receive_id_type is PomeloPublicMessageReceiveIDTypeEnum.chat_id:
            message_id = message.send_text_with_chat_id(chat_id=data.user_id, content=data.content)
        return success_response(data={'message_id': message_id}, msg='发送文本消息成功')
    except Exception as e:
        return fail_response(msg=f"发送文本消息失败 : {str(e)}")


@im.post('/send_interactive', name='发送卡片消息')
async def public_send_text(receive_id_type: PomeloPublicMessageReceiveIDTypeEnum, data: PomeloPublicMessageInteractiveScheme):
    try:
        message = PomeloLarkSuiteMessageServices(bot_id=data.bot_id)
        message_id = ''
        if receive_id_type is PomeloPublicMessageReceiveIDTypeEnum.open_id:
            message_id = message.send_text_with_open_id(open_id=data.user_id, content=data.content)
        elif receive_id_type is PomeloPublicMessageReceiveIDTypeEnum.chat_id:
            message_id = message.send_text_with_chat_id(chat_id=data.user_id, content=data.content)
        return success_response(data={'message_id': message_id}, msg='发送卡片消息成功')
    except Exception as e:
        return fail_response(msg=f"发送卡片消息失败 : {str(e)}")


@im.post('/send_image', name='发送图片消息')
async def public_send_text(receive_id_type: PomeloPublicMessageReceiveIDTypeEnum, data: PomeloPublicMessageImageSchema):
    try:
        message = PomeloLarkSuiteMessageServices(bot_id=data.bot_id)
        message_id = ''
        if receive_id_type is PomeloPublicMessageReceiveIDTypeEnum.open_id:
            message.send_image_url_with_open_id(open_id=data.user_id, image_url=data.image_url)
        elif receive_id_type is PomeloPublicMessageReceiveIDTypeEnum.chat_id:
            message.send_image_url_with_chat_id(chat_id=data.user_id, image_url=data.image_url)
        return success_response(data={'message_id': message_id}, msg='发送图片消息成功')
    except Exception as e:
        return fail_response(msg=f"发送图片消息失败 : {str(e)}")


@im.post('/send_download', name='发送下载消息')
async def public_send_download(receive_id_type: PomeloPublicMessageReceiveIDTypeEnum, data: PomeloPublicMessageDownloadSchema):
    try:
        message = PomeloLarkSuiteMessageServices(bot_id=data.bot_id)
        message_id = ''
        if receive_id_type is PomeloPublicMessageReceiveIDTypeEnum.open_id:
            message_id = message.send_download_file_open_id(open_id=data.user_id, title=data.title, file_url=data.file_url, desc=data.desc)
        elif receive_id_type is PomeloPublicMessageReceiveIDTypeEnum.chat_id:
            message_id = message.send_download_file_chat_id(chat_id=data.user_id, title=data.title, file_url=data.file_url, desc=data.desc)
        return success_response(data={'message_id': message_id}, msg='发送下载消息成功')
    except Exception as e:
        return fail_response(msg=f"发送下载消息失败 : {str(e)}")
