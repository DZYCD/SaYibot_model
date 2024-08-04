"""
the beginning of the "SaYi"
"""

from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.exception import MatcherException
from ..time_freezer import delay
weather = on_command("你好", rule=to_me(), aliases={"hello"}, priority=10, block=True)


@weather.handle()
async def handle_function():
    if delay():
        return
    try:
        await weather.finish("你好。")
    except MatcherException:
        raise
    except Exception as e:
        pass  # do something here