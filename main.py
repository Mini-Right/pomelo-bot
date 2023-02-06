#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2023/2/4 00:09
# @Author      : Mini-Right
# @Email       : www@anyu.wang
# @File        : main.py
# @Software    : PyCharm
# @Description :
import uvicorn

from pomelo import pomelo

if __name__ == "__main__":
    uvicorn.run('pomelo.__init__:pomelo',
                host="localhost",
                port=3000,
                workers=1)
