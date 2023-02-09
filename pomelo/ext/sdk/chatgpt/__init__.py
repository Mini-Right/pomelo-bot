#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/9 17:53
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : __init__.py.py
# @Software    : PyCharm
# @Description :
import openai


def chatgpt(question):
    openai.api_key = ''
    print('调用开始')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=1024,
        n=1,
        temperature=0.5,
        stop=None
    )
    result = response.get('choices')[0].get('text')
    return result
