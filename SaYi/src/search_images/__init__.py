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
import json
import time
import requests
from .data import search

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service

url = "https://soutubot.moe/"
path = "C:\\Pycharm_projects\\SaYibot\\SaYi\\src\\plugins\\search_images\\local.jpg"
def get_image(path,filename):
    img_src = filename
    response = requests.get(img_src)
    with open(path, 'wb') as file_obj:
        file_obj.write(response.content)
def image_search(file):
    service = Service("C:\\Pycharm_projects\\SaYibot\\SaYi\\src\\asserts\\127.0.6533.119\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options, service=service)
    driver.maximize_window()
    picname = file
    link = "https://soutubot.moe"


    # driver.get(link)
# #app > div > div > div > div.flex.flex-col.sm\:flex-row > div.w-full.px-4.sm\:px-0 > div > input
    try:
        driver.get(link)
        elm = driver.find_element("css selector", "#app > div > div > div > div.flex.flex-col.sm\:flex-row > div.w-full.px-4.sm\:px-0 > div > input")
        js = 'arguments[0].removeAttribute("class");'
        driver.execute_script(js, elm)
        elm.send_keys(picname)
        time.sleep(10)
        driver.refresh()
        time.sleep(10)
        get_conver_header = {}
        target_url = ""
        for request in driver.requests:
            # print(request.url)
            if "https://soutubot.moe/api/results/" in request.url:
                target_url = request.url
                for header_key in request.headers:
                    get_conver_header[header_key] = request.headers[header_key]
                break
        r = requests.get(target_url, headers=get_conver_header)
        r = json.loads(r.text)
        driver.close()
        return r
    except Exception as e:
        driver.close()
        print(e)


image_searcher = on_command("找找原作", rule=to_me(), priority=10, block=True)


@image_searcher.handle()
async def _(event: Event):
    if delay():
        return
    user = event.get_session_id()
    if ("1109876092" not in user) and ("2655709439" not in user) and ("3487365663" not in user):
        await image_searcher.finish("权限不足，去看看别的功能吧")
    await image_searcher.pause("查找什么图？")


@image_searcher.handle()
async def _(event: Event):
    msg = str(event.get_message())
    if "url" in msg:
        msg = msg.replace("&#91;", "[")
        msg = msg.replace("&#93;", "]")
        msg = msg.replace("&amp;", "&")
        msg = msg.split("url=")[1]
        msg = msg.split(']')[0]
        get_image(path, msg)
        result = []
        try:
            res = image_search(path)["data"][0]
            result = [res["source"], res["title"], res["subjectPath"], res["page"], res["similarity"]]
        except:
            logger.error("Find results Failed")
            await image_searcher.finish("查找失败，可能由于网络波动或处理太慢。请稍后再试")
        try:
            logger.success("Find results!:{}".format(result))
            if float(result[4]) < 35.0:
                await image_searcher.finish("你这张图貌似在{}站没收录...不过最佳匹配为\n{}\n神秘数字：[{}].page[{}]".format(result[0][:2], result[1], result[2].split("g/")[1], result[3]))
            await image_searcher.finish("唔，你这张图片最佳匹配为{}站收录的\n{}\n神秘数字：[{}].page[{}]".format(result[0][:2], result[1], result[2].split("g/")[1], result[3]))
        except MatcherException:
            raise
        except Exception as e:
            await image_searcher.finish("查找失败，可能由于防火墙被屏蔽。请稍后再试")
            raise e
    else:
        await image_searcher.finish("我需要一张图片。")

image_finder = on_command("搜图", rule=to_me(), priority=10, block=True)


@image_finder.handle()
async def _(event: Event):
    if delay():
        return
    await image_finder.pause("查找什么图？")


@image_finder.handle()
async def _(event: Event):
    msg = str(event.get_message())
    if "url" in msg:
        msg = msg.replace("&#91;", "[")
        msg = msg.replace("&#93;", "]")
        msg = msg.replace("&amp;", "&")
        msg = msg.split("url=")[1]
        msg = msg.split(']')[0]
        get_image(path, msg)
        try:
            await image_finder.finish(search(path), at_sender=True)
        except MatcherException:
            raise
        except Exception as e:
            await image_finder.finish("查找失败，可能由于防火墙被屏蔽。请稍后再试")
            raise e
    else:
        await image_finder.finish("我需要一张图片。")


