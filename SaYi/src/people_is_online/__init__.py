#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/10/15 下午10:28
# @Author  : 单子叶蚕豆_DzyCd
# @File    : test.py
# @IDE     : PyCharm
import random
import time

from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.adapters import Event
from ..dataset_controller import DataSetControl

from ..time_freezer import delay

call = on_command("叫醒", rule=to_me(), aliases={"唤醒", "通知", "提醒"}, priority=10, block=True)
focus = on_command("捧场", rule=to_me(), priority=10, block=True)
stop_focus = on_command("停止捧场", rule=to_me(), priority=10, block=True)
message_list = ["还活着吗", "起床了~", "别睡了，来聊天", "再不醒我要报警了", "你 有 早 八", "懒死你得了", "滴滴~"]

dataset = DataSetControl()


@focus.handle()
async def _(args: Message = CommandArg()):
    if delay():
        return

    caller_id = args.get('at')
    receiver_id = str(caller_id).split('=')[1]
    receiver_id = receiver_id.split(']')[0]
    receiver_id = receiver_id.split(',')[0]
    if caller_id:
        dataset.update_value(str(receiver_id), "focus", "True")
        await focus.finish(caller_id + MessageSegment.text(" 我会看着你。"))
    else:
        await focus.finish("需要我聚焦谁？")


@stop_focus.handle()
async def _(args: Message = CommandArg()):
    if delay():
        return

    caller_id = args.get('at')
    receiver_id = str(caller_id).split('=')[1]
    receiver_id = receiver_id.split(']')[0]
    receiver_id = receiver_id.split(',')[0]
    if caller_id:
        dataset.update_value(str(receiver_id), "focus", "False")
        await stop_focus.finish(caller_id + MessageSegment.text(" 我走了，不理你了。"))
    else:
        await stop_focus.finish("不需要关注谁了?")


@call.handle()
async def handle_function(args: Message = CommandArg()):
    if delay():
        return

    caller_id = args.get('at')
    recevier_id = str(caller_id).split('=')[1]
    recevier_id = recevier_id.split(']')[0]
    recevier_id = recevier_id.split(',')[0]
    text = args.get('text')
    caller_text = str(args.get('text'))
    caller_text.strip()
    if caller_id:
        dataset.update_value(str(recevier_id), "in_calling", "True")
        dataset.update_value(str(recevier_id), "calling_time", str(time.time()))
        if len(caller_text) > 1:
            await call.finish(caller_id + text + MessageSegment.text('!'))
        else:
            await call.finish(caller_id + random.choice(message_list))
    else:
        await call.reject("你要喊谁？")
