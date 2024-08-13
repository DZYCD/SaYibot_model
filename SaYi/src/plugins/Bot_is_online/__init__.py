from nonebot.rule import to_me
from nonebot.adapters import Event
from nonebot.plugin import on_command, on_type, on_message
from nonebot.adapters.onebot.v11 import PokeNotifyEvent, PrivateMessageEvent

from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.exception import MatcherException
import random
from ..time_freezer import delay
from ..dataset_controller import DataSetControl

message_list = ["我在", "等待指令", "什么事？", "需要什么吗", "在线在线在线，别吵", "在线", "?"]
message_list_poke = ["可爱捏", "有话直说，别戳", "...", "怎么了"]


async def poke_replier(matcher: Matcher):
    if delay():
        return
    try:
        await matcher.finish(random.choice(message_list_poke))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


morning = on_command("在吗", rule=to_me(), priority=9, block=True)
night = on_type((PokeNotifyEvent,), rule=to_me(), priority=10, block=True)
update_info = on_command("更新日志", priority=1, block=True)
job_path = "./update.json"
dataset = DataSetControl(job_path)


@update_info.handle()
async def _(event: Event):
    if delay():
        return
    try:
        info = dataset.get_dataset()
        msg = [MessageSegment.text("SaYi现在是[ PRMoment.2 ]版本")]
        for i in info:
            msg.append(MessageSegment.text("---version {0}---\n{1}".format(i, info[i])))
        await update_info.finish(random.choice(msg))
    except MatcherException:
        raise
    except Exception as e:
        await update_info.finish("出错了...")


@morning.handle()
async def _():
    if delay():
        return
    try:
        await morning.finish(random.choice(message_list))
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here
