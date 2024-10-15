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
from nonebot.rule import is_type

from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.plugin import on_command, on_message
from nonebot.rule import to_me
from ..dataset_controller import DataSetControl

from ..time_freezer import delay


async def limit_permission(event: Event):
    id_ = str(event.get_session_id())
    if "group_868949744_3211235676" in id_:
        return False
    return True

dataset = DataSetControl()
group_rule = is_type(GroupMessageEvent)
awake_message = on_message(priority=99, permission=limit_permission, rule=group_rule)
awaking_msg = ["终于回话了", "醒了过来", "已读刚回", "上线了。好久不见", "终于来啦。"]
focus_list = ["可爱捏", "?", "你说得对。", "我没意见", "我听不见", "哦", "啊?", "......", "然后呢？"]
focus_graph = ["C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/第一杀手1.png",
               "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/第一杀手2.png",
               "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/yamato1.png",
                  "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊15.png",
   "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊16.png"
   "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊3.png",
   "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊4.png",
    "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊5.png",
    "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊6.png",
    "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊7.png",
    "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊8.png",
     "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊9.png",
    "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊10.png",
    "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊11.png",
    "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊12.png",
     "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊13.png",
    "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/闲聊14.png"]


@awake_message.handle()
async def _(event: Event):
    if delay():
        return
    effector_id = event.get_session_id().split('_')[2]
    if dataset.get_value(str(effector_id), "in_calling") == "True":
        dataset.update_value(str(effector_id), "in_calling", "False")
        times = float(dataset.get_value(str(effector_id), "calling_time"))
        if times < 300:
            return
        await awake_message.finish(MessageSegment.at(str(effector_id))+MessageSegment.text("过了{:.1f}秒后{}!".format(time.time()-times, random.choice(awaking_msg))))

    if dataset.get_value(str(effector_id), "focus") == "True":
        res = random.randint(100, 999)
        print(res)
        if res > 930:
            await awake_message.finish(random.choice(focus_list))
        elif res > 850:
            await awake_message.finish(MessageSegment.image(random.choice(focus_graph)))
