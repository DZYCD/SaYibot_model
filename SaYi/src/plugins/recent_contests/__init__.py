from nonebot.rule import to_me
from nonebot.plugin import on_command

from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.rule import is_type
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from nonebot.exception import MatcherException
from nonebot.params import CommandArg
import random
import time
from nonebot.adapters import Bot, Event
from ..dataset_controller import DataSetControl
from ..time_freezer import delay
from .data_source import get_contest_list, to_date, to_minutes


content = on_command("最近比赛", aliases={"近期比赛"}, rule=to_me(), priority=10, block=True)


@content.handle()
async def _(args: Message = CommandArg()):
    msg = args.extract_plain_text()
    try:
        oj = "OJ"
        if "cf" in msg:
            oj = "CodeForces"
            contest_list = get_contest_list(["CodeForces"])
        elif "洛谷" in msg:
            oj = "洛谷"
            contest_list = get_contest_list(["LuoGu"])
        elif "牛客" in msg:
            oj = "牛客"
            contest_list = get_contest_list(["NowCoder"])
        elif "计蒜客" in msg:
            oj = "计蒜客"
            contest_list = get_contest_list(["JiSuanKe"])
        else:
            contest_list = get_contest_list()

        msg = MessageSegment.text("接下来公开的{}比赛:\n\n".format(oj))
        msg += MessageSegment.text(">>>总共{}场比赛\n\n".format(len(contest_list)))
        for i in contest_list:
            msg += MessageSegment.text("--{0}--\n{1}\n|\n比赛时长:{2}minutes \n"
                                       "当前状态:>>>[{3}]   \n比赛日期:{4}\nlink:{5}\n\n".format(i[0], i[1], to_minutes(i[3]-i[2]), i[4],
                                                                                    to_date(i[2]), i[6]))
        await content.finish(msg)
    except MatcherException:
        raise
    except:
        await content.finish("发生了未知错误")

