#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/10/15 下午10:28
# @Author  : 单子叶蚕豆_DzyCd
# @File    : test.py
# @IDE     : PyCharm
from nonebot import on_command, require, get_bots
from nonebot.adapters.cqhttp import MessageSegment, Message
from nonebot.exception import MatcherException
from nonebot.params import CommandArg
import os
from nonebot.adapters import Event
from nonebot.rule import to_me
from random import randint, choice
from ..time_freezer import scheduler, delay
from ..dataset_controller import DataSetControl
from ..web_processor import webshot
import time
import datetime

weather = on_command("天气", rule=to_me(), aliases={"查天气"}, priority=1, block=True)

image_path = "C:\\Pycharm_projects\\SaYibot\\SaYi\\src\\plugins\\weather_show\\weather_image.png"


@weather.handle()
async def _(args: Message = CommandArg()):
    if delay():
        return
    try:
        first_time = time.time()
        locate = args.extract_plain_text()
        webshot("https://www.msn.cn/zh-cn/weather/forecast/in-" + locate, image_path)
        img = f"file:///" + image_path
        await weather.finish(MessageSegment.image(img) + MessageSegment.text("处理了:{:.2f}秒".format(time.time()-first_time)))
    except:
        raise