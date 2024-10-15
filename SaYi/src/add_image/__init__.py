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
import httpx
import json
import requests
from nonebot import logger
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

dataset = DataSetControl("./src/plugins/add_image/image.json")

image_adder = on_command("添加", rule=to_me(), priority=10, block=True)
get_image = on_command("来只", aliases={"来点", "来个"}, priority=10, block=True)
image_list = on_command("图片列表", rule=to_me(), priority=10, block=True)
pixiv_image = on_command("插画", priority=10, block=True)

base = "C:/Pycharm_projects/SaYibot/SaYi/src/plugins/add_image/image_library/"


@pixiv_image.handle()
async def _(args: Message = CommandArg()):
    url = "https://image.anosu.top/pixiv/json"
    if len(args):
        url = url + f"?keyword={args}"
    response = requests.get(url).text
    m = {}
    try:
        m = json.loads(response)[0]

    except Exception as e:
        await pixiv_image.finish("没找到关键tag...\n不过你可以尝试翻译成日文或者英文再试一次")
    msg = "pid:{}\n>>>{}\ntags:{}".format(m["pid"], m["title"], m["tags"])
    await pixiv_image.finish(msg + MessageSegment.image(m["url"]))


def image_save(path, filename):
    img_src = filename
    response = requests.get(img_src)
    with open(base + path, 'wb') as file_obj:
        file_obj.write(response.content)
    return base + path


@image_adder.handle()
async def _(event: Event, args: Message = CommandArg()):
    if delay():
        return
    user = event.get_session_id()
    #if ("1109876092" not in user) and ("3837076318" not in user) and ("2411501021" not in user):
    #    await image_adder.finish("权限不足，去看看别的功能吧")
    name = args.extract_plain_text()
    dataset.update_value("adding", "target", name)
    await image_adder.pause("添加什么？")


@image_adder.handle()
async def _(event: Event):
    msg = str(event.get_message())

    msg = msg.replace("&#91;", "[")
    msg = msg.replace("&#93;", "]")
    msg = msg.replace("&amp;", "&")
    if "url=" in msg:
        msg = msg.split("url=")[1]
        msg = msg.split(']')[0]

    name = dataset.get_value("adding", "target")
    try:
        p = dataset.get_value(name, "using")
        if "cn:443/" in msg:
            msg = image_save(name + str(p + 1) + ".mp4", msg)
        elif "download?" in msg:
            msg = image_save(name + str(p + 1) + ".png", msg)
        dataset.update_value(name, "using", p + 1)
        dataset.update_value(name, str(p + 1), msg)
    except:
        dataset.update_value(name, "using", 1)
        dataset.update_value(name, "1", msg)

    await image_adder.finish("添加成功！")


@get_image.handle()
async def _(event: Event, args: Message = CommandArg()):
    if delay():
        return
    msg = args.extract_plain_text()
    if "皇帝" in msg:
        user = event.get_session_id()
        if ("1109876092" not in user) and ("3837076318" not in user) and ("3487365663" not in user):
            await image_adder.finish("受皇帝影响，这个词只能在他允许的范围内使用")

    outmsg = ""
    try:
        p = dataset.get_value(msg, "using")
        outmsg = dataset.get_value(msg, str(random.randint(1, p)))
        logger.success("Get pic:{}".format(outmsg))
    except:
        await get_image.finish("他貌似还没有被添加")

    try:
        await get_image.finish(MessageSegment.image(outmsg))
    except MatcherException:
        raise
    except Exception as e:
        try:
            await get_image.finish(MessageSegment.video(outmsg))
        except MatcherException:
            raise
        except Exception as e:
            await get_image.finish(MessageSegment.text(outmsg))

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
