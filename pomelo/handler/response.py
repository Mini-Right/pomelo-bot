#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2022/1/29 15:48
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : response.py
# @Software    : PyCharm
# @Description :
import logging
from typing import Union

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

__all__ = ["success_response", "fail_response", "login_fail_response"]


def response(
    data: Union[list, dict, str, any] = None,
    msg: str = None,
    code: int = 200,
    status_code: int = 200,
):
    content = {
        "data": data,
        "msg": msg,
        "code": code,
    }
    logger.info(content)
    return JSONResponse(status_code=status_code, content=jsonable_encoder(content))


def success_response(*, data: Union[list, dict, str, any] = None, msg: str = "成功"):
    return response(data, msg, 200)


def fail_response(*, data: Union[list, dict, str, any] = None, msg: str = None):
    return response(data, msg, 500)


def login_fail_response(*, data: Union[list, dict, str, any] = None, msg: str = None):
    return response(data, msg, 500, status_code=401)
