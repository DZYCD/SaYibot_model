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
dataset = DataSetControl()
group_rule = is_type(GroupMessageEvent)
awake_message = on_message(priority=99, rule=group_rule)
awaking_msg = ["终于回话了", "醒了过来", "已读刚回"]
focus_list = ["可爱捏", "?", "你说得对。", "我没意见", "原来如此！"]


@awake_message.handle()
async def _(event: Event):
    if delay():
        return
    effector_id = event.get_session_id().split('_')[2]
    if dataset.get_value(str(effector_id), "in_calling") == "True":
        dataset.update_value(str(effector_id), "in_calling", "False")
        times = float(dataset.get_value(str(effector_id), "calling_time"))
        await awake_message.finish(MessageSegment.at(str(effector_id))+MessageSegment.text("过了{:.1f}秒后{}!".format(time.time()-times, random.choice(awaking_msg))))

    if dataset.get_value(str(effector_id), "focus") == "True":
        res = random.randint(100, 999)
        if res > 800:
            await awake_message.finish(random.choice(focus_list))
