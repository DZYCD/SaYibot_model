import time
import pandas
import logging

from nonebot.plugin import PluginMetadata
from nonebot.log import LoguruHandler, logger
from nonebot import get_driver, get_plugin_config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .config import Config


def check_time():
    pd = pandas.read_json("E:\\Pycharm_projects\\SaYibot\\SaYi\\src\\plugins\\time_freezer\\config.json", orient='index')[0]
    first_time = pd["time"]
    cont = pd["set"]
    now_time = time.time()
    is_allowed = (now_time - first_time) > cont
    print("time passed:{}".format(now_time - first_time))
    if is_allowed:
        pd["time"] = now_time
    pd.to_json("E:\\Pycharm_projects\\SaYibot\\SaYi\\src\\plugins\\time_freezer\\config.json")
    return is_allowed


def delay():
    if not check_time():
        print("time error")
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
