#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/6 01:23
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : events.py
# @Software    : PyCharm
# @Description :
import json

from pomelo.cache.bot_app import bot_config
from pomelo.ext import logging
from pomelo.ext.sdk.lark_suite.im import LarkSuiteIMAPI
from pomelo.ext.sdk.chatgpt import chatgpt
from pomelo.ext.session import RedisSession
logger = logging.getLogger(__name__)


class LarkSuiteEventsServices(object):
    def __init__(self, data: dict):
        self.data = data
        logger.info(f"事件订阅: {data}")
        header: dict = self.data.get('header')
        self.event_type: str = header.get('event_type')
        self.event_id: str = header.get('event_id')
        self.token: str = header.get('token')
        self.create_time: str = header.get('create_time')
        self.app_id: str = header.get('app_id')
        self.event: dict = self.data.get('event')
        self.bot_config = bot_config(bot_id=self.app_id)
        logger.info(f"事件: {self.event_type}")

    def im_chat_member_bot_added_v1(self):
        """机器人进群"""
        chat_id = self.event.get('chat_id')
        name = self.event.get('name')
        open_id = self.event.get('operator_id').get('open_id')
        chat_info = LarkSuiteIMAPI(app_id=self.app_id, app_secret=self.bot_config.get('app_secret')).chat_get(chat_id=chat_id)
        logger.info(f"[机器人进群] 群名: {name} 操作用户: {open_id} 群信息: {chat_info}")

    def im_chat_member_bot_deleted_v1(self):
        """机器人退群"""
        chat_id = self.event.get('chat_id')
        name = self.event.get('name')
        open_id = self.event.get('operator_id').get('open_id')
        chat_info = LarkSuiteIMAPI(app_id=self.app_id, app_secret=self.bot_config.get('app_secret')).chat_get(chat_id=chat_id)
        logger.info(f"[机器人退群] 群名: {name} 操作用户: {open_id} 群信息: {chat_info}")

    def im_message_receive_v1(self):
        """接收消息"""
        LarkSuiteEventImMessageReceiveServices(app_id=self.app_id, event_data=self.event).main()

    def im_message_reaction_created_v1(self):
        """消息被reaction"""
        reaction_type = self.event.get('reaction_type', {}).get('emoji_type')
        message_id = self.event.get('message_id')
        logger.info(f"[消息被reaction] {message_id} 被reaction: {reaction_type}")

    def im_message_reaction_deleted_v1(self):
        """消息被取消reaction"""
        reaction_type = self.event.get('reaction_type', {}).get('emoji_type')
        message_id = self.event.get('message_id')
        logger.info(f"[{message_id}] 被取消reaction: {reaction_type}")

    def main(self):
        event_func_name = self.event_type.replace('.', '_')
        try:
            event_func = getattr(self, event_func_name)
            event_func()
        except Exception as e:
            logger.warning(f"事件: {self.event_type} 未定义: {e}")


class LarkSuiteEventImMessageReceiveServices(object):
    def __init__(self, app_id: str, event_data: dict):
        self.app_id = app_id
        self.bot_config = bot_config(bot_id=self.app_id)
        self.sender: dict = event_data.get('sender')
        self.message: dict = event_data.get('message')
        # 发消息用户openID
        self.open_id = self.sender.get('sender_id', {}).get('open_id')
        # 消息ID
        self.message_id = self.message.get('message_id')
        # 群组ID
        self.chat_id = self.message.get('chat_id')
        # 群组类型 p2p:单聊 / group:群组 topic_group:话题群
        self.chat_type = self.message.get('chat_type')
        # 消息类型 text / image / file / post / sticker(表情包)
        self.message_type = self.message.get('message_type')
        # 消息内容
        self.content: dict = json.loads(self.message.get('content'))

    def text(self):
        text: str = self.content.get('text')
        logger.info(f"[接收消息-text] 发送人: {self.message_id} 群组类型: {self.chat_type} 发送内容: {text}")
        receive_id = self.chat_id if self.chat_type == 'group' else self.open_id
        receive_id_type = 'chat_id' if self.chat_type == 'group' else 'open_id'
        if text.startswith('小右'):
            try:
                result = chatgpt(text.replace('小右', ''))
            except Exception as e:
                logger.warning(f"对话出错啦: {e}")
                result = '对话出错啦 请稍候再试~~~😭'
            content = {
                "config": {
                    "wide_screen_mode": True
                },
                "elements": [
                    {
                        "tag": "markdown",
                        "content": f"""<at id="{self.open_id}""></at> \n**提问**: {text}\n**回答**: \n{result}"""
                    }
                ]
            }
            LarkSuiteIMAPI(app_id=self.app_id, app_secret=self.bot_config.get('app_secret')).message_create(receive_id=receive_id, msg_type='interactive', content=json.dumps(content), receive_id_type=receive_id_type)
            LarkSuiteIMAPI(app_id=self.app_id, app_secret=self.bot_config.get('app_secret')).message_reactions(message_id=self.message_id, emoji_type='OK')

    def image(self):
        image_key = self.content.get('image_key')
        logger.info(f"[接收消息-image] 发送人: {self.message_id} 群组类型: {self.chat_type} 发送内容: {image_key}")

    def file(self):
        file_key = self.content.get('file_key')
        file_name = self.content.get('file_name')
        logger.info(f"[接收消息-file] 发送人: {self.message_id} 群组类型: {self.chat_type} 发送内容: {file_name} {file_key}")

    def post(self):
        logger.info(f"[接收消息-post] 发送人: {self.message_id} 群组类型: {self.chat_type} 发送内容: {self.chat_type}")

    def sticker(self):
        file_key = self.content.get('file_key')
        logger.info(f"[接收消息-sticker] 发送人: {self.message_id} 群组类型: {self.chat_type} 发送内容: {file_key}")

    def main(self):
        if RedisSession.pomelo.exists(f"message_id:{self.message_id}"):
            logger.info(f"消息: {self.message_id} 已处理")
            return
        message_type_func = getattr(self, self.message_type)
        message_type_func()
        RedisSession.pomelo.set(name=f"message_id:{self.message_id}", value=self.message_id, ex=60 * 60 * 24 * 2)
