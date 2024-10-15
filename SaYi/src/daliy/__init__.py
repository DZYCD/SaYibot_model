#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/10/15 下午10:28
# @Author  : 单子叶蚕豆_DzyCd
# @File    : test.py
# @IDE     : PyCharm
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.exception import MatcherException
import random
from ..time_freezer import delay

morning = on_command("早安", rule=to_me(), aliases={"早上好"}, priority=10, block=True)
night = on_command("晚安", rule=to_me(), priority=10, block=True)


@morning.handle()
async def handle_function():
    if delay():
        return
    try:
        await morning.finish("早上好！")
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@night.handle()
async def handle_function():
    if delay():
        return
    try:
        await night.finish("做个好梦！")
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here
