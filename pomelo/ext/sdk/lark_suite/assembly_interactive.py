#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/5 16:17
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : assembly_interactive.py
# @Software    : PyCharm
# @Description :
import json
from typing import List
from enum import Enum


class LarkSuiteInteractiveHeaderTemplateEnum(str, Enum):
    blue = 'blue'
    wathet = 'wathet'
    turquoise = 'turquoise'
    green = 'green'
    yellow = 'yellow'
    orange = 'orange'
    red = 'red'
    carmine = 'carmine'
    violet = 'violet'
    purple = 'purple'
    indigo = 'indigo'
    grey = 'grey'


class LarkSuiteInteractiveButtonTypeEnum(str, Enum):
    default = 'default'
    primary = 'primary'
    danger = 'danger'


class LarkSuiteAssemblyInteractive(object):
    def __init__(self):
        self.content = {
            'config': {"wide_screen_mode": True},
            'elements': []
        }

    def add_header(self, content: str, template: str = 'blue'):
        """
        添加标题
        :param content:     标题内容
        :param template:    标题样式  blue / wathet / turquoise / green / yellow / orange / red / carmine / violet / purple / indigo / grey
        :return:
        """
        self.content['header'] = {
            "template": template,
            "title": {
                "content": content,
                "tag": "plain_text"
            }
        }
        return self

    def add_text(self, content: str):
        self.content['elements'].append(
            {
                "tag": "div",
                "text": {
                    "content": content,
                    "tag": "plain_text"
                }
            }
        )
        return self

    def add_markdown(self, content: str):
        self.content['elements'].append(
            {
                "tag": "markdown",
                "content": content,
            }
        )
        return self

    def add_image(self, image_key: str):
        self.content['elements'].append(
            {
                "tag": "img",
                "img_key": image_key,
                "alt": {
                    "tag": "plain_text",
                    "content": ""
                },
                "mode": "fit_horizontal",
                "preview": True
            }
        )
        return self

    def add_br(self):
        self.content['elements'].append(
            {
                "tag": "hr"
            }
        )
        return self

    def add_button(self, button_title: str, url: str, button_type: str = 'default'):
        """
        添加按钮
        :param button_title:    按钮文本
        :param url:             跳转URL
        :param button_type:     按钮样式 default / primary / danger
        :return:
        """
        self.content['elements'].append(
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": button_title,
                        },
                        "url": url,
                        "type": button_type,
                    }
                ]
            }
        )
        return self

    def add_button_group(self, button_config_list: List[dict]):
        """
        添加按钮组
        :param button_config_list:  按钮组配置
        [
            {
                'button_title': '按钮组一',
                'url': 'https://www.baidu.com/',
                'button_type': 'default',
            },
            {
                'button_title': '按钮组二',
                'url': 'https://www.baidu.com/',
                'button_type': 'primary',
            },
            {
                'button_title': '按钮组三',
                'url': 'https://www.baidu.com/',
                'button_type': 'danger',
            }
        ]
        :return:
        """
        self.content['elements'].append(
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": button_config.get('button_title'),
                        },
                        "url": button_config.get('url'),
                        "type": button_config.get('button_type'),
                    }
                    for button_config in button_config_list
                ]
            }
        )
        return self

    def dumps(self):
        return json.dumps(self.content)
