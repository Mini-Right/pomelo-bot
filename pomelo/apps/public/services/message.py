#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/4 23:17
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : message.py
# @Software    : PyCharm
# @Description :
import json
import os

from fastapi import File, UploadFile

from pomelo.cache.bot_app import bot_config
from pomelo.ext.sdk.lark_suite.assembly_interactive import LarkSuiteAssemblyInteractive, LarkSuiteInteractiveHeaderTemplateEnum, LarkSuiteInteractiveButtonTypeEnum
from pomelo.ext.sdk.lark_suite.im import LarkSuiteIMAPI
from pomelo.utils import download
from root_path import root_path


class PomeloLarkSuiteMessageServices(object):
    def __init__(self, bot_id: str):
        self.bot_id = bot_id
        bot_config_info: dict = bot_config(bot_id=bot_id)
        self.im = LarkSuiteIMAPI(app_id=bot_config_info.get('app_id'), app_secret=bot_config_info.get('app_secret'))
        self.interactive = LarkSuiteAssemblyInteractive()

    @staticmethod
    def _text(content: str):
        return json.dumps({'text': content})

    def send_text_with_open_id(self, open_id: str, content: str):
        """
        发送文本消息到用户
        :param open_id:     用户ID
        :param content:     文本内容
        :return: message_id
        """
        content = self._text(content=content)
        return self.im.message_create(receive_id=open_id, msg_type='text', content=content, receive_id_type='open_id')

    def send_text_with_chat_id(self, chat_id: str, content: str):
        """
        发送文本消息到群组
        :param chat_id:     群组ID
        :param content:     文本内容
        :return: message_id
        """
        content = self._text(content=content)
        return self.im.message_create(receive_id=chat_id, msg_type='text', content=content, receive_id_type='chat_id')

    @staticmethod
    def _interactive(content: dict):
        return json.dumps(content)

    def send_interactive_with_open_id(self, open_id: str, content: dict):
        """
        发送消息卡片到用户
        :param open_id:     用户ID
        :param content:     消息卡片内容 json
        :return: message_id
        """
        content = self._interactive(content)
        return self.im.message_create(receive_id=open_id, msg_type='interactive', content=content, receive_id_type='open_id')

    def send_interactive_with_chat_id(self, chat_id: str, content: dict):
        """
        发送消息卡片到群组
        :param chat_id:     群组ID
        :param content:     消息卡片内容 json
        :return: message_id
        """
        content = self._interactive(content)
        return self.im.message_create(receive_id=chat_id, msg_type='interactive', content=content, receive_id_type='chat_id')

    def _image_url(self, image_url: str):
        image_path = f"{root_path()}/files/{image_url.split('/')[-1]}"
        download(url=image_url, local_path=image_path)
        image_key = self.im.image_create(image_path=image_path)
        os.remove(image_path)
        return json.dumps({'image_key': image_key})

    def send_image_url_with_open_id(self, open_id: str, image_url: str):
        """
        发送图片到用户
        :param open_id:     用户ID
        :param image_url:   图片URL
        :return: message_id
        """
        content = self._image_url(image_url=image_url)
        return self.im.message_create(receive_id=open_id, msg_type='image', content=content, receive_id_type='open_id')

    def send_image_url_with_chat_id(self, chat_id: str, image_url: str):
        """
        发送图片到群组
        :param chat_id:     群组ID
        :param image_url:   图片URL
        :return: message_id
        """
        content = self._image_url(image_url=image_url)
        return self.im.message_create(receive_id=chat_id, msg_type='image', content=content, receive_id_type='chat_id')

    async def _image(self, file: UploadFile = File(...)):
        image_path = f"{root_path()}/files/{file.filename.split('/')[-1]}"
        with open(image_path, 'wb') as f:
            f.write(await file.read())
        image_key = self.im.image_create(image_path=image_path)
        os.remove(image_path)
        return json.dumps({'image_key': image_key})

    async def send_image_with_open_id(self, open_id: str, file: UploadFile = File(...)):
        """
        发送图片到用户
        :param open_id:     用户ID
        :param file:        图片文件对象
        :return: message_id
        """
        content = await self._image(file=file)
        return self.im.message_create(receive_id=open_id, msg_type='image', content=content, receive_id_type='open_id')

    async def send_image_with_chat_id(self, chat_id: str, file: UploadFile = File(...)):
        """
        发送图片到用户
        :param chat_id:     群组ID
        :param file:        图片文件对象
        :return: message_id
        """
        content = await self._image(file=file)
        return self.im.message_create(receive_id=chat_id, msg_type='image', content=content, receive_id_type='chat_id')

    def _download(self, title: str, file_url: str, desc: str = None):
        interactive = self.interactive.add_header(content=title, template=LarkSuiteInteractiveHeaderTemplateEnum.blue)
        if desc:
            interactive.add_text(content=desc)
        interactive.add_button(button_title='点击下载', url=file_url, button_type=LarkSuiteInteractiveButtonTypeEnum.primary)
        content = interactive.content
        return content

    def send_download_file_open_id(self, open_id: str, title: str, file_url: str, desc: str = None):
        """
        发送文件下载到用户
        :param open_id:     用户ID
        :param title:       标题
        :param file_url:    文件URL
        :param desc:        描述
        :return:
        """
        content = self._download(title=title, file_url=file_url, desc=desc)
        return self.send_interactive_with_open_id(open_id=open_id, content=content)

    def send_download_file_chat_id(self, chat_id: str, title: str, file_url: str, desc: str = None):
        """
        发送文件下载到用户
        :param chat_id:     群组ID
        :param title:       标题
        :param file_url:    文件URL
        :param desc:        描述
        :return:
        """
        content = self._download(title=title, file_url=file_url, desc=desc)
        return self.send_interactive_with_chat_id(chat_id=chat_id, content=content)
