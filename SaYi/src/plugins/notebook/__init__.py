import random
import httpx
from nonebot.rule import to_me
from nonebot.plugin import on_command, on_type, on_message
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.exception import MatcherException
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import PokeNotifyEvent, PrivateMessageEvent
from ..dataset_controller import DataSetControl
from ..time_freezer import delay

dataset = DataSetControl("C:\\Users\\DZYCD\\PycharmProjects\\SaYibot\\SaYi\\src\\plugins\\notebook\\note.json")


note_adder = on_command("记笔记", rule=to_me(), aliases={"添加笔记"}, priority=10, block=True)
get_note = on_command("看笔记", rule=to_me(), aliases={"查笔记", "查看笔记"}, priority=10, block=True)
note_list = on_command("所有笔记", rule=to_me(), aliases={"笔记列表"}, priority=10, block=True)


@note_adder.handle()
async def _(event: Event, args: Message = CommandArg()):
    if delay():
        return
    user = event.get_session_id()
    if ("1109876092" not in user) and ("3837076318" not in user):
        await note_adder.finish("权限不足，去看看别的功能吧")

    name = args.extract_plain_text()
    name.strip(" ")
    dataset.update_value("adding", "target", name)
    await note_adder.pause("内容是?")


@note_adder.handle()
async def _(event: Event):
    msg = str(event.get_message())
    msg = msg.replace("&#91;", "[")
    msg = msg.replace("&#93;", "]")
    name = dataset.get_value("adding", "target")
    dataset.update_value(name, "content", msg)
    await note_adder.finish("添加成功！")


@get_note.handle()
async def _(event: Event, args: Message = CommandArg()):
    if delay():
        return
    user = event.get_session_id()
    if ("1109876092" not in user) and ("3837076318" not in user):
        await get_note.finish("权限不足，去看看别的功能吧")
    msg = args.extract_plain_text()
    try:
        outmsg = dataset.get_value(msg, "content")
        if outmsg == "false":
            await get_note.finish("貌似还没有被添加这个标题的笔记")
        await get_note.finish(MessageSegment.text(outmsg))
    except MatcherException:
        raise
    except:
        await get_note.finish("貌似还没有被添加这个标题的笔记")


@note_list.handle()
async def _(event: Event):
    if delay():
        return
    user = event.get_session_id()
    if ("1109876092" not in user) and ("3837076318" not in user):
        await note_list.finish("权限不足，去看看别的功能吧")
    try:
        note = dataset.get_dataset()
        title_list = []
        for i in note:
            title_list.append(i)
        title_list.remove("adding")
        msg = MessageSegment.text("SaYi总共记录了{}条笔记，标题分别为：".format(len(title_list)) + "\n" + str(title_list))
        await note_adder.finish(msg)
    except MatcherException:
        raise
    except:
        await note_list.finish("出错了...")
