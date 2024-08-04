from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.exception import MatcherException
import random
from ..time_freezer import delay

morning = on_command("早安", rule=to_me(), aliases={"早上好"}, priority=10, block=True)
night = on_command("晚安", rule=to_me(), priority=10, block=True)


@morning.handle()
async def handle_function():
    if delay():
        return
    try:
        await morning.finish("早上好！")
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here


@night.handle()
async def handle_function():
    if delay():
        return
    try:
        await night.finish("做个好梦！")
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here
