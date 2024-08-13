import random
import httpx
from nonebot.rule import to_me
from nonebot.plugin import on_command, on_type, on_message
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.exception import MatcherException
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import PokeNotifyEvent, PrivateMessageEvent
from ..dataset_controller import DataSetControl
from ..time_freezer import delay

dataset = DataSetControl("E:\\Pycharm_projects\\SaYibot\\SaYi\\src\\plugins\\add_image\\image.json")

image_adder = on_command("添加", rule=to_me(), priority=10, block=True)
get_image = on_command("来只", aliases={"来点"}, priority=10, block=True)
image_list = on_command("图片列表", rule=to_me(), priority=10, block=True)


@image_adder.handle()
async def _(event: Event, args: Message = CommandArg()):
    if delay():
        return
    user = event.get_session_id()
    if ("1109876092" not in user) and ("3837076318" not in user):
        await image_adder.finish("权限不足，去看看别的功能吧")
    name = args.extract_plain_text()
    dataset.update_value("adding", "target", name)
    await image_adder.pause("添加什么图？")


@image_adder.handle()
async def _(event: Event):
    msg = str(event.get_message())
    if "url" in msg:
        if "download?" in msg:
            await image_adder.finish("添加失败，请从pc端传入图像")
        msg = msg.split("url=")[1]
        msg = msg.split(']')[0]
        name = dataset.get_value("adding", "target")
        try:
            p = dataset.get_value(name, "using")
            dataset.update_value(name, "using", p + 1)
            dataset.update_value(name, str(p + 1), msg)
        except:
            dataset.update_value(name, "using", 1)
            dataset.update_value(name, "1", msg)
        await image_adder.finish("添加成功！")
    else:
        await image_adder.reject("我需要一张图片。")


@get_image.handle()
async def _(args: Message = CommandArg()):
    if delay():
        return
    msg = args.extract_plain_text()
    try:
        p = dataset.get_value(msg, "using")
        outmsg = dataset.get_value(msg, str(random.randint(1, p)))
        await get_image.finish(MessageSegment.image(outmsg))
    except MatcherException:
        raise
    except:
        await get_image.finish("他貌似还没有被添加")


@image_list.handle()
async def _(event: Event):
    if delay():
        return
    user = event.get_session_id()
    if ("1109876092" not in user) and ("3837076318" not in user):
        await image_list.finish("权限不足，去看看别的功能吧")
    try:
        note = dataset.get_dataset()
        title_list = []
        for i in note:
            title_list.append(i)
        title_list.remove("adding")
        msg = MessageSegment.text("SaYi总共记录了{}个关键词，分别为：".format(len(title_list)) + "\n" + str(title_list))
        await image_list.finish(msg)
    except MatcherException:
        raise
    except:
        await image_list.finish("出错了...")


async def get_data(url):
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.text.strip()
    return data
