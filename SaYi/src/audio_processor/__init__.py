#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/10/15 下午10:28
# @Author  : 单子叶蚕豆_DzyCd
# @File    : test.py
# @IDE     : PyCharm
from nonebot import logger
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.rule import to_me
from nonebot.plugin import on_command, on_message
from nonebot.exception import MatcherException
from nonebot.permission import SUPERUSER
import os


from ..dataset_controller import DataSetControl

audio = on_command("说话", rule=to_me(), priority=10, block=True)
role = on_command("谁能说话", rule=to_me(), priority=10, block=True)
role_list = ["阿慈谷日富美", "初音未来", "白洲梓", "才羽桃井", "黑崎小雪", "黑崎小雪", "砂狼白子", "御坂美琴", "天童爱丽丝", "空崎日奈"]

dataset = DataSetControl("./src/plugins/audio_processor/text.json")
audio_path = "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/audio_processor/audio.wav"
bat_file = "E:/DZYCDscript/ba_bert/ba_bert/test.bat"


@audio.handle()
async def _(event: Event):
    await audio.finish("啊。。。本地暂时用不了")

    text = event.get_plaintext().strip()
    text = text.split("说话")[1]
    role = "御坂美琴"
    if len(text.split("-", maxsplit=1))==2:
        text, role = text.split("-", maxsplit=1)
        if role not in role_list:
            role = "御坂美琴"
    res = dataset.get_dataset()
    res["role"] = role
    res["text"] = text
    dataset.save_dataset(res)
    try:
        await audio.send(MessageSegment.text("处理中...预计需要半分钟"))
    except MatcherException:
        raise

    os.system(bat_file)

    await audio.finish(MessageSegment.record(audio_path))


@role.handle()
async def _():
    try:
        await role.finish("现在可以使用的角色有\n{}\n默认：初音未来".format(role_list))
    except MatcherException:
        raise
    except Exception as e:
        pass