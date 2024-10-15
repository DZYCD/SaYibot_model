#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/10/15 下午10:28
# @Author  : 单子叶蚕豆_DzyCd
# @File    : test.py
# @IDE     : PyCharm
import time
import pandas
import logging

from nonebot.plugin import PluginMetadata
from nonebot.log import LoguruHandler, logger
from nonebot import get_driver, get_plugin_config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .config import Config


def check_time():
    pd = pandas.read_json("C:\\Pycharm_projects\\SaYibot\\SaYi\\src\\plugins\\time_freezer\\config.json", orient='index')[0]
    first_time = pd["time"]
    cont = pd["set"]
    now_time = time.time()
    is_allowed = (now_time - first_time) > cont
    if is_allowed:
        pd["time"] = now_time
    else:
        logger.error("Time Crashed:{:.2f}".format(now_time - first_time))
    pd.to_json("C:\\Pycharm_projects\\SaYibot\\SaYi\\src\\plugins\\time_freezer\\config.json")

    return is_allowed


def delay():
    if not check_time():
        return True
    return False


driver = get_driver()
plugin_config = get_plugin_config(Config)

scheduler = AsyncIOScheduler()
scheduler.configure(plugin_config.apscheduler_config)


async def _start_scheduler():
    if not scheduler.running:
        scheduler.start()
        logger.opt(colors=True).info("<y>Scheduler Started</y>")


async def _shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.opt(colors=True).info("<y>Scheduler Shutdown</y>")


if plugin_config.apscheduler_autostart:
    driver.on_startup(_start_scheduler)
    driver.on_shutdown(_shutdown_scheduler)

aps_logger = logging.getLogger("apscheduler")
aps_logger.setLevel(plugin_config.apscheduler_log_level)
aps_logger.handlers.clear()
aps_logger.addHandler(LoguruHandler())
