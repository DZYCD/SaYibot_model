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
import requests
import json

from nonebot.exception import MatcherException
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.adapters import Bot, Event
from nonebot.params import CommandArg
from nonebot import get_bots, on_command, logger
from ..time_freezer import delay
from .data_source import DataGet, DataProcess

songpicker = on_command("点歌", aliases={"播放", "歌曲", "查歌"}, priority=9, block=True)

dataGet = DataGet()


def song_search_2(ids):
    link = "https://oiapi.net/API/QQMusicJSONArk?url=https://music.163.com/#/song?id={}".format(ids)
    # driver.get(link)
    print(link)
    res = json.loads(requests.get(link).text)
    print(res["data"])
    return res["data"]


def song_search(ids):

    link = "https://tenapi.cn/v2/songinfo?id={}".format(ids)
    # driver.get(link)
    print(link)
    # print(requests.get(link))

    req = requests.get(link).text
    res = json.loads(req)

    return [res["data"]["songs"], res["data"]["cover"], "https://music.163.com/#/song?id={}".format(ids), res["data"]["sings"]]


@songpicker.handle()
async def _(event: Event, args: Message = CommandArg()):
    if delay():
        return
    song_name = args.extract_plain_text()
    user = event.get_user_id()
    if len(song_name) < 1:
        await songpicker.reject("歌名?")
    song_ids = []
    song_com = ""
    try:
        song_ids = await dataGet.song_ids(song_name=song_name)
        song_com = await dataGet.song_comments(song_id=song_ids[0])
    except Exception as e:
        logger.error("Failed to find song : {0}".format(song_name))
        await songpicker.reject("没找到这首歌...也许你可以缩短一下关键词")
    if not song_ids:
        await songpicker.finish("这曲子貌似不在曲库中，你最好去网易云看一眼")

    try:
        print(MessageSegment.music("163", song_ids[0]))
        await songpicker.send(MessageSegment.music("163", song_ids[0]))
        if len(song_com):
            await songpicker.finish(MessageSegment.text(str(song_com[random.randint(0, len(song_com) - 1)])))
        return
    except MatcherException:
        return
    except Exception as e:
        await songpicker.send("卡片发不出去...直接给你链接吧")

    try:
        res = song_search(song_ids[0])
    except Exception as e:
        logger.error("Bad Web Connection {}".format(song_name))
        await songpicker.finish(MessageSegment.text("...网络貌似爆炸了。你等下子再试试"))
        raise e

    logger.success("Success find song : {0}-->{1}".format(res[0], res[2]))
    await songpicker.send(MessageSegment.text("{}\n歌手： {}".format(res[0], res[3])) + MessageSegment.image(res[1]) + MessageSegment.text(res[2]))
    try:
        if len(song_com):
            await songpicker.finish(MessageSegment.text(str(song_com[random.randint(0, len(song_com) - 1)])))
        else:
            return
    except MatcherException:
        raise
    except Exception as e:
        pass

